const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
function app(mobile=true, saved={}){
 const errors=[],scrolls=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
 const dom=new JSDOM(html,{url:'https://zwazi.github.io/Pre-trip/',runScripts:'outside-only',virtualConsole:vc});
 const w=dom.window;w.matchMedia=q=>({matches:q.includes('max-width')&&mobile});w.confirm=()=>true;
 w.requestAnimationFrame=fn=>fn();w.scrollTo=options=>scrolls.push(options);
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};
 w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'));};
 for(const [key,value] of Object.entries(saved)) w.localStorage.setItem(key,JSON.stringify(value));
 // Run the page's actual scripts in document order, without loading network images.
 for(const script of w.document.scripts) w.eval(script.src?fs.readFileSync(path.join(root,new URL(script.src).pathname.replace('/Pre-trip/','')),'utf8'):script.textContent);
 return {w,d:w.document,errors,scrolls,close:()=>w.close()};
}
test('Bullet icons, notes, search, accordion and scroll continue working on mobile and desktop',()=>{
 for(const mobile of [true,false]){
  const a=app(mobile),{d,w}=a,$=id=>d.getElementById(id),card=d.querySelector('[data-id="c1"]').closest('.check-card');
  assert.equal($('headerDetails').hidden,mobile);
  const toggle=card.querySelector('.details-toggle'),details=card.querySelector('.check-details');
  toggle.click();assert(!details.hidden);assert.equal(toggle.getAttribute('aria-expanded'),'true');assert(toggle.querySelector('svg'));assert.equal(toggle.textContent.trim(),'');assert(a.scrolls.length>0);
  assert.equal(details.lastElementChild,card.querySelector('.note-button'));card.querySelector('.note-button').click();
  $('noteText').value='Inspection review note';$('noteText').dispatchEvent(new w.Event('input'));$('noteDone').click();
  toggle.click();assert(details.hidden);toggle.click();assert.equal(details.querySelector('.note-preview').textContent,'Inspection review note');
  $('exportNotes').click();assert($('exportText').value.includes('Inspection review note'));assert($('exportText').value.includes('I check underneath the truck'));$('exportClose').click();
  card.querySelector('.task-check').click();assert.equal($('doneCount').textContent,'1');
  $('section-2').querySelector('.section-toggle').click();assert.equal(d.querySelectorAll('.inspection-section:not(.collapsed)').length,1);
  $('search').value='volt meter';$('search').dispatchEvent(new w.Event('input'));assert.equal(d.querySelectorAll('.inspection-section:not(.collapsed)').length,1);assert(!d.querySelector('[data-id="c44"]').closest('.check-card').classList.contains('hidden'));
  $('reset').click();assert.equal($('doneCount').textContent,'0');assert.equal($('exportNotes').textContent,'Export notes (0)');assert.deepEqual(a.errors,[]);a.close();
 }
});
test('Updated structure has unique controls, correct counts, searchable bullets and no image UI',()=>{
 const a=app(),{d,w}=a;
 const ids=[...d.querySelectorAll('.task-check')].map(b=>b.dataset.id);
 assert.equal(ids.length,142);assert.equal(new Set(ids).size,142);
 const domIds=[...d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(domIds).size,domIds.length);
 assert.equal(d.querySelectorAll('img,image,.image-toggle,#visualDialog,script[src]').length,0);
 assert.equal(d.querySelectorAll('.inspection-section').length,23);
 for(const [index,section] of [...d.querySelectorAll('.inspection-section')].entries()){
  assert(section.querySelector('.section-title').textContent.startsWith(`${index+1}.`));
  assert.equal(section.querySelector('.section-count').textContent,`0/${section.querySelectorAll('.task-check').length}`);
 }
 const sectionIds=id=>[...d.querySelectorAll(`#${id} .task-check`)].map(b=>b.dataset.id);
 assert.deepEqual(sectionIds('section-15'),['c91','c98','c92','c93','c94','c96','c97','c95']);
 assert(sectionIds('section-16').includes('c99'));
 assert.deepEqual(sectionIds('section-17'),['c105','c106']);
 assert.deepEqual(sectionIds('section-17-suspension'),['c110-leaf-hangers','c110-leaf-springs','c110-u-bolts','c109','c110','c107','c108']);
 for(const box of d.querySelectorAll('.task-check')){
  const card=box.closest('.check-card'),toggle=card.querySelector('.details-toggle');
  assert.equal(d.getElementById(toggle.getAttribute('aria-controls')),card.querySelector('.check-details'));
  for(const li of card.querySelectorAll('.script-lines li')) assert(card.dataset.search.includes(li.textContent.toLowerCase()));
 }
 for(const [query,id] of [['power-steering hoses','c14-hoses'],['same size and type','c118'],['sneeze','c52'],['backward','c55']]){
  d.getElementById('search').value=query;d.getElementById('search').dispatchEvent(new w.Event('input'));
  assert(!d.querySelector(`[data-id="${id}"]`).closest('.check-card').classList.contains('hidden'));
 }
 assert.deepEqual(a.errors,[]);a.close();
});
test('Saved progress and merged notes survive the split, merge and section moves',()=>{
 const STORE='cmv_school_pretrip_cleaned_v3',NOTES='cmv_pretrip_notes_v1';
 const a=app(true,{[STORE]:['structure-updated','c14','c106','c105-release-button','c99','c110'],[NOTES]:{'c105-release-button':{text:'Button note'},c106:{text:'Arm note'}}});
 const {d,w}=a;
 for(const id of ['c14','c14-hoses','c106','c99','c110']) assert(d.querySelector(`[data-id="${id}"]`).checked);
 const card=d.querySelector('[data-id="c106"]').closest('.check-card');
 assert.equal(card.querySelector('.note-preview').textContent,'Arm note\n\nButton note');
 d.getElementById('exportNotes').click();assert.match(d.getElementById('exportText').value,/Sliding Tandem Release Arm \/ Button/);
 assert.equal(JSON.parse(w.localStorage.getItem(NOTES))['c105-release-button'],undefined);
 d.querySelector('[data-id="c1"]').click();
 const saved=JSON.parse(w.localStorage.getItem(STORE));assert(saved.includes('september-11-updated'));
 a.close();
 const b=app(true,{[STORE]:saved});assert(b.d.querySelector('[data-id="c106"]').checked);b.close();
 const c=app(true,{[STORE]:['structure-updated','c106']});assert(!c.d.querySelector('[data-id="c106"]').checked);c.close();
});
