from django.test import TestCase


class PeachjamViewsTest(TestCase):
    fixtures = ["documents/sample_documents"]

    def test_login_page(self):
        response = self.client.get("/accounts/login/")
        self.assertTemplateUsed(response, "account/login.html")

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # documents
        self.assertEqual(response.context.get("documents_count"), 8)

        recent_judgments = [
            r_j.title for r_j in response.context.get("recent_judgments")
        ]
        self.assertIn(
            "Obi vs Federal Republic of Nigeria [2016] ECOWASCJ 52 (09 November 2016)",
            recent_judgments,
        )

        recent_documents = [
            r_d.title for r_d in response.context.get("recent_documents")
        ]
        self.assertIn(
            "Activity Report of the Pan-African Parliament, July 2016 to June 2017",
            recent_documents,
        )

        recent_instruments = [
            r_i.title for r_i in response.context.get("recent_instruments")
        ]
        self.assertIn(
            "African Charter on Elections, Democracy and Governance", recent_instruments
        )

        recent_legislation = [
            r_l.title for r_l in response.context.get("recent_legislation")
        ]
        self.assertIn(
            "African Union Non-Aggression and Common Defence Pact", recent_legislation
        )

        # authors
        authors = [c.name for c in response.context.get("authors")]
        self.assertIn("ECOWAS Community Court of Justice", authors)

    def test_judgment_listing(self):
        response = self.client.get("/judgments/")
        self.assertEqual(response.status_code, 200)

        documents = [doc.title for doc in response.context.get("documents")]
        self.assertIn(
            "Ababacar and Ors vs Senegal [2018] ECOWASCJ 17 (29 June 2018)",
            documents,
        )
        self.assertIn(
            "ECOWAS Community Court of Justice",
            response.context["facet_data"]["courts"],
        )
        self.assertEqual(response.context["facet_data"]["years"], [2016, 2018])

    def test_judgment_detail(self):
        response = self.client.get(
            "/akn/aa-au/judgment/ecowascj/2018/17/eng@2018-06-29"
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["document"].doc_type, "judgment")
        self.assertEqual(
            response.context["document"].expression_frbr_uri,
            "/akn/aa-au/judgment/ecowascj/2018/17/eng@2018-06-29",
        )
        self.assertTrue(hasattr(response.context["document"], "court"))
        self.assertEqual(response.context["document"].date.year, 2018)

    def test_legislation_listing(self):
        response = self.client.get("/legislation/")
        self.assertEqual(response.status_code, 200)

        documents = [doc.title for doc in response.context.get("documents")]
        self.assertIn(
            "African Civil Aviation Commission Constitution (AFCAC)",
            documents,
        )
        self.assertEqual(response.context["facet_data"]["years"], [1969, 2005])

    def test_legislation_detail(self):
        response = self.client.get(
            "/akn/aa-au/act/pact/2005/non-aggression-and-common-defence/eng@2005-01-31"
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["document"].doc_type, "legislation")
        self.assertEqual(
            response.context["document"].expression_frbr_uri,
            "/akn/aa-au/act/pact/2005/non-aggression-and-common-defence/eng@2005-01-31",
        )
        self.assertEqual(response.context["document"].date.year, 2005)
        self.assertTrue(hasattr(response.context["document"], "repealed"))
        self.assertFalse(hasattr(response.context["document"], "author"))

    def test_legal_instrument_listing(self):
        response = self.client.get("/legal_instruments/")
        self.assertEqual(response.status_code, 200)

        documents = [doc.title for doc in response.context.get("documents")]
        self.assertIn(
            "African Charter on Democracy, Elections and Governance",
            documents,
        )
        self.assertEqual(response.context["facet_data"]["years"], [2007])

    def test_legal_instrument_detail(self):
        response = self.client.get(
            "/akn/aa-au/act/charter/2007/elections-democracy-and-governance/eng@2007-01-30"
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["document"].doc_type, "legal_instrument")
        self.assertEqual(
            response.context["document"].expression_frbr_uri,
            "/akn/aa-au/act/charter/2007/elections-democracy-and-governance/eng@2007-01-30",
        )
        self.assertEqual(response.context["document"].date.year, 2007)
        self.assertTrue(hasattr(response.context["document"], "author"))

    def test_generic_document_listing(self):
        response = self.client.get("/generic_documents/")
        self.assertEqual(response.status_code, 200)

        documents = [doc.title for doc in response.context.get("documents")]
        self.assertIn(
            "Activity Report of the Pan-African Parliament, July 2016 to June 2017",
            documents,
        )
        self.assertEqual(response.context["facet_data"]["years"], [2017])

    def test_generic_document_detail(self):
        response = self.client.get(
            "/akn/aa-au/doc/activity-report/2017/nn/eng@2017-07-03"
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["document"].doc_type, "generic_document")
        self.assertEqual(
            response.context["document"].expression_frbr_uri,
            "/akn/aa-au/doc/activity-report/2017/nn/eng@2017-07-03",
        )
        self.assertEqual(response.context["document"].date.year, 2017)
        self.assertTrue(hasattr(response.context["document"], "author"))
