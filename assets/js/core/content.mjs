// Pure content rules. No DOM, network, or rendering dependencies.
export const normalize = (value = '') => String(value).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
export function searchContent(items, query, limit = 20) {
  const terms = normalize(query).slice(0, 200).split(/\s+/).filter(Boolean);
  if (!terms.length) return [];
  return items.map((item, index) => {
    const title = normalize(item.title);
    const topics = normalize([...(item.topics || []), item.type].join(' '));
    const body = normalize(`${item.description || ''} ${item.text || ''}`);
    if (!terms.every(term => title.includes(term) || topics.includes(term) || body.includes(term))) return null;
    const score = terms.reduce((total, term) => total + (title.includes(term) ? 10 : 0) + (topics.includes(term) ? 4 : 0) + (body.includes(term) ? 1 : 0), 0);
    return { item, score, index };
  }).filter(Boolean).sort((a, b) => b.score - a.score || a.index - b.index).slice(0, limit).map(match => match.item);
}
export function matchesCategory(item, category) {
  return category === 'all' || normalize(item.category) === normalize(category);
}
export function localContentPath(value, origin) {
  try {
    const url = new URL(value, origin);
    return url.origin === origin && ['http:', 'https:'].includes(url.protocol) ? `${url.pathname}${url.search}${url.hash}` : null;
  } catch { return null; }
}
