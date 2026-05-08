/* ============================================================
   EPIRUS ASSETS — main.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initCookieBanner();
  setActiveNavLink();
  setCurrentYear();
  initTagFilter();
});

/* ── Navigation ────────────────────────────────────────────── */
function initNav() {
  const burger = document.querySelector('.nav-burger');
  const links  = document.querySelector('.nav-links');
  if (!burger || !links) return;

  const close = () => {
    burger.classList.remove('is-open');
    links.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  };

  burger.addEventListener('click', () => {
    const opening = !burger.classList.contains('is-open');
    if (opening) {
      burger.classList.add('is-open');
      links.classList.add('is-open');
      burger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    } else {
      close();
    }
  });

  links.querySelectorAll('a').forEach(a => a.addEventListener('click', close));

  document.addEventListener('click', e => {
    if (!burger.contains(e.target) && !links.contains(e.target)) close();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') close();
  });
}

/* ── Active nav link ────────────────────────────────────────── */
function setActiveNavLink() {
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a[href]').forEach(a => {
    const href = a.getAttribute('href').split('/').pop();
    if (href === current) a.classList.add('is-active');
  });
}

/* ── Cookie banner ──────────────────────────────────────────── */
function initCookieBanner() {
  const banner = document.getElementById('cookie-banner');
  if (!banner) return;

  if (localStorage.getItem('ea_consent')) {
    banner.classList.add('is-hidden');
    return;
  }

  document.getElementById('cookie-accept')?.addEventListener('click', () => {
    localStorage.setItem('ea_consent', 'accepted');
    banner.classList.add('is-hidden');
  });

  document.getElementById('cookie-reject')?.addEventListener('click', () => {
    localStorage.setItem('ea_consent', 'rejected');
    banner.classList.add('is-hidden');
  });
}

/* ── Footer / year ──────────────────────────────────────────── */
function setCurrentYear() {
  document.querySelectorAll('.js-year').forEach(el => {
    el.textContent = new Date().getFullYear();
  });
}

/* ── Tag filter (investments page) ─────────────────────────── */
function initTagFilter() {
  const tags = document.querySelectorAll('[data-filter]');
  const cards = document.querySelectorAll('[data-category]');
  if (!tags.length || !cards.length) return;

  tags.forEach(tag => {
    tag.addEventListener('click', () => {
      tags.forEach(t => t.classList.remove('is-active'));
      tag.classList.add('is-active');

      const filter = tag.getAttribute('data-filter');
      cards.forEach(card => {
        const show = filter === 'all' || card.getAttribute('data-category') === filter;
        card.style.display = show ? '' : 'none';
      });
    });
  });
}
