import { createKnowledgeGraph, graphSummary, mockVault } from './graph.js';

const state = { notes: [], graph: { entities: [], relations: [] }, selected: null };

const $ = (selector) => document.querySelector(selector);
const noteList = $('#note-list');
const entityList = $('#entity-list');
const relationList = $('#relation-list');
const details = $('#details');

function render() {
  const summary = graphSummary(state.graph);
  $('#notes-count').textContent = state.notes.length;
  $('#entities-count').textContent = summary.entities;
  $('#relations-count').textContent = summary.relationships;
  $('#types-count').textContent = summary.types;
  $('#vault-status').textContent = state.notes.length ? `${state.notes.length} notes indexed` : 'Vault not connected';
  $('#import-button').textContent = state.notes.length ? 'Re-index mock vault' : 'Import mock vault';

  noteList.innerHTML = state.notes.map((note) => `
    <li><button class="note" data-note="${note.id}"><strong>${note.title}</strong><span>${note.folder} · ${note.modified}</span></button></li>`).join('') || '<li class="empty">Import a vault to see source notes.</li>';
  entityList.innerHTML = state.graph.entities.map((entity) => `
    <li><button class="entity ${state.selected === entity.id ? 'active' : ''}" data-entity="${entity.id}"><span>${entity.label}</span><em>${entity.type}</em></button></li>`).join('') || '<li class="empty">Entities will appear after indexing.</li>';
  relationList.innerHTML = state.graph.relations.map((relation) => `
    <li><span>${labelFor(relation.source)}</span><b>${relation.label}</b><span>${labelFor(relation.target)}</span><small>Evidence: ${relation.evidence}</small></li>`).join('') || '<li class="empty">Relationships will appear after indexing.</li>';
}

function labelFor(id) {
  return state.graph.entities.find((entity) => entity.id === id)?.label ?? id;
}

function showNote(id) {
  const note = state.notes.find((item) => item.id === id);
  details.innerHTML = `<p class="eyebrow">Source note</p><h3>${note.title}</h3><p>${note.content}</p><p class="meta">${note.folder} · Updated ${note.modified}</p>`;
}

function showEntity(id) {
  state.selected = id;
  const entity = state.graph.entities.find((item) => item.id === id);
  const connections = state.graph.relations.filter((relation) => relation.source === id || relation.target === id);
  details.innerHTML = `<p class="eyebrow">Inferred entity</p><h3>${entity.label}</h3><p>${entity.type} · ${connections.length} relationship${connections.length === 1 ? '' : 's'}</p><ul>${connections.map((relation) => `<li>${relation.label} ${labelFor(relation.source === id ? relation.target : relation.source)} <small>(${relation.evidence})</small></li>`).join('')}</ul>`;
  render();
}

$('#import-button').addEventListener('click', () => {
  state.notes = mockVault;
  state.graph = createKnowledgeGraph(mockVault);
  state.selected = null;
  details.innerHTML = '<p class="eyebrow">Import complete</p><h3>Mock Obsidian vault indexed</h3><p>Explore inferred people, projects, decisions, risks, and the source notes that support each connection.</p>';
  render();
});

noteList.addEventListener('click', (event) => {
  const id = event.target.closest('[data-note]')?.dataset.note;
  if (id) showNote(id);
});
entityList.addEventListener('click', (event) => {
  const id = event.target.closest('[data-entity]')?.dataset.entity;
  if (id) showEntity(id);
});

render();
