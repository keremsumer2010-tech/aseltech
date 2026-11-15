"""Every local link and image on the published site must exist (PC1; see tools/check_site.py)."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("check_site", Path(__file__).resolve().parents[1] / "tools" / "check_site.py")
check_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_site)


def test_no_broken_site_links():
    broken = check_site.check()
    assert not broken, "Broken site links:\n" + "\n".join(broken)
