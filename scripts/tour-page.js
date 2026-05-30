/* ============================================================
   VIBE TURISTIC — tour detail page renderer
   Reads window.VIBE_TOUR_KEY ('3' | '5'); uses window.VIBE.
   ============================================================ */
(function () {
  'use strict';
  var V = window.VIBE || {};
  var key = window.VIBE_TOUR_KEY || '5';

  V.renderTourDates && V.renderTourDates(document.getElementById('dates'), key);
  V.renderInfoGrid && V.renderInfoGrid(document.getElementById('infogrid'), key);
  V.renderIncluded && V.renderIncluded(document.getElementById('inc-list'), key);
  V.renderNotIncluded && V.renderNotIncluded(document.getElementById('notinc-list'));
  V.renderTake && V.renderTake(document.getElementById('take'));
  V.renderGallery && V.renderGallery(document.getElementById('gallery'));

  /* ---- Auto-scrolling photo ribbon ---- */
  (function () {
    var strip = document.getElementById('gallery');
    if (!strip) return;
    var dir = 1, paused = false, resumeT;
    function pause() {
      paused = true;
      clearTimeout(resumeT);
      resumeT = setTimeout(function () { paused = false; }, 2500);
    }
    ['pointerdown', 'wheel', 'touchstart', 'mouseenter'].forEach(function (ev) {
      strip.addEventListener(ev, pause, { passive: true });
    });
    strip.addEventListener('mouseleave', function () { paused = false; });
    setInterval(function () {
      if (paused) return;
      var max = strip.scrollWidth - strip.clientWidth;
      if (max <= 4) return;
      if (strip.scrollLeft >= max - 1) dir = -1;
      else if (strip.scrollLeft <= 0) dir = 1;
      strip.scrollLeft += dir * 0.8;
    }, 24);
  })();

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
})();
