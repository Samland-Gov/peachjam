import logging

import igraph as ig
from elasticsearch import helpers

from peachjam.models import CoreDocument
from peachjam_search.documents import SearchableDocument

from ..models import ExtractedCitation

log = logging.getLogger(__name__)


class GraphRanker:
    """Reads and writes ranks for works based on graph weights using PageRank."""

    def __init__(self, force_update=False):
        self.force_update = force_update

    def rank_and_publish(self):
        self.populate_graph()
        self.calculate_ranks()
        self.publish_ranks()

    def populate_graph(self):
        """Build the graph database from our database."""
        citations = ExtractedCitation.objects.prefetch_related(
            "citing_work", "target_work"
        ).all()

        # create the works
        log.info("Creating graph")
        works = {c.citing_work for c in citations} | {c.target_work for c in citations}

        # igraph's vertices are 0-indexed, so we need to map our works to integers
        self.work_ids = {w: i for i, w in enumerate(works)}

        # it's fastest to add everything all at once
        edges = [
            (self.work_ids[c.citing_work], self.work_ids[c.target_work])
            for c in citations
        ]

        self.graph = ig.Graph(n=len(self.work_ids), edges=edges, directed=True)
        log.info("Created graph")

    def calculate_ranks(self):
        log.info("Running pagerank")
        self.ranks = self.graph.pagerank()
        log.info("Finished pagerank")

    def publish_ranks(self):
        """Store ranks for each work."""
        updated = []
        for work, rank in zip(self.work_ids.keys(), self.ranks):
            if work.ranking != rank or self.force_update:
                work.save(update_fields=["ranking"])
                updated.append(work)

        log.info(f"Updated db rankings for {len(updated)} works")

        self.bulk_update(updated)

    def bulk_update(self, works):
        """use elasticsearch client to bulk update the "ranking" field on the provided docs"""
        docs = CoreDocument.objects.filter(work__in=works).values(
            "id", "work__ranking", "language__iso_639_2T"
        )
        log.info(
            f"updating index with {len(docs)} documents",
        )
        searchable_doc = SearchableDocument()
        actions = (
            {
                "_op_type": "update",
                "_index": searchable_doc.get_index_for_language(
                    doc["language__iso_639_2T"]
                ),
                "_id": doc["id"],
                "doc": {"ranking": doc["work__ranking"]},
            }
            for doc in docs
        )
        helpers.bulk(
            SearchableDocument._index._get_connection(),
            actions,
            chunk_size=1000,
            request_timeout=60 * 60 * 30,
        )
        log.info("Updated index")
