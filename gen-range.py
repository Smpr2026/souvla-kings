#!/usr/bin/env python3
"""Generates src/range-options.html: four working layouts for the range section."""
import pathlib, html

M = [
 dict(id='open', name='Open Souvla', role='The starting size', size='700 × 400 mm', w=700, d=400,
      price='$649', pre='from', img=1,
      kit=[('3','large skewers'),('6','skewer forks'),('11','souvlaki skewers'),('2','grills'),
           ('','Removable charcoal tray'),('','Geared motor'),('','Speed controller')],
      spec={'skewers':'3 large + 11 souvlaki','forks':'6','grills':'2','motors':'1 geared','ctrl':'1','tray':'Yes','yeeros':'—'}),
 dict(id='hooded', name='Hooded Souvla', role='The same size, with the hood', size='700 × 400 mm', w=700, d=400,
      price='$849', pre='from', img=1,
      kit=[('3','large skewers'),('6','skewer forks'),('11','souvlaki skewers'),('2','grills'),
           ('','Removable charcoal tray'),('','Geared motor'),('','Speed controller')],
      spec={'skewers':'3 large + 11 souvlaki','forks':'6','grills':'2','motors':'1 geared','ctrl':'1','tray':'Yes','yeeros':'—'}),
 dict(id='chain', name='Large Chain Drive', role='The one most people buy', size='900 × 600 mm', w=900, d=600,
      price='$1099', pre='from', img=1,
      kit=[('11','large skewers'),('12','forks'),('2','grills'),('','Removable charcoal tray'),('','Large geared motor')],
      spec={'skewers':'11 large','forks':'12','grills':'2','motors':'1 large geared','ctrl':'Ring','tray':'Yes','yeeros':'—'}),
 dict(id='mega', name='Mega Souvla', role='Chain drive with a full rotisserie over it', size='Ring for size', w=None, d=None,
      price='$1399', pre='from', img=3,
      kit=[('1','XL geared motor'),('1','geared chain motor'),('1','12 mm Mega skewer'),('2','speed controllers'),
           ('11','8 mm skewers'),('2','large forks'),('12','skewer forks'),('2','grills'),('2','yeeros discs'),
           ('','Removable charcoal tray')],
      spec={'skewers':'1 Mega (12 mm) + 11 × 8 mm','forks':'2 large + 12','grills':'2','motors':'1 XL + 1 chain','ctrl':'2','tray':'Yes','yeeros':'2 discs'}),
 dict(id='double', name='Double Mega', role='Top of the range', size='900 × 600 mm', w=900, d=600,
      price='$1699', pre='from', img=3,
      kit=[('2','XL motors'),('1','chain motor'),('3','speed controllers'),('2','XL skewers'),('4','large forks'),
           ('2','back straps'),('4','yeeros discs'),('11','chain skewers'),('12','chain skewer forks'),('2','large grills')],
      spec={'skewers':'2 XL + 11 chain','forks':'4 large + 12','grills':'2 large','motors':'2 XL + 1 chain','ctrl':'3','tray':'Ring','yeeros':'4 discs + 2 straps'}),
 dict(id='triple', name='Triple Mega', role='Three spits across, built to order', size='Ring for size', w=None, d=None,
      price='Price on call', pre='', img=3,
      kit=[('','For clubs, fetes and catering'),('','Ring for the kit list and the lead time')],
      spec={'skewers':'Ring','forks':'Ring','grills':'Ring','motors':'Ring','ctrl':'Ring','tray':'Ring','yeeros':'Ring'}),
]
TEL = 'tel:+61429543435'
e = html.escape

def price_html(m, cls='price'):
    if m['pre']:
        return f'<span class="{cls}"><small>{m["pre"]}</small>{m["price"]}</span>'
    return f'<span class="{cls} ask">{m["price"]}</span>'

def kit_line(m):
    out = []
    for n, t in m['kit']:
        out.append(f'<li><b>{n}</b> {e(t)}</li>' if n else f'<li>{e(t)}</li>')
    return '<ul class="kitline">' + ''.join(out) + '</ul>'

def kit_rows(m):
    out = []
    for n, t in m['kit']:
        out.append(f'<li><span class="qn">{n or "&bull;"}</span><span>{e(t)}</span></li>')
    return '<ul class="kitrows">' + ''.join(out) + '</ul>'

def footprint(m, maxw=900, maxd=600, box=132):
    """To-scale plan of the cooking surface."""
    if not m['w']:
        return ('<div class="fp fp-none"><svg viewBox="0 0 132 92" aria-hidden="true">'
                '<rect x="6" y="6" width="120" height="80" rx="2" fill="none" stroke="var(--steel-2)" '
                'stroke-width="2" stroke-dasharray="5 4"/></svg><span class="fp-lb">Ring for size</span></div>')
    w = box * m['w'] / maxw; d = box * 0.66 * m['d'] / maxd
    x = (box - w) / 2; y = (87 - d) / 2
    return (f'<div class="fp"><svg viewBox="0 0 {box} 92" aria-hidden="true">'
            f'<rect x="6" y="6" width="120" height="80" rx="2" fill="none" stroke="var(--steel)" stroke-width="1" stroke-dasharray="3 3"/>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{d:.1f}" rx="2" fill="color-mix(in oklab,var(--blue) 12%,#fff)" '
            f'stroke="var(--blue-deep)" stroke-width="2"/></svg><span class="fp-lb">{e(m["size"])}</span></div>')

# ---------- A: compare grid ----------
SPEC_ROWS = [('size','Size'),('skewers','Skewers'),('forks','Forks'),('grills','Grills'),
             ('motors','Motors'),('ctrl','Speed controllers'),('yeeros','Yeeros gear'),('tray','Charcoal tray')]
def layout_a():
    head = ''.join(f'<th scope="col"><span class="cm-n">{e(m["name"])}</span></th>' for m in M)
    rows = ''
    for key, label in SPEC_ROWS:
        cells = ''.join(f'<td>{e(m["size"] if key=="size" else m["spec"][key])}</td>' for m in M)
        rows += f'<tr><th scope="row">{label}</th>{cells}</tr>'
    prices = ''.join(f'<td>{price_html(m,"cm-p")}</td>' for m in M)
    rows += f'<tr class="cm-price"><th scope="row">Price</th>{prices}</tr>'
    return f'''<div class="cmwrap">
<table class="compare">
<thead><tr><th scope="col"><span class="sr">Spec</span></th>{head}</tr></thead>
<tbody>{rows}</tbody>
</table></div>
<p class="fine-note">A dash means it is not listed in that model&rsquo;s spec, not that it is missing. Ring to confirm.</p>'''

# ---------- B: size cards ----------
def layout_b():
    cards = ''
    for m in M:
        cards += f'''<li class="card">
<div class="card-top">{footprint(m)}</div>
<div class="card-body">
  <h3>{e(m["name"])}</h3>
  <p class="role">{e(m["role"])}</p>
  {kit_rows(m)}
</div>
<div class="card-foot">{price_html(m,"price")}<a class="btn btn-line btn-sm" href="{TEL}">Call</a></div>
</li>'''
    return f'<ul class="cards">{cards}</ul>'

# ---------- C: one at a time ----------
def layout_c():
    tabs = ''.join(
        f'<button class="ctab" role="tab" aria-selected="{"true" if i==0 else "false"}" '
        f'aria-controls="p-{m["id"]}" id="t-{m["id"]}" data-i="{i}">{e(m["name"])}</button>'
        for i, m in enumerate(M))
    panels = ''
    for i, m in enumerate(M):
        panels += f'''<div class="cpanel" id="p-{m["id"]}" role="tabpanel" aria-labelledby="t-{m["id"]}"{"" if i==0 else " hidden"}>
  <div class="cp-left">
    <p class="role">{e(m["role"])}</p>
    <h3>{e(m["name"])}</h3>
    <p class="cp-size">{e(m["size"])}</p>
    <div class="cp-price">{price_html(m,"price")}</div>
    <a class="btn btn-primary" href="{TEL}">Call or text 0429 543 435</a>
  </div>
  <div class="cp-right">
    <p class="cp-lb">What comes with it</p>
    {kit_rows(m)}
  </div>
</div>'''
    return f'<div class="ctabs" role="tablist" aria-label="Models">{tabs}</div><div class="cpanels">{panels}</div>'

# ---------- D: editorial bands ----------
def layout_d():
    bands = ''
    for i, m in enumerate(M):
        bands += f'''<li class="band{' alt' if i % 2 else ''}">
  <div class="bd-price">{price_html(m,"bigp")}</div>
  <div class="bd-body">
    <h3>{e(m["name"])}</h3>
    <p class="role">{e(m["role"])} &middot; {e(m["size"])}</p>
    {kit_line(m)}
  </div>
</li>'''
    return f'<ul class="bands">{bands}</ul>'

CSS = """
:root{--paper:#fbfcfe;--paper-2:#f1f3f8;--paper-3:#e6e9f1;--steel:#d3d8e4;--steel-2:#b9c0d0;
--ink:#11141c;--ink-2:#454b5c;--ink-3:#6b7284;--blue:#0012fb;--blue-deep:#0410c4;--blue-ink:#000b8f;
--blue-tint:#eceefe;--char:#12141b;--ease:cubic-bezier(.16,1,.3,1);
--sans:'Archivo','Helvetica Neue',Arial,sans-serif;color-scheme:light}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:1.0625rem;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img,svg{display:block;max-width:100%}
p{margin:0}a{color:inherit}button{font:inherit;color:inherit}
h1,h2,h3{margin:0;font-weight:800;line-height:1.03;letter-spacing:-.018em;font-stretch:112%;text-wrap:balance}
h1{font-size:clamp(2.2rem,4.6vw,3.6rem);font-weight:900}
h2{font-size:clamp(1.8rem,3.4vw,2.8rem)}
.wrap{width:min(1240px,100% - 2*clamp(1.1rem,4vw,3rem));margin-inline:auto}
:focus-visible{outline:2.5px solid var(--blue);outline-offset:3px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;font-weight:700;font-size:1rem;text-decoration:none;padding:.8rem 1.3rem;border-radius:2px;border:1.5px solid transparent;line-height:1;cursor:pointer;white-space:nowrap;transition:background .18s,color .18s,border-color .18s,transform .18s var(--ease)}
.btn-primary{background:var(--blue-deep);color:#fff}
.btn-primary:hover{background:var(--blue);transform:translateY(-1px)}
.btn-line{border-color:var(--steel-2);color:var(--ink);background:#fff}
.btn-line:hover{border-color:var(--ink)}
.btn-sm{padding:.55rem .95rem;font-size:.92rem}
.rule{display:flex;align-items:center;gap:.8rem;font-weight:700;font-size:.85rem;letter-spacing:.12em;text-transform:uppercase;color:var(--blue-ink);margin-bottom:1rem}
.rule::after{content:"";height:1.5px;flex:1;background:var(--steel)}
/* chrome */
.bar{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.6rem clamp(1rem,3vw,2rem);background:color-mix(in oklab,var(--paper) 94%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--steel)}
.bar img{height:42px;width:auto}
.tabs{display:flex;gap:.35rem;overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{flex:none;display:inline-flex;align-items:center;gap:.5rem;padding:.5rem .8rem;border:1.5px solid var(--steel);border-radius:2px;text-decoration:none;color:var(--ink-2);font-weight:700;font-size:.93rem;transition:color .15s,border-color .15s,background .15s}
.tab b{display:grid;place-items:center;width:1.4rem;height:1.4rem;border-radius:50%;background:var(--paper-3);color:var(--ink);font-size:.82rem}
.tab:hover{color:var(--ink);border-color:var(--ink-3)}
.intro{padding:clamp(2rem,4.5vw,3.4rem) 0 clamp(1.2rem,2.5vw,2rem)}
.intro p{color:var(--ink-2);font-size:1.12rem;max-width:60ch;margin-top:.9rem}
.opt{padding-block:clamp(2.6rem,5vw,4.5rem);border-top:1px solid var(--steel)}
.opt:nth-child(even){background:#fff}
.ohead{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:.5rem clamp(2rem,5vw,4rem);align-items:end;margin-bottom:clamp(1.6rem,3vw,2.6rem)}
.ohead .rule{grid-column:1/-1}
.ohead .sub{color:var(--ink-2);font-size:1.05rem;padding-bottom:.3rem}
@media (max-width:860px){.ohead{grid-template-columns:1fr}}
.price{font-weight:900;font-size:clamp(1.4rem,2.2vw,1.85rem);letter-spacing:-.028em;font-stretch:112%;white-space:nowrap;font-variant-numeric:tabular-nums}
.price small{font-weight:600;font-size:.6em;letter-spacing:.09em;text-transform:uppercase;color:var(--blue-ink);margin-right:.4em;font-stretch:100%}
.price.ask{font-weight:700;font-size:1rem;color:var(--ink-2);letter-spacing:.01em}
.kitrows{list-style:none;margin:0;padding:0;display:grid;gap:.28rem}
.kitrows li{display:grid;grid-template-columns:1.7rem 1fr;gap:.55rem;align-items:baseline;color:var(--ink-2);font-size:.96rem}
.kitrows .qn{font-weight:800;color:var(--ink);font-variant-numeric:tabular-nums;text-align:right}
.kitline{list-style:none;margin:.55rem 0 0;padding:0;color:var(--ink-2);font-size:.97rem;line-height:1.5;max-width:74ch}
.kitline li{display:inline;white-space:nowrap}
.kitline li:not(:last-child)::after{content:" · ";color:var(--ink-3)}
.kitline b{color:var(--ink);font-weight:700;font-variant-numeric:tabular-nums}
.fine-note{margin-top:1rem;color:var(--ink-3);font-size:.9rem}
/* A compare */
.cmwrap{overflow-x:auto;border:1px solid var(--steel);background:#fff}
.compare{border-collapse:collapse;width:100%;min-width:920px;font-size:.95rem}
.compare th,.compare td{text-align:left;padding:.8rem .9rem;border-bottom:1px solid var(--steel);vertical-align:middle}
.compare thead th{background:var(--paper-2);border-bottom:2px solid var(--ink);position:sticky;top:0}
.cm-n{font-weight:800;font-size:1rem;letter-spacing:-.01em;display:block}
.compare tbody th{font-weight:600;color:var(--ink-3);font-size:.84rem;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;background:#fff;position:sticky;left:0;border-right:1px solid var(--steel)}
.compare tbody tr:hover td{background:var(--blue-tint)}
.compare td{color:var(--ink-2)}
.cm-price td{padding-block:1.1rem;border-bottom:0}
.cm-p{font-weight:900;font-size:1.3rem;letter-spacing:-.02em;font-stretch:112%;font-variant-numeric:tabular-nums;white-space:nowrap}
.cm-p small{font-weight:600;font-size:.58em;letter-spacing:.09em;text-transform:uppercase;color:var(--blue-ink);margin-right:.35em;font-stretch:100%;display:block}
.cm-p.ask{font-weight:700;font-size:.95rem;color:var(--ink-2)}
/* B cards */
.cards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:1px;background:var(--steel);border:1px solid var(--steel)}
.card{background:#fff;display:grid;grid-template-rows:auto 1fr auto;transition:background .18s}
.card:hover{background:var(--blue-tint)}
.card-top{padding:1.2rem 1.3rem .4rem;display:flex;justify-content:center}
.fp{display:grid;justify-items:center;gap:.4rem}
.fp svg{width:132px;height:92px}
.fp-lb{font-weight:700;font-size:.82rem;letter-spacing:.06em;color:var(--blue-ink);font-variant-numeric:tabular-nums}
.fp-none .fp-lb{color:var(--ink-3)}
.card-body{padding:.6rem 1.3rem 1.1rem}
.card-body h3{font-size:1.25rem}
.card .role{color:var(--ink-3);font-size:.92rem;margin:.15rem 0 .8rem}
.card-foot{display:flex;align-items:center;justify-content:space-between;gap:.8rem;padding:.9rem 1.3rem;border-top:1px solid var(--steel)}
/* C tabs */
.ctabs{display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:1.6rem}
.ctab{padding:.6rem 1rem;border:1.5px solid var(--steel);background:#fff;border-radius:2px;font-weight:700;font-size:.96rem;cursor:pointer;transition:background .16s,border-color .16s,color .16s}
.ctab:hover{border-color:var(--ink-3)}
.ctab[aria-selected=true]{background:var(--ink);border-color:var(--ink);color:#fff}
.cpanels{border:1px solid var(--steel);background:#fff}
.cpanel{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:clamp(1.5rem,4vw,4rem);padding:clamp(1.5rem,3vw,2.6rem)}
.cpanel[hidden]{display:none}
.cp-left .role{color:var(--blue-ink);font-weight:700;font-size:.85rem;letter-spacing:.09em;text-transform:uppercase}
.cp-left h3{font-size:clamp(1.8rem,3vw,2.5rem);margin:.4rem 0 .3rem}
.cp-size{color:var(--ink-3);font-weight:600;font-variant-numeric:tabular-nums}
.cp-price{margin:1.1rem 0 1.3rem;padding-top:1.1rem;border-top:2px solid var(--ink)}
.cp-price .price{font-size:clamp(2rem,3.4vw,2.9rem)}
.cp-lb{font-weight:700;font-size:.82rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-bottom:.7rem}
@media (max-width:820px){.cpanel{grid-template-columns:1fr}}
/* D bands */
.bands{list-style:none;margin:0;padding:0;border-top:2px solid var(--ink)}
.band{display:grid;grid-template-columns:minmax(0,auto) minmax(0,1fr);gap:clamp(1rem,3vw,3rem);align-items:start;padding:clamp(1.4rem,2.6vw,2.1rem) clamp(.4rem,1vw,.8rem);border-bottom:1px solid var(--steel);transition:background .18s}
.band:hover{background:var(--blue-tint)}
.band.alt{grid-template-columns:minmax(0,1fr) minmax(0,auto)}
.band.alt .bd-price{order:2;text-align:right}
.band.alt .bd-body{order:1}
.bigp{font-weight:900;font-size:clamp(2.2rem,4.4vw,3.6rem);letter-spacing:-.035em;font-stretch:112%;line-height:.92;white-space:nowrap;font-variant-numeric:tabular-nums;display:block;min-width:5.5ch}
.bigp small{display:block;font-weight:600;font-size:.24em;letter-spacing:.12em;text-transform:uppercase;color:var(--blue-ink);font-stretch:100%;margin-bottom:.25em}
.bigp.ask{font-size:clamp(1.1rem,1.7vw,1.4rem);font-weight:800;color:var(--ink-2);line-height:1.2}
.band h3{font-size:clamp(1.3rem,2.1vw,1.7rem)}
.band .role{color:var(--ink-3);font-size:.94rem;margin-top:.2rem}
@media (max-width:760px){.band,.band.alt{grid-template-columns:1fr}.band.alt .bd-price{order:0;text-align:left}.band.alt .bd-body{order:1}}
/* verdict */
.verdict{padding:clamp(2.4rem,5vw,4rem) 0;border-top:1px solid var(--steel)}
.verdict p{color:var(--ink-2);max-width:62ch;margin-top:.8rem}
"""

JS = """
document.querySelectorAll('.ctab').forEach(t => t.addEventListener('click', () => {
  const tabs = [...document.querySelectorAll('.ctab')];
  const panels = [...document.querySelectorAll('.cpanel')];
  tabs.forEach(o => o.setAttribute('aria-selected', String(o === t)));
  panels.forEach((p, i) => { p.hidden = i !== +t.dataset.i; });
}));
const io = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('on', t.dataset.for === e.target.id));
}), { threshold: .3 });
document.querySelectorAll('.opt').forEach(s => io.observe(s));
"""

OPTS = [
 ('a','Compare them side by side','Every spec in one grid, models across the top. Best when someone already knows they want a souvla and is deciding which one.', layout_a),
 ('b','Cards, drawn to scale','Each model as a card, with the cooking surface drawn to scale so the jump from 700 to 900 is something you can see.', layout_b),
 ('c','One at a time','Pick a model and only that one shows. Calm, and the kit list gets room to breathe instead of being squeezed.', layout_c),
 ('d','Big price bands','Full width rows with the price at display size, alternating left and right. Bold, and it scrolls like a poster.', layout_d),
]

def build(logo_uri):
    nav = ''.join(f'<a class="tab" href="#{i}" data-for="{i}"><b>{i.upper()}</b>{e(t)}</a>' for i, t, _, _ in OPTS)
    secs = ''
    for i, title, blurb, fn in OPTS:
        secs += f'''<section class="opt" id="{i}">
<div class="wrap">
  <div class="ohead"><p class="rule">Option {i.upper()}</p><h2>{e(title)}</h2><p class="sub">{e(blurb)}</p></div>
  {fn()}
</div>
</section>'''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Souvla Kings Range Layouts</title>
<meta name="description" content="Four layouts for the Souvla Kings range section, built with the real models, kit lists and prices.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..900&display=swap">
<style>{CSS}</style></head>
<body>
<nav class="bar" aria-label="Options"><img src="{logo_uri}" alt="Souvla Kings"><div class="tabs">{nav}</div></nav>
<header class="wrap intro"><h1>Four ways to lay out the range.</h1>
<p>Same six builds, same prices and kit lists, four different layouts. Tell me a letter and it goes into the site. Two can be combined if you want the grid on desktop and the cards on a phone.</p></header>
{secs}
<section class="verdict"><div class="wrap">
<h2>My pick: B.</h2>
<p>The cards give every model the same amount of room, the drawn footprint answers the question people actually ring about, and it stacks to one column on a phone without turning into a wall of text. Option A is the one to add underneath it if you want a proper spec comparison as well.</p>
</div></section>
<script>{JS}</script>
</body></html>'''

root = pathlib.Path(__file__).parent
logo = 'data:image/webp;base64,' + (root/'assets/logo.b64').read_text().strip()
(root/'src/range-options.html').write_text(build('__LOGO__'))
out = build(logo)
(root/'range-options.html').write_text(out)
strip = {'<!doctype html>','<html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">','</head>','<body>','</body></html>'}
(root/'range-options-artifact.html').write_text('\n'.join(l for l in out.split('\n') if l.strip() not in strip))
print('written', len(out), 'bytes')
