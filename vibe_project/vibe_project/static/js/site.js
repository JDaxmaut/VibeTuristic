(function () {
  'use strict';

  var tabs = document.querySelectorAll('.tab');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var el = document.getElementById(tab.getAttribute('data-target'));
      if (el) window.scrollTo({ top: el.offsetTop - 86, behavior: 'smooth' });
    });
  });
  var sections = ['program', 'schedule', 'reviews', 'why', 'dresscode', 'ask'].map(function (id) { return document.getElementById(id); });
  function onScroll() {
    var y = window.scrollY + 140, active = null;
    sections.forEach(function (s) { if (s && s.offsetTop <= y) active = s.id; });
    tabs.forEach(function (t) { t.classList.toggle('is-active', t.getAttribute('data-target') === active); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

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
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value },
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

  var cookie = document.getElementById('cookie');
  if (cookie) {
    try {
      if (!localStorage.getItem('vt_cookie_ok')) {
        cookie.hidden = false;
      }
    } catch (e) { cookie.hidden = false; }
    var ok = document.getElementById('cookie-ok');
    if (ok) ok.addEventListener('click', function () {
      cookie.hidden = true;
      try { localStorage.setItem('vt_cookie_ok', '1'); } catch (e) {}
    });
  }

  onScroll();

  // Mobile bottom nav: hide on scroll down, show on scroll up
  var tabnav = document.getElementById('tabnav');
  var mobBtn = document.querySelector('.mob-book-btn');
  if (tabnav && window.matchMedia('(max-width:640px)').matches) {
    var lastY = window.scrollY;
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          var y = window.scrollY;
          var goingDown = y > lastY && y > 80;
          tabnav.classList.toggle('nav--hidden', goingDown);
          if (mobBtn) mobBtn.classList.toggle('nav--hidden', goingDown);
          lastY = y;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }
})();
