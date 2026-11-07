# Polypompholyx — Hugo site (migrated from WordPress)

Hugo site using the [Ananke](https://github.com/gohugo-ananke/ananke) theme, restyled to
follow the look of www.polypompholyx.com (banner image over a dark nav bar, grey page,
white post panels with date badges, sidebar with Recent Posts / Categories / Blogroll / Archives).

## Quick start

Requires Hugo **extended ≥ 0.146** and Go (for Hugo Modules), plus Python 3 for the image download.

```bash
# 1. Fetch the Ananke theme (Option A – Hugo Module, as configured in hugo.toml)
hugo mod get -u

# 2. Download the images/files the posts reference (≈810 files, ~ a few hundred MB)
python3 tools/download_uploads.py          # re-runnable; failures listed in tools/uploads_failed.txt

# 3. Preview
hugo server
```

Build for deployment with `hugo --gc --minify` (output in `public/`).

**Option B – git submodule instead of a module:** delete the `[module]` block in `hugo.toml`, then
```bash
git init   # if not already a repo
git submodule add https://github.com/gohugo-ananke/ananke.git themes/ananke
echo "theme = 'ananke'" >> hugo.toml
rm go.mod
```

## What was migrated

| WordPress | Hugo |
|---|---|
| 119 published posts | `content/posts/<slug>.md` |
| 3 pages (About, Perl, R) | `content/about.md`, `perl.md`, `r.md` |
| 124 approved comments | stored in each page's front matter (`wp_comments`), rendered read-only under the article |
| 9 categories, 205 tags | `content/categories/`, `content/tags/` (display names + original slugs) |
| 430 attachments + resized variants | listed in `tools/uploads.txt`, downloaded to `static/wp-content/uploads/` |

* **URLs are preserved.** Every post/page has an explicit `url:` taken from WordPress
  (`/2017/01/modularorigami/`), categories/tags keep `/category/…` and `/tag/…`, and old WordPress
  slugs (`_wp_old_slug`) are kept as `aliases` (redirects).
* Image paths keep `/wp-content/uploads/…`, so no image links changed.
* `[caption]` → `<figure class="wp-caption">`; `[latex]` → KaTeX (loaded only on pages with `math: true`);
  `[video]`/`[videojs]` → `<video>`; code blocks get `perl` / `r` highlighting in those categories.
* The Vegetable Empire table (`/2013/03/vegetable-empire-2013/`) is kept as raw HTML with its inline CSS.
* Drafts, revisions, `custom_css` entries and the Graphene widget configuration are not migrated.

## Differences from the WordPress site

* **Sidebar:** on the home page it sits at the right as before; on single posts/pages Ananke's layout has
  no sidebar column, so the same widgets appear in a row beneath the article.
* **Comments are archived, not live.** To accept new comments, add Disqus/Commento
  (see Ananke docs → Customisation → Comments) or similar.
* **No search** (WordPress `?s=` links were pointed at tag pages). Pagefind is a good static option.
* **RSS** is now `/feed.xml` (WordPress: `/feed/`). Add a redirect on your host if subscribers need it.
* **Archives:** month links in the sidebar go to a single `/archives/` page with `#YYYY-MM` anchors,
  rather than WordPress's `/2020/03/` listing pages.

## Tuning the look

All colours/widths are CSS variables at the top of `assets/ananke/css/custom.css`.
Layout pieces live in `layouts/`:

* `layouts/home.html` – paginated front page + sidebar
* `layouts/_partials/pp-*.html` – post teaser, pager, widgets, comments
* `layouts/_partials/hooks/*.html` – Ananke hook points (banner, footer licence line, comments, KaTeX)

The banner image is set by `params.banner_image` in `hugo.toml`.

## Re-running the conversion

```bash
python3 tools/wp2hugo.py path/to/export.xml
```
Requires `pandoc`, `lxml`, `beautifulsoup4`, `PyYAML`. It overwrites generated content under
`content/posts`, `content/categories`, `content/tags` and the three pages, so make manual edits
after you are happy with the migration (or copy the script's output elsewhere first).
