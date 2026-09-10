#!/usr/bin/env python3
"""Builds the Souvla Kings site.

  index.html          the site, images loaded from assets/
  souvla-kings.html   one self-contained file with every image inlined
  gallery.html        Souvla Days, built from whatever is in assets/gallery/

To add gallery photos: drop them in assets/gallery/, optionally add a caption
line to assets/gallery/captions.txt, then run this script.
"""
import pathlib, re, struct, html, json

root = pathlib.Path(__file__).parent


# ---------- image dimensions, without any third-party library ----------
def img_size(path):
    d = path.open('rb').read(64 * 1024)
    if d[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', d[16:24])
    if d[:4] == b'RIFF' and d[8:12] == b'WEBP':
        tag = d[12:16]
        if tag == b'VP8 ':
            return (struct.unpack('<H', d[26:28])[0] & 0x3fff,
                    struct.unpack('<H', d[28:30])[0] & 0x3fff)
        if tag == b'VP8L':
            b = d[21:25]
            w = ((b[0] | (b[1] & 0x3f) << 8) + 1)
            h = (((b[1] >> 6) | b[2] << 2 | (b[3] & 0x0f) << 10) + 1)
            return w, h
        if tag == b'VP8X':
            return (1 + int.from_bytes(d[24:27], 'little'),
                    1 + int.from_bytes(d[27:30], 'little'))
    if d[:2] == b'\xff\xd8':                       # jpeg: find the frame header
        i = 2
        while i < len(d) - 9:
            if d[i] != 0xFF:
                i += 1
                continue
            m = d[i + 1]
            if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            ln = struct.unpack('>H', d[i + 2:i + 4])[0]
            if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack('>HH', d[i + 5:i + 9])
                return w, h
            i += 2 + ln
    return None


# ---------- gallery ----------
def build_gallery():
    tpl = (root / 'src/gallery.html').read_text()
    folder = root / 'assets/gallery'
    exts = {'.jpg', '.jpeg', '.png', '.webp'}
    photos = sorted(p for p in folder.glob('*') if p.suffix.lower() in exts) if folder.is_dir() else []

    caps = {}
    cf = folder / 'captions.txt'
    if cf.is_file():
        for line in cf.read_text().splitlines():
            line = line.split('#', 1)[0].strip()
            if '|' in line:
                name, cap = line.split('|', 1)
                caps[name.strip()] = cap.strip()

    if not photos:
        body = ('    <div class="empty">\n'
                '      <h3>No photos up yet.</h3>\n'
                '      <p>Text a photo of your souvla to 0429 543 435 and it goes here.</p>\n'
                '    </div>')
    else:
        cls = 'grid-photos one' if len(photos) == 1 else ('grid-photos few' if len(photos) <= 4 else 'grid-photos')
        out = [f'    <div class="{cls}">']
        for p in photos:
            src = f'assets/gallery/{p.name}'
            cap = caps.get(p.name, '')
            alt = cap or f'A Souvla Kings souvla in use, {p.stem.replace("-", " ").lstrip("0123456789 ")}'
            size = img_size(p)
            dims = f' width="{size[0]}" height="{size[1]}"' if size else ''
            e = html.escape
            out.append(
                '      <figure class="shot">\n'
                f'        <button type="button" data-full="{e(src)}" data-cap="{e(cap)}" data-alt="{e(alt)}">\n'
                f'          <img src="{e(src)}" alt="{e(alt)}"{dims} loading="lazy" decoding="async">\n'
                '        </button>'
                + (f'\n        <figcaption>{e(cap)}</figcaption>' if cap else '') +
                '\n      </figure>')
        out.append('    </div>')
        body = '\n'.join(out)

    (root / 'gallery.html').write_text(tpl.replace('__PHOTOS__', body))
    return len(photos)



# ---------- shop ----------
ICONS = {
 'motor': '<rect x="14" y="24" width="62" height="36" rx="4"/><path d="M26 34h38M26 42h38M26 50h38"/><path d="M76 42h34"/><circle cx="118" cy="42" r="8"/>',
 'motor-xl': '<rect x="8" y="18" width="72" height="46" rx="4"/><path d="M22 30h44M22 41h44M22 52h44"/><path d="M80 41h32"/><circle cx="120" cy="41" r="11"/>',
 'chain-motor': '<rect x="10" y="26" width="50" height="32" rx="4"/><path d="M22 36h26M22 46h26"/><path d="M60 42h16"/><circle cx="100" cy="42" r="19"/><circle cx="100" cy="42" r="7"/><path d="M100 23v-7M100 61v7M81 42h-7M119 42h7M113 29l5-5M87 55l-5 5M113 55l5 5M87 29l-5-5"/>',
 'dial': '<rect x="26" y="20" width="88" height="44" rx="5"/><circle cx="56" cy="42" r="13"/><path d="M56 42v-9"/><path d="M84 32h20M84 42h20M84 52h20"/>',
 'skewer': '<path d="M20 44h96"/><rect x="12" y="36" width="26" height="16" rx="8"/><path d="M116 44l14-4v8z"/>',
 'skewer-xl': '<path d="M18 42h100" stroke-width="6"/><rect x="8" y="31" width="30" height="22" rx="11"/><path d="M118 42l16-6v12z"/>',
 'skewer-small': '<path d="M42 44h58"/><rect x="34" y="37" width="22" height="14" rx="7"/><path d="M100 44l12-3.5v7z"/>',
 'fork': '<path d="M18 42h34"/><rect x="52" y="26" width="12" height="32" rx="3"/><path d="M64 34h32M64 50h32"/><path d="M96 34l12-4v8zM96 50l12-4v8z"/>',
 'grill': '<rect x="16" y="18" width="108" height="48" rx="3"/><path d="M16 28h108M16 38h108M16 48h108M16 58h108"/><path d="M44 18v48M70 18v48M96 18v48"/>',
 'tray': '<path d="M22 26h96l-14 36H36z"/><path d="M32 36h76M36 48h68"/>',
 'disc': '<circle cx="70" cy="42" r="26"/><circle cx="70" cy="42" r="7"/><path d="M70 16v10M70 58v10M44 42h10M86 42h10M52 24l7 7M81 53l7 7M88 24l-7 7M59 53l-7 7"/>',
 'strap': '<path d="M20 30c26 22 74 22 100 0"/><path d="M20 30v14c26 22 74 22 100 0V30"/><circle cx="34" cy="36" r="3"/><circle cx="70" cy="45" r="3"/><circle cx="106" cy="36" r="3"/>',
 'riser': '<path d="M52 12v58M64 12v58"/><path d="M52 20h12M52 30h12M52 40h12M52 50h12M52 60h12"/><path d="M64 40h22"/><circle cx="96" cy="40" r="11"/><path d="M96 40l14 12"/><rect x="106" y="48" width="16" height="8" rx="4"/>',
}


def icon_svg(name):
    body = ICONS.get(name)
    if not body:
        return '<svg viewBox="0 0 140 80" aria-hidden="true"><rect x="20" y="20" width="100" height="40" rx="4" fill="none" stroke="currentColor" stroke-width="3"/></svg>'
    return ('<svg viewBox="0 0 140 80" fill="none" stroke="currentColor" stroke-width="3" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>')


def read_catalogue():
    f = root / 'assets/shop/products.txt'
    items = []
    if not f.is_file():
        return items
    for line in f.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = [c.strip() for c in line.split('|')]
        if len(parts) < 6:
            continue
        pid, group, name, price, image, blurb = parts[:6]
        addon = parts[6] if len(parts) > 6 and parts[6] else None
        items.append({
            'id': pid, 'group': group, 'name': name,
            'price': None if price.upper() == 'POA' else int(float(price)),
            'image': image, 'blurb': blurb, 'addon': addon,
        })
    return items


def money(n):
    return '$' + format(n, ',d')


def build_shop():
    items = read_catalogue()
    if not items:
        return 0
    e = html.escape
    machines, parts = [], []
    qty = ('<span class="qty"><button type="button" data-step="down" aria-label="One fewer">&minus;</button>'
           '<input type="number" min="1" max="99" value="1" data-cardqty aria-label="Quantity">'
           '<button type="button" data-step="up" aria-label="One more">+</button></span>')

    for it in items:
        by_id = {i['id']: i for i in items}
        blurb, dims = it['blurb'], ''
        if '. ' in blurb:
            head, rest = blurb.split('. ', 1)
            if 'mm' in head or head.lower().startswith('ring'):
                dims, blurb = head, rest
        price_html = (f'<span class="price tnum">{money(it["price"])}</span>'
                      if it['price'] is not None else '<span class="price poa">Price on call</span>')

        if it['group'].lower().startswith('souvla'):
            src = it['image']
            if src in ('soon', '') or src.startswith('icon:'):
                img = ('<div class="mach-img soon"><span>' + icon_svg('grill') +
                       '<b>Photo coming</b></span></div>')
            else:
                img = (f'<div class="mach-img"><img src="assets/shop/{e(src)}" '
                       f'alt="{e(it["name"])}" loading="lazy" decoding="async"></div>')
                img = img.replace('assets/shop/../', 'assets/')
            extra = ''
            a = by_id.get(it['addon']) if it['addon'] else None
            if a:
                ap = money(a['price']) if a['price'] is not None else 'price on call'
                extra = (f'<label class="addon"><input type="checkbox" data-addon="{e(a["id"])}">'
                         f'<span><b>Add the {e(a["name"].lower())}</b>, {ap}. {e(a["blurb"])}</span></label>')
            note = 'Free assembly and Sydney delivery' if it['price'] is not None else 'Built to order'
            machines.append(
                f'      <article class="mach">\n{img}\n        <div>\n'
                f'          <h3>{e(it["name"])}</h3>\n'
                + (f'          <p class="dims">{e(dims)}</p>\n' if dims else '') +
                f'          <p class="blurb">{e(blurb)}</p>\n'
                f'          <div class="priceline">{price_html}<span class="note">{note}</span></div>\n'
                f'{extra}\n'
                f'          <div class="buyrow">{qty}<button class="btn btn-primary" type="button" data-add="{e(it["id"])}">Add to order</button></div>\n'
                f'        </div>\n      </article>')
        else:
            if it['image'].startswith('icon:'):
                ico = f'<span class="ico">{icon_svg(it["image"][5:])}</span>'
            else:
                src = it['image'].replace('../', '')
                ico = f'<span class="ico"><img src="assets/{e(src)}" alt="{e(it["name"])}" loading="lazy"></span>'
            pf = (f'<span class="p tnum">{money(it["price"])}</span>' if it['price'] is not None
                  else '<span class="p poa">Price on call</span>')
            parts.append(
                f'      <article class="part">{ico}<b>{e(it["name"])}</b><p>{e(it["blurb"])}</p>'
                f'<div class="foot">{pf}<button class="btn btn-line btn-sm" type="button" data-add="{e(it["id"])}">Add</button></div></article>')

    data = json.dumps([{'id': i['id'], 'name': i['name'], 'price': i['price']} for i in items],
                      separators=(',', ':'))
    tpl = (root / 'src/shop.html').read_text()
    tpl = tpl.replace('__MACHINES__', '    <div class="machines">\n' + '\n'.join(machines) + '\n    </div>')
    tpl = tpl.replace('__PARTS__', '    <div class="parts">\n' + '\n'.join(parts) + '\n    </div>')
    tpl = tpl.replace('__DATA__', data)
    (root / 'shop.html').write_text(tpl)
    return len(items)


# ---------- main site ----------
src = (root / 'src/site.html').read_text()

web = src.replace('__LOGO__', 'assets/logo.webp')
for i in (1, 2, 3):
    web = web.replace(f'data:image/webp;base64,__IMG{i}__', f'assets/bbq-{i}.webp')
assert '__LOGO__' not in web and '__IMG' not in web, 'unreplaced placeholder in web build'
(root / 'index.html').write_text(web)

one = src.replace('__LOGO__', 'data:image/webp;base64,' + (root / 'assets/logo.b64').read_text().strip())
for i in (1, 2, 3):
    one = one.replace(f'__IMG{i}__', (root / f'assets/bbq-{i}.b64').read_text().strip())
assert '__LOGO__' not in one and '__IMG' not in one, 'unreplaced placeholder in standalone build'
strip = {'<!doctype html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         '</head>', '<body>', '</body>', '</html>'}
(root / 'souvla-kings.html').write_text('\n'.join(l for l in one.split('\n') if l.strip() not in strip))

n = build_gallery()
m = build_shop()
print(f'index.html {len(web)//1024} KB   souvla-kings.html {len(one)//1024} KB   '
      f'gallery.html {n} photo(s)   shop.html {m} product(s)')
