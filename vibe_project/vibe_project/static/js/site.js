(function () {
  'use strict';

  /* ---- Tab nav: scroll-to section ---- */
  var tabs = document.querySelectorAll('.tab');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var el = document.getElementById(tab.getAttribute('data-target'));
      if (el) window.scrollTo({ top: el.offsetTop - 86, behavior: 'smooth' });
    });
  });

  var sections = ['program', 'schedule', 'reviews', 'why', 'dresscode', 'ask']
    .map(function (id) { return document.getElementById(id); });

  /* RAF-throttle: запускаем обработчик максимум 1 раз за кадр,
     не блокируем главный поток при быстром скролле */
  var _rafPending = false;
  function onScroll() {
    if (_rafPending) return;
    _rafPending = true;
    requestAnimationFrame(function () {
      _rafPending = false;
      var y = window.scrollY + 140, active = null;
      sections.forEach(function (s) { if (s && s.offsetTop <= y) active = s.id; });
      tabs.forEach(function (t) {
        t.classList.toggle('is-active', t.getAttribute('data-target') === active);
      });
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- Reveal on scroll ---- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  /* ---- Accordion — GPU-safe open/close via grid-template-rows ----
     Нет анимации height → нет Layout/Reflow на всей странице.
     Стрелка анимируется только через transform (compositor thread). */
  document.querySelectorAll('.acc-head').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = this.closest('.acc-item');
      var willOpen = !item.classList.contains('open');
      item.classList.toggle('open');
      btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    });
  });

  /* ---- Booking form ---- */
  var form = document.getElementById('askform');
  if (form) {
    var ca = Math.floor(Math.random() * 8) + 2;
    var cb = Math.floor(Math.random() * 8) + 2;
    var captchaSum = ca + cb;
    var qEl = document.getElementById('captcha-q');
    if (qEl) qEl.textContent = ca + ' + ' + cb;
    var capWrap = document.querySelector('.captcha');
    var capInput = document.getElementById('captcha-input');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (i) {
        if (!i.value.trim()) { i.style.borderColor = 'var(--pop)'; ok = false; }
      });
      if (capInput && parseInt(capInput.value, 10) !== captchaSum) {
        capWrap.classList.add('bad');
        capWrap.classList.remove('ok');
        ok = false;
      } else if (capWrap) {
        capWrap.classList.remove('bad');
        capWrap.classList.add('ok');
      }
      if (!ok) return;

      var data = {};
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        if (el.name) data[el.name] = el.value;
      });

      fetch('/booking/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
      }).then(function (r) { return r.json(); }).then(function (resp) {
        if (resp.ok) {
          form.classList.add('sent');
          form.querySelector('button[type=submit]').textContent = 'Заявка отправлена ✓';
        }
      }).catch(function () {
        form.classList.add('sent');
        form.querySelector('button[type=submit]').textContent = 'Заявка отправлена ✓';
      });
    });
    form.querySelectorAll('input').forEach(function (i) {
      i.addEventListener('input', function () { i.style.borderColor = ''; });
    });
    if (capInput) capInput.addEventListener('input', function () {
      if (capWrap) capWrap.classList.remove('bad');
    });
  }

  /* ---- Cookie banner ---- */
  var cookie = document.getElementById('cookie');
  if (cookie) {
    try {
      if (!localStorage.getItem('vt_cookie_ok')) { cookie.hidden = false; }
    } catch (e) { cookie.hidden = false; }
    var ok = document.getElementById('cookie-ok');
    if (ok) ok.addEventListener('click', function () {
      cookie.hidden = true;
      try { localStorage.setItem('vt_cookie_ok', '1'); } catch (e) {}
    });
  }

  onScroll();

  /* ---- Mobile book btn: appear only when hero btn--neon is out of view ---- */
  var mobBtn = document.querySelector('.mob-book-btn');
  var heroBtn = document.querySelector('.hero__cta .btn--neon');
  if (mobBtn && heroBtn && window.matchMedia('(max-width:640px)').matches) {
    var mobIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        mobBtn.classList.toggle('nav--hidden', e.isIntersecting);
      });
    }, { threshold: 0, rootMargin: '0px' });
    mobIo.observe(heroBtn);
  }
})();
