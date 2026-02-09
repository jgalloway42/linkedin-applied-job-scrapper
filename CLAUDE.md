# Claude Code Project Guide

## Project Overview
LinkedIn Job Application Scraper - A tool to extract and track job applications from LinkedIn for unemployment records and personal tracking.

## Development Environment

### Conda Environment: LISCRAPE
**IMPORTANT:** All scripts in this project must be run using the `LISCRAPE` conda environment.

```bash
# Activate the environment before running any scripts
conda activate LISCRAPE
```

Both main scripts include automatic environment checking and will warn if not running in LISCRAPE.

## Project Structure

```
linkedin-applied-job-scrapper/
├── src/
│   └── data_prep/
│       ├── linkedin_scraper.py       # Main scraper script
│       └── generate_job_report.py    # Report generation script
├── reports/                          # Output directory (auto-created)
│   ├── Week_Ending_YYYY_MM_DD.txt   # Scraped job data
│   └── figures/                      # Generated charts (auto-created)
│       └── job_applications_summary_*.png
├── README.md                         # User documentation
└── CLAUDE.md                         # This file (developer guide)
```

## Key Scripts

### 1. linkedin_scraper.py
**Purpose:** Scrapes LinkedIn job applications within a date range

**Usage:**
```bash
conda activate LISCRAPE
python src/data_prep/linkedin_scraper.py --start-date 2026-01-25 --end-date 2026-01-31
```

**Key Features:**
- Date range filtering
- Smart pagination (stops when reaching old jobs)
- Manual login (keeps credentials secure)
- Outputs to `reports/Week_Ending_YYYY_MM_DD.txt`
- Auto-creates reports directory

**Dependencies:**
- selenium
- Chrome WebDriver

### 2. generate_job_report.py
**Purpose:** Generates cumulative bar chart from all week-ending reports

**Usage:**
```bash
conda activate LISCRAPE
python src/data_prep/generate_job_report.py
```

**Key Features:**
- Reads all `Week_Ending_*.txt` files from reports/
- Creates single cumulative bar chart
- Saves to `reports/figures/job_applications_summary_TIMESTAMP.png`
- Shows summary statistics
- Auto-creates figures directory

**Dependencies:**
- matplotlib

## Output Formats

### Report Text Files
Location: `reports/Week_Ending_YYYY_MM_DD.txt`

Format:
```
2026-01-28, applied to Company Name for Job Title
2026-01-28, applied to Another Company for Another Job Title
```

### Chart Images
Location: `reports/figures/job_applications_summary_YYYY_MM_DD_HHMMSS.png`

- High-resolution (300 DPI)
- LinkedIn blue color scheme (#0077B5)
- Shows job count per week
- Includes summary statistics

## Development Notes

### File Naming Convention
- All date-based files use zero-padded format: `YYYY_MM_DD`
- This ensures proper chronological sorting
- Week ending date is used for report filenames

### Date Parsing
The scraper handles LinkedIn's relative date formats:
- "3h ago", "1d ago", "2w ago" (abbreviated)
- "3 hours ago", "1 day ago" (full words)
- "today", "yesterday", "just now"

### Environment Checking
Both scripts automatically check for the LISCRAPE conda environment and warn if not active. This prevents dependency issues.

### Auto-Directory Creation
- `reports/` directory is created by linkedin_scraper.py
- `reports/figures/` directory is created by generate_job_report.py
- No manual setup required

## Common Workflows

### Weekly Job Tracking
```bash
conda activate LISCRAPE

# Scrape this week's applications
python src/data_prep/linkedin_scraper.py --start-date 2026-02-03 --end-date 2026-02-09

# Generate updated chart
python src/data_prep/generate_job_report.py
```

### Backfilling Historical Data
```bash
conda activate LISCRAPE

# Scrape week by week
python src/data_prep/linkedin_scraper.py --start-date 2026-01-01 --end-date 2026-01-07
python src/data_prep/linkedin_scraper.py --start-date 2026-01-08 --end-date 2026-01-14
# ... etc

# Generate comprehensive chart
python src/data_prep/generate_job_report.py
```

## Git Status
- Git repository is initialized
- Main branch: `main`
- Recent changes include:
  - Output directory standardization to `reports/`
  - Conda environment integration
  - Report generation functionality

## Important Reminders

1. **Always activate LISCRAPE** before running scripts
2. **Reports directory** is in project root (auto-created)
3. **Figures directory** is in reports/ (auto-created)
4. **Date formats** use underscores in filenames, hyphens in data
5. **Manual login required** for LinkedIn scraper (security by design)
6. **Chart timestamps** ensure no overwrites of generated reports

## Future Enhancements (Potential)
- Email notifications when scraping completes
- Database storage instead of text files
- Web dashboard for visualization
- Automated weekly scheduling
- Multiple profile support
- Export to PDF format
