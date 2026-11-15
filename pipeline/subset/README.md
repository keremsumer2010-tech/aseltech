# Raw NISAR subsets (`*.npz`)

These are the cut-down NISAR L2 GUNW pairs (382 files, about 1.7 GB) that the analysis reads.
They are **not stored in the repository** any more, so the repository ZIP stays small.
The website does not use them.

Three ways to get them back:

1. **Release package:** download `aseltech_pipeline_subsets_npz.zip` from the repository's
   GitHub Releases and unzip it in the repository root (it recreates `pipeline/subset/...`).
2. **From git history:** they were last tracked in commit `243c9b9`:
   `git checkout 243c9b9 -- pipeline/subset`
   (then `git rm -r --cached -q pipeline/subset` so they are not committed again).
3. **Rebuild them** from NASA's archive with the open pipeline:
   `python pipeline/search.py <region>` then `python analysis/fetch_subset.py <region> <track> <frame> <n>`
   (needs a free NASA Earthdata login; see `web/data.html`, "Reproduce our data in 5 steps").

New `*.npz` files in this folder are ignored by git (`.gitignore`).
