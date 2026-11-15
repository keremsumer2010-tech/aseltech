# Final site QA · Cambridge pass

**Date:** 2026-11-15  
**Live site:** https://keremsumer2010-tech.github.io/aseltech/  
**Published revision observed:** baseline deployment before the local Cambridge edits. The updated home and science pages were not yet published during this live review.

## Viewports and pages

Reviewed the live Home, Atlas, Science, Data, FAQ, Present, and Simulator pages at **1440 × 900** and **375 × 812**.

- No horizontal document overflow was measured on any page at either viewport. At 375 px, the header navigation is horizontally scrollable; later links require a horizontal swipe.
- Images with a non-empty source loaded on the pages reviewed. The homepage has an empty-source image element for its hidden lightbox, which is a placeholder and not a visible broken image.
- Page controls and links had accessible names; no unnamed buttons or form controls were found. This pass inspected control labels and targets; it did not activate every control.
- The page content was readable at both widths. The homepage's initial mobile view is dense: its headline and world map occupy most of the first screen, with the evidence section further down.

## Console and defects

- **Present page:** the browser reported `SyntaxError: Identifier 'ROOT' has already been declared` on `present.html`. The duplicate declarations are in that page's scripts and are outside PC7's authorized file list; recorded for the page owner to fix.
- **Other reviewed pages:** no page-specific console error was observed during this pass.
- The live build predates the Cambridge edits to `web/index.html`, `web/science.html`, and `web/css/cambridge.css`. Their final responsive appearance and browser console state still need a post-deploy check.

## Local checks

Before the commit attempt, `python tools/check_site.py` reported **43 pages checked, 0 broken links**. `python -m pytest -q` reported **109 passed, 1 warning** (`PendingDeprecationWarning` from `analysis/cumulative.py`).

The local preview server could not bind to localhost under the current sandbox network restrictions, so the edited pages could not be opened in the browser before deployment.
