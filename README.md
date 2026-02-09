# LinkedIn Job Application Scraper

A Python script to extract your LinkedIn job applications and save them in a structured format for unemployment records with automatic date range filtering and weekly file naming.

## ⚠️ Important Disclaimers

1. **LinkedIn Terms of Service**: Automated scraping may violate LinkedIn's ToS. Use this tool responsibly and only for your personal records.
2. **For Personal Use Only**: This tool is designed to help you track your own job applications.
3. **No Guarantees**: LinkedIn frequently updates their website structure, which may break this scraper.

## Features

✅ **Date Range Filtering**: Extract only applications within a specific date range  
✅ **Automatic File Naming**: Generates files as `Week_Ending_YYYY_MM_DD.txt`  
✅ **Batch Processing**: Generate multiple weekly reports in one session  
✅ **Zero-Padded Dates**: Files sort correctly (e.g., `Week_Ending_2026_01_31.txt`)  
✅ **Manual Login**: You stay in control of your credentials  

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- ChromeDriver (will be installed automatically via webdriver-manager)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Chrome is installed:**
   - The script uses Chrome WebDriver
   - Make sure Google Chrome is installed on your system

## Usage

### Basic Usage - Single Week

**With specific date range:**
```bash
python linkedin_scraper.py --start-date 2026-01-25 --end-date 2026-01-31
```

**End date defaults to today:**
```bash
python linkedin_scraper.py --start-date 2026-01-25
```

**No arguments (defaults to last 7 days):**
```bash
python linkedin_scraper.py
```

### Batch Processing - Multiple Weeks

For generating multiple weekly reports for unemployment claims:

```bash
python batch_weekly_reports.py
```

This interactive script will:
1. Ask for the start date of your first week
2. Ask how many weeks to process
3. Show you all the week ranges it will create
4. Process them all in one browser session (you only log in once!)

**Example workflow:**
```
Enter the start date of the first week (YYYY-MM-DD): 2026-01-01
How many weeks do you want to process? 4

Week 1: 2026-01-01 to 2026-01-07 → Week_Ending_2026_01_07.txt
Week 2: 2026-01-08 to 2026-01-14 → Week_Ending_2026_01_14.txt
Week 3: 2026-01-15 to 2026-01-21 → Week_Ending_2026_01_21.txt
Week 4: 2026-01-22 to 2026-01-28 → Week_Ending_2026_01_28.txt
```

### How It Works

1. **Login Once:**
   - A Chrome window opens
   - Log in to LinkedIn manually when prompted
   - The script continues automatically after login

2. **Automatic Extraction:**
   - Scrolls through all your applied jobs
   - Filters applications by date range
   - Shows which jobs match your criteria

3. **File Generation:**
   - Creates files named `Week_Ending_YYYY_MM_DD.txt`
   - Uses the END date of the range for the filename
   - Files are sorted chronologically when listed

4. **Output Format:**
   ```
   2026-01-28, applied to Braze for Senior Forward-Deployed Data Scientist, AI Deployment
   2026-01-28, applied to The Voleon Group for Data Scientist, Technical Lead (Remote-USA)
   ```

## Examples

### Example 1: Last Week's Applications
```bash
python linkedin_scraper.py --start-date 2026-01-25 --end-date 2026-01-31
```
Output: `Week_Ending_2026_01_31.txt`

### Example 2: Specific Week Ending Today
```bash
python linkedin_scraper.py --start-date 2026-02-03
```
Output: `Week_Ending_2026_02_09.txt` (assuming today is Feb 9)

### Example 3: Generate 4 Weeks of Reports
```bash
python batch_weekly_reports.py
# Enter start date: 2026-01-01
# Enter number of weeks: 4
```
Outputs:
- `Week_Ending_2026_01_07.txt`
- `Week_Ending_2026_01_14.txt`
- `Week_Ending_2026_01_21.txt`
- `Week_Ending_2026_01_28.txt`

## File Naming Convention

The script uses **zero-padded dates** for proper sorting:

✅ **Good** (sorts correctly):
```
Week_Ending_2026_01_07.txt
Week_Ending_2026_01_14.txt
Week_Ending_2026_01_21.txt
Week_Ending_2026_02_04.txt
```

❌ **Bad** (doesn't sort correctly):
```
Week_Ending_2026_1_7.txt
Week_Ending_2026_1_14.txt
Week_Ending_2026_1_21.txt
Week_Ending_2026_2_4.txt
```

## Customization

### Adjust Scroll Behavior

If you have many applications, edit `linkedin_scraper.py` and increase `max_attempts`:

```python
max_attempts = 50  # Default is 30, increase if needed
```

## Troubleshooting

### No Jobs Found in Date Range

If the script says "No jobs found in date range":

1. **Check your date range:** Verify you applied to jobs during that period
2. **LinkedIn date format:** LinkedIn shows relative dates ("2 days ago") which are approximations
3. **Expand the range:** Try a wider date range to see if the parsing is correct
4. **Check console output:** The script shows which jobs were filtered out and why

### Date Parsing Issues

The script converts LinkedIn's relative dates ("2 weeks ago") to actual dates. If dates seem wrong:

1. Check the console output - it shows the raw date text from LinkedIn
2. Dates are approximate for anything older than "yesterday"
3. For precise records, cross-reference with your LinkedIn notifications/emails

### "Could not find job cards" Error

LinkedIn's HTML structure may have changed:

1. The script will attempt alternative selectors automatically
2. Check console output for suggested selectors
3. Open an issue with the error message so the script can be updated

### Browser Issues

**ChromeDriver version mismatch:**
```bash
pip install --upgrade webdriver-manager selenium
```

**Login timeout:**
- You have 5 minutes (300 seconds) to log in
- If you need more time, edit the timeout in `login()` method

**Browser doesn't close:**
- Press Ctrl+C to force quit
- Or manually close the browser window

## Quick Reference

### Command Options

| Command | Description |
|---------|-------------|
| `python linkedin_scraper.py` | Last 7 days (default) |
| `--start-date YYYY-MM-DD` | Set start date |
| `--end-date YYYY-MM-DD` | Set end date (defaults to today) |
| `python batch_weekly_reports.py` | Interactive batch processing |

### File Naming

- Pattern: `Week_Ending_YYYY_MM_DD.txt`
- Uses the **end date** of the range
- Zero-padded for correct sorting
- Example: `Week_Ending_2026_01_31.txt`

### Date Format

- Input: `YYYY-MM-DD` (e.g., 2026-01-25)
- Output in file: `YYYY-MM-DD, applied to ...`

## Tips for Unemployment Claims

1. **Weekly Reports:** Use the batch processor to generate one file per week
2. **Consistent Naming:** The zero-padded format ensures files sort chronologically
3. **Verification:** Cross-check with LinkedIn emails for precise application dates
4. **Keep Records:** Save these files as proof of job search activity
5. **Regular Updates:** Run weekly to maintain current records

## Privacy & Security

- Your credentials are NOT stored by this script
- You log in manually through the actual LinkedIn website
- The script only reads publicly visible (to you) job application data
- No data is sent anywhere except saved locally to your text file
- Files are created in the same directory where you run the script

## Advanced Usage

### Programmatic Usage

You can also import and use the scraper in your own Python scripts:

```python
from linkedin_scraper import LinkedInJobScraper

# Create scraper with date range
scraper = LinkedInJobScraper(
    start_date="2026-01-25",
    end_date="2026-01-31"
)

# Run the scraper
scraper.run()

# Output will be: Week_Ending_2026_01_31.txt
```

### Custom Date Ranges

For non-weekly ranges (e.g., monthly unemployment claims):

```bash
# January 2026
python linkedin_scraper.py --start-date 2026-01-01 --end-date 2026-01-31

# Output: Week_Ending_2026_01_31.txt (despite being a month, not a week)
```

## Privacy & Security

- Your credentials are NOT stored by this script
- You log in manually through the actual LinkedIn website
- The script only reads publicly visible (to you) job application data
- No data is sent anywhere except saved locally to your text file

## Support

If LinkedIn changes their page structure:
1. Check the console output for specific error messages
2. Inspect the page elements manually
3. Update the CSS selectors in the script accordingly

## License

This script is provided as-is for personal use. Use responsibly and in accordance with LinkedIn's Terms of Service.
