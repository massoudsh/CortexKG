import test from 'node:test';
import assert from 'node:assert/strict';
import { createKnowledgeGraph, graphSummary, mockVault } from './graph.js';

test('indexes mock vault into a connected knowledge graph', () => {
  const graph = createKnowledgeGraph(mockVault);
  const summary = graphSummary(graph);

  assert.equal(summary.entities, 7);
  assert.equal(summary.relationships, 6);
  assert.equal(summary.types, 6);
  assert.ok(graph.relations.some((relation) => relation.label === 'owns'));
  assert.ok(graph.relations.some((relation) => relation.label === 'must resolve before'));
});

test('does not create relationships whose entities are absent from selected notes', () => {
  const graph = createKnowledgeGraph([mockVault[3]]);

  assert.equal(graph.entities.length, 1);
  assert.equal(graph.entities[0].label, 'PostgreSQL');
  assert.equal(graph.relations.length, 0);
});
