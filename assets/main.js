(function () {
  var d = document, h = d.getElementById('hdr');
  // Cabecera: transparente sobre el hero, sólida al bajar
  function onScroll() { h.classList.toggle('solid', window.scrollY > 40); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  // Menú móvil
  var btn = d.querySelector('.menu-btn'), nav = d.getElementById('nav');
  function setMenu(open) {
    d.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open); btn.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    d.body.style.overflow = open ? 'hidden' : '';
  }
  btn.addEventListener('click', function () { setMenu(!d.body.classList.contains('menu-open')); });
  nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') setMenu(false); });
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  // Aparición suave
  var els = [].slice.call(d.querySelectorAll('.rv'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });

  // Índice de documentación: resalta el tema visible
  var toc = [].slice.call(d.querySelectorAll('.toc a'));
  if (toc.length && 'IntersectionObserver' in window) {
    var map = {}; toc.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (x) { if (x.isIntersecting) { toc.forEach(function (a) { a.classList.remove('on'); }); map[x.target.id].classList.add('on'); } });
    }, { rootMargin: '-20% 0px -70% 0px' });
    d.querySelectorAll('.doc-block').forEach(function (b) { so.observe(b); });
  }

  // Videos de fondo: cargan cuando se ven, se pausan al salir y respetan "reducir movimiento"
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var vids = [].slice.call(d.querySelectorAll('video.bgvid'));
  if (vids.length && !still && 'IntersectionObserver' in window) {
    var vo = new IntersectionObserver(function (es) {
      es.forEach(function (x) {
        var v = x.target;
        if (!v.offsetParent) return; // variante oculta (móvil/escritorio)
        if (x.isIntersecting) {
          if (!v.getAttribute('src')) v.src = v.getAttribute('data-src');
          var pr = v.play(); if (pr && pr.catch) pr.catch(function () {});
        } else v.pause();
      });
    }, { rootMargin: '150px 0px' });
    vids.forEach(function (v) { vo.observe(v); });
  }

  // Formulario: abre el correo con el mensaje preparado (sin servidor)
  var f = d.getElementById('f');
  if (f) f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var g = function (id) { return d.getElementById(id).value.trim(); };
    var body = 'Nombre: ' + g('n') + '\nCorreo: ' + g('m') + '\n\n' + g('x');
    location.href = 'mailto:' + f.getAttribute('action').replace('mailto:', '') +
      '?subject=' + encodeURIComponent(g('a') || 'Consulta desde la web') + '&body=' + encodeURIComponent(body);
  });
})();
