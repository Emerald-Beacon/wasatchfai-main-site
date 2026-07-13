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

  // Hero carousel
  initCarousel();

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

  // ============ HERO CAROUSEL ============
  function initCarousel() {
    const carousel = document.querySelector('.hero-carousel');
    if (!carousel) return;
    const slides = Array.from(carousel.querySelectorAll('.hero-slide'));
    if (slides.length === 0) return;
    const track = carousel.querySelector('.hero-track');
    const prevBtn = carousel.querySelector('.hero-arrow.prev');
    const nextBtn = carousel.querySelector('.hero-arrow.next');
    const dotsWrap = carousel.querySelector('.hero-dots');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let current = slides.findIndex(s => s.classList.contains('is-active'));
    if (current < 0) { current = 0; slides[0].classList.add('is-active'); }
    let timer = null;

    // Build dot indicators from slide count
    const dots = slides.map((_, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', 'Show slide ' + (i + 1));
      dot.setAttribute('aria-selected', i === current ? 'true' : 'false');
      dot.addEventListener('click', () => { goTo(i); restart(); });
      dotsWrap && dotsWrap.appendChild(dot);
      return dot;
    });

    function goTo(i) {
      const n = slides.length;
      const idx = ((i % n) + n) % n;
      if (idx === current) return;
      slides[current].classList.remove('is-active');
      dots[current] && dots[current].setAttribute('aria-selected', 'false');
      current = idx;
      slides[current].classList.add('is-active');
      dots[current] && dots[current].setAttribute('aria-selected', 'true');
    }
    const next = () => goTo(current + 1);
    const prev = () => goTo(current - 1);

    function start() {
      if (reduceMotion) return; // honor reduced motion: no auto-advance
      stop();
      timer = setInterval(next, 6000);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function restart() { stop(); start(); }

    nextBtn && nextBtn.addEventListener('click', () => { next(); restart(); });
    prevBtn && prevBtn.addEventListener('click', () => { prev(); restart(); });

    // Pause on hover, resume on leave
    carousel.addEventListener('mouseenter', stop);
    carousel.addEventListener('mouseleave', start);

    // Keyboard support
    carousel.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { prev(); restart(); }
      else if (e.key === 'ArrowRight') { next(); restart(); }
    });

    // Touch swipe
    let startX = null;
    if (track) {
      track.addEventListener('touchstart', (e) => {
        startX = e.changedTouches[0].clientX;
        stop();
      }, { passive: true });
      track.addEventListener('touchend', (e) => {
        if (startX === null) return;
        const dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 40) { dx < 0 ? next() : prev(); }
        startX = null;
        start();
      }, { passive: true });
    }

    start();
  }
});
