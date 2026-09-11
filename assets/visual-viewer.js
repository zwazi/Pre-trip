/* Shared photo/diagram viewer. Each image is stored once; overlays vary by check. */
(() => {
  'use strict';
  const catalog = window.PRETRIP_VISUALS;
  const dialog = document.getElementById('visualDialog');
  const canvas = document.getElementById('visualCanvas');
  const title = document.getElementById('visualTitle');
  const caption = document.getElementById('visualCaption');
  const note = document.getElementById('visualNote');
  const legend = document.getElementById('visualLegend');
  const count = document.getElementById('visualCount');
  const prev = document.getElementById('visualPrev');
  const next = document.getElementById('visualNext');
  const zoom = document.getElementById('visualZoom');
  const annotations = document.getElementById('visualAnnotations');
  const error = document.getElementById('visualError');
  const ns = 'http://www.w3.org/2000/svg';
  let views = [], active = 0, opener, serial = 0;
  function svg(tag, attrs = {}) {
    const el = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
    return el;
  }
  function resetZoom() {
    canvas.classList.remove('zoomed');
    zoom.setAttribute('aria-pressed', 'false');
    zoom.textContent = 'Enlarge';
    canvas.scrollTop = canvas.scrollLeft = 0;
  }
  function render() {
    const view = views[active];
    const asset = view.photo ? catalog.photos[view.photo] : catalog.diagrams[view.diagram];
    const w = asset.width, h = asset.height, unit = Math.max(w, h);
    serial++;
    const renderSerial = serial;
    resetZoom();
    canvas.replaceChildren();
    legend.replaceChildren();
    error.hidden = true;
    caption.textContent = (view.photo ? 'YOUR PHOTO · ' : 'ILLUSTRATIVE DIAGRAM · ') + asset.title;
    note.textContent = view.note || 'Numbered pointers identify the parts for this check.';
    count.textContent = `${active + 1} / ${views.length}`;
    prev.disabled = active === 0;
    next.disabled = active === views.length - 1;
    const figure = svg('svg', {viewBox: `0 0 ${w} ${h}`, role: 'img', 'aria-label': title.textContent + '. ' + view.marks.map(m => m.label).join('; ')});
    figure.style.aspectRatio = `${w} / ${h}`;
    const photo = svg('image', {href: asset.src, width: w, height: h, preserveAspectRatio: 'xMidYMid meet'});
    photo.addEventListener('error', () => { if (serial === renderSerial) error.hidden = false; });
    figure.append(photo);
    const defs = svg('defs');
    const arrowId = `guide-arrow-${serial}`;
    const arrow = svg('marker', {id: arrowId, viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 5, markerHeight: 5, orient: 'auto-start-reverse'});
    arrow.append(svg('path', {d: 'M 0 0 L 10 5 L 0 10 z', fill: '#ffce66'}));
    defs.append(arrow);figure.append(defs);
    const marks = svg('g', {class: 'visual-marks', 'aria-hidden': 'true'});
    marks.style.display = annotations.getAttribute('aria-pressed') === 'true' ? '' : 'none';
    const radius = unit * .020;
    view.marks.forEach((m, i) => {
      const x = m.x / 100 * w, y = m.y / 100 * h;
      const bw = m.w / 100 * w, bh = m.h / 100 * h;
      const ax = Math.min(w-radius*1.3, Math.max(radius*1.3, (m.ax ?? m.x - 6) / 100 * w));
      const ay = Math.min(h-radius*1.3, Math.max(radius*1.3, (m.ay ?? m.y - 6) / 100 * h));
      const targetX = m.tx == null ? x+bw/2 : m.tx/100*w;
      const targetY = m.ty == null ? y+bh/2 : m.ty/100*h;
      const group = svg('g');
      group.append(svg('rect', {x,y,width:bw,height:bh,rx:unit*.005,fill:'#ffce66','fill-opacity':'.1',stroke:'#171715','stroke-width':unit*.007}));
      group.append(svg('rect', {x,y,width:bw,height:bh,rx:unit*.005,fill:'none',stroke:'#ffce66','stroke-width':unit*.0035}));
      group.append(svg('line', {x1:ax,y1:ay,x2:targetX,y2:targetY,stroke:'#171715','stroke-width':unit*.007}));
      group.append(svg('line', {x1:ax,y1:ay,x2:targetX,y2:targetY,stroke:'#ffce66','stroke-width':unit*.0035,'marker-end':`url(#${arrowId})`}));
      group.append(svg('circle', {cx:ax,cy:ay,r:radius,fill:'#ffce66',stroke:'#171715','stroke-width':unit*.0025}));
      const number = svg('text', {x:ax,y:ay,'text-anchor':'middle','dominant-baseline':'central',fill:'#171715','font-family':'system-ui,sans-serif','font-size':radius*1.2,'font-weight':'800'});
      number.textContent=i+1;group.append(number);marks.append(group);
      const item = document.createElement('li');
      const badge = document.createElement('span');badge.className='visual-number';badge.textContent=i+1;badge.setAttribute('aria-hidden','true');
      const label=document.createElement('span');label.textContent=m.label;item.append(badge,label);legend.append(item);
    });
    figure.append(marks);canvas.append(figure);
  }
  document.querySelectorAll('.image-toggle').forEach(button => {
    button.addEventListener('click', () => {
      const card = button.closest('.check-card');
      const id = card.querySelector('.task-check').dataset.id;
      const guide = catalog?.checks[id];
      if (!guide) return;
      opener = button;
      title.textContent = card.querySelector('.component-title').textContent;
      views = guide.views;active = 0;
      annotations.setAttribute('aria-pressed','true');
      render();dialog.showModal();document.getElementById('visualClose').focus();
    });
  });
  document.getElementById('visualClose').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { resetZoom();opener?.focus(); });
  prev.addEventListener('click', () => { if(active>0){active--;render();} });
  next.addEventListener('click', () => { if(active<views.length-1){active++;render();} });
  annotations.addEventListener('click', () => {
    const visible=annotations.getAttribute('aria-pressed')!=='true';
    annotations.setAttribute('aria-pressed',String(visible));
    canvas.querySelector('.visual-marks').style.display=visible?'':'none';
  });
  zoom.addEventListener('click', () => {
    const enlarged=canvas.classList.toggle('zoomed');
    zoom.setAttribute('aria-pressed',String(enlarged));zoom.textContent=enlarged?'Fit image':'Enlarge';
  });
  dialog.addEventListener('keydown', e => {
    if(e.target===canvas && canvas.classList.contains('zoomed')) return;
    if(e.key==='ArrowLeft' && active>0){e.preventDefault();active--;render();}
    if(e.key==='ArrowRight' && active<views.length-1){e.preventDefault();active++;render();}
  });
})();
