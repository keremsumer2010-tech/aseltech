#!/usr/bin/env bash
# Rebuild the published site folder (same layout as .github/workflows/pages.yml) and upload it to
# Cloudflare Pages project "nisar-vision" (https://nisar-vision.pages.dev). PC1.
# Needs a one-time `npx wrangler@3 login`. Usage: bash tools/deploy_cloudflare.sh
set -e
cd "$(dirname "$0")/.."
S="${TMPDIR:-/tmp}/nisar_cf_site"
rm -rf "$S"; mkdir -p "$S/docs" "$S/risk" "$S/validation"
cp -r web/. "$S/"; rm -f "$S/panel.html"
cp -r data "$S/data"; cp -r game "$S/game"
cp -r docs/story "$S/docs/story"; cp -r docs/bulletins "$S/docs/bulletins"; cp -r docs/bulletins "$S/bulletins"
cp risk/*.geojson "$S/risk/"; cp validation/gnss_stations.csv "$S/validation/"
[ -d web3d ] && cp -r web3d "$S/web3d"
python tools/check_site.py
npx.cmd --yes wrangler@3 pages deploy "$S" --project-name nisar-vision --branch main --commit-dirty=true 2>/dev/null \
  || npx --yes wrangler@3 pages deploy "$S" --project-name nisar-vision --branch main --commit-dirty=true
