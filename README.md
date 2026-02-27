[![CI/CD](https://github.com/jgalloway42/linkedin-applied-job-scrapper/actions/workflows/cicd.yml/badge.svg)](https://github.com/jgalloway42/linkedin-applied-job-scrapper/actions/workflows/cicd.yml)

# LinkedIn Applied Job Scraper

Extracts your job applications from LinkedIn and tracks them by week. Generates text reports for unemployment records and a cumulative bar chart for personal tracking.

---

## Setup

**Prerequisites:** [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and Google Chrome installed locally.

```bash
# Create and activate the conda environment
conda create -n LISCRAPE python=3.11
conda activate LISCRAPE

# Clone the repo and install dependencies
git clone https://github.com/<your-username>/linkedin-applied-job-scrapper.git
cd linkedin-applied-job-scrapper
make install
```

---

## Usage

### Scrape job applications

```bash
make scrape ARGS="--start-date 2026-02-17 --end-date 2026-02-23"
```

Chrome will open automatically. Log in to LinkedIn manually — no credentials are stored. The scraper runs once you're logged in and saves results to `reports/Week_Ending_YYYY_MM_DD.txt`.

Optional flags:
```bash
--debug           # Verbose output for troubleshooting
--test-parsing    # Test date parsing logic without opening a browser
```

### Generate the weekly chart

```bash
make report
```

Reads all `Week_Ending_*.txt` files from `reports/` and saves a bar chart to `reports/figures/`.

### Backfill historical data

```bash
make scrape ARGS="--start-date 2026-01-01 --end-date 2026-01-07"
make scrape ARGS="--start-date 2026-01-08 --end-date 2026-01-14"
make report
```

---

## Output

**Report files** — `reports/Week_Ending_YYYY_MM_DD.txt`
```
2026-02-21, applied to Acme Corp for Software Engineer
2026-02-20, applied to Example Inc for Data Analyst
```

**Chart** — `reports/figures/job_applications_summary_YYYY_MM_DD_HHMMSS.png`

Bar chart showing applications per week, LinkedIn blue color scheme, 300 DPI.

> The `reports/` directory is gitignored — output files stay local.

---

## Development

```bash
make lint      # Pylint (warnings and errors)
make test      # pytest with coverage
make format    # Black formatter
make refactor  # format + lint
```

---

## CI/CD

GitHub Actions runs `make install && make lint && make test` on every push and pull request to `main`.

See [`.github/workflows/cicd.yml`](.github/workflows/cicd.yml).
