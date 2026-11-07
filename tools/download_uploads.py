#!/usr/bin/env python3
"""
Download every file in tools/uploads.txt into static/wp-content/uploads/,
preserving the original paths so no URLs in the content need to change.

Usage:  python3 tools/download_uploads.py [--workers 8]
Safe to re-run: files that already exist are skipped.
"""
import argparse, concurrent.futures as cf, sys, urllib.request, urllib.error
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
LIST = ROOT / 'tools' / 'uploads.txt'
DEST = ROOT / 'static'

def fetch(url):
    rel = unquote(urlparse(url).path.lstrip('/'))          # wp-content/uploads/...
    out = DEST / rel
    if out.exists() and out.stat().st_size:
        return url, 'skip'
    out.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'wp2hugo-migration/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            out.write_bytes(r.read())
        return url, 'ok'
    except urllib.error.HTTPError as e:
        return url, f'HTTP {e.code}'
    except Exception as e:                                   # network hiccup
        return url, f'ERR {e}'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=8)
    a = ap.parse_args()
    urls = [u.strip() for u in LIST.read_text().splitlines() if u.strip()]
    stats, failed = {}, []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for i, (url, res) in enumerate(ex.map(fetch, urls), 1):
            stats[res.split()[0]] = stats.get(res.split()[0], 0) + 1
            if res not in ('ok', 'skip'):
                failed.append((url, res))
            if i % 50 == 0 or i == len(urls):
                print(f'{i}/{len(urls)}  {stats}', flush=True)
    if failed:
        (ROOT / 'tools' / 'uploads_failed.txt').write_text('\n'.join(f'{r}\t{u}' for u, r in failed) + '\n')
        print(f'\n{len(failed)} files failed - see tools/uploads_failed.txt '
              f'(some are resized variants WordPress generated and may simply no longer exist).')
    return 0

if __name__ == '__main__':
    sys.exit(main())
