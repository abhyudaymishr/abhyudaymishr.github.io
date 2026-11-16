import { matchesCategory } from '../core/content.mjs';
export function mountProjectFilters(root) {
  if (!root) return;
  const bar = root.querySelector('[data-project-filters]');
  const cards = [...root.querySelectorAll('[data-project]')];
  const count = root.querySelector('[data-project-count]');
  if (!bar || !count) return;
  const buttons = [...bar.querySelectorAll('[data-filter]')];
  const apply = category => {
    if (!buttons.some(button => button.dataset.filter === category)) category = 'all';
    let total = 0;
    for(const card of cards) { card.hidden = !matchesCategory(card.dataset, category); if(!card.hidden) ++total; }
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    count.textContent = `${total} project${total === 1 ? '' : 's'}${category === 'all' ? ' across all research areas' : ` in ${category}`}`;
  };
  bar.hidden = false; count.hidden = false;
  bar.addEventListener('click', event => { const button = event.target.closest('[data-filter]'); if(!button) return; const url = new URL(location.href); if(button.dataset.filter === 'all') url.searchParams.delete('area'); else url.searchParams.set('area', button.dataset.filter); history.pushState(null, '', url); apply(button.dataset.filter); });
  window.addEventListener('popstate', () => apply(new URLSearchParams(location.search).get('area') || 'all'));
  apply(new URLSearchParams(location.search).get('area') || 'all');
}
