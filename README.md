[![CI/CD](https://github.com/jgalloway42/linkedin-applied-job-scrapper/actions/workflows/cicd.yml/badge.svg)](https://github.com/jgalloway42/linkedin-applied-job-scrapper/actions/workflows/cicd.yml)
# LinkedIn Job Application Scraper

Extract and track your LinkedIn job applications for unemployment records and personal tracking — with automatic date range filtering, smart pagination, and weekly report generation.

## ⚠️ Disclaimers

1. **LinkedIn Terms of Service**: Automated scraping may violate LinkedIn's ToS. Use responsibly and only for your own personal records.
2. **For Personal Use Only**: This tool reads your own application history — nothing else.
3. **No Guarantees**: LinkedIn frequently updates their site structure, which may break selectors.

---

## Features

- **Date Range Filtering** — extract only applications within a specific window
- **Smart Pagination** — stops automatically when it reaches jobs older than your range
- **Manual Login** — you enter credentials yourself; nothing is stored
- **Weekly Reports** — output as `Week_Ending_YYYY_MM_DD.txt` with zero-padded dates for correct sorting
- **Chart Generation** — cumulative bar chart across all weeks via `make report`
- **CI/CD Ready** — GitHub Actions lint + test on every push; Docker image auto-published to GHCR

---

## Getting Started

Choose one of three options:

### Option 1: GitHub Codespaces (recommended — no local setup)

1. Click **Code → Codespaces → Create codespace on main** on the GitHub repo page
2. Wait for the container to build (~3–5 min first time; Chrome is pre-installed)
3. Open the terminal and run:
   ```bash
   make scrape ARGS="--start-date 2026-02-17 --end-date 2026-02-23"
   ```

Free tier: 60 hours/month on personal GitHub accounts.

### Option 2: Docker (local)

```bash
make build
make scrape ARGS="--start-date 2026-02-17 --end-date 2026-02-23"
make report
```

Requires Docker Desktop and, on Linux/Mac, an X11 display for the Chrome window.

### Option 3: Local Python

**Prerequisites:** Python 3.11+, Google Chrome installed

```bash
make install
make scrape ARGS="--start-date 2026-02-17 --end-date 2026-02-23"
make report
```

---

## Usage

### Scrape Applications

```bash
# Specific date range
make scrape ARGS="--start-date 2026-01-25 --end-date 2026-01-31"

# End date only — start auto-calculated as 7 days prior
make scrape ARGS="--end-date 2026-02-21"

# Start date only — end defaults to today
make scrape ARGS="--start-date 2026-01-25"

# Last 7 days (default)
make scrape
```

### Generate Chart

```bash
make report
```

Reads all `reports/Week_Ending_*.txt` files and saves a bar chart to `reports/figures/`.

### How Scraping Works

1. A Chrome window opens — log in to LinkedIn manually when prompted (5-minute timeout)
2. The scraper pages through your applied jobs, stopping when it reaches jobs older than your start date
3. Matching applications are saved to `reports/Week_Ending_YYYY_MM_DD.txt`

**Output format:**
```
2026-01-28, applied to Braze for Senior Forward-Deployed Data Scientist
2026-01-28, applied to The Voleon Group for Data Scientist, Technical Lead (Remote-USA)
```

---

## All Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install Python dependencies |
| `make lint` | Run pylint on all Python files |
| `make test` | Run pytest with coverage |
| `make format` | Auto-format with Black |
| `make refactor` | format + lint |
| `make build` | Build Docker image locally |
| `make container-lint` | Lint Dockerfile with hadolint |
| `make scrape` | Run scraper (last 7 days) |
| `make scrape ARGS="..."` | Run scraper with date args |
| `make report` | Generate chart from existing reports |
| `make all` | install → lint → test → format → deploy |

---

## File Naming Convention

Zero-padded dates ensure correct chronological sorting:

```
reports/Week_Ending_2026_01_07.txt   ← sorts correctly
reports/Week_Ending_2026_01_14.txt
reports/Week_Ending_2026_01_21.txt
reports/Week_Ending_2026_02_04.txt
```

The **end date** of the scraped range is used for the filename.

---

## Tips for Unemployment Claims

1. Run weekly with Sunday–Saturday ranges to match typical claim periods
2. The zero-padded filenames sort chronologically in any file explorer
3. Cross-check with LinkedIn notification emails for exact application timestamps
4. Keep the `reports/` folder backed up — it is gitignored and local only

---

## Troubleshooting

### No jobs found in date range
- Verify you applied during that period on LinkedIn
- LinkedIn relative dates ("2 weeks ago") are approximations — try widening the range slightly
- Run with `--debug` flag for detailed date parsing output: `make scrape ARGS="--debug"`

### "Could not find job cards" error
LinkedIn's HTML may have changed. The script tries alternative selectors automatically and prints suggestions. Check console output and update CSS selectors in [src/linkedin_scraper.py](src/linkedin_scraper.py) if needed.

### ChromeDriver version mismatch
```bash
pip install --upgrade webdriver-manager selenium
```

### Login timeout
You have 5 minutes (300 seconds). To extend it, edit the timeout value in the `login()` method in [src/linkedin_scraper.py](src/linkedin_scraper.py).

---

## Advanced Usage

### Programmatic import

```python
from src.linkedin_scraper import LinkedInJobScraper

scraper = LinkedInJobScraper(
    start_date="2026-01-25",
    end_date="2026-01-31"
)
scraper.run()
# Output: reports/Week_Ending_2026_01_31.txt
```

### Monthly ranges

```bash
make scrape ARGS="--start-date 2026-01-01 --end-date 2026-01-31"
# Output: reports/Week_Ending_2026_01_31.txt
```

---

## CI/CD

On every push to `main`:
- **CI/CD workflow** — runs `make install`, `make lint`, `make test`
- **Docker Image workflow** — builds and pushes image to `ghcr.io/jgalloway42/linkedin-applied-job-scrapper:latest`

---

## Privacy & Security

- Credentials are **never stored** — you log in manually through LinkedIn's own login page
- The script only reads job application data visible to your own account
- No data is sent anywhere; all output is saved locally in `reports/`
- `reports/` is gitignored — your job search history never touches the repo

---

## License

Provided as-is for personal use. Use responsibly and in accordance with LinkedIn's Terms of Service.
