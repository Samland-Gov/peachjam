import { CopyToClipboard } from './clipboard';
import PdfRenderer from './pdf-renderer';
import { RelationshipEnrichments } from './RelationshipEnrichment';
import DocumentList from './document-list';
import DocumentContent from './document-content';
import NavigationSelect from './navigation-select';
import { ToggleTab } from './tabs';
import TaxonomyTree from './taxonomy-tree';
import TermsOfUse from './terms-of-use';

import FindDocuments from './FindDocuments/index.vue';
import LegislationTable from './LegislationTable/index.vue';

const components: Record<string, any> = {
  // Data components
  CopyToClipboard,
  DocumentContent,
  DocumentList,
  NavigationSelect,
  PdfRenderer,
  RelationshipEnrichments,
  ToggleTab,
  TaxonomyTree,
  TermsOfUse,

  // Vue components
  FindDocuments,
  LegislationTable
};

export default components;
