export const mockVault = [
  {
    id: 'project-atlas',
    title: 'Project Atlas',
    folder: 'Projects',
    modified: '2026-10-09',
    content: 'Maya owns the API migration for Project Atlas. The team chose PostgreSQL for the knowledge service. Review the security risk with Omar next Tuesday.',
  },
  {
    id: 'api-migration',
    title: 'API Migration',
    folder: 'Projects',
    modified: '2026-10-08',
    content: 'Project Atlas needs the API migration before the November launch. Maya will coordinate with Omar on the security review.',
  },
  {
    id: 'security-review',
    title: 'Security Review',
    folder: 'Meetings',
    modified: '2026-10-07',
    content: 'Omar identified a token retention risk. The decision is to encrypt backups and complete the review before launch.',
  },
  {
    id: 'postgresql',
    title: 'PostgreSQL',
    folder: 'Technology',
    modified: '2026-10-03',
    content: 'PostgreSQL is the selected store for the knowledge service because the team needs reliable relationships and audit history.',
  },
];

const entities = [
  { id: 'maya', label: 'Maya', type: 'Person' },
  { id: 'omar', label: 'Omar', type: 'Person' },
  { id: 'project-atlas', label: 'Project Atlas', type: 'Project' },
  { id: 'api-migration', label: 'API Migration', type: 'Initiative' },
  { id: 'postgresql', label: 'PostgreSQL', type: 'Technology' },
  { id: 'security-risk', label: 'Token retention risk', type: 'Risk' },
  { id: 'november-launch', label: 'November launch', type: 'Milestone' },
];

const relations = [
  { source: 'maya', target: 'api-migration', label: 'owns', evidence: 'Project Atlas' },
  { source: 'api-migration', target: 'project-atlas', label: 'supports', evidence: 'API Migration' },
  { source: 'project-atlas', target: 'postgresql', label: 'uses', evidence: 'Project Atlas' },
  { source: 'omar', target: 'security-risk', label: 'identified', evidence: 'Security Review' },
  { source: 'security-risk', target: 'november-launch', label: 'must resolve before', evidence: 'Security Review' },
  { source: 'omar', target: 'api-migration', label: 'reviews', evidence: 'API Migration' },
];

export function createKnowledgeGraph(notes) {
  const noteTitles = new Set(notes.map((note) => note.title));
  const activeEntities = entities.filter((entity) =>
    entity.type !== 'Project' && entity.type !== 'Initiative'
      ? notes.some((note) => note.content.toLowerCase().includes(entity.label.toLowerCase().replace('token retention ', '')))
      : noteTitles.has(entity.label),
  );
  const entityIds = new Set(activeEntities.map((entity) => entity.id));
  const activeRelations = relations.filter(
    (relation) => entityIds.has(relation.source) && entityIds.has(relation.target),
  );
  return { entities: activeEntities, relations: activeRelations };
}

export function graphSummary(graph) {
  const types = new Set(graph.entities.map((entity) => entity.type));
  return {
    entities: graph.entities.length,
    relationships: graph.relations.length,
    types: types.size,
  };
}
