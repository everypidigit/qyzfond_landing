// Every language has a complete server-rendered page, including social metadata.
const body = document.body;
const base = body.dataset.base || '';
const page = body.dataset.page || '';
const query = new URLSearchParams(location.search);
const explicit = query.get('lang')?.toLowerCase();
const normalize = value => value === 'kz' ? 'kk' : value;
const languages = ['ru', 'kk', 'en'];
const pathLanguage = location.pathname.slice(base.length).split('/').filter(Boolean)[0];
let preferred;
try { preferred = localStorage.getItem('qyz-lang'); } catch {}
const requested = normalize(explicit) || (languages.includes(pathLanguage) ? pathLanguage : preferred);
if (languages.includes(requested) && requested !== body.dataset.lang) {
  const target = new URL(base + '/' + requested + '/' + page + (page ? '/' : '') + location.hash, location.origin);
  location.replace(target.href);
} else {
  try { localStorage.setItem('qyz-lang', body.dataset.lang); } catch {}
  document.querySelectorAll('.languages a').forEach(a => {
    a.hash = location.hash;
    a.addEventListener('click', () => { try { localStorage.setItem('qyz-lang', a.dataset.lang); } catch {} });
  });
}
document.querySelectorAll('[data-until]').forEach(el => {
  if (Date.now() >= Date.parse(el.dataset.until)) el.hidden = true;
});
const menu = document.querySelector('.menu-button');
menu?.addEventListener('click', () => {
  const open = body.classList.toggle('menu-open');
  menu.setAttribute('aria-expanded', String(open));
});
document.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => {
  body.classList.remove('menu-open'); menu?.setAttribute('aria-expanded', 'false');
}));
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(items => items.forEach(item => {
    if (item.isIntersecting) { item.target.classList.add('shown'); observer.unobserve(item.target); }
  }), {threshold: 0.03});
  document.querySelectorAll('section').forEach(section => observer.observe(section));
} else document.querySelectorAll('section').forEach(section => section.classList.add('shown'));

