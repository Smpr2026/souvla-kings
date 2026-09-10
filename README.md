# Souvla Kings

The website for Souvla Kings BBQ & Rotisseries, Sydney.

## Live site

`index.html` at the repo root is the site. It references the images in `assets/`,
so GitHub Pages can serve the repo root as-is. `.nojekyll` is there so Pages
serves the files without running Jekyll over them.

## Editing

Edit **`src/site.html`**, never the built files, then run:

```
python3 build.py
```

That writes two things:

- `index.html` — the hosted site, images loaded from `assets/` (about 41 KB)
- `souvla-kings.html` — one self-contained file with every image inlined, for emailing or previewing offline

## Assets

| File | What it is |
|---|---|
| `assets/logo.webp` | The badge logo, transparent background |
| `assets/bbq-1.webp` | Chain drive souvla, angled. Hero and the parts diagram |
| `assets/bbq-2.webp` | The same unit front on. **Not used** — the render reads "SOUNLA KINGS" |
| `assets/bbq-3.webp` | Mega Souvla, twin posts |

## Other pages in this repo

| File | What it is |
|---|---|
| `concepts.html` | Four early design directions |
| `range-options.html` | Four layouts for the range section |
| `animated-site.html` | First pass: dark, with smoke flowing through the page |

## Before this goes live

The prices, sizes and kit lists were taken from the Souvla Kings Facebook and
Instagram posts. Check these before pointing customers at it:

1. Are the six prices current, or were they sale prices?
2. Triple Mega has no public price, size or kit list.
3. Is delivery free Australia-wide, or free in Sydney metro with freight charged elsewhere? The posts say both.
4. What exactly is the "Hi rise conversion" at $99, and which models take it?
5. Is the 1500 mm commercial unit still sold? It was last posted in December 2020.
6. Add an email address and trading hours if you want them shown.
