// Motor de animación determinista: el renderizador fija el tiempo y toma capturas.
(function () {
  const ease = p => 1 - Math.pow(1 - p, 3);
  const clamp = v => Math.max(0, Math.min(1, v));
  const fmt = (v, dec, miles, decimal) => {
    let s = Number(v).toFixed(dec);
    let [ent, fr] = s.split('.');
    const neg = ent.startsWith('-');
    if (neg) ent = ent.slice(1);
    if (ent.length > 4) ent = ent.replace(/\B(?=(\d{3})+(?!\d))/g, miles);
    return (neg ? '-' : '') + ent + (fr ? decimal + fr : '');
  };
  window.__beatStarts = [0];

  function apply(el, t) {
    const b = parseInt(el.dataset.b || '0', 10);
    const start = window.__beatStarts[b];
    const dur = parseFloat(el.dataset.dur || '0.45');
    const delay = parseFloat(el.dataset.delay || '0');
    let p = start === undefined ? 0 : clamp((t - start - delay) / dur);
    const e = ease(p);
    const a = el.dataset.a || 'up';
    switch (a) {
      case 'up': el.style.opacity = e; el.style.transform = `translateY(${(1 - e) * 46}px)`; break;
      case 'down': el.style.opacity = e; el.style.transform = `translateY(${(e - 1) * 46}px)`; break;
      case 'left': el.style.opacity = e; el.style.transform = `translateX(${(1 - e) * -70}px)`; break;
      case 'right': el.style.opacity = e; el.style.transform = `translateX(${(1 - e) * 70}px)`; break;
      case 'pop': el.style.opacity = clamp(p * 2.2); el.style.transform = `scale(${0.82 + 0.18 * e + Math.sin(p * Math.PI) * 0.04})`; break;
      case 'fade': el.style.opacity = e; break;
      case 'grow': el.style.setProperty('--g', e); el.style.opacity = p > 0 ? 1 : 0; break;
      case 'strike': el.style.setProperty('--s', e); break;
      case 'hl': el.style.setProperty('--h', e); break;
      case 'count': {
        const from = parseFloat(el.dataset.from || '0'), to = parseFloat(el.dataset.to);
        const dec = parseInt(el.dataset.dec || '0', 10);
        el.textContent = (el.dataset.pre || '') + fmt(from + (to - from) * e, dec, el.dataset.miles || ' ', el.dataset.decimal || ',') + (el.dataset.suf || '');
        el.style.opacity = p > 0 ? 1 : 0; break;
      }
      case 'draw': {
        const len = parseFloat(el.dataset.len || '3000');
        el.style.strokeDasharray = len; el.style.strokeDashoffset = len * (1 - e);
        el.style.opacity = p > 0 ? 1 : 0; break;
      }
      case 'type': {
        if (el.__full === undefined) el.__full = el.innerHTML;
        const txt = el.__full;
        // escribe respetando etiquetas HTML simples
        let n = Math.round(el.dataset.chars * clamp((t - start - delay) / dur)), out = '', count = 0, i = 0;
        while (i < txt.length && count < n) {
          if (txt[i] === '<') { const j = txt.indexOf('>', i); out += txt.slice(i, j + 1); i = j + 1; continue; }
          if (txt[i] === '&') { const j = txt.indexOf(';', i); out += txt.slice(i, j + 1); i = j + 1; count++; continue; }
          out += txt[i]; i++; count++;
        }
        // cerrar etiquetas abiertas
        const abiertas = (out.match(/<span[^>]*>/g) || []).length - (out.match(/<\/span>/g) || []).length;
        out += '</span>'.repeat(Math.max(0, abiertas));
        const caret = p < 1 && p > 0 ? '<i class="caret"></i>' : '';
        el.innerHTML = out + caret; el.style.opacity = p > 0 ? 1 : 0; break;
      }
    }
  }

  function over(el) {
    const cs = getComputedStyle(el);
    const maxH = cs.maxHeight === 'none' ? Infinity : parseFloat(cs.maxHeight);
    return el.scrollHeight > maxH + 4 || el.scrollWidth > el.clientWidth + 4;
  }
  function fit() {
    document.querySelectorAll('.fit').forEach(el => {
      let size = parseFloat(getComputedStyle(el).fontSize);
      const min = parseFloat(el.dataset.min || '28');
      let guard = 0;
      while (over(el) && size > min && guard < 80) {
        size -= 2; el.style.fontSize = size + 'px'; guard++;
      }
      el.dataset.fitted = size;
    });
  }
  // Planillas y tarjetas: reducir la letra hasta que el contenido entre a lo ancho
  function fitWidth() {
    document.querySelectorAll('.fitw').forEach(el => {
      const box = el.parentElement;
      let size = parseFloat(getComputedStyle(el).fontSize), guard = 0;
      const min = parseFloat(el.dataset.min || '22');
      while (el.scrollWidth > box.clientWidth + 2 && size > min && guard < 60) {
        size -= 1; el.style.fontSize = size + 'px'; guard++;
      }
    });
  }
  window.__over = over;

  window.setup = function () {
    document.querySelectorAll('[data-a="type"]').forEach(el => {
      el.__full = el.innerHTML;
      el.dataset.chars = el.textContent.length;
    });
    document.querySelectorAll('[data-a="draw"]').forEach(el => {
      if (el.getTotalLength) el.dataset.len = Math.ceil(el.getTotalLength()) + 2;
    });
    fit();
    fitWidth();
    const beats = {};
    document.querySelectorAll('[data-b]').forEach(el => {
      const b = parseInt(el.dataset.b, 10);
      const end = parseFloat(el.dataset.dur || '0.45') + parseFloat(el.dataset.delay || '0');
      beats[b] = Math.max(beats[b] || 0, end);
    });
    const overflow = [];
    document.querySelectorAll('.fit').forEach(el => {
      if (over(el)) overflow.push(el.className + ': ' + el.textContent.slice(0, 40));
    });
    document.querySelectorAll('.fitw, .vs .card, .calc .l, .opt, .li').forEach(el => {
      const box = el.classList.contains('fitw') ? el.parentElement : el;
      if (box.scrollWidth > box.clientWidth + 4) overflow.push('ancho ' + el.className + ': ' + el.textContent.slice(0, 40));
    });
    // nada puede salirse del escenario (por abajo pisaría los subtítulos)
    const st = document.getElementById('stage');
    if (st) {
      const lim = st.getBoundingClientRect().bottom + 4;
      st.querySelectorAll(':scope > *, .sheet, .list, .steps, .calc, .opts, .vs').forEach(el => {
        const b = el.getBoundingClientRect().bottom;
        if (b > lim) overflow.push('alto ' + el.className + ': sobra ' + Math.round(b - lim + 4) + 'px');
      });
    }
    return { beats, overflow };
  };

  window.setState = function (t, beatStarts, capHtml, capT) {
    window.__beatStarts = beatStarts;
    document.querySelectorAll('[data-b]').forEach(el => apply(el, t));
    const cap = document.getElementById('cap');
    if (cap) {
      if (cap.__last !== capHtml) { cap.innerHTML = capHtml || ''; cap.__last = capHtml; }
      const p = clamp(capT / 0.14), e = ease(p);
      cap.style.opacity = capHtml ? clamp(p * 1.6) : 0;
      cap.style.transform = `translateX(-50%) scale(${0.9 + 0.1 * e})`;
    }
  };
})();
