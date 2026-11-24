"""Smoke test: build an EPUB from two fixture articles. No network, no Calibre."""
import importlib.util
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_dry_build_makes_epub(tmp_path):
    shutil.copytree(ROOT / "fixtures" / "articles", tmp_path / "articles")
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "kobo-digest-build.py"), "--dry-build", str(tmp_path)],
        capture_output=True, text=True, cwd=tmp_path,
        env={"PATH": "/usr/bin:/bin", "HOME": str(tmp_path), "KOBO_PAPER_CONFIG": str(tmp_path / "none.json")},
    )
    assert r.returncode == 0, r.stdout + r.stderr
    epub = tmp_path / "read-later.epub"
    assert epub.exists()
    with zipfile.ZipFile(epub) as z:
        names = z.namelist()
        assert "mimetype" in names
        assert "EPUB/art_0.xhtml" in names and "EPUB/art_1.xhtml" in names
        assert "EPUB/frontpage.xhtml" in names
        body = z.read("EPUB/art_0.xhtml").decode()
    assert "Example Article" in body


def test_queue_extracts_kobo_lines():
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("kq", ROOT / "scripts" / "kobo-queue.py")
    kq = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kq)
    assert kq.extract_urls("hi\nkobo: https://example.com/x\nkobo: <https://example.org/y>\nnope") == [
        "https://example.com/x", "https://example.org/y"]


def test_xteink_is_default_and_kobo_gating():
    import json
    sys.path.insert(0, str(ROOT / "scripts"))
    import kobo_config
    assert kobo_config.DEFAULTS["device"] == "xteink"
    spec = importlib.util.spec_from_file_location("ki", ROOT / "scripts" / "kobo-interests.py")
    ki = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ki)
    try:
        ki.kobo_reading({"device": "xteink"})
    except RuntimeError as e:
        assert "not kobo" in str(e)
    else:
        raise AssertionError("expected RuntimeError")
