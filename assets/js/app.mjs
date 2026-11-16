import { createContentRepository } from './data/content-repository.mjs';
import { mountSearch, mountSearchDialog } from './ui/search.mjs';
import { mountProjectFilters } from './ui/projects.mjs';
const repository = createContentRepository(document.body.dataset.indexUrl);
mountSearchDialog(document.querySelector('[data-search-dialog]'), repository);
const searchPage = document.querySelector('[data-search-page]');
if (searchPage) mountSearch(searchPage, repository);
mountProjectFilters(document.querySelector('[data-project-browser]'));
const navigation = document.querySelector('[data-navigation]');
navigation?.addEventListener('keydown', event => { if(event.key === 'Escape') { navigation.open = false; navigation.querySelector('summary').focus(); } });
document.addEventListener('click', event => { if(navigation?.open && !navigation.contains(event.target)) navigation.open = false; });
const toc = document.querySelector('[data-toc]');
if (toc) {
  for (const heading of document.querySelectorAll('.article-body h2[id]')) {
    const item = document.createElement('li'); const link = document.createElement('a');
    link.href = `#${heading.id}`; link.textContent = heading.textContent; item.append(link); toc.append(item);
  }
  if(toc.children.length) toc.closest('[data-toc-container]').hidden = false;
}
