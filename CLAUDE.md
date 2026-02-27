# Claude Code Project Guide

## Project Overview
LinkedIn Job Application Scraper - A tool to extract and track job applications from LinkedIn for unemployment records and personal tracking. Runs locally with conda.

## Project Structure

```
linkedin-applied-job-scrapper/
├── .github/
│   └── workflows/
│       └── cicd.yml             # Lint + test on push/PR
├── src/
│   ├── __init__.py
│   ├── linkedin_scraper.py      # Main scraper script
│   └── generate_job_report.py   # Report generation script
├── reports/                     # Output directory (gitignored, auto-created)
│   ├── Week_Ending_YYYY_MM_DD.txt
│   └── figures/
│       └── job_applications_summary_*.png
├── main.py                      # CLI entry point
├── Makefile                     # Common commands
├── requirements.txt             # Python dependencies
├── test_main.py                 # Smoke tests
├── README.md
└── CLAUDE.md                    # This file
```

## Common Commands (Makefile)

```bash
make install         # Install dependencies
make lint            # Pylint on all Python files
make test            # Run pytest with coverage
make format          # Black formatter
make refactor        # format + lint

# Run the scraper (opens Chrome for manual login)
make scrape ARGS="--start-date 2026-02-17 --end-date 2026-02-23"

# Generate chart from existing report files
make report
```

## Key Scripts

### src/linkedin_scraper.py
**Purpose:** Scrapes LinkedIn job applications within a date range

**Usage:**
```bash
make scrape ARGS="--start-date 2026-01-25 --end-date 2026-01-31"
# or directly:
python main.py scrape --start-date 2026-01-25 --end-date 2026-01-31
```

**Key Features:**
- Manual login (keeps credentials secure — Chrome window opens, you log in)
- Date range filtering with smart pagination
- Outputs to `reports/Week_Ending_YYYY_MM_DD.txt`

**Dependencies:** selenium, webdriver-manager, Chrome

### src/generate_job_report.py
**Purpose:** Generates cumulative bar chart from all week-ending reports

**Usage:**
```bash
make report
# or directly:
python main.py report
```

**Key Features:**
- Reads all `Week_Ending_*.txt` files from reports/
- Saves chart to `reports/figures/job_applications_summary_TIMESTAMP.png`
- High-resolution (300 DPI), LinkedIn blue color scheme

**Dependencies:** matplotlib

## Output Formats

### Report Text Files
Location: `reports/Week_Ending_YYYY_MM_DD.txt`

```
2026-01-28, applied to Company Name for Job Title
2026-01-28, applied to Another Company for Another Job Title
```

### Chart Images
Location: `reports/figures/job_applications_summary_YYYY_MM_DD_HHMMSS.png`

## Development Notes

### Date Parsing
The scraper handles LinkedIn's relative date formats:
- `"3h ago"`, `"1d ago"`, `"2w ago"` (abbreviated)
- `"3 hours ago"`, `"1 day ago"` (full words)
- `"today"`, `"yesterday"`, `"just now"`

### File Naming Convention
All date-based files use zero-padded format (`YYYY_MM_DD`) for correct chronological sorting.

### Auto-Directory Creation
- `reports/` is created by linkedin_scraper.py
- `reports/figures/` is created by generate_job_report.py

## Common Workflows

### Weekly Job Tracking
```bash
make scrape ARGS="--start-date 2026-02-17 --end-date 2026-02-23"
make report
```

### Backfilling Historical Data
```bash
make scrape ARGS="--start-date 2026-01-01 --end-date 2026-01-07"
make scrape ARGS="--start-date 2026-01-08 --end-date 2026-01-14"
make report
```

## GitHub Actions

- **cicd.yml**: Runs `make install && make lint && make test` on every push/PR to main

## Important Reminders

1. **Manual login required** for the scraper (security by design — no credentials stored)
2. **Reports directory** is gitignored — output files stay local
3. **Date formats** use underscores in filenames, hyphens in data content
4. **Chart timestamps** prevent overwriting previously generated reports
