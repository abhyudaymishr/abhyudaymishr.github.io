// The only network boundary. Both search surfaces share a single, cached request.
export function createContentRepository(url, fetcher = globalThis.fetch) {
  let pending;
  return {
    load() {
      if (!pending) pending = fetcher(url, { credentials: 'same-origin' }).then(response => {
        if (!response.ok) throw new Error('Content index unavailable');
        return response.json();
      }).then(data => {
        if (!Array.isArray(data.items)) throw new Error('Invalid content index');
        return data.items.filter(item => typeof item.title === 'string' && typeof item.url === 'string');
      }).catch(error => { pending = undefined; throw error; });
      return pending;
    }
  };
}
