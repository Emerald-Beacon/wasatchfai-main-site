document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu
  const toggle = document.getElementById('menuToggle');
  const nav = document.getElementById('mainNav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
    nav.querySelectorAll('a').forEach(a => {
      if (!a.closest('.has-dropdown') || a.closest('.dropdown-menu')) {
        a.addEventListener('click', () => nav.classList.remove('open'));
      }
    });
  }

  // Services dropdown: tap-to-open on mobile, hover handled by CSS on desktop
  nav && nav.querySelectorAll('li.has-dropdown > a').forEach(link => {
    link.addEventListener('click', (e) => {
      if (window.matchMedia('(max-width: 980px)').matches) {
        e.preventDefault();
        link.closest('li').classList.toggle('open');
      }
    });
  });

  // Reveal on scroll
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
});
