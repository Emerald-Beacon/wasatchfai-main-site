// Opt in to the scroll-reveal styling only once this script is running, so a
// failed or blocked script can never leave content stuck at opacity 0.
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.documentElement.classList.add('js-reveal');
}

document.addEventListener('DOMContentLoaded', () => {
  // Reveal on scroll — set up first so a fault anywhere below cannot leave
  // sections invisible.
  const show = (el) => { el.classList.add('in'); io.unobserve(el); };
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) show(e.target); });
  }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // Chrome throttles IntersectionObserver in background tabs, which can leave
  // whole sections blank when a page loads unfocused or from a restored
  // session. Sweep anything already at or above the fold.
  const sweep = () => {
    document.querySelectorAll('.reveal:not(.in)').forEach(el => {
      if (el.getBoundingClientRect().top < window.innerHeight + 100) show(el);
    });
  };
  window.addEventListener('load', () => setTimeout(sweep, 400));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) sweep(); });
  // A jump link can land far past anything the observer has seen.
  window.addEventListener('hashchange', () => setTimeout(sweep, 50));

  // Mobile menu
  const toggle = document.getElementById('menuToggle');
  const nav = document.getElementById('mainNav');
  if (toggle && nav) {
    if (!nav.id) nav.id = 'mainNav';
    toggle.setAttribute('aria-controls', nav.id);
    const setMenu = (open) => {
      nav.classList.toggle('open', open);
      toggle.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
    };
    setMenu(false);
    toggle.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
    nav.querySelectorAll('a').forEach(a => {
      if (!a.closest('.has-dropdown') || a.closest('.dropdown-menu')) {
        a.addEventListener('click', () => setMenu(false));
      }
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); toggle.focus(); }
    });
    document.addEventListener('click', (e) => {
      if (!nav.classList.contains('open')) return;
      if (!nav.contains(e.target) && !toggle.contains(e.target)) setMenu(false);
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

  // ============ ON THIS PAGE ============
  // A condition page runs eight sections and 1,100+ words with no way in.
  // Build the contents from the h2 ids already in the markup.
  (function initToc() {
    const article = document.querySelector('.detail-body, .prose');
    const aside = document.querySelector('.detail-aside');
    if (!article) return;
    const heads = [...article.querySelectorAll('h2[id]')];
    if (heads.length < 3) return;

    const toc = document.createElement('details');
    toc.className = 'toc';
    const summary = document.createElement('summary');
    summary.textContent = 'On this page';
    toc.appendChild(summary);

    const list = document.createElement('ol');
    list.className = 'toc-list';
    const links = heads.map(h => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.className = 'toc-link';
      a.href = '#' + h.id;
      a.textContent = h.textContent.trim();
      li.appendChild(a);
      list.appendChild(li);
      return a;
    });
    toc.appendChild(list);

    // Desktop keeps it open in the sticky rail; phones get it collapsed at the
    // top of the article, where the rail no longer is.
    const wide = window.matchMedia('(min-width: 981px)');
    const place = () => {
      if (wide.matches && aside) {
        toc.open = true;
        if (toc.parentElement !== aside) aside.insertBefore(toc, aside.firstChild);
      } else {
        // Blog posts have no rail, so the contents sit inline — open on a wide
        // screen where there is room, collapsed on a phone where there isn't.
        toc.open = wide.matches;
        if (toc.parentElement !== article) article.insertBefore(toc, article.firstChild);
      }
    };
    place();
    wide.addEventListener('change', place);

    // Highlight the section being read.
    let active = null;
    const spy = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = heads.indexOf(e.target);
        if (i < 0) return;
        if (active) active.removeAttribute('aria-current');
        active = links[i];
        active.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-100px 0px -70% 0px' });
    heads.forEach(h => spy.observe(h));

    // Surface the urgency guidance, which sits seventh of eight in the article.
    const urgent = heads.find(h => /when should you see|when to see|warning signs?/i.test(h.textContent));
    const card = aside && aside.querySelector('.aside-card');
    if (urgent && card) {
      const note = document.createElement('p');
      note.className = 'aside-urgent';
      note.innerHTML =
        '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">'
        + '<path d="M12 2 1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v5h2v-5z"/></svg>'
        + '<span>Not sure whether this needs a visit? Read <a href="#' + urgent.id + '">'
        + urgent.textContent.trim().replace(/\?$/, '').toLowerCase() + '</a>.</span>';
      card.insertBefore(note, card.querySelector('.aside-phones'));
    }
  })();

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
