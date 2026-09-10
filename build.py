#!/usr/bin/env python3
"""Builds the Souvla Kings site from src/site.html.

  index.html          for hosting: references assets/*.webp, small and cacheable
  souvla-kings.html   self-contained single file with every image inlined
"""
import pathlib, re

root = pathlib.Path(__file__).parent
src = (root / 'src/site.html').read_text()

# --- hosting build: external images ---
web = src.replace('__LOGO__', 'assets/logo.webp')
for i in (1, 2, 3):
    web = web.replace(f'data:image/webp;base64,__IMG{i}__', f'assets/bbq-{i}.webp')
assert '__LOGO__' not in web and '__IMG' not in web, 'unreplaced placeholder in web build'
(root / 'index.html').write_text(web)

# --- standalone build: inlined images ---
one = src.replace('__LOGO__', 'data:image/webp;base64,' + (root / 'assets/logo.b64').read_text().strip())
for i in (1, 2, 3):
    one = one.replace(f'__IMG{i}__', (root / f'assets/bbq-{i}.b64').read_text().strip())
assert '__LOGO__' not in one and '__IMG' not in one, 'unreplaced placeholder in standalone build'
strip = {'<!doctype html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         '</head>', '<body>', '</body>', '</html>'}
(root / 'souvla-kings.html').write_text('\n'.join(l for l in one.split('\n') if l.strip() not in strip))

m = re.search(r'<script>(.*?)</script>', src, re.S)
(root / '.build-script-check.js').write_text(m.group(1).replace('__LOGO__', 'x').replace('__IMG1__', 'x').replace('__IMG3__', 'x'))
print(f'index.html {len(web)//1024} KB   souvla-kings.html {len(one)//1024} KB')
