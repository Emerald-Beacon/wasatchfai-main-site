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
      track.addEventListener('touchcancel', () => {
        startX = null;
        start();
      }, { passive: true });
    }

    start();
  }

  // ============ SERVICES SEARCH FILTER ============
  if (document.getElementById('serviceSearch')) {
    const input = document.getElementById('serviceSearch');
    const cards = Array.from(document.querySelectorAll('#servicesGrid .help-card'));
    const empty = document.getElementById('servicesEmpty');
    const status = document.getElementById('servicesStatus');
    if (input && cards.length) {
      input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        let visible = 0;
        cards.forEach(card => {
          const haystack = (card.dataset.name || '') + ' ' + card.textContent.toLowerCase();
          const match = q === '' || haystack.toLowerCase().includes(q);
          card.style.display = match ? '' : 'none';
          if (match) visible++;
        });
        if (empty) empty.hidden = visible !== 0;
        if (status) {
          status.textContent = visible === 0
            ? 'No services match your search.'
            : visible + ' service' + (visible === 1 ? '' : 's') + ' found.';
        }
      });
    }
  }

  // ============ CURSOR FOOTPRINTS (desktop mouse only) ============
  (function initFootprints() {
    const finePointer = window.matchMedia('(pointer: fine)').matches;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!finePointer || reduce) return; // skip on touch devices & reduced-motion

    const STEP = 52;   // px of cursor travel between prints
    const PERP = 8;    // px each foot sits off the path centre line
    const LIFE = 1500; // ms a print lives (fades over ~2-3 following steps)
    const foot = '<svg viewBox="0 0 64 96" fill="currentColor" aria-hidden="true">'
      + '<ellipse cx="18" cy="15" rx="7.5" ry="9.5"/>'
      + '<ellipse cx="32" cy="9" rx="6" ry="7.5"/>'
      + '<ellipse cx="42" cy="10" rx="5.2" ry="6.5"/>'
      + '<ellipse cx="50" cy="14" rx="4.3" ry="5.3"/>'
      + '<ellipse cx="56" cy="20" rx="3.5" ry="4.3"/>'
      + '<path d="M16 42 C13 30 23 25 33 25 C45 25 53 31 52 45 C51 57 47 64 46 72 C45 83 39 91 32 91 C25 91 19 84 21 74 C27 62 27 50 16 42 Z"/>'
      + '</svg>';

    let lastX = null, lastY = null, travel = 0, side = 1;

    window.addEventListener('mousemove', (e) => {
      if (lastX === null) { lastX = e.clientX; lastY = e.clientY; return; }
      const dx = e.clientX - lastX, dy = e.clientY - lastY;
      const d = Math.hypot(dx, dy);
      lastX = e.clientX; lastY = e.clientY;
      if (d === 0) return;
      travel += d;
      if (travel < STEP) return;
      travel = 0;
      const deg = Math.atan2(dy, dx) * 180 / Math.PI; // 0deg = moving right
      const perpX = -dy / d, perpY = dx / d;           // unit vector perpendicular to travel
      const ox = perpX * PERP * side, oy = perpY * PERP * side;
      const print = document.createElement('div');
      print.className = 'footprint';
      print.innerHTML = foot;
      print.style.left = (e.clientX + ox) + 'px';
      print.style.top = (e.clientY + oy) + 'px';
      // art points "up" by default: +90deg faces travel direction; scaleX mirrors L/R feet
      print.style.transform = 'translate(-50%,-50%) rotate(' + (deg + 90) + 'deg) scaleX(' + side + ')';
      document.body.appendChild(print);
      setTimeout(() => print.remove(), LIFE);
      side *= -1; // alternate left / right foot
    }, { passive: true });
  })();
});
