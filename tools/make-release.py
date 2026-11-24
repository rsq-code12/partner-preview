#!/usr/bin/env python3
"""Build the go-live copy of the partner page for https://partners.alurei.app into ./release/.

Same pages as the preview, with these differences:
- search engines may index it (robots meta + robots.txt + sitemap.xml), with canonical and social-share tags
- preview-only behaviour is off everywhere ("Preview only" notes, ?preview=1)
- the sign-up's last button says "Back to alurei.app" and opens https://alurei.app
- CNAME is staged as CNAME.staged (rename to CNAME, or set the custom domain, on go-live day)
Run from the repo root: python3 tools/make-release.py
"""
import pathlib, re, shutil

SITE = 'https://partners.alurei.app'
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'release'
PAGES = {'index.html': '/', 'signup.html': '/signup.html', 'privacy.html': '/privacy.html', 'terms.html': '/terms.html'}

def must(s, a, b, n=1):
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} x {a[:60]!r}, found {c}')
    return s.replace(a, b)

if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'assets', OUT / 'assets')

for name, path in PAGES.items():
    s = (ROOT / name).read_text(encoding='utf-8')
    s = must(s, '<meta name="robots" content="noindex, nofollow">', '<meta name="robots" content="index, follow">')
    title = re.search(r'<title>(.*?)</title>', s).group(1)
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = desc_m.group(1) if desc_m else 'Free to join: no fees, no commission.'
    tags = [f'<link rel="canonical" href="{SITE}{path}">']
    if 'property="og:title"' not in s:
        tags += [f'<meta property="og:title" content="{title}">', f'<meta property="og:description" content="{desc}">', '<meta property="og:image" content="assets/icon.png">']
    tags += [f'<meta property="og:url" content="{SITE}{path}">', '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Alurei">', '<meta name="twitter:card" content="summary">']
    s = must(s, '<title>', '\n'.join(tags) + '\n<title>')
    s = must(s, '<meta property="og:image" content="assets/icon.png">', f'<meta property="og:image" content="{SITE}/assets/icon.png">')
    if name == 'index.html':
        s = must(s, "const PREVIEW_HOST = ['rsq-code12.github.io', 'localhost', '127.0.0.1'].includes(location.hostname) || location.protocol === 'file:' || qs.get('preview') === '1';",
                 "const PREVIEW_HOST = false; // go-live copy: no preview behaviour")
    if name == 'signup.html':
        s = must(s, "const PREVIEW = ['rsq-code12.github.io', 'localhost', '127.0.0.1'].includes(location.hostname) || location.protocol === 'file:' || Q.get('preview') === '1';",
                 "const PREVIEW = false; // go-live copy: no preview behaviour")
        s = must(s, '<a class="btn sec" id="backLink" href="index.html" data-i18n="sent.back">Back to the partner page</a>',
                 '<a class="btn sec" id="backLink" href="https://alurei.app" data-i18n="sent.back">Back to alurei.app</a>')
        s = must(s, "$('#backLink').href = l === 'ar' ? 'index.html?lang=ar' : 'index.html';", "$('#backLink').href = 'https://alurei.app';")
        s = must(s, "'sent.back': 'العودة إلى صفحة الشركاء'", "'sent.back': 'العودة إلى ⁦alurei.app⁩'")
    (OUT / name).write_text(s, encoding='utf-8')

(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in PAGES.values()) + '</urlset>\n')
(OUT / 'CNAME.staged').write_text('partners.alurei.app\n')
(OUT / '.nojekyll').write_text('')
(OUT / 'README.md').write_text('# Alurei partner page (go-live copy)\n\nBuilt from rsq-code12/partner-preview with `python3 tools/make-release.py`. Do not edit here.\n\n'
    'Go-live: see GO-LIVE.md. `CNAME.staged` is NOT active; GitHub Pages only uses a file named `CNAME`.\n')
print('release/ built:', sorted(p.name for p in OUT.iterdir()))
