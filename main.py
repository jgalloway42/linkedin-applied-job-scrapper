"""
LinkedIn Job Scraper - Entry Point

Usage:
    python main.py scrape --start-date 2026-02-17 --end-date 2026-02-23
    python main.py report
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Job Scraper Tools")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("scrape", help="Run the LinkedIn scraper (opens Chrome for manual login)")
    subparsers.add_parser("report", help="Generate job application chart from existing reports")
    args, remaining = parser.parse_known_args()

    if args.command == "scrape":
        subprocess.run([sys.executable, "src/linkedin_scraper.py"] + remaining, check=False)
    elif args.command == "report":
        subprocess.run([sys.executable, "src/generate_job_report.py"], check=False)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
