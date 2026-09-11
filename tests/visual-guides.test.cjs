const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
function app(mobile=true){
 const errors=[],scrolls=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
 const dom=new JSDOM(html,{url:'https://zwazi.github.io/Pre-trip/',runScripts:'outside-only',virtualConsole:vc});
 const w=dom.window;w.matchMedia=q=>({matches:q.includes('max-width')&&mobile});w.confirm=()=>true;
 w.requestAnimationFrame=fn=>fn();w.scrollTo=options=>scrolls.push(options);
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};
 w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'));};
 // Run the page's actual scripts in document order, without loading network images.
 for(const script of w.document.scripts) w.eval(script.src?fs.readFileSync(path.join(root,new URL(script.src).pathname.replace('/Pre-trip/','')),'utf8'):script.textContent);
 return {w,d:w.document,errors,scrolls,close:()=>w.close()};
}
test('Every check has a valid photo or diagram with on-image markers and real asset files',()=>{
 const a=app(),{d,w}=a,c=w.PRETRIP_VISUALS;
 const ids=[...d.querySelectorAll('.task-check')].map(b=>b.dataset.id);
 assert.equal(ids.length,139);assert.equal(new Set(ids).size,139);assert.deepEqual(Object.keys(c.checks).sort(),ids.sort());
 assert.equal(Object.keys(c.photos).length,30);
 for(const check of Object.values(c.checks)){
  assert(check.views.length>0);
  for(const view of check.views){
   assert(Boolean(view.photo)!==Boolean(view.diagram));const asset=view.photo?c.photos[view.photo]:c.diagrams[view.diagram];
   assert(asset);assert(asset.width>0&&asset.height>0);assert(fs.statSync(path.join(root,asset.src)).size>0);
   assert(view.marks.length>0);
   for(const m of view.marks){assert(m.label);assert(m.x>=0&&m.y>=0&&m.w>0&&m.h>0&&m.x+m.w<=100&&m.y+m.h<=100);}
   if(view.diagram){const svg=new w.DOMParser().parseFromString(fs.readFileSync(path.join(root,asset.src),'utf8'),'image/svg+xml');assert.equal(svg.querySelector('parsererror'),null);assert(view.note);}
  }
 }
 assert.deepEqual(a.errors,[]);a.close();
});
test('Every image button opens the right labeled view without changing progress or revealing bullets',()=>{
 const a=app(),{d,w}=a;
 assert.equal(d.querySelectorAll('.image-toggle').length,139);assert.equal(d.querySelectorAll('.check-details[hidden]').length,139);
 assert.equal(d.querySelectorAll('#visualCanvas image').length,0,'Images must not load until opened');
 for(const card of d.querySelectorAll('.check-card')){
  const box=card.querySelector('.task-check'),button=card.querySelector('.image-toggle'),toggle=card.querySelector('.details-toggle');
  assert.equal(button.parentElement,toggle.parentElement);assert.equal(button.textContent.trim(),'');assert.equal(toggle.textContent.trim(),'');assert(button.querySelector('svg'));assert(toggle.querySelector('svg'));
  assert(button.getAttribute('aria-label').includes(card.querySelector('.component-title').textContent));button.click();
  assert(d.getElementById('visualDialog').open);assert.equal(d.getElementById('visualTitle').textContent,card.querySelector('.component-title').textContent);
  const view=w.PRETRIP_VISUALS.checks[box.dataset.id].views[0];
  const image=d.querySelector('#visualCanvas image');assert(image.getAttribute('href').startsWith('assets/'));
  assert.equal(d.querySelectorAll('#visualLegend li').length,view.marks.length);assert.equal(d.querySelectorAll('.visual-marks>g').length,view.marks.length);
  assert.equal(box.checked,false);assert(card.querySelector('.check-details').hidden);
  d.getElementById('visualClose').click();assert.equal(d.activeElement,button);
 }
 assert.equal(d.getElementById('doneCount').textContent,'0');assert.deepEqual(a.errors,[]);a.close();
});
test('Alternate views, zoom, pointer toggle, keyboard navigation, close, and image failures',()=>{
 const a=app(),{d,w}=a,$=id=>d.getElementById(id);
 d.querySelector('[data-id="c35"]').closest('.check-card').querySelector('.image-toggle').click();
 assert.match($('visualCaption').textContent,/ILLUSTRATIVE DIAGRAM/);assert.equal($('visualNext').disabled,true);$('visualClose').click();
 d.querySelector('[data-id="c6"]').closest('.check-card').querySelector('.image-toggle').click();
 assert.match($('visualCaption').textContent,/YOUR PHOTO/);assert.equal($('visualPrev').disabled,true);assert.equal($('visualCount').textContent,'1 / 2');
 const first=d.querySelector('#visualCanvas image').getAttribute('href');$('visualAnnotations').click();assert.equal(d.querySelector('.visual-marks').style.display,'none');
 $('visualZoom').click();assert($('visualCanvas').classList.contains('zoomed'));
 $('visualNext').click();assert.equal($('visualCount').textContent,'2 / 2');assert.notEqual(d.querySelector('#visualCanvas image').getAttribute('href'),first);assert.equal($('visualNext').disabled,true);assert(!$('visualCanvas').classList.contains('zoomed'));
 assert.equal(d.querySelector('.visual-marks').style.display,'none');$('visualAnnotations').click();assert.equal(d.querySelector('.visual-marks').style.display,'');
 $('visualDialog').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));assert.equal($('visualCount').textContent,'1 / 2');
 d.querySelector('#visualCanvas image').dispatchEvent(new w.Event('error'));assert.equal($('visualError').hidden,false);
 $('visualNext').click();assert.equal($('visualError').hidden,true);
 $('visualClose').click();assert.equal($('visualDialog').open,false);assert.deepEqual(a.errors,[]);a.close();
});
test('Bullet icons, notes, search, accordion and scroll continue working on mobile and desktop',()=>{
 for(const mobile of [true,false]){
  const a=app(mobile),{d,w}=a,$=id=>d.getElementById(id),card=d.querySelector('[data-id="c1"]').closest('.check-card');
  assert.equal($('headerDetails').hidden,mobile);
  const toggle=card.querySelector('.details-toggle'),details=card.querySelector('.check-details');
  toggle.click();assert(!details.hidden);assert.equal(toggle.getAttribute('aria-expanded'),'true');assert(toggle.querySelector('svg'));assert.equal(toggle.textContent.trim(),'');assert(a.scrolls.length>0);
  assert.equal(details.lastElementChild,card.querySelector('.note-button'));card.querySelector('.note-button').click();
  $('noteText').value='Photo review note';$('noteText').dispatchEvent(new w.Event('input'));$('noteDone').click();
  toggle.click();assert(details.hidden);card.querySelector('.image-toggle').click();assert(details.hidden);$('visualClose').click();toggle.click();assert.equal(details.querySelector('.note-preview').textContent,'Photo review note');
  $('exportNotes').click();assert($('exportText').value.includes('Photo review note'));assert($('exportText').value.includes('I check underneath the truck'));$('exportClose').click();
  card.querySelector('.task-check').click();assert.equal($('doneCount').textContent,'1');
  $('section-2').querySelector('.section-toggle').click();assert.equal(d.querySelectorAll('.inspection-section:not(.collapsed)').length,1);
  $('search').value='volt meter';$('search').dispatchEvent(new w.Event('input'));assert.equal(d.querySelectorAll('.inspection-section:not(.collapsed)').length,1);assert(!d.querySelector('[data-id="c44"]').closest('.check-card').classList.contains('hidden'));
  $('reset').click();assert.equal($('doneCount').textContent,'0');assert.equal($('exportNotes').textContent,'Export notes (0)');assert.deepEqual(a.errors,[]);a.close();
 }
});
