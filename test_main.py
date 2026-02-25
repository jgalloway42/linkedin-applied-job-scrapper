"""
Smoke tests — verify imports and CLI entry point load without errors.
These run in CI without a browser or LinkedIn session.
"""

import subprocess
import sys


def test_scraper_imports():
    """linkedin_scraper module imports cleanly (no selenium launch)"""
    result = subprocess.run(
        [sys.executable, "-c", "import src.linkedin_scraper"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_report_imports():
    """generate_job_report module imports cleanly"""
    result = subprocess.run(
        [sys.executable, "-c", "import src.generate_job_report"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_main_help():
    """main.py --help exits cleanly"""
    result = subprocess.run(
        [sys.executable, "main.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "scrape" in result.stdout
    assert "report" in result.stdout
