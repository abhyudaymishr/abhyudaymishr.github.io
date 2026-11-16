import { searchContent, localContentPath } from '../core/content.mjs';
export function mountSearch(root, repository) {
  const input = root.querySelector('[data-search-input]');
  const results = root.querySelector('[data-search-results]');
  const status = root.querySelector('[data-search-status]');
  const form = root.querySelector('[data-search-form]');
  if (!input || !results || !status || !form) return;
  let version = 0, timer;
  const run = async () => {
    const request = ++version;
    const query = input.value.trim();
    results.replaceChildren();
    if (!query) { status.textContent = 'Search projects, publications, and research notes.'; return; }
    status.textContent = 'Searching…';
    try {
      const items = await repository.load();
      if (request !== version) return;
      const matches = searchContent(items, query);
      status.textContent = matches.length ? `${matches.length} result${matches.length === 1 ? '' : 's'} for “${query}”` : `No results for “${query}”. Try a topic such as quantum, topology, or operators.`;
      for (const item of matches) {
        const path = localContentPath(item.url, location.origin);
        if (!path) continue;
        const link = document.createElement('a'); link.className = 'search-result'; link.href = path;
        const type = document.createElement('small'); type.textContent = item.type;
        const heading = document.createElement('h3'); heading.textContent = item.title;
        const description = document.createElement('p'); description.textContent = item.description || '';
        link.append(type, heading, description); results.append(link);
      }
    } catch {
      if (request === version) status.textContent = 'Search is temporarily unavailable. Browse the projects and writing pages, or try again.';
    }
  };
  input.addEventListener('input', () => { ++version; clearTimeout(timer); timer = setTimeout(run, 120); });
  form.addEventListener('submit', event => { event.preventDefault(); clearTimeout(timer); run(); if (!root.matches('dialog')) { const url = new URL(location.href); if(input.value.trim()) url.searchParams.set('q', input.value.trim()); else url.searchParams.delete('q'); history.replaceState(null, '', url); } });
  if (!root.matches('dialog')) { input.value = new URLSearchParams(location.search).get('q')?.slice(0, 200) || ''; if (input.value) run(); }
  return { run, input };
}
export function mountSearchDialog(dialog, repository) {
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const search = mountSearch(dialog, repository);
  let trigger;
  const open = element => { if(dialog.open) return; trigger = element; dialog.showModal(); search.input.focus(); };
  document.querySelectorAll('[data-open-search]').forEach(link => link.addEventListener('click', event => { if(event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return; event.preventDefault(); open(link); }));
  dialog.querySelector('[data-close-search]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => trigger?.focus());
  dialog.addEventListener('click', event => { if(event.target !== dialog) return; const r = dialog.getBoundingClientRect(); if(event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); });
  document.addEventListener('keydown', event => { const editing = event.target.closest('input,textarea,select,[contenteditable]'); if(!editing && (event.key === '/' || ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k'))) { event.preventDefault(); open(document.activeElement); } });
}
