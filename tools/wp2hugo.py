#!/usr/bin/env python3
"""
Convert a WordPress WXR export into a Hugo content tree.

Usage:  python3 tools/wp2hugo.py path/to/export.xml [site_root]

Produces (relative to site_root, default = parent of tools/):
  content/_index.md
  content/posts/<slug>.md           (published posts; URL preserved via `url:`)
  content/<slug>.md                 (published pages: about, perl, r ...)
  content/categories/<term>/_index.md, content/tags/<term>/_index.md
  tools/uploads.txt                 (every /wp-content/uploads/ file referenced)
Requires: pandoc, lxml, beautifulsoup4, PyYAML
"""
import html, os, re, subprocess, sys, json
from collections import defaultdict
from pathlib import Path
from lxml import etree
from bs4 import BeautifulSoup
import yaml

NS = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
    'dc': 'http://purl.org/dc/elements/1.1/',
}
SITE_RE = re.compile(r'https?://(?:www\.)?polypompholyx\.com', re.I)
UPLOAD_RE = re.compile(r'(?:https?://(?:www\.)?polypompholyx\.com)?/wp-content/uploads/[^\s"\'<>)\]]+', re.I)

def t(el, path):
    r = el.find(path, NS)
    return (r.text or '') if r is not None else ''

def urlize(name):
    """Approximation of Hugo's urlize, used to name taxonomy term folders."""
    s = name.strip().lower()
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'[^\w\-.~]', '', s, flags=re.U)
    return s

# --------------------------------------------------------------------------
# WordPress content -> markdown
# --------------------------------------------------------------------------
BLOCK = (r'p|div|ul|ol|li|table|thead|tbody|tr|td|th|h[1-6]|blockquote|figure|hr|dl|dt|dd|'
         r'pre|form|section|article|aside|style|script|ZZ(?:FIG|PRE)\d+ZZ')
BLOCK_START = re.compile(r'\s*<?/?(?:%s)\b' % BLOCK, re.I)

def autop(text):
    """Small re-implementation of WordPress's wpautop()."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    stash = {}
    def keep(m):
        k = 'ZZPRE%dZZ' % len(stash)
        stash[k] = m.group(0)
        return k
    text = re.sub(r'<(pre|script|style)\b.*?</\1>', keep, text, flags=re.S | re.I)
    # blockquotes: recurse so the paragraphs inside get wrapped too
    def bq(m):
        return '<blockquote%s>\n%s\n</blockquote>' % (m.group(1), autop_inner(m.group(2), stash))
    text = re.sub(r'<blockquote([^>]*)>(.*?)</blockquote>', bq, text, flags=re.S | re.I)
    out = autop_blocks(text)
    for k, v in stash.items():
        out = out.replace(k, v)
    return out

def autop_inner(text, stash):
    return autop_blocks(text.strip())

def autop_blocks(text):
    parts = re.split(r'\n\s*\n', text.strip())
    out = []
    for b in parts:
        b = b.strip('\n')
        if not b.strip():
            continue
        if BLOCK_START.match(b) or b.strip().startswith('<blockquote'):
            out.append(b)
        else:
            out.append('<p>' + b.strip().replace('\n', '<br />\n') + '</p>')
    return '\n\n'.join(out)

def rewrite_urls(s):
    # uploads -> local absolute path; links to old site -> relative
    s = re.sub(r'https?://(?:www\.)?polypompholyx\.com(/wp-content/uploads/)', r'\1', s, flags=re.I)
    s = re.sub(r'(href|src)=(["\'])https?://(?:www\.)?polypompholyx\.com(/[^"\']*)?\2',
               lambda m: '%s=%s%s%s' % (m.group(1), m.group(2), m.group(3) or '/', m.group(2)), s, flags=re.I)
    s = re.sub(r'\]\(https?://(?:www\.)?polypompholyx\.com(/[^)]*)?\)',
               lambda m: '](%s)' % (m.group(1) or '/'), s, flags=re.I)
    return s

def convert_body(raw, figs, maths, lang=''):
    """raw = WP post_content.  Returns (markdown, has_math)."""
    s = raw.replace('\xa0', ' ') if False else raw
    s = rewrite_urls(s)

    # [video mp4="..."] / [videojs mp4="..."] -> <video>
    def video(m):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        src = a.get('mp4') or a.get('src') or ''
        w = ' width="%s"' % a['width'] if a.get('width') else ''
        h = ' height="%s"' % a['height'] if a.get('height') else ''
        k = 'ZZFIG%dZZ' % len(figs)
        figs[k] = '<video controls preload="metadata"%s%s src="%s"></video>' % (w, h, src)
        return '\n\n<p>' + k + '</p>\n\n'
    s = re.sub(r'\[video(?:js)?\s+([^\]]*)\](?:\s*\[/video(?:js)?\])?', video, s, flags=re.I)
    # old WordPress search links -> tag pages (Hugo has no server-side search)
    s = re.sub(r'(href=["\'])/\?s=([A-Za-z0-9_-]+)', r'\1/tag/\2/', s)

    # [latex] -> placeholder
    def latex(m):
        expr = html.unescape(m.group(1)).strip()
        expr = re.sub(r'\\\\(?=[A-Za-z{}|])', r'\\', expr)   # \\bar -> \bar
        k = 'ZZMATH%dZZ' % len(maths)
        maths[k] = '<span class="math">\\(' + html.escape(expr, quote=False) + '\\)</span>'
        return k
    s = re.sub(r'\[latex[\s\u00a0]*[^\]]*\](.*?)\[/latex\]', latex, s, flags=re.S | re.I)
    has_math = bool(maths)

    # [caption] -> <figure>
    def caption(m):
        attrs, inner = m.group(1), m.group(2).strip()
        align = (re.search(r'align="([^"]*)"', attrs) or [None, 'alignnone'])[1]
        width = (re.search(r'width="(\d+)"', attrs) or [None, ''])[1]
        # image block = optional <a> wrapping an <img>, or bare <img>
        im = re.match(r'\s*(<a\b[^>]*>\s*<img\b[^>]*>\s*</a>|<img\b[^>]*>)(.*)$', inner, re.S | re.I)
        if im:
            img, cap = im.group(1), im.group(2).strip()
        else:
            img, cap = '', inner
        img = re.sub(r'<img\b', '<img loading="lazy"', img, count=1, flags=re.I)
        img = re.sub(r'\s(?:width|height)="\d+"', '', img)
        img = re.sub(r'\sclass="[^"]*"', '', img)
        style = ' style="max-width:%spx"' % width if width else ''
        figcap = '<figcaption>%s</figcaption>' % cap.replace('\n', ' ') if cap else ''
        h = '<figure class="wp-caption %s"%s>%s%s</figure>' % (align, style, img.replace('\n', ' '), figcap)
        k = 'ZZFIG%dZZ' % len(figs)
        figs[k] = h
        return '\n\n<p>' + k + '</p>\n\n'
    s = re.sub(r'\[caption([^\]]*)\](.*?)\[/caption\]', caption, s, flags=re.S | re.I)

    # complex tables and <style> blocks can't be expressed in Markdown: keep as raw HTML
    def rawblock(m):
        blk = re.sub(r'\n\s*\n', '\n', m.group(0))      # a blank line would end the HTML block
        k = 'ZZFIG%dZZ' % len(figs)
        figs[k] = blk
        return '\n\n<p>' + k + '</p>\n\n'
    s = re.sub(r'<style\b.*?</style>', rawblock, s, flags=re.S | re.I)
    s = re.sub(r'<table\b(?=[^>]*(?:style=|class=))[^>]*>.*?</table>|<table\b[^>]*>(?=(?:(?!</table>).)*?(?:rowspan|colspan)).*?</table>',
               rawblock, s, flags=re.S | re.I)

    s = s.replace('<!--more-->', '')
    s = autop(s)

    r = subprocess.run(
        ['pandoc', '-f', 'html-native_divs-native_spans', '-t', 'gfm-raw_html+raw_html',
         '--wrap=none', '--shift-heading-level-by=1'],
        input=s, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    md = r.stdout
    for k, v in figs.items():
        md = md.replace(k, '\n\n' + v + '\n\n')
    for k, v in maths.items():
        md = md.replace(k, v)
    md = re.sub(r'(?<=[A-Za-z0-9-])//+(?=["\')\s])', '/', md)   # stray double slashes in internal links
    md = re.sub(r'^``` code\s*$', '```' + lang, md, flags=re.M)
    md = re.sub(r'^``` rinput\s*$', '```r', md, flags=re.M)
    md = re.sub(r'^``` (?:routput|output)\s*$', '```text', md, flags=re.M)
    md = re.sub(r'\n{3,}', '\n\n', md).strip() + '\n'
    return md, has_math

# --------------------------------------------------------------------------
# comments
# --------------------------------------------------------------------------
ALLOWED = {'a', 'em', 'strong', 'i', 'b', 'code', 'pre', 'blockquote', 'br', 'p',
           'ul', 'ol', 'li', 'del', 'sub', 'sup', 'strike', 'cite', 'abbr'}

def clean_comment(raw):
    raw = html.unescape(raw) if '&lt;' in raw and '<' not in raw else raw
    soup = BeautifulSoup(autop(raw), 'html.parser')
    for tag in soup.find_all(True):
        if tag.name not in ALLOWED:
            tag.unwrap()
            continue
        keep = {}
        if tag.name == 'a' and tag.get('href', '').lower().startswith(('http', '/', 'mailto:')):
            keep = {'href': tag['href'], 'rel': 'nofollow ugc'}
        tag.attrs = keep
    return str(soup)

def build_comments(item):
    rows = {}
    for c in item.findall('wp:comment', NS):
        if t(c, 'wp:comment_approved') != '1':
            continue
        cid = int(t(c, 'wp:comment_id'))
        rows[cid] = dict(
            id=cid,
            parent=int(t(c, 'wp:comment_parent') or 0),
            author=t(c, 'wp:comment_author') or 'Anonymous',
            url=t(c, 'wp:comment_author_url'),
            date=t(c, 'wp:comment_date_gmt').replace(' ', 'T') + 'Z',
            kind=t(c, 'wp:comment_type') or 'comment',
            html=clean_comment(t(c, 'wp:comment_content')),
        )
    children = defaultdict(list)
    for r in sorted(rows.values(), key=lambda r: r['date']):
        children[r['parent'] if r['parent'] in rows else 0].append(r)
    ordered = []
    def walk(pid, depth):
        for r in children[pid]:
            r['depth'] = min(depth, 4)
            ordered.append(r)
            walk(r['id'], depth + 1)
    walk(0, 0)
    for r in ordered:
        r.pop('parent', None)
    return ordered

# --------------------------------------------------------------------------
def main():
    export = Path(sys.argv[1])
    root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent
    content = root / 'content'
    tree = etree.parse(str(export), etree.XMLParser(recover=True, huge_tree=True))
    chan = tree.getroot().find('channel')

    # term name lookup (nicename -> display name)
    cat_names = {t(c, 'wp:category_nicename'): t(c, 'wp:cat_name') for c in chan.findall('wp:category', NS)}
    tag_names = {t(c, 'wp:tag_slug'): t(c, 'wp:tag_name') for c in chan.findall('wp:tag', NS)}

    items = chan.findall('item')
    attach = {}
    for it in items:
        if t(it, 'wp:post_type') == 'attachment':
            attach[t(it, 'wp:post_id')] = t(it, 'wp:attachment_url')

    uploads = set(attach.values())
    used_cats, used_tags = {}, {}
    n_posts = n_pages = n_comments = 0
    needs_review = []

    for it in items:
        typ, status = t(it, 'wp:post_type'), t(it, 'wp:status')
        if typ not in ('post', 'page') or status != 'publish':
            continue
        title = html.unescape(t(it, 'title')).strip()
        link = t(it, 'link')
        path = SITE_RE.sub('', link) or '/'
        slug = t(it, 'wp:post_name')
        raw = t(it, 'content:encoded')
        uploads.update(re.sub(r'^/', 'https://www.polypompholyx.com/', u) if u.startswith('/')
                       else u.replace('http://', 'https://') for u in UPLOAD_RE.findall(raw))

        cats, tags = [], []
        for c in it.findall('category'):
            dom, nice, name = c.get('domain'), c.get('nicename'), html.unescape(c.text or '')
            if dom == 'category':
                cats.append(name); used_cats[name] = nice
            elif dom == 'post_tag':
                tags.append(name); used_tags[name] = nice
        lang = 'perl' if ('Perl' in cats or slug == 'perl') else 'r' if ('R' in cats or slug == 'r') else ''

        figs, maths = {}, {}
        md, has_math = convert_body(raw, figs, maths, lang)
        if '<style' in raw or 'class="rotated"' in raw:
            needs_review.append(path)

        meta, old_slugs = {}, []
        for pm in it.findall('wp:postmeta', NS):
            k, v = t(pm, 'wp:meta_key'), t(pm, 'wp:meta_value')
            meta[k] = v
            if k == '_wp_old_slug' and v and v != slug:
                old_slugs.append(v)

        gmt = t(it, 'wp:post_date_gmt')
        fm = {'title': title,
              'date': gmt.replace(' ', 'T') + 'Z',
              'lastmod': t(it, 'wp:post_modified_gmt').replace(' ', 'T') + 'Z',
              'url': path,
              'slug': slug,
              'draft': False,
              'wp_id': int(t(it, 'wp:post_id'))}
        if old_slugs:   # WordPress redirected these; Hugo aliases do the same
            fm['aliases'] = [re.sub(r'[^/]+/$', o + '/', path) for o in old_slugs]
        ex = t(it, 'excerpt:encoded').strip()
        if ex:
            fm['description'] = html.unescape(re.sub('<[^>]+>', '', ex))
        if has_math:
            fm['math'] = True
        if typ == 'post':
            if cats: fm['categories'] = cats
            if tags: fm['tags'] = tags
            thumb = attach.get(meta.get('_thumbnail_id', ''))
            if thumb:
                fm['thumbnail'] = SITE_RE.sub('', thumb)
            out = content / 'posts' / (slug + '.md')
            n_posts += 1
        else:
            fm['wp_page'] = True
            out = content / (slug + '.md')
            n_pages += 1
        comments = build_comments(it)
        if comments:
            fm['wp_comments'] = comments
            n_comments += len(comments)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text('---\n' + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=100000)
                       + '---\n\n' + md, encoding='utf-8')

    # taxonomy term pages (display name + original URL slug)
    for folder, used, names in (('categories', used_cats, cat_names), ('tags', used_tags, tag_names)):
        for name, nice in used.items():
            d = content / folder / urlize(name)
            d.mkdir(parents=True, exist_ok=True)
            (d / '_index.md').write_text(
                '---\n' + yaml.safe_dump({'title': name, 'slug': nice}, allow_unicode=True, sort_keys=False)
                + '---\n', encoding='utf-8')

    # hand-written scaffolding (only created if missing, never overwritten)
    scaffold = {
        content / '_index.md': '---\ntitle: Polypompholyx\n---\n',
        content / 'posts' / '_index.md': '---\ntitle: Posts\n---\n',
        content / 'archives.md': '---\ntitle: Archives\nurl: /archives/\n---\n\n{{< pp-archives >}}\n',
    }
    for f, txt in scaffold.items():
        if not f.exists():
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(txt, encoding='utf-8')

    (root / 'tools').mkdir(exist_ok=True)
    (root / 'tools' / 'uploads.txt').write_text('\n'.join(sorted(uploads)) + '\n', encoding='utf-8')
    print(f'posts={n_posts} pages={n_pages} comments={n_comments} '
          f'categories={len(used_cats)} tags={len(used_tags)} uploads={len(uploads)}')
    if needs_review:
        print('NEEDS MANUAL REVIEW (inline <style>/classes):', needs_review)

if __name__ == '__main__':
    main()
