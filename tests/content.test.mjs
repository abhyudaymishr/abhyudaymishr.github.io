import test from 'node:test';
import assert from 'node:assert/strict';
import { normalize, searchContent, matchesCategory, localContentPath } from '../assets/js/core/content.mjs';
import { createContentRepository } from '../assets/js/data/content-repository.mjs';

const entries = [
  { title: 'Fluid dynamics', description: 'A quantum-inspired approach', topics: ['Scientific ML'], type: 'Project' },
  { title: 'Qudit quantum circuits', description: 'Generalized simulation', topics: ['Quantum computing'], type: 'Project' },
  { title: 'Café notes', text: 'Research on local geometric operators', topics: [], type: 'Research note' }
];
test('search prioritizes title matches over body matches', () => {
  assert.equal(searchContent(entries, 'quantum')[0].title, 'Qudit quantum circuits');
});
test('all query terms must match, across different fields', () => {
  assert.deepEqual(searchContent(entries, 'fluid quantum').map(x => x.title), ['Fluid dynamics']);
  assert.deepEqual(searchContent(entries, 'fluid qudit'), []);
});
test('search normalizes accents, case, and extra whitespace', () => {
  assert.equal(normalize('  CAFÉ  '), 'cafe');
  assert.equal(searchContent(entries, ' CAFE ')[0].title, 'Café notes');
});
test('empty queries, unknown topics, and result limits behave predictably', () => {
  assert.deepEqual(searchContent(entries, '  '), []);
  assert.deepEqual(searchContent(entries, 'absent'), []);
  assert.equal(searchContent(entries, 'quantum', 1).length, 1);
});
test('search includes the full article text and content type', () => {
  assert.equal(searchContent(entries, 'geometric')[0].title, 'Café notes');
  assert.equal(searchContent(entries, 'note')[0].title, 'Café notes');
});
test('category rules handle all, case differences, and unmatched areas', () => {
  assert.equal(matchesCategory({ category: 'Scientific ML' }, 'all'), true);
  assert.equal(matchesCategory({ category: 'Scientific ML' }, 'scientific ml'), true);
  assert.equal(matchesCategory({ category: 'Scientific ML' }, 'Topology'), false);
});
test('search result links reject script URLs and foreign origins', () => {
  const origin = 'https://abhyudaymishr.github.io';
  assert.equal(localContentPath('javascript:alert(1)', origin), null);
  assert.equal(localContentPath('https://unrelated.example/steal', origin), null);
  assert.equal(localContentPath('//unrelated.example/', origin), null);
  assert.equal(localContentPath(`${origin}/projects/?area=Quantum#details`, origin), '/projects/?area=Quantum#details');
});
test('concurrent readers share one request and cached content', async () => {
  let calls = 0;
  const repository = createContentRepository('/content-index.json', async () => { ++calls; return { ok: true, json: async () => ({ items: entries.map((x,i) => ({ ...x, url: `/item/${i}/` })) }) }; });
  const [a,b] = await Promise.all([repository.load(), repository.load()]);
  await repository.load();
  assert.equal(calls, 1); assert.equal(a,b); assert.equal(a.length, 3);
});
test('a failed content request can be retried', async () => {
  let calls = 0;
  const repository = createContentRepository('/index.json', async () => ++calls === 1 ? { ok: false } : { ok: true, json: async () => ({ items: [] }) });
  await assert.rejects(repository.load());
  assert.deepEqual(await repository.load(), []); assert.equal(calls, 2);
});
test('malformed index structures fail and malformed entries are ignored', async () => {
  const bad = createContentRepository('/index.json', async () => ({ ok: true, json: async () => ({ items: {} }) }));
  await assert.rejects(bad.load(), /Invalid content index/);
  const partial = createContentRepository('/index.json', async () => ({ ok: true, json: async () => ({ items: [{ title: 'Valid', url: '/' }, { title: 'Invalid' }] }) }));
  assert.equal((await partial.load()).length, 1);
});
