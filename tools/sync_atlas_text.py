"""Keep atlas numbers in the story documents in step with data/global/atlas.json (PC1).

1. technical_note.md: the ranking table between <!-- ATLAS_TABLE_START --> and <!-- ATLAS_TABLE_END -->
   is regenerated from atlas.json (markers are inserted around the existing table on first run).
2. Region-count phrases such as "21 regions (9 reliable, 12 indicative)" and "21-region" are rewritten
   to the current counts in the files listed in FILES.
Usage: python tools/sync_atlas_text.py   (prints what changed; run after every atlas rebuild)
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A = json.loads((ROOT / "data/global/atlas.json").read_text(encoding="utf-8"))
N, NR, NI = A["n_regions"], A["n_reliable"], A["n_indicative"]
CW = A.get("common_window") or (A["regions"][0].get("common_window") if A["regions"] else None) or []
FILES = ["docs/story/technical_note.md", "docs/story/technical_note.html", "docs/story/slides.html", "docs/story/atlas_feature.md",
         "docs/story/press_summary.md", "docs/story/project_page.md", "docs/story/submission_form.md",
         "docs/story/global_atlas.md"]


def fmt(v, d=1):
    return "—" if not isinstance(v, (int, float)) else (f"−{abs(v):.{d}f}" if v < 0 else f"{v:.{d}f}")


def table():
    head = ("| Rank | Region | Period (pairs, days) | Common-window rate (cm/100d) | Full-period rate (cm/100d) "
            "| Peak 1 km LOS (cm) | Valid px | Confidence / QC |\n|---:|---|---|---:|---:|---:|---:|---|")
    rows = []
    for r in A["regions"]:
        per = r.get("period") or ["", ""]
        vf = r.get("valid_fraction")
        tag = r["confidence"] + (" · indicative only" if r.get("indicative_only") else "")
        if r.get("qc_flags"):
            tag += " · QC: " + ", ".join(r["qc_flags"]).replace("_", " ")
        name = f"{r['name']}" + (f", {r['country']}" if r.get("country") else "")
        rows.append(f"| {r['rank']} | **{name}** | `{per[0]} → {per[1]}` ({r.get('n_pairs','—')}, {r.get('days','—')} d) | "
                    f"**{fmt(r.get('rate_cm_per_100d_common'))}** | {fmt(r.get('rate_cm_per_100d'))} | {fmt(r.get('max_cm_los'))} | "
                    f"{'—' if vf is None else f'{vf*100:.1f}%'} | {tag} |")
    note = (f"\n\n*Generated from `data/global/atlas.json` by `tools/sync_atlas_text.py`: {N} regions, {NR} reliable, {NI} indicative; "
            f"ranked by the common window {' → '.join(CW)} (reliable regions first). LOS, provisional NISAR data.*")
    return head + "\n" + "\n".join(rows) + note


def sync_table(text):
    if "<!-- ATLAS_TABLE_START -->" not in text:
        m = re.search(r"\n(\| Rank \| Region[^\n]*\n\|[-:| ]+\|\n(?:\|[^\n]*\n)+)", text)
        if not m:
            return text, False
        text = text[:m.start(1)] + "<!-- ATLAS_TABLE_START -->\n" + m.group(1) + "<!-- ATLAS_TABLE_END -->\n" + text[m.end(1):]
    new = re.sub(r"<!-- ATLAS_TABLE_START -->.*?<!-- ATLAS_TABLE_END -->",
                 lambda _: "<!-- ATLAS_TABLE_START -->\n" + table() + "\n<!-- ATLAS_TABLE_END -->", text, flags=re.S)
    return new, new != text


def sync_counts(text):
    t = re.sub(r"\b\d+ (worldwide )?regions \(\s*`?\d+`? reliable,\s*`?\d+`? indicative\)",
               lambda m: f"{N} {m.group(1) or ''}regions ({NR} reliable, {NI} indicative)", text)
    t = re.sub(r"`\d+` worldwide regions \(`\d+` reliable, `\d+` indicative",
               f"`{N}` worldwide regions (`{NR}` reliable, `{NI}` indicative", t)
    t = re.sub(r"\b\d+-region\b", f"{N}-region", t)
    return t, t != text


def html_rows():
    out = []
    for r in A["regions"]:
        per = r.get("period") or ["", ""]
        vf = r.get("valid_fraction")
        tag = r["confidence"] + (" &middot; indicative only" if r.get("indicative_only") else "")
        if r.get("qc_flags"):
            tag += " &middot; QC: " + ", ".join(r["qc_flags"]).replace("_", " ")
        h = lambda v: fmt(v).replace("−", "&minus;")
        name = r["name"] + (f", {r['country']}" if r.get("country") else "")
        out.append(f"        <tr><td>{r['rank']}</td><td><strong>{name}</strong></td><td>{per[0]} &rarr; {per[1]} ({r.get('n_pairs','—')}, {r.get('days','—')})</td>"
                   f"<td><strong>{h(r.get('rate_cm_per_100d_common'))}</strong></td><td>{h(r.get('rate_cm_per_100d'))}</td><td>{h(r.get('max_cm_los'))}</td>"
                   f"<td>{h(r.get('max_cm_vertical_est'))}</td><td>{'—' if vf is None else f'{vf*100:.1f}%'}</td><td>{tag}</td></tr>")
    return "\n".join(out)


def sync_html(text):
    m = re.search(r"(<h3>5\.1 Global Subsidence Atlas.*?<tbody>\n)(.*?)(\s*</tbody>)", text, flags=re.S)
    if not m:
        return text, False
    new = text[:m.start(2)] + html_rows() + text[m.end(2):]
    new = re.sub(r"ranks \d+ completed regions", f"ranks {N} completed regions", new)
    new = re.sub(r"separates \d+ <code>reliable</code> basins \(ranks 1&ndash;\d+", f"separates {NR} <code>reliable</code> basins (ranks 1&ndash;{NR}", new)
    new = re.sub(r"separates \d+ <code>reliable</code> basins \(ranks 1–\d+", f"separates {NR} <code>reliable</code> basins (ranks 1–{NR}", new)
    return new, new != text


changed = []
for f in FILES:
    p = ROOT / f
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    s2, c1 = sync_table(s) if f.endswith("technical_note.md") else (sync_html(s) if f.endswith("technical_note.html") else (s, False))
    s3, c2 = sync_counts(s2)
    if c1 or c2:
        p.write_text(s3, encoding="utf-8", newline="")
        changed.append(f + (" [table]" if c1 else "") + (" [counts]" if c2 else ""))
print(f"atlas {N}/{NR}/{NI}; updated: {', '.join(changed) or 'nothing'}")
