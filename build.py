"""Build the Adapty prototype wall (event page) for the November 11 batch.

Same look and mechanics as adapty-prototype-wall-nov (London): app-coloured cards with a mini QR,
tap a card and the whole screen becomes that app's QR, swipe for the next one.

Usage: PYTHONPATH=<dir with qrcode> python3 build.py <path to adapty-prototype-wall-nov/index.html>
"""
import json, re, sys, os
import qrcode

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(sys.argv[1]).read()

# key, title, sub, owner, url, card bg, ink, ink2, stage bg, ring, cta, cta ink, fade colour
APPS = [
    ('mobipdf', 'MobiPDF', 'PDF editor · MobiSystems', 'Eddie', 'https://eddieatadapty.github.io/mobisystems-flow-rebuild/',
     'linear-gradient(150deg,#E8423C,#C21F26)', '#fff', 'rgba(255,255,255,.8)', 'linear-gradient(180deg,#E8423C 0%,#C21F26 100%)', '#FFD9D6', '#fff', '#C21F26', '#C82329'),
    ('pickup', 'Pickup Music', 'Guitar, piano and bass', 'Eddie', 'https://eddieatadapty.github.io/pickupmusic-flow-rebuild/',
     'linear-gradient(150deg,#5B3BF0,#3320B8)', '#fff', 'rgba(255,255,255,.8)', 'linear-gradient(180deg,#5B3BF0 0%,#2A1A9E 100%)', '#FF5BB5', '#fff', '#2A1A9E', '#3B24C4'),
    ('norton', 'Norton 360', 'Security and VPN · Gen Digital', 'Bogdan', 'https://bterzic123.github.io/norton-flow-rebuild-v2/',
     '#FFE01B', '#111', 'rgba(17,17,17,.72)', 'linear-gradient(180deg,#FFE01B 0%,#FFD000 100%)', '#111', '#111', '#FFE01B', '#FFE01B'),
    ('fishingpoints', 'Fishing Points', 'Fishing map and forecast', 'Eddie', 'https://eddieatadapty.github.io/fishing-points-flow-rebuild/',
     'linear-gradient(150deg,#2A86E8,#0F57B8)', '#fff', 'rgba(255,255,255,.8)', 'linear-gradient(180deg,#2A86E8 0%,#0D4C9E 100%)', '#8FE6FF', '#fff', '#0D4C9E', '#1767C8'),
    ('ivy', 'Ivy', 'Processed food scanner', 'Bogdan', 'https://bterzic123.github.io/ivy-flow-rebuild/',
     '#F4F0E6', '#0F3F3A', 'rgba(15,63,58,.7)', 'linear-gradient(180deg,#F4F0E6 0%,#E6EFE9 100%)', '#1F5C55', '#0F3F3A', '#fff', '#F4F0E6'),
    ('lingolooper', 'LingoLooper', 'AI language game · Lumi Labs', 'Eddie', 'https://eddieatadapty.github.io/lingolooper-flow-rebuild/',
     'linear-gradient(150deg,#FF8A3D,#E8531E)', '#fff', 'rgba(255,255,255,.82)', 'linear-gradient(180deg,#FF8A3D 0%,#E2481A 100%)', '#FFF1A8', '#fff', '#E2481A', '#EC5F25'),
    ('fastic', 'Fastic', 'Weight loss and fasting', 'Bogdan', 'https://bterzic123.github.io/fastic-flow-rebuild/',
     'linear-gradient(150deg,#4CB8F2,#2B8FD9)', '#fff', 'rgba(255,255,255,.85)', 'linear-gradient(180deg,#5CC0F4 0%,#2B8FD9 100%)', '#FFB000', '#fff', '#1F78BE', '#3299DE'),
    ('yousician', 'Yousician', 'Learn and play guitar', 'Eddie', 'https://eddieatadapty.github.io/yousician-flow-rebuild/',
     '#16181B', '#fff', 'rgba(255,255,255,.72)', 'radial-gradient(90% 50% at 50% 0%,#1F3A2C,transparent 70%),#16181B', '#2EE07F', '#2EE07F', '#0E1A12', '#16181B'),
    ('babbel', 'Babbel', 'Language learning', 'Bogdan', 'https://bterzic123.github.io/babbel-flow-rebuild-v2/',
     'linear-gradient(150deg,#FF7A2F,#F25A12)', '#fff', 'rgba(255,255,255,.82)', 'linear-gradient(180deg,#FF7A2F 0%,#EE5310 100%)', '#FFE2CF', '#fff', '#EE5310', '#F7631A'),
    ('structured', 'Structured', 'Visual day planner · unorderly', 'Polina', 'https://plykhvar-glitch.github.io/structured-flow-rebuild/',
     'linear-gradient(150deg,#F7A9A5,#EC8681)', '#fff', 'rgba(255,255,255,.88)', 'linear-gradient(180deg,#F7A9A5 0%,#E9827D 100%)', '#FFFFFF', '#fff', '#C9605B', '#EF8F8A'),
    ('welltory', 'Welltory', 'Stress and heart rate', 'Bogdan', 'https://bterzic123.github.io/welltory-flow-rebuild/',
     'radial-gradient(80% 70% at 100% 100%,#5A1408,transparent 70%),#0E0C14', '#fff', 'rgba(255,255,255,.72)', 'radial-gradient(90% 45% at 50% 100%,#7A1C0C,transparent 75%),#0E0C14', '#FF5A36', '#FF5A36', '#fff', '#0E0C14'),
]


def qr_svg(url):
    q = qrcode.QRCode(border=4, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url); q.make(fit=True); m = q.get_matrix(); n = len(m); d = []
    for y, r in enumerate(m):
        x = 0
        while x < n:
            if r[x]:
                s = x
                while x < n and r[x]: x += 1
                d.append('M%d %dh%dv1h-%dz' % (s, y, x - s, x - s))
            else:
                x += 1
    return ('<svg viewBox="0 0 %d %d" shape-rendering="crispEdges" role="img" aria-label="QR code"><rect width="%d" height="%d" fill="#fff"/>'
            '<path fill="#000" d="%s"/></svg>') % (n, n, n, n, ''.join(d))


def rgba(hex_, a):
    h = hex_.lstrip('#'); return 'rgba(%d,%d,%d,%s)' % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


# ---- style: the London wall's stylesheet, with this batch's palettes instead of the old ones
css = re.search(r'<style>(.*?)</style>', SRC, re.S).group(1)
css = '\n'.join(l for l in css.split('\n') if not re.match(r'\s*(\.v-|/\* per-app|\.ic\.bc|\s+--s-bg|\s+--s-)', l))
pal = ['/* per-app card and stage palettes */']
for (k, t, sub, own, url, cbg, ink, ink2, sbg, ring, cta, ctaink, fade) in APPS:
    pal.append('.v-%s{--c-bg:%s;--c-ink:%s;--c-ink2:%s;--c-edge:rgba(255,255,255,.08);--c-fade:linear-gradient(90deg,%s 40%%,%s 80%%);'
               '--s-bg:%s;--s-ink:%s;--s-chip:%s;--s-ring:%s;--s-cta:%s;--s-cta-ink:%s}'
               % (k, cbg, ink, ink2, fade, rgba(fade, .1), sbg, ink, 'rgba(17,17,17,.1)' if ink != '#fff' else 'rgba(255,255,255,.16)', ring, cta, ctaink))
pal.append('.card .art img{right:0;top:0;height:100%;width:58%;object-fit:cover;object-position:50% 8%;-webkit-mask:linear-gradient(90deg,transparent 0,#000 38%);mask:linear-gradient(90deg,transparent 0,#000 38%)}')
pal.append('.card .art::after{display:none}')
pal.append('.card .tap{background:rgba(255,255,255,.94);color:#141218;padding:6px 9px;border-radius:999px;font-size:10px;box-shadow:0 4px 12px rgba(0,0,0,.18)}')
pal.append('.card .ic{border:0}')
pal.append('.card[hidden]{display:none!important}')
css = css.replace('</style>', '') + '\n' + '\n'.join(pal) + '\n'

logo = re.search(r'(<svg class="logo".*?</svg>)', SRC, re.S).group(1)
head = SRC[:SRC.index('<style>')]
head = re.sub(r'<meta property="og:description" content="[^"]*">',
              '<meta property="og:description" content="Onboarding and paywall prototypes for MobiPDF, Pickup Music, Norton 360, Fishing Points, Ivy, LingoLooper, Fastic, Yousician, Babbel, Structured and Welltory, rebuilt in each app\'s own design.">', head)

views = []
for (k, t, sub, own, url, *_r) in APPS:
    u = url + '?view=proto'
    views.append({'key': k, 'title': t, 'sub': sub, 'cls': 'v-' + k, 'icon': 'img/%s-icon.png' % k,
                  'art': 'img/%s-art.jpg' % k, 'url': u, 'short': url.replace('https://', '').rstrip('/'), 'qr': qr_svg(u)})

body = '''<body>

<div class="glow" aria-hidden="true"><i></i><i></i></div>
<main class="page">
  <div class="top">
    %(logo)s
    <span class="sep"></span><span class="lbl">Prototype wall</span>
    <span class="n">%(n)d apps</span>
  </div>
  <h1>Their onboarding and paywall, <em>rebuilt</em> and live on their phone.</h1>
  <p class="lede">Each prototype is the app’s own flow redrawn in its own design: five ranked ideas and a paywall that uses their answers. Tap a card and hand them the screen.</p>
  <div class="grid" id="grid"></div>
  <div class="how">
    <div><b>1 · Tap</b>Pick the company you are talking to.</div>
    <div><b>2 · Show</b>Their camera scans the code on your screen.</div>
    <div><b>3 · Swipe</b>Next company, without going back.</div>
  </div>
  <p class="foot">Every code opens the prototype straight on the phone, with the audit one tap away. Links stay live on GitHub Pages.</p>
</main>

<section class="stage" id="stage" hidden aria-modal="true" role="dialog" aria-label="Prototype QR code">
  <div class="s-top">
    <button class="s-btn" id="close" aria-label="Back to all apps"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></button>
    <div class="dots" id="dots"></div>
    <span style="width:44px;flex:none"></span>
  </div>
  <div class="s-mid" id="sMid"></div>
  <p class="scan" id="scan">Point your camera here</p>
  <div class="s-bot" id="sBot">
    <span class="s-url" id="sUrl"></span>
    <button class="s-act" id="copy"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M15 9V6.5A2.5 2.5 0 0 0 12.5 4h-6A2.5 2.5 0 0 0 4 6.5v6A2.5 2.5 0 0 0 6.5 15H9"/></svg>Copy</button>
    <a class="s-act pri" id="open" href="#" target="_blank" rel="noopener">Open<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M8 7h9v9"/></svg></a>
  </div>
  <div class="nav-arrows"><button class="s-btn" id="prev" aria-label="Previous"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></button><button class="s-btn" id="next" aria-label="Next"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button></div>
</section>
<div class="toast" id="toast"></div>

<script>
var VIEWS=%(views)s;
function $(s){ return document.querySelector(s); }
function icon(v){ return '<span class="ic"><img src="'+v.icon+'" alt=""></span>'; }
var LIST=VIEWS.map(function(_,i){ return i; });
$('#grid').innerHTML=VIEWS.map(function(v,i){
  return '<button class="card '+v.cls+'" data-i="'+i+'"><span class="art"><img src="'+v.art+'" alt=""></span><span class="id"><span class="ics">'+icon(v)+'</span><span><h2>'+v.title+'</h2><span class="kind">'+v.sub+'<br>Onboarding + paywall</span></span></span>'
   +'<span class="go"><span class="minis"><span class="mini">'+v.qr+'</span></span><span class="tap">Tap to show</span></span></button>';
}).join('');
var pos=-1, stage=$('#stage'), lock=null;
function render(p){
  pos=(p+LIST.length)%%LIST.length; var v=VIEWS[LIST[pos]];
  stage.className='stage '+v.cls;
  $('#sMid').className='s-mid';
  $('#sMid').innerHTML='<div class="s-app"><div class="s-id">'+icon(v)+'<div><h2>'+v.title+'</h2><small>'+v.sub+'</small></div></div><div class="qr">'+v.qr+'</div></div>';
  $('#scan').innerHTML='Point your camera here<small>Opens the '+v.title+' prototype in the browser</small>';
  $('#sUrl').textContent=v.short; $('#open').href=v.url;
  $('#dots').innerHTML=LIST.map(function(_,j){ return '<i'+(j===pos?' class="on"':'')+'></i>'; }).join('');
  try{ history.replaceState(null,'','#'+v.key); }catch(e){}
}
function show(i){ var p=LIST.indexOf(i); if(p<0){ LIST=VIEWS.map(function(_,j){ return j; }); p=i; } render(p); stage.hidden=false; document.body.style.overflow='hidden'; $('#close').focus();
  if(navigator.wakeLock&&navigator.wakeLock.request){ navigator.wakeLock.request('screen').then(function(l){ lock=l; }).catch(function(){}); } }
function hide(){ stage.hidden=true; document.body.style.overflow=''; pos=-1; try{ history.replaceState(null,'',location.pathname+location.search); }catch(e){} if(lock){ try{ lock.release(); }catch(e){} lock=null; } }
document.querySelectorAll('.card').forEach(function(c){ c.addEventListener('click',function(){ show(+c.dataset.i); }); });
$('#close').addEventListener('click',hide);
$('#prev').addEventListener('click',function(){ render(pos-1); });
$('#next').addEventListener('click',function(){ render(pos+1); });
document.addEventListener('keydown',function(e){ if(stage.hidden) return; if(e.key==='Escape') hide(); if(e.key==='ArrowRight') render(pos+1); if(e.key==='ArrowLeft') render(pos-1); });
var x0=null,y0=null;
stage.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; y0=e.touches[0].clientY; },{passive:true});
stage.addEventListener('touchend',function(e){ if(x0===null) return; var dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0; if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)) render(pos+(dx<0?1:-1)); x0=null; },{passive:true});
function toast(m){ var t=$('#toast'); t.textContent=m; t.classList.add('show'); setTimeout(function(){ t.classList.remove('show'); },1600); }
$('#copy').addEventListener('click',function(){ var u=VIEWS[LIST[pos]].url;
  try{ navigator.clipboard.writeText(u).then(function(){ toast('Link copied'); },function(){ sel(); }); }catch(e){ sel(); }
  function sel(){ var r=document.createRange(); r.selectNodeContents($('#sUrl')); var s=getSelection(); s.removeAllRanges(); s.addRange(r); toast('Link selected, copy it'); } });
/* open a company straight from its link, e.g. #babbel */
var h=(location.hash||'').slice(1); VIEWS.forEach(function(v,i){ if(v.key===h) show(i); });
</script>
<script>
var BUILD='w2';
fetch(location.pathname+'?cb='+Date.now(),{cache:'no-store'}).then(function(r){ return r.text(); }).then(function(x){
  var m=x.match(/var BUILD='([^']+)'/); if(m && m[1]!==BUILD){ var q=new URLSearchParams(location.search); q.set('v',m[1]); location.replace(location.pathname+'?'+q.toString()+location.hash); }
}).catch(function(){});
</script>
</body>
</html>
''' % {'logo': logo, 'n': len(APPS), 'views': json.dumps(views, ensure_ascii=False)}

open(os.path.join(HERE, 'index.html'), 'w').write(head + '<style>' + css + '</style>\n</head>\n' + body)
open(os.path.join(HERE, '.nojekyll'), 'w').write('')
print('ok', len(APPS))
