"""Build reusable schematic SVGs and per-check photo overlays. No inspection text is generated here."""
import json, re
from pathlib import Path
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'; diagrams={}; photos={}; checks={}

def diagram(name,title,parts,extra=''):
    # Parts are separate labeled illustrations, not a claim about this truck's exact layout.
    body=[]; regions={}
    for key,label,box,shape in parts:
        x,y,w,h=box;regions[key]=[x/10,y/6.5,w/10,h/6.5]
        body.append(f'<g>{shape}</g><text x="{x+w/2}" y="{min(625,y+h+24)}" text-anchor="middle">{escape(label)}</text>')
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="1000" height="650"><rect width="1000" height="650" rx="20" fill="#20201d"/><style>text{{font:18px system-ui,sans-serif;fill:#e7e2d7}}.part{{fill:#45453d;stroke:#c4beaf;stroke-width:4;stroke-linejoin:round}}.line{{fill:none;stroke:#c4beaf;stroke-width:8;stroke-linecap:round}}.thin{{fill:none;stroke:#c4beaf;stroke-width:3}}.dark{{fill:#20201d;stroke:#c4beaf;stroke-width:4}}</style><text x="35" y="40" style="font-size:22px;font-weight:700">{escape(title)}</text><text x="35" y="68" style="font-size:15px;fill:#aaa797">Illustrative component guide · not the exact vehicle layout · not to scale</text>{extra}{''.join(body)}</svg>'''
    if name == 'wheel':
        svg = re.sub(r'<text x="[^"]+" y="[^"]+" text-anchor="middle">.*?</text>', '', svg)
    (OUT/'diagrams'/f'{name}.svg').write_text(svg)
    diagrams[name]={'src':f'assets/diagrams/{name}.svg','width':1000,'height':650,'title':title,'regions':regions}
def rect(x,y,w,h):return f'<rect class="part" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'
def circle(x,y,r):return f'<circle class="part" cx="{x}" cy="{y}" r="{r}"/>'
def line(d):return f'<path class="line" d="{d}"/>'
def part(k,l,b,s):return (k,l,b,s)
# Engine accessories are intentionally separate vignettes: their positions vary by engine.
diagram('engine','Engine accessories',[
 part('alternator','Alternator + wiring',(70,130,230,130),rect(110,150,140,95)+circle(110,197,35)+line('M250 170 H280 V125')+'<path class="thin" d="M155 160 V230 M180 160 V230 M205 160 V230"/>'),
 part('water','Water pump + pulley',(390,130,200,130),circle(485,195,60)+circle(485,195,25)+line('M540 175 H580 V145')),
 part('belt','Belt + pulleys',(690,125,220,135),circle(730,200,35)+circle(865,170,25)+'<path class="thin" d="M722 162 L860 142 Q907 142 894 190 L742 235 Q682 234 694 193 Z"/>'),
 part('compressor','Air compressor',(70,380,230,140),rect(100,410,160,100)+'<path class="thin" d="M110 420 H250 M110 435 H250 M110 450 H250 M110 465 H250"/>'+line('M160 410 V390 H220 V365')),
 part('pump','Power-steering pump',(390,375,210,140),rect(445,400,115,95)+circle(430,448,32)+line('M550 410 H595 M550 480 H595')),
 part('reservoir','Power-steering reservoir',(710,370,175,150),rect(730,390,130,125)+rect(765,370,60,20)+'<path class="thin" d="M740 465 H850"/>'+line('M770 515 V540 M830 515 V540')),
])
diagram('steering','Steering linkage',[
 part('gear','Steering gearbox',(90,125,200,140),rect(125,145,130,100)+line('M180 145 V110')),
 part('pitman','Pitman arm',(150,300,115,145),line('M200 310 L220 420')+circle(200,310,18)+circle(220,420,18)),
 part('drag','Drag link',(260,380,285,60),line('M275 410 H520')+circle(275,410,18)+circle(520,410,18)),
 part('tie','Tie rod',(565,350,330,75),line('M585 387 H875')+circle(585,387,18)+circle(875,387,18)),
 part('pins','Castle nut + cotter pin',(675,140,130,100),rect(705,165,70,45)+'<path class="thin" d="M710 165 V150 M733 165 V150 M756 165 V150 M740 145 V225 L760 230 M740 220 L720 230"/>'),
])
diagram('suspension','Suspension component guide',[
 part('hanger','Spring hanger + bushing',(70,140,150,165),'<path class="part" d="M95 150 H200 L185 275 H110 Z"/>'+circle(148,245,24)),
 part('spring','Leaf spring pack',(290,165,330,100),'<path class="line" d="M310 190 Q450 280 600 190 M325 215 Q455 295 585 215 M345 242 Q455 308 570 242"/>'),
 part('ubolts','U-bolts + securing nuts',(715,140,175,150),'<path class="line" d="M730 265 V165 Q755 125 780 165 V265 M820 265 V165 Q845 125 870 165 V265"/>'+rect(720,260,70,18)+rect(810,260,70,18)),
 part('shock','Shock absorber + mounts',(85,375,170,175),circle(165,385,15)+line('M165 400 V435')+rect(142,425,46,80)+line('M165 505 V535')+circle(165,540,15)),
 part('airbag','Air bag + mounts',(360,385,180,145),rect(365,390,170,18)+rect(375,410,150,94)+rect(365,505,170,18)+'<path class="thin" d="M375 440 H525 M375 472 H525"/>'),
 part('arm','Control / torque arm + bushings',(660,395,250,110),line('M685 450 H880')+circle(685,450,30)+circle(880,450,30)),
])
diagram('brakes','Air-brake actuator and drum — simplified cutaway',[
 part('hose','Air hose',(55,135,220,80),line('M70 155 C110 130 130 200 175 165 S235 160 260 190')),
 part('chamber','Brake chamber + clamp ring',(80,250,195,120),rect(90,265,155,90)+'<path class="thin" d="M210 265 V355"/>'+line('M150 265 V240')),
 part('pushrod','Pushrod + clevis',(265,285,145,65),line('M250 315 H380')+'<path class="thin" d="M370 300 H405 V330 H370"/>'),
 part('slack','Slack adjuster',(400,290,75,195),'<path class="part" d="M410 305 H445 L460 455 H400 Z"/>'+circle(427,445,18)),
 part('drum','Brake drum',(595,185,325,325),'<circle class="part" cx="760" cy="350" r="150"/><circle class="dark" cx="760" cy="350" r="127"/>'),
 part('lining','Brake linings',(648,232,225,238),'<path d="M690 252 A120 120 0 0 0 690 448 M830 252 A120 120 0 0 1 830 448" fill="none" stroke="#aba899" stroke-width="22"/>'),
],extra='<path class="thin" d="M447 445 H560 V350 H715"/><circle class="dark" cx="760" cy="350" r="32"/>')
diagram('wheel','Wheel and dual-tire guide',[
 part('tire','Tire',(75,125,360,360),'<circle class="part" cx="255" cy="305" r="165"/><circle class="dark" cx="255" cy="305" r="118"/>'),
 part('rim','Rim',(143,193,224,224),'<circle class="part" cx="255" cy="305" r="108"/><circle class="dark" cx="255" cy="305" r="78"/>'),
 part('hub','Hub / axle seal',(209,259,92,92),circle(255,305,40)),
 part('lugs','Lug nuts',(169,219,172,172),''.join(circle(255+int(72*__import__('math').cos(a)),305+int(72*__import__('math').sin(a)),10) for a in [i*__import__('math').pi/5 for i in range(10)])),
 part('valve','Valve stem + cap',(295,200,65,65),line('M310 250 L343 219')+rect(338,208,20,18)),
 part('duals','Dual tires / Budd spacing',(580,145,330,280),rect(595,160,100,250)+rect(790,160,100,250)+'<path class="thin" d="M640 180 V390 H842 V180 M640 250 H842"/><path class="line" d="M720 320 H765"/>'),
])
# Label placement outside vignettes is handled specially for the nested wheel parts below.
diagram('cab','Cab controls — illustrative layout',[
 part('gauges','Instrument cluster',(65,120,340,170),rect(75,135,320,145)+''.join(circle(x,195,37) for x in [130,235,340])+'<text x="130" y="245" text-anchor="middle">AIR</text><text x="235" y="245" text-anchor="middle">OIL</text><text x="340" y="245" text-anchor="middle">TEMP</text>'),
 part('abs','ABS / warning lamps',(455,120,170,85),rect(465,135,150,55)+'<text x="540" y="170" text-anchor="middle">ABS</text>'),
 part('key','Ignition key',(720,125,155,100),circle(760,168,30)+line('M770 180 L820 205 H850')),
 part('parking','Parking-brake controls',(475,300,390,100),'<path class="part" d="M500 335 L535 305 L570 335 L535 365 Z"/><rect class="part" x="670" y="310" width="75" height="55" rx="10"/><text x="535" y="390" text-anchor="middle">TRACTOR</text><text x="708" y="390" text-anchor="middle">TRAILER</text>'),
 part('pedals','Clutch / service brake / accelerator',(90,395,320,150),rect(110,420,70,90)+rect(220,420,80,90)+rect(340,420,40,105)),
 part('controls','Lights / wipers / horn',(480,460,365,105),rect(495,470,330,70)+'<text x="660" y="515" text-anchor="middle">LIGHTS · WIPERS · HORN</text>'),
])
diagram('safety','Cab safety and emergency equipment',[
 part('belt','Seat belt + buckle',(80,125,225,200),rect(115,135,130,120)+rect(100,255,165,40)+'<path class="line" d="M130 145 L245 260 M110 275 H205"/>'+rect(207,260,32,27)),
 part('triangles','Reflective triangles',(395,120,225,175),'<path class="part" d="M505 130 L605 280 H405 Z M505 175 L550 250 H460 Z"/>'),
 part('extinguisher','Fire extinguisher + pin + gauge',(735,110,140,215),rect(760,180,85,135)+rect(780,145,40,35)+line('M780 145 H845 M805 158 Q870 140 875 230')+circle(782,205,14)),
 part('chocks','Wheel chocks',(90,410,250,120),'<path class="part" d="M100 510 L180 425 L205 510 Z M230 510 L310 425 L335 510 Z"/>'),
 part('contact','Handholds + steps',(490,385,300,170),line('M510 400 V520 M765 400 V520')+rect(540,445,190,25)+rect(540,505,190,25)),
])
diagram('coupling','Fifth-wheel coupling — simplified views',[
 part('apron','Trailer apron',(70,125,440,35),rect(75,130,430,25)),
 part('skid','Fifth-wheel skid plate',(100,180,375,38),rect(105,182,365,30)),
 part('pin','Kingpin + locking jaws',(245,165,110,135),rect(285,160,35,110)+'<path class="line" d="M250 245 H280 M325 245 H355"/>'),
 part('base','Mounting platform + bolts',(90,345,420,80),rect(100,355,400,55)+''.join(circle(x,380,8) for x in [130,210,300,390,470])),
 part('rail','Sliding rail + locking pins',(605,140,295,100),rect(615,160,275,55)+''.join(circle(x,185,9) for x in [650,700,750,800,850])),
 part('release','Release handle',(620,315,280,90),line('M630 340 H865 V380 H820')),
 part('air','Air line',(630,460,260,80),line('M640 480 Q700 545 750 480 T880 495')),
])
diagram('trailer-suspension','Trailer suspension and tandem controls',[
 part('rail','Sliding tandem rail',(85,130,450,70),rect(95,140,430,45)+''.join(circle(x,162,10) for x in [130,185,240,295,350,405,460,500])),
 part('button','Tandem release button',(685,130,170,90),rect(695,140,150,65)+circle(770,171,22)),
 part('release','Mechanical release arm',(90,290,365,90),line('M105 320 H420 V360 H375')),
 part('hanger','Control-arm hanger',(500,280,110,180),'<path class="part" d="M510 290 H595 L580 435 H525 Z"/>'+circle(552,402,22)),
 part('arm','Control arm + bushings',(90,470,330,90),line('M120 505 H385')+circle(120,505,30)+circle(385,505,30)),
 part('shock','Shock absorber',(685,285,75,155),line('M722 290 V335')+rect(702,325,40,80)+line('M722 405 V435')),
 part('airbag','Air bag',(780,450,135,115),rect(790,460,115,95)+'<path class="thin" d="M790 490 H905 M790 525 H905"/>'),
])
diagram('lights','Front and rear lighting groups — illustrative',[
 part('front','Front combination lamps + reflectors',(80,135,370,155),rect(95,150,120,90)+rect(305,150,120,90)+'<circle cx="155" cy="195" r="30" fill="#d59b3c"/><circle cx="365" cy="195" r="30" fill="#d59b3c"/>'),
 part('reverse','Clear reverse lamps',(565,135,330,140),circle(645,200,40)+circle(815,200,40)),
 part('clearance','Outer clearance lamps',(90,420,350,75),rect(105,435,85,40)+rect(335,435,85,40)),
 part('rear','Red tail / brake / indicator lamps',(575,385,330,120),''.join(circle(x,445,32) for x in [620,735,850])),
])
diagram('procedure','Inspection and test reminders',[
 part('speak','Name the test / speak the script',(85,140,365,200),'<path class="part" d="M100 155 H430 V290 H220 L170 330 V290 H100 Z"/><text x="265" y="230" text-anchor="middle">SAY THE FULL PHRASE</text>'),
 part('timer','Time / observe / listen',(560,140,295,210),circle(700,245,85)+line('M700 245 V190 M700 245 L745 265')+rect(675,130,50,25)),
 part('memory','Recall the component checks',(220,410,560,125),rect(240,420,520,100)+'<text x="500" y="480" text-anchor="middle">PMS · CBB · WTF · ABC · NL</text>'),
])
diagram('landing-gear','Landing-gear crank assembly — illustrative',[
 part('leg','Landing-gear leg',(175,140,175,360),rect(195,150,130,280)+rect(220,430,80,60)+rect(175,490,175,20)),
 part('crank','Crank handle + shaft',(400,185,395,185),line('M330 220 H650 V325 H760')+rect(720,310,80,30)),
 part('keeper','Handle keeper',(695,410,110,80),'<path class="line" d="M710 430 V470 H785 V430"/>'),
])
diagrams['cab']['regions'].update({'tractor':[49,46,9,12],'trailer':[66,46,10,12],'clutch':[10,63,9,17],'brake':[21,63,10,17]})
diagram('gauges','Instrument gauges — illustrative, not live readings',[
 part('oil','Oil pressure',(85,135,190,170),circle(180,220,70)+line('M180 220 L145 180')),
 part('temperature','Water temperature',(410,135,190,170),circle(505,220,70)+line('M505 220 L470 180')),
 part('volts','Voltmeter',(735,135,190,170),circle(830,220,70)+line('M830 220 L795 180')),
 part('fuel','Fuel level',(85,385,190,170),circle(180,470,70)+line('M180 470 L145 430')),
 part('def','DEF level',(410,385,190,170),circle(505,470,70)+line('M505 470 L470 430')),
 part('air','Primary / secondary air',(735,385,190,170),circle(830,470,70)+line('M830 470 L795 430 M830 470 L865 425')),
])
diagram('controls','Cab controls — functions to locate',[
 part('lights','Running lights / high beams',(75,135,240,130),rect(90,155,210,85)+'<text x="195" y="208" text-anchor="middle">LIGHTS</text>'),
 part('signals','Left / right / hazards',(380,135,240,130),rect(395,155,210,85)+'<text x="500" y="208" text-anchor="middle">←  △  →</text>'),
 part('city','City horn',(695,135,230,130),circle(810,195,55)+circle(810,195,20)),
 part('airhorn','Highway horn',(75,390,240,125),line('M190 390 V460')+'<path class="part" d="M160 460 H220 L210 490 H170 Z"/>'),
 part('heater','Heater',(380,385,240,140),rect(395,410,210,90)+circle(440,455,20)+circle(550,455,20)),
 part('defrost','Defrost',(695,385,230,140),rect(710,410,200,90)+'<path class="thin" d="M755 480 V435 M810 480 V435 M865 480 V435"/>'),
])
diagram('driving','Driving controls — illustrative',[
 part('wheel','Steering wheel',(90,125,275,275),circle(225,260,115)+circle(225,260,24)+line('M115 260 H200 M250 260 H335 M225 285 V370')),
 part('pedal','Service-brake pedal',(475,155,160,170),rect(500,180,105,110)+line('M555 180 V145')),
 part('gear','Transmission / neutral',(740,155,120,205),line('M800 310 V200')+circle(800,180,28)+'<text x="800" y="350" text-anchor="middle">N</text>'),
 part('tractor','Tractor parking brake',(300,450,125,95),'<path class="part" d="M310 495 L365 455 L415 495 L365 535 Z"/>'),
 part('trailer','Trailer parking brake',(580,450,130,95),rect(590,465,110,65)),
])
# Metadata for every inspected source. Photos are normalized and stripped of EXIF when optimized.
from PIL import Image
captions=['Fifth wheel from side','Fifth wheel from rear','Tractor front','Passenger-side engine bay','Exhaust and drivetrain underside','Driver-side engine bay','Driver-side lower engine bay','Driver door and steps','Open driver door','Rear cab and connections','Catwalk and fuel tank','Trailer connections','Trailer bulkhead','Drive axle top view','Drive suspension from side','Drive wheels','Front splash guard','Rear tractor mud flaps and lights','Landing gear underside','Trailer front upper corner','Trailer side','Trailer side lamps and reflector','Landing gear and crossmembers','Trailer sliding tandem','Trailer axle and brake chambers','Trailer leaf springs and wheel interior','Trailer wheels','Trailer mud flap','Rear side lamps and door tie','Trailer rear']
for path,caption in zip(sorted((OUT/'photos').glob('*.webp')),captions):
    short=path.stem[-6:]; im=Image.open(OUT/'photos'/f'{path.stem}.webp')
    photos[short]={'src':f'assets/photos/{path.stem}.webp','width':im.width,'height':im.height,'title':caption,'original':path.with_suffix('.jpg').name}

def P(cid,photo,regions,note=''):
    checks[cid]={'views':[{'photo':photo,'marks':[dict(zip(['label','x','y','w','h'],r)) for r in regions],'note':note}]}
def D(cid,name,keys,note='This component is not clearly visible in the supplied photos. Diagram shows its general form; actual layout varies.'):
    checks[cid]={'views':[{'diagram':name,'marks':[dict(zip(['label','x','y','w','h'],[label,*diagrams[name]['regions'][key]])) for key,label in keys],'note':note}]}
def also(cid,name,keys,note='Simplified component detail. Actual arrangement varies.'):
    temp='__temp';D(temp,name,keys,note);checks[cid]['views']+=checks.pop(temp)['views']
def same(cid,other):checks[cid]=json.loads(json.dumps(checks[other]))
# Front and engine.
P('c1','143623',[('Ground beneath the tractor',7,72,86,12)])
P('c2-id','143623',[('Three central ID lights',42,32,13,3)])
P('c2-clearance','143623',[('Left outer clearance light',24,32,4,3),('Right outer clearance light',69,32,4,3)])
P('c2-headlights','143623',[('Left headlamp / high-beam cluster',5,55,15,10),('Right headlamp / high-beam cluster',80,55,16,10)])
D('c2-indicators','lights',[('front','Front indicator / running / four-way lamps and reflectors')],'The front combination lamps and corresponding reflectors are not distinct in the front photo; this is an illustrative group.')
P('c3','143623',[('Hood — unlatch on both sides',14,43,70,23)],'Hood location shown. The side latches are outside this photo; the callout does not identify a latch.')
P('c4','143642',[('Upper coolant hose',57,10,22,14),('Visible hose runs and connections',24,12,31,33)],'Examples of visible hoses; inspect the other accessible hoses too.')
P('c6','143652',[('Exhaust outlet / tailpipe',40,35,35,39)]);checks['c6']['views'].append({'photo':'143642','marks':[{'label':'Engine exhaust / heat-shield area','x':24,'y':32,'w':13,'h':31}],'note':'The shield covers portions of the exhaust assembly.'})
D('c7','engine',[('alternator','Alternator and electrical connections'),('belt','Drive belt and pulleys')])
P('c8','143709',[('Coolant reservoir',16,8,23,28)])
D('c9','engine',[('water','Water pump'),('belt','Drive belt and pulleys')])
P('c11','143709',[('Engine-oil dipstick handle',47,28,3,9)],'The dipstick must be withdrawn to inspect its level marks; those marks are not visible here.')
D('c13','engine',[('compressor','Air compressor')])
D('c12','engine',[('pump','Power-steering pump')])
D('c14','engine',[('reservoir','Power-steering reservoir and line connections')],'The reservoir cannot be positively identified from these engine views; use this schematic as a component reference.')
D('c15','steering',[('gear','Steering gearbox')])
D('c16','steering',[('pitman','Pitman arm'),('drag','Drag link'),('tie','Tie rod'),('pins','Castle nuts and cotter pins')])
for cid,key,label in [('c17','hanger','Leaf spring hangers and bushings'),('c18','spring','Leaf springs'),('c19','ubolts','U-bolts and bottom securing nuts'),('c20','shock','Shock absorber and both mounts')]:D(cid,'suspension',[(key,label)])
for cid,key,label in [('c21','hose','Brake hose'),('c22','chamber','Brake chamber and clamp ring'),('c23','pushrod','Pushrod / clevis'),('c24','drum','Brake drum'),('c25','lining','Brake linings')]:D(cid,'brakes',[(key,label)])
also('c23','brakes',[('pushrod','Pushrod'),('slack','Slack adjuster')]);checks['c23']['views']=checks['c23']['views'][1:]
P('c26','143714',[('Steer tire tread',46,73,37,26)],'This photo shows the tread. The wheel diagram provides the sidewall reference.');also('c26','wheel',[('tire','Tire sidewall and tread')])
for cid,key,label in [('c27','valve','Valve stem and cap'),('c28','rim','Rim'),('c29','lugs','Lug nuts'),('c30','hub','Hub seal')]:D(cid,'wheel',[(key,label)])
P('c31','143720',[('Cab-side lamp / reflector location',5,53,10,5)],'The visible amber unit is the location reference; lamp functions must be checked on the vehicle.')
P('c32','143720',[('Mirror and upper support',13,14,15,23),('Mirror mounting arm and base',14,31,29,15)])
P('c33','143720',[('Upper step',30,66,69,6),('Lower step',32,78,67,7)])
P('c34','143728',[('Door / inner panel',24,3,24,89),('Cab opening and door seal',43,0,20,90)])
D('c35','safety',[('triangles','Reflective triangles'),('extinguisher','Fire extinguisher, gauge and pin'),('chocks','Wheel chocks')],'The side compartment contents were not photographed. These are illustrations of the equipment named in this check.')
P('c37','143742',[('Fuel tank',1,45,41,25),('Fuel cap',3,48,13,7)])
P('c38','143720',[('Cab steps',29,65,70,22)],'The exterior photo shows the steps; handholds are shown schematically.');also('c38','safety',[('contact','Handholds and steps for three points of contact')])
D('c39','safety',[('belt','Seat belt webbing, anchor points and buckle')])
D('c40','cab',[('key','Ignition'),('abs','ABS indicator'),('parking','Parking-brake controls'),('clutch','Clutch on manual vehicles')],'Illustrative control locations. Follow the safe-start wording in the checklist.');
P('c41','143623',[('Left mirror',2,39,13,9),('Right mirror',84,40,11,5)])
P('c42','143623',[('Windshield',22,35,56,10)])
P('c43','143623',[('Left wiper',23,41,22,3),('Right wiper',52,41,26,3)])
D('c44','gauges',[(k,l) for k,l in [('oil','Oil pressure'),('temperature','Water temperature'),('volts','Voltmeter'),('fuel','Fuel level'),('def','DEF level'),('air','Primary and secondary air pressure')]],'The instrument cluster was not photographed close up. These are illustrative gauges, not actual readings.')
D('c45','controls',[(k,l) for k,l in [('lights','Running lights / high beams'),('signals','Left / right / hazards'),('city','City horn'),('airhorn','Highway horn'),('heater','Heater'),('defrost','Defrost')]])
D('c46','cab',[('gauges','Build and observe air pressure'),('key','Engine / key state'),('parking','Both parking-brake controls')],'Visual reminder only; use the checklist for the sequence.');also('c46','safety',[('chocks','Confirm wheel chocks')])
D('c47','procedure',[('speak','Verbally name the test')],'This is a spoken test instruction, not a physical component.')
D('c48','cab',[('brake','Service-brake pedal'),('gauges','Air-pressure gauges')],'Illustrative controls; the checklist supplies the test sequence and limits.');also('c48','procedure',[('timer','Time the test and listen')])
D('c49','cab',[('gauges','Air-pressure gauges and low-air warning'),('brake','Service-brake pedal')],'The low-air warning indicator and buzzer are associated with the instrument cluster. The separate ABS indicator is not the low-air warning.')
D('c50','cab',[('parking','Parking-brake valves'),('gauges','Air-pressure gauges'),('brake','Service-brake pedal')],'Illustrative controls; observe valve movement on the actual vehicle.')
for cid in ['c51','c56']:
 P(cid,'143728',[('Cab opening for exit',44,3,20,89)],'Use the exit sequence in the checklist.');also(cid,'safety',[('belt','Seat belt'),('contact','Handholds and steps')]);
also('c51','safety',[('chocks','Wheel chocks')])
same('c52','c38')
for cid,key,label in [('c53','tractor','Tractor parking-brake control'),('c54','trailer','Trailer parking-brake control'),('c55','brake','Service-brake pedal')]:D(cid,'cab',[(key,label)],'Control-location illustration. Perform the test using the checklist sequence.')
also('c40','driving',[('gear','Transmission in neutral')])
also('c55','driving',[('wheel','Steering wheel'),('pedal','Service-brake pedal')])
also('c56','cab',[('key','Ignition key')])
# Tractor rear and drive axles.
P('c57','143739',[('Left upper L-shaped tape',18,6,23,9),('Right upper tape',71,22,4,7)])
P('c58','143739',[('Electrical cable to tractor connection',42,53,18,20)],'The green electrical cable is bundled with the other lines in places; trace it to its tractor connector.')
P('c59','143742',[('Tractor air-line connection area',3,38,27,12)],'Two air lines connect here; their tractor fittings are partly obscured.')
P('c60','143751',[('Electrical plug at trailer',21,36,20,13),('Green electrical line',2,47,21,39)])
P('c61','143751',[('Service-air gladhand and hose',18,29,34,16),('Emergency-air gladhand and hose',51,31,15,17)])
P('c62','143742',[('Catwalk',42,30,45,14),('Access steps',43,46,27,18)])
P('c63','143801',[('Left frame rail',1,1,25,87),('Right frame rail',65,0,18,99),('Crossmember',0,89,67,10)])
P('c64','143652',[('Drive shaft',1,0,56,19),('U-joint / yoke',57,5,15,27)])
P('c65','143801',[('Transverse torque rod and end mounts',30,10,38,26)],'One visible rod is highlighted; other torque / torsion members require another viewing angle.')
D('c66','suspension',[('hanger','Leaf spring hanger and bushing')])
D('c67','suspension',[('spring','Leaf spring'),('ubolts','U-bolts and bottom nuts')])
P('c69','143810',[('Shock absorber and mount area',37,12,26,42)])
D('c70','suspension',[('airbag','Air bag and mounts')])
P('c71','143801',[('Left visible brake hose',21,62,16,20),('Right visible brake hose',58,58,9,35)])
P('c72','143801',[('Left brake chamber',22,74,17,21),('Right brake chamber',53,72,13,24)])
D('c73','brakes',[('pushrod','Pushrod / clevis'),('slack','Slack adjuster')])
D('c74','brakes',[('drum','Brake drum')]);D('c75','brakes',[('lining','Brake linings')])
P('c76','143831',[('Gap between dual tires',58,32,11,17)],'The tire gap is visible from above; the rim-mating surfaces are hidden.');also('c76','wheel',[('duals','Dual tires and rim spacing')])
P('c77','143822',[('Outer drive tire',0,31,73,41),('Inner drive tire',49,30,47,27)])
D('c78','wheel',[('valve','Valve stems and caps')])
P('c79','143822',[('Drive-wheel rim',4,42,48,21)])
D('c80','wheel',[('lugs','Lug nuts')],'The lug nuts are partly hidden by the angle of the drive-wheel photo.')
P('c81','143822',[('Axle flange / seal area',29,48,13,7)])
P('c82','143839',[('Second set of drive tires',3,7,16,48)],'Apply the same inspection to this second drive-axle tire set.')
P('c83','143839',[('Left rear mud flap',24,32,28,67),('Right rear mud flap',66,29,8,40)])
P('c83-splash','143831',[('Splash guard',22,34,50,39)])
P('c84','143839',[('Left DOT tape strip',28,25,11,22),('Upper DOT tape strip',44,24,10,7)])
P('c85-red','143839',[('Visible rear red lamps',51,22,10,25)],'The inner red lamps are visible; check all matching lamps across the rear.');also('c85-red','lights',[('rear','Rear red lamp group')])
D('c85-reverse','lights',[('reverse','Clear reverse lights')],'The reverse lamps cannot be distinguished reliably in the rear-tractor photo.')
# Trailer exterior and coupling.
P('c86','143755',[('Trailer bulkhead',15,0,84,76)])
P('c87','143911',[('Upper front clearance lamp',26,0,3,5)],'Small lamp at the upper front corner. Enlarge the photo to see the lens.')
P('c88','143913',[('Front side amber marker location',19,88,4,10)])
P('c89','143913',[('Front side amber reflector / marker area',19,88,4,10)],'This distant view does not distinguish the reflector from the neighboring lamp.');also('c89','lights',[('front','Amber reflector / marker reference')])
P('c90','143913',[('Side DOT tape run',30,56,36,29)])
P('c91','142029',[('Trailer apron above fifth wheel',24,30,53,18)])
P('c92','142826',[('Skid plate / apron contact interface',18,34,54,12)],'The contact seam is visible; the greased top surface is mostly covered by the trailer.')
P('c93','142029',[('Fifth-wheel mounting platform',25,62,47,13)])
P('c94','142029',[('Sliding rail',5,67,79,13)],'Rail location is visible; locking pins are partly obscured.');also('c94','coupling',[('rail','Sliding rail and locking pins')])
P('c95','142029',[('Mounting bolts along base',3,68,69,10)])
P('c96','142029',[('Fifth-wheel release handle',23,52,16,10)],'Handle projects from the left side of the fifth wheel; follow it to its lock.')
P('c97','142826',[('Air line below coupling',28,68,22,14)])
D('c98','coupling',[('pin','Kingpin shank and locking jaws')],'The coupling photos do not expose the full jaw engagement; a cutaway shows the relationship.')
P('c99','143755',[('Clearance between trailer front and tractor tires',37,64,49,23)],'Use the actual vehicle to check the complete turning-clearance area.')
P('c100','143946',[('Trailer crossmembers',10,0,66,30)])
P('c101','143845',[('Near landing-gear leg',51,12,16,72),('Far landing-gear leg',22,26,8,37)])
P('c102','143946',[('Near landing-gear foot',52,72,16,13),('Far landing-gear foot',28,61,6,6)])
D('c103','landing-gear',[('crank','Landing-gear crank handle'),('keeper','Handle keeper')],'The landing-gear crank handle is not clearly visible in the supplied underside photos. This L-shaped handle illustrates the part, not its mounting location.')
P('c104','143926',[('Amber side reflector',47,44,7,4),('Side combination lamp',44,50,13,4)])
P('c105','143959',[('Sliding tandem rail and holes',7,13,60,33)])
D('c105-release-button','trailer-suspension',[('button','Sliding tandem release button')],'An air-release button is not visible in these tandem photos; this is a generic control illustration.')
P('c106','143959',[('Tandem mechanical release handle',27,42,10,14)],'Handle is behind the front tandem support; enlarge for the bent grip.')
D('c107','trailer-suspension',[('hanger','Control-arm hangers and bushings')],'The photographed trailer shows leaf-spring suspension. This diagram covers the control-arm hardware named by the checklist.')
D('c108','trailer-suspension',[('arm','Control arm and bushings')],'The photographed trailer shows leaf-spring suspension; a control-arm arrangement is shown schematically.')
D('c109','trailer-suspension',[('shock','Trailer shock absorber')],'No trailer shock absorber is clearly visible in the photos.')
D('c110','trailer-suspension',[('airbag','Trailer air bag and mounts')],'The photographed trailer has visible leaf springs; no trailer air bag is shown.')
D('c111','brakes',[('hose','Hose'),('chamber','Chamber'),('pushrod','Pushrod'),('slack','Slack adjuster'),('drum','Drum'),('lining','Linings')],'Memory aid for the no-pointing trailer-brake check. Follow the wording in the checklist.')
P('c112','144003',[('Visible air-hose runs to brake chambers',27,49,34,20)],'Some hose runs are behind the axle and other components.')
P('c113','144003',[('Left visible brake chamber',27,70,20,29),('Right visible brake chamber',49,73,18,26)])
D('c114','brakes',[('pushrod','Pushrod'),('slack','Slack adjuster')])
P('c115','144005',[('Inboard brake-drum area',54,42,23,28)],'The drum surface is partially hidden by the suspension.');also('c115','brakes',[('drum','Brake drum cutaway')])
D('c116','brakes',[('lining','Brake linings')],'The friction linings are inside the drums and are not exposed in the supplied photos.')
P('c117','144013',[('Gap between dual tires',51,34,10,25)],'The tire gap is shown; the rim mating surfaces are not exposed.');also('c117','wheel',[('duals','Budd spacing: dual tires and rims')])
P('c118','144013',[('Near trailer tire',6,28,57,38),('Inner trailer tire',55,31,33,25)])
D('c119','wheel',[('valve','Valve stem and cap')])
P('c120','144013',[('Trailer rim',10,40,29,22)])
D('c121','wheel',[('lugs','Trailer lug nuts')],'The photographed trailer wheel does not expose the lug nuts clearly.')
D('c122','wheel',[('hub','Trailer hub seal')],'The hub is not clearly visible at this camera angle.')
P('c123','144013',[('Rear tandem wheel set',71,56,28,40)],'Repeat the same inspection on this second wheel set.')
P('c124','144018',[('Trailer mud flap',29,33,42,34)])
P('c125','144022',[('Door tie / holdback loop',31,45,5,6)])
P('c126','144022',[('Amber ABS lamp below ABS label',54,53,3,7)])
P('c127','144022',[('Red side marker lamp',63,56,3,7)])
P('c128','144029',[('Three central rear ID lamps',47,21,11,2)])
P('c129','144029',[('Left outer clearance lamp position',16,21,6,2),('Right outer clearance lamp position',75,21,7,2)],'The outer corners are distant in this photo. Check outer clearance lights only if equipped.');also('c129','lights',[('clearance','Outer clearance lamps, if equipped')])
P('c130','144029',[('Left upper L-shaped tape',15,22,10,11),('Right upper L-shaped tape',73,22,10,11)],'The upper tape is weathered and low contrast in this photo.')
P('c131','144029',[('Left door hinges',14,23,8,29),('Right door hinges',77,23,9,31)])
P('c132','144029',[('Center door seal seam',48,22,4,32),('Outer door seal perimeter',14,22,71,34)],'The closed doors conceal some seal surfaces; inspect them with the doors open.')
P('c133','144029',[('Left door latch / handle',35,51,12,4),('Right door latch / handle',54,51,10,4)])
P('c134','144029',[('Lower DOT reflective tape',18,63,64,3)])
P('c135','144029',[('Left rear red lamp group',15,56,16,3),('Right rear red lamp group',69,56,16,3)],'Several functions share the red lamps; verify the correct function on the vehicle.')
same('c136','c135')
D('c137','procedure',[('speak','Speak the complete phrase'),('memory','Use acronyms as memory prompts')],'This is a spoken exam reminder, not a physical vehicle part.')
# Point onto component material rather than the empty center of rings or grouped parts.
diagram_targets = {
 'wheel': {'tire':(11,40),'rim':(25.5,30.5),'lugs':(25.5,35.8),'valve':(34.3,33.7)},
 'brakes': {'drum':(90,54),'lining':(86.8,54)},
 'suspension': {'spring':(45.5,38.5),'ubolts':(78,33)},
 'safety': {'belt':(19.2,32),'triangles':(50.5,23),'chocks':(17,75),'contact':(63,70)},
 'engine': {'belt':(80,23)},
 'lights': {'front':(15.5,30),'reverse':(64.5,30.8),'clearance':(15,70)},
}
for guide in checks.values():
 for view in guide['views']:
  if 'diagram' not in view: continue
  name=view['diagram']
  for mark in view['marks']:
   box=[mark[k] for k in ['x','y','w','h']]
   for key,target in diagram_targets.get(name,{}).items():
    if box == diagrams[name]['regions'][key]: mark['tx'],mark['ty']=target
# Show individual targets when the checklist names a left/right lamp pair.
for cid,boxes in {
 'c2-indicators':[('Left front combination group',9.5,23,12,14),('Right front combination group',30.5,23,12,14)],
 'c85-reverse':[('Left reverse lamp',60.5,24.6,8,12.3),('Right reverse lamp',77.5,24.6,8,12.3)],
}.items():
 checks[cid]['views'][0]['marks']=[dict(zip(['label','x','y','w','h'],box)) for box in boxes]
# Fail closed if a check is forgotten. No automatic generic picture fallbacks.
ids=re.findall(r'class="task-check" data-id="([^"]+)"', (ROOT/'index.html').read_text())
assert set(ids)==set(checks),(set(ids)-set(checks),set(checks)-set(ids))
for cid,check in checks.items():
 for v in check['views']:
  assert v['marks'],cid
  for m in v['marks']:
   assert 0<=m['x']<=100 and 0<=m['y']<=100 and m['w']>0 and m['h']>0,(cid,m)
   assert m['x']+m['w']<=100 and m['y']+m['h']<=100,(cid,m)
data={'photos':photos,'diagrams':diagrams,'checks':checks}
(OUT/'visual-guides.js').write_text('window.PRETRIP_VISUALS = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
print(f'{len(checks)} checks; {len(photos)} reviewed photos; {len(diagrams)} reusable diagrams; '+str(sum(any('photo' in v for v in c['views']) for c in checks.values()))+' checks with photo views')
