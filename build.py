#!/usr/bin/env python3
"""Builds the Souvla Kings site.

  index.html          the site, images loaded from assets/
  souvla-kings.html   one self-contained file with every image inlined
  gallery.html        Souvla Days, built from whatever is in assets/gallery/

To add gallery photos: drop them in assets/gallery/, optionally add a caption
line to assets/gallery/captions.txt, then run this script.
"""
import pathlib, re, struct, html

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
print(f'index.html {len(web)//1024} KB   souvla-kings.html {len(one)//1024} KB   gallery.html {n} photo(s)')
