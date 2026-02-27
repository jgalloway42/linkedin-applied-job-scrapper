"""
LinkedIn Job Application Scraper with Date Range Filtering
Extracts jobs you've applied to from LinkedIn and saves them with proper naming convention.

Usage:
    conda activate LISCRAPE
    python linkedin_scraper.py --start-date 2026-01-25 --end-date 2026-01-31
    python linkedin_scraper.py --start-date 2026-01-25  # End date defaults to today

Requirements:
    - Conda environment: LISCRAPE
    - selenium, Chrome WebDriver
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime, timedelta
import time
import re
import argparse
import os

class LinkedInJobScraper:
    def __init__(self, start_date=None, end_date=None, debug_mode=False):
        """
        Initialize scraper with date range

        Args:
            start_date: datetime object or string (YYYY-MM-DD) for start of range
            end_date: datetime object or string (YYYY-MM-DD) for end of range
            debug_mode: bool, enable detailed debugging output
        """
        self.driver = None
        self.debug_mode = debug_mode
        self._date_log = []
        
        # Parse end_date first so start_date can default relative to it
        if isinstance(end_date, str):
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        elif isinstance(end_date, datetime):
            self.end_date = end_date
        else:
            self.end_date = datetime.now()

        if isinstance(start_date, str):
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        elif isinstance(start_date, datetime):
            self.start_date = start_date
        else:
            self.start_date = self.end_date - timedelta(days=6)  # Default to 7-day window ending on end_date
            
        # Generate output filename using the end date (latest day of range)
        # Create reports directory in project root if it doesn't exist
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reports_dir = os.path.join(project_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)

        filename = f"Week_Ending_{self.end_date.strftime('%Y_%m_%d')}.txt"
        self.output_file = os.path.join(reports_dir, filename)

        print(f"\nDate Range: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        print(f"Output File: {self.output_file}")
        
    def setup_driver(self):
        """Initialize the Chrome WebDriver with options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add user agent to appear more like a real browser
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        
    def login(self):
        """Navigate to LinkedIn and wait for manual login"""
        print("\nOpening LinkedIn...")
        self.driver.get("https://www.linkedin.com/login")
        
        print("\n" + "="*60)
        print("PLEASE LOG IN MANUALLY IN THE BROWSER WINDOW")
        print("="*60)
        print("\nWaiting for you to complete login...")
        print("(The script will continue automatically once you're logged in)")
        
        # Wait for successful login (check for global navigation)
        try:
            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            print("\n✓ Login successful!")
            time.sleep(2)
        except TimeoutException:
            print("\n✗ Login timeout. Please try again.")
            raise
            
    def navigate_to_applied_jobs(self):
        """Navigate to the applied jobs page"""
        print("\nNavigating to applied jobs...")
        self.driver.get("https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED")
        time.sleep(3)
        
    def scroll_to_load_all_jobs(self):
        """Load jobs via scrolling and pagination until we reach jobs older than our date range"""
        print(f"\nLoading jobs until we reach dates before {self.start_date.strftime('%Y-%m-%d')}...")

        page = 1
        max_pages = 100  # Safety limit

        while page <= max_pages:
            # Scroll to bottom of current page to ensure all content is loaded
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Get all current job cards ON THIS PAGE
            try:
                job_cards = self.driver.find_elements(By.XPATH, "//li[.//div[@data-chameleon-result-urn]]")
            except Exception:  # pylint: disable=broad-exception-caught
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "li")

            current_cards = len(job_cards)
            print(f"  Page {page}: Found {current_cards} jobs on current view")

            # Check ALL jobs on current page to see if we should stop
            # Stop if ANY job on this page is older than our start date
            should_stop = False
            checked_jobs = 0
            old_jobs_on_page = 0
            failed_extractions = 0

            for card in job_cards:
                try:
                    date_text, _ = self._extract_date_text(card)
                    if date_text:
                        parsed_date = self.parse_linkedin_date(date_text)
                        if parsed_date:
                            checked_jobs += 1
                            # Check if this job is older than our start date
                            if parsed_date < self.start_date.replace(hour=0, minute=0, second=0, microsecond=0):
                                old_jobs_on_page += 1
                        else:
                            failed_extractions += 1
                    else:
                        failed_extractions += 1
                except Exception:  # pylint: disable=broad-exception-caught
                    failed_extractions += 1
                    continue

            print(f"    Checked {checked_jobs} dates: {old_jobs_on_page} old, {checked_jobs - old_jobs_on_page} in range, {failed_extractions} failed")

            # If we checked at least 5 jobs and more than half are too old, stop
            if checked_jobs >= 5 and old_jobs_on_page > checked_jobs / 2:
                print(f"  Found {old_jobs_on_page}/{checked_jobs} jobs older than {self.start_date.strftime('%Y-%m-%d')} on this page - stopping")
                should_stop = True

            if should_stop:
                break

            # Look for "Next" pagination button
            next_button = None
            next_button_selectors = [
                "button[aria-label='View next page']",
                "button[aria-label='Next']",
                "button.artdeco-pagination__button--next",
                "li.artdeco-pagination__indicator--number.active + li button",
            ]

            for selector in next_button_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            next_button = btn
                            break
                    if next_button:
                        break
                except Exception:  # pylint: disable=broad-exception-caught
                    continue

            # If we found a next button, click it
            if next_button:
                try:
                    # Scroll the button into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                    time.sleep(1)
                    next_button.click()
                    print(f"  Clicking 'Next' to load page {page + 1}...")
                    time.sleep(3)  # Wait for page to load
                    page += 1
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"  Could not click next button: {str(e)}")
                    break
            else:
                # No next button found - we've reached the end
                print("  No more pages available")
                break

        print(f"✓ Finished loading jobs across {page} page(s)")

    def scroll_and_extract_all_jobs(self):
        """Load jobs via pagination and extract from each page until we reach jobs older than our date range"""
        print(f"\nLoading and extracting jobs until we reach dates before {self.start_date.strftime('%Y-%m-%d')}...")

        all_jobs = []
        page = 1
        max_pages = 100  # Safety limit

        while page <= max_pages:
            # Scroll to bottom of current page to ensure all content is loaded
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Get all current job cards ON THIS PAGE
            try:
                job_cards = self.driver.find_elements(By.XPATH, "//li[.//div[@data-chameleon-result-urn]]")
            except Exception:  # pylint: disable=broad-exception-caught
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "li")

            current_cards = len(job_cards)
            print(f"\n  Page {page}: Found {current_cards} jobs")

            # Extract jobs from current page
            page_jobs = []
            old_jobs_on_page = 0
            checked_jobs = 0

            for idx, card in enumerate(job_cards, 1):
                try:
                    # Extract job title
                    job_title = None
                    title_selectors = [
                        "a[href*='/jobs/view/']",
                        "a[data-test-app-aware-link]",
                        "span.entity-result__title-text a",
                    ]
                    for selector in title_selectors:
                        try:
                            title_elements = card.find_elements(By.CSS_SELECTOR, selector)
                            for elem in title_elements:
                                text = elem.text.strip()
                                # Clean up the title: remove newlines and ", Verified" badges
                                text = text.replace('\n', ' ').replace(', Verified', '').strip()
                                if text and len(text) > 3:
                                    job_title = text
                                    break
                            if job_title:
                                break
                        except Exception:  # pylint: disable=broad-exception-caught
                            continue

                    if not job_title:
                        continue

                    # Extract company name
                    company_name = None
                    company_selectors = [
                        "div.t-14.t-black.t-normal",
                        "span.entity-result__primary-subtitle",
                    ]
                    for selector in company_selectors:
                        try:
                            company_elements = card.find_elements(By.CSS_SELECTOR, selector)
                            for elem in company_elements:
                                text = elem.text.strip()
                                if text and len(text) > 1 and "remote" not in text.lower() and "united states" not in text.lower():
                                    company_name = text
                                    break
                            if company_name:
                                break
                        except Exception:  # pylint: disable=broad-exception-caught
                            continue

                    if not company_name:
                        company_name = "Unknown Company"

                    # Extract application date
                    date_text, date_error = self._extract_date_text(card)
                    application_datetime = self.parse_linkedin_date(date_text)

                    # Validate the parsed date
                    if application_datetime and not self._validate_parsed_date(application_datetime, date_text):
                        continue

                    # Log the date parsing
                    self._log_date_parsing(date_text, application_datetime, job_title, company_name)

                    # Count for stopping logic
                    if application_datetime:
                        checked_jobs += 1
                        if application_datetime < self.start_date.replace(hour=0, minute=0, second=0, microsecond=0):
                            old_jobs_on_page += 1

                    # Store job data
                    job_data = {
                        'date': application_datetime,
                        'date_str': application_datetime.strftime("%Y-%m-%d") if application_datetime else 'UNKNOWN',
                        'company': company_name,
                        'title': job_title,
                        'raw_date_text': date_text,
                        'date_error': date_error
                    }
                    page_jobs.append(job_data)

                    # Filter by date range
                    if application_datetime and self.is_date_in_range(application_datetime):
                        print(f"    ✓ {job_data['date_str']} - {company_name} - {job_title}")
                    else:
                        reason = "no date" if not application_datetime else "outside range"
                        print(f"    ✗ {job_data['date_str']} - {company_name} - {job_title} ({reason})")

                except Exception as e:  # pylint: disable=broad-exception-caught
                    if self.debug_mode:
                        print(f"    Warning: Could not extract data from card {idx}: {str(e)}")
                    continue

            # Add page jobs to all jobs
            all_jobs.extend(page_jobs)
            print(f"    Extracted {len(page_jobs)} jobs from page {page}")
            print(f"    Checked {checked_jobs} dates: {old_jobs_on_page} old, {checked_jobs - old_jobs_on_page} in range")

            # Check if we should stop (if most jobs on this page are too old)
            should_stop = False
            if checked_jobs >= 5 and old_jobs_on_page > checked_jobs / 2:
                print(f"    Found {old_jobs_on_page}/{checked_jobs} jobs older than {self.start_date.strftime('%Y-%m-%d')} - stopping")
                should_stop = True

            if should_stop:
                break

            # Look for "Next" pagination button
            next_button = None
            next_button_selectors = [
                "button[aria-label='View next page']",
                "button[aria-label='Next']",
                "button.artdeco-pagination__button--next",
                "li.artdeco-pagination__indicator--number.active + li button",
            ]

            for selector in next_button_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            next_button = btn
                            break
                    if next_button:
                        break
                except Exception:  # pylint: disable=broad-exception-caught
                    continue

            # If we found a next button, click it
            if next_button:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                    time.sleep(1)
                    next_button.click()
                    print(f"    Clicking 'Next' to load page {page + 1}...")
                    time.sleep(3)
                    page += 1
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"    Could not click next button: {str(e)}")
                    break
            else:
                print("    No more pages available")
                break

        # Print summary
        self._print_date_parsing_summary()

        # Filter to only jobs in date range
        filtered_jobs = [job for job in all_jobs if job['date'] and self.is_date_in_range(job['date'])]

        print(f"\n✓ Found {len(all_jobs)} total applications across {page} page(s)")
        print(f"✓ {len(filtered_jobs)} applications in date range")

        return filtered_jobs

    def parse_linkedin_date(self, date_text):
        """
        Parse LinkedIn's relative date format and return datetime object

        Args:
            date_text: String like "Applied 19h ago", "Applied 1d ago", "Applied 2w ago"

        Returns:
            datetime object or None if parsing fails
        """
        if not date_text:
            if self.debug_mode:
                print("  [PARSE WARNING] Date text is None or empty")
            return None

        # Use current time as reference
        now = datetime.now()

        date_text_lower = date_text.lower()

        # Remove common prefixes to normalize
        date_text_lower = re.sub(r'^applied\s+(on\s+company\s+website\s+)?', '', date_text_lower)

        # Handle "just now" / "now"
        if 'just now' in date_text_lower or date_text_lower.strip() == 'now':
            return now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Handle "today"
        if 'today' in date_text_lower:
            return now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Handle "yesterday"
        if 'yesterday' in date_text_lower:
            return now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)

        # Handle relative time patterns
        # Try abbreviated formats first (LinkedIn's current format)
        abbreviated_patterns = [
            (r'(\d+)h\s+ago', 'hours'),
            (r'(\d+)d\s+ago', 'days'),
            (r'(\d+)w\s+ago', 'weeks'),
            (r'(\d+)m\s+ago', 'months'),
            (r'(\d+)y\s+ago', 'years'),
        ]

        for pattern, unit in abbreviated_patterns:
            match = re.search(pattern, date_text_lower)
            if match:
                number = int(match.group(1))

                if unit == 'hours':
                    return now - timedelta(hours=number)
                elif unit == 'days':
                    return now - timedelta(days=number)
                elif unit == 'weeks':
                    return now - timedelta(weeks=number)
                elif unit == 'months':
                    return now - timedelta(days=number * 30)  # Approximate, sufficient for 1-2 week range
                elif unit == 'years':
                    return now - timedelta(days=number * 365)

        # Try full word patterns (legacy support)
        full_word_patterns = [
            (r'(\d+)\s+hours?\s+ago', 'hours'),
            (r'(\d+)\s+days?\s+ago', 'days'),
            (r'(\d+)\s+weeks?\s+ago', 'weeks'),
            (r'(\d+)\s+months?\s+ago', 'months'),
            (r'(\d+)\s+years?\s+ago', 'years'),
        ]

        for pattern, unit in full_word_patterns:
            match = re.search(pattern, date_text_lower)
            if match:
                number = int(match.group(1))

                if unit == 'hours':
                    return now - timedelta(hours=number)
                elif unit == 'days':
                    return now - timedelta(days=number)
                elif unit == 'weeks':
                    return now - timedelta(weeks=number)
                elif unit == 'months':
                    return now - timedelta(days=number * 30)
                elif unit == 'years':
                    return now - timedelta(days=number * 365)

        # If no pattern matched, return None instead of defaulting to now
        if self.debug_mode:
            print(f"  [PARSE ERROR] Could not parse date format: '{date_text}'")
        return None

    def _validate_parsed_date(self, parsed_date, raw_text):
        """
        Validate that a parsed date is reasonable

        Args:
            parsed_date: Parsed datetime object
            raw_text: Original date text for error messages

        Returns:
            bool: True if valid, False otherwise
        """
        if not parsed_date:
            return False

        now = datetime.now()

        # Check if date is in the future (likely a parsing error)
        if parsed_date > now:
            if self.debug_mode:
                print(f"  [VALIDATION ERROR] Date is in future: {parsed_date} from '{raw_text}'")
            return False

        # Check if date is too old (> 2 years, likely an error)
        two_years_ago = now - timedelta(days=730)
        if parsed_date < two_years_ago:
            if self.debug_mode:
                print(f"  [VALIDATION WARNING] Date is > 2 years old: {parsed_date} from '{raw_text}'")
            # Don't reject, but warn

        return True

    def is_date_in_range(self, date):
        """Check if a date falls within the specified range"""
        if not date:
            return False

        # Set time to start of day for comparison
        date_only = date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_only = self.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_only = self.end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        in_range = start_only <= date_only <= end_only

        if self.debug_mode and not in_range:
            print(f"  [FILTER] Date {date_only.strftime('%Y-%m-%d')} outside range "
                  f"[{start_only.strftime('%Y-%m-%d')} to {end_only.strftime('%Y-%m-%d')}]")

        return in_range

    def _log_date_parsing(self, raw_text, parsed_date, job_title, company):
        """
        Log detailed date parsing information for debugging

        Args:
            raw_text: Original date text from LinkedIn
            parsed_date: Parsed datetime object
            job_title: Job title for context
            company: Company name for context
        """
        log_entry = {
            'raw_text': raw_text,
            'parsed_date': parsed_date.strftime('%Y-%m-%d %H:%M:%S') if parsed_date else 'FAILED',
            'job': f"{company} - {job_title}",
            'in_range': self.is_date_in_range(parsed_date) if parsed_date else False
        }

        if self.debug_mode:
            print(f"[DATE PARSE] Raw: '{raw_text}' → {log_entry['parsed_date']} | In range: {log_entry['in_range']}")

        # Store for later analysis
        self._date_log.append(log_entry)

    def _print_date_parsing_summary(self):
        """Print summary of date parsing results"""
        if not hasattr(self, '_date_log') or not self._date_log:
            return

        from collections import Counter

        print("\n" + "="*60)
        print("DATE PARSING SUMMARY")
        print("="*60)

        # Group by raw text patterns
        raw_texts = Counter(log['raw_text'] for log in self._date_log)

        print("\nDate formats encountered:")
        for text, count in raw_texts.most_common():
            print(f"  {count:3d}x: '{text}'")

        # Parse success rate
        failed = sum(1 for log in self._date_log if log['raw_text'] is None)
        total = len(self._date_log)
        print(f"\nExtraction success: {total - failed}/{total} ({100*(total-failed)/total:.1f}%)")

        # Date range filtering
        in_range = sum(1 for log in self._date_log if log['in_range'])
        print(f"Jobs in date range: {in_range}/{total} ({100*in_range/total:.1f}%)")

        # Show failed extractions
        if failed > 0:
            print(f"\nFailed to extract date from {failed} jobs:")
            for log in [l for l in self._date_log if l['raw_text'] is None][:5]:  # Show first 5
                print(f"  - {log['job']}")

    def _extract_date_text(self, card):
        """
        Extract date text from a job card with detailed error reporting

        Args:
            card: Selenium WebElement representing a job card

        Returns:
            tuple: (date_text, error_message)
        """
        # Try multiple selector strategies (updated for 2026 LinkedIn structure)
        strategies = [
            {
                'name': 'LinkedIn 2026 insights container',
                'selector': 'div.entity-result__insights span',
                'filter': lambda text: 'applied' in text.lower() and 'application viewed' not in text.lower()
            },
            {
                'name': 'LinkedIn 2026 simple insight text',
                'selector': 'div.reusable-search-simple-insight__text-container span',
                'filter': lambda text: 'applied' in text.lower() and 'application viewed' not in text.lower()
            },
            {
                'name': 'Primary metadata spans (legacy)',
                'selector': 'div.entity-result__metadata span',
                'filter': lambda text: 'applied' in text.lower() and 'application viewed' not in text.lower()
            },
            {
                'name': 'Alternative metadata (legacy)',
                'selector': 'div.job-card-container__metadata span',
                'filter': lambda text: 'applied' in text.lower() and 'application viewed' not in text.lower()
            },
            {
                'name': 'Time elements',
                'selector': 'time',
                'filter': lambda text: len(text.strip()) > 0
            },
            {
                'name': 'Any span with date-like text (last resort)',
                'selector': 'span',
                'filter': lambda text: re.search(r'\d+[hdwm]\s+ago|applied|yesterday|today|just now', text.lower()) and 'application viewed' not in text.lower()
            }
        ]

        for strategy in strategies:
            try:
                elements = card.find_elements(By.CSS_SELECTOR, strategy['selector'])
                for elem in elements:
                    text = elem.text.strip()
                    if text and strategy['filter'](text):
                        if self.debug_mode:
                            print(f"  [SUCCESS] Found date via '{strategy['name']}': '{text}'")
                        return text, None
            except Exception as e:  # pylint: disable=broad-exception-caught
                if self.debug_mode:
                    print(f"  [FAILED] Strategy '{strategy['name']}': {str(e)}")
                continue

        # No strategy worked
        error_msg = "All date extraction strategies failed"
        if self.debug_mode:
            print(f"  [ERROR] {error_msg}")
            print(f"  Card text preview: {card.text[:200]}")

        return None, error_msg

    def extract_jobs(self):
        """Extract job application data from the page"""
        print("\nExtracting job data...")
        all_jobs = []
        filtered_jobs = []
        
        try:
            # Wait for job cards to load - try multiple selectors
            selectors_to_try = [
                "li.reusable-search__result-container",  # Old selector
                "li div[data-chameleon-result-urn]",      # New selector - uses data attribute
                "div.entity-result__insights",             # Fallback - date container
            ]

            job_cards = []
            for selector in selectors_to_try:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if "data-chameleon-result-urn" in selector:
                        # Find parent <li> elements
                        job_cards = self.driver.find_elements(By.XPATH, "//li[.//div[@data-chameleon-result-urn]]")
                    else:
                        job_cards = self.driver.find_elements(By.CSS_SELECTOR, selector)

                    if len(job_cards) > 0:
                        print(f"Found {len(job_cards)} total job applications using selector: {selector}")
                        break
                except TimeoutException:
                    continue

            if len(job_cards) == 0:
                raise TimeoutException("Could not find job cards with any selector")
            
            for idx, card in enumerate(job_cards, 1):
                try:
                    # Extract job title - try multiple strategies
                    job_title = None
                    title_selectors = [
                        "a[href*='/jobs/view/']",  # Any link to a job posting
                        "a[data-test-app-aware-link]",  # 2026 structure
                        "span.entity-result__title-text a",  # Legacy
                    ]
                    for selector in title_selectors:
                        try:
                            title_elements = card.find_elements(By.CSS_SELECTOR, selector)
                            for elem in title_elements:
                                text = elem.text.strip()
                                # Clean up the title: remove newlines and ", Verified" badges
                                text = text.replace('\n', ' ').replace(', Verified', '').strip()
                                if text and len(text) > 3:  # Skip empty or very short text
                                    job_title = text
                                    break
                            if job_title:
                                break
                        except NoSuchElementException:
                            continue

                    if not job_title:
                        if self.debug_mode:
                            print(f"  [WARNING] Could not extract job title for card {idx}")
                            # Print all links to help debug
                            try:
                                all_links = card.find_elements(By.TAG_NAME, "a")
                                print(f"    Found {len(all_links)} links in card")
                                for link in all_links[:3]:
                                    print(f"      Link text: '{link.text[:50]}'")
                            except Exception:  # pylint: disable=broad-exception-caught
                                pass
                        continue

                    # Extract company name - try multiple selectors
                    company_name = None
                    company_selectors = [
                        "div.t-14.t-black.t-normal",  # 2026 structure - first div with these classes
                        "span.entity-result__primary-subtitle",  # Legacy
                    ]
                    for selector in company_selectors:
                        try:
                            company_elements = card.find_elements(By.CSS_SELECTOR, selector)
                            for elem in company_elements:
                                text = elem.text.strip()
                                # Company name should not contain "Remote", "United States", etc.
                                if text and len(text) > 1 and "remote" not in text.lower() and "united states" not in text.lower():
                                    company_name = text
                                    break
                            if company_name:
                                break
                        except NoSuchElementException:
                            continue

                    if not company_name:
                        company_name = "Unknown Company"

                    # Extract application date with new robust method
                    date_text, date_error = self._extract_date_text(card)

                    if date_error and self.debug_mode:
                        print(f"  [WARNING] {date_error} for card {idx}: {company_name} - {job_title}")

                    # Parse the date with validation
                    application_datetime = self.parse_linkedin_date(date_text)

                    # Validate the parsed date
                    if application_datetime and not self._validate_parsed_date(application_datetime, date_text):
                        if self.debug_mode:
                            print(f"  [VALIDATION FAILED] Skipping job {idx} due to invalid date")
                        continue

                    # Log the date parsing
                    self._log_date_parsing(date_text, application_datetime, job_title, company_name)

                    # Store all jobs (even with failed dates for debugging)
                    job_data = {
                        'date': application_datetime,
                        'date_str': application_datetime.strftime("%Y-%m-%d") if application_datetime else 'UNKNOWN',
                        'company': company_name,
                        'title': job_title,
                        'raw_date_text': date_text,
                        'date_error': date_error
                    }
                    all_jobs.append(job_data)

                    # Filter by date range (only if we have a valid date)
                    if application_datetime and self.is_date_in_range(application_datetime):
                        filtered_jobs.append(job_data)
                        print(f"  ✓ {job_data['date_str']} - {company_name} - {job_title}")
                    else:
                        reason = "no date" if not application_datetime else "outside range"
                        print(f"  ✗ {job_data['date_str']} - {company_name} - {job_title} ({reason})")
                        if self.debug_mode and date_text:
                            print(f"      Raw date: '{date_text}'")

                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"  Warning: Could not extract data from card {idx}: {str(e)}")
                    if self.debug_mode:
                        import traceback
                        traceback.print_exc()
                    continue
                    
        except TimeoutException:
            print("✗ Could not find job cards. The page structure may have changed.")
            print("\nTrying alternative selectors...")
            self._try_alternative_selectors()

        # Print date parsing summary
        self._print_date_parsing_summary()

        print(f"\n✓ Found {len(all_jobs)} total applications")
        print(f"✓ {len(filtered_jobs)} applications in date range")

        return filtered_jobs
        
    def _try_alternative_selectors(self):
        """Try alternative CSS selectors if the main ones don't work"""
        alternative_selectors = [
            "div.jobs-search-results__list-item",
            "li.job-card-container",
            "div.scaffold-layout__list-item",
            "li[class*='reusable-search']",
        ]
        
        for selector in alternative_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(elements) > 0:
                    print(f"\n  Found {len(elements)} elements with selector: {selector}")
                    print("  Please update the code to use this selector")
                    # Print first element's HTML for inspection
                    if elements:
                        print(f"\n  First element classes: {elements[0].get_attribute('class')}")
            except Exception:  # pylint: disable=broad-exception-caught
                continue
        
    def save_to_file(self, jobs):
        """Save jobs to file in the specified format"""
        if not jobs:
            print(f"\n✗ No jobs found in date range {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
            print("  File will not be created.")
            return
            
        print(f"\nSaving {len(jobs)} jobs to {self.output_file}...")
        
        # Sort by date (most recent first)
        jobs.sort(key=lambda x: x['date'], reverse=True)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for job in jobs:
                line = f"{job['date_str']}, applied to {job['company']} for {job['title']}\n"
                f.write(line)
                
        print(f"✓ Successfully saved to {self.output_file}")
        print(f"\nFile location: {os.path.abspath(self.output_file)}")
        
    def run(self):
        """Main execution flow"""
        try:
            self.setup_driver()
            self.login()
            self.navigate_to_applied_jobs()
            jobs = self.scroll_and_extract_all_jobs()
            self.save_to_file(jobs)

        except KeyboardInterrupt:
            print("\n\n✗ Scraping interrupted by user.")

        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"\n✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            
        finally:
            if self.driver:
                print("\nClosing browser...")
                time.sleep(2)
                self.driver.quit()
                
        print("\n" + "="*60)
        print("SCRAPING COMPLETE!")
        print("="*60)


def test_date_parsing():
    """Test date parsing with various LinkedIn date formats"""
    test_cases = [
        # LinkedIn's current abbreviated formats
        "Applied 3h ago",
        "Applied 19h ago",
        "Applied 1d ago",
        "Applied 3d ago",
        "Applied 7d ago",
        "Applied 1w ago",
        "Applied 2w ago",
        "Applied 1m ago",
        "Applied 3m ago",
        # With extra text
        "Applied on Company Website 3d ago",
        "Applied on Company Website 1w ago",
        # Should be ignored (not application dates)
        "Application viewed 3h ago",
        # Special cases
        "Applied yesterday",
        "Applied today",
        "Applied just now",
        # Legacy full-word formats
        "Applied 2 hours ago",
        "Applied 3 days ago",
        "Applied 1 week ago",
        "Applied 2 weeks ago",
    ]

    print("\n" + "="*60)
    print("DATE PARSING TEST")
    print("="*60)
    print(f"Reference date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    scraper = LinkedInJobScraper(debug_mode=False)

    for test_text in test_cases:
        result = scraper.parse_linkedin_date(test_text)
        if result:
            days_ago = (datetime.now() - result).days
            print(f"[OK] '{test_text:45s}' -> {result.strftime('%Y-%m-%d')} ({days_ago} days ago)")
        else:
            print(f"[FAIL] '{test_text:45s}' -> FAILED TO PARSE")

    print("="*60)


def check_conda_environment():
    """Check if running in the correct conda environment"""
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', None)

    if conda_env != 'LISCRAPE':
        print("\n" + "!"*60)
        print("WARNING: Not running in LISCRAPE conda environment")
        print("!"*60)
        print(f"Current environment: {conda_env if conda_env else 'None (base or no conda)'}")
        print("\nPlease activate the LISCRAPE environment:")
        print("  conda activate LISCRAPE")
        print("\nContinuing anyway, but you may encounter missing dependencies...")
        print("!"*60 + "\n")
        input("Press Enter to continue or Ctrl+C to exit...")
    else:
        print(f"✓ Running in conda environment: {conda_env}\n")


def main():
    # Check conda environment first
    check_conda_environment()

    parser = argparse.ArgumentParser(
        description='Scrape LinkedIn job applications within a date range',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --start-date 2026-01-25 --end-date 2026-01-31
  %(prog)s --start-date 2026-01-25  # End date defaults to today
  %(prog)s  # Defaults to last 7 days
        """
    )
    
    parser.add_argument(
        '--start-date',
        type=str,
        help='Start date in YYYY-MM-DD format (default: 7 days ago)'
    )
    
    parser.add_argument(
        '--end-date',
        type=str,
        help='End date in YYYY-MM-DD format (default: today)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode with detailed logging'
    )

    parser.add_argument(
        '--test-parsing',
        action='store_true',
        help='Test date parsing with sample formats'
    )

    args = parser.parse_args()
    
    # Validate dates if provided
    if args.start_date:
        try:
            datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid start date format '{args.start_date}'. Use YYYY-MM-DD")
            return
            
    if args.end_date:
        try:
            datetime.strptime(args.end_date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid end date format '{args.end_date}'. Use YYYY-MM-DD")
            return
    
    # Handle test-parsing mode
    if args.test_parsing:
        test_date_parsing()
        return

    scraper = LinkedInJobScraper(
        start_date=args.start_date,
        end_date=args.end_date,
        debug_mode=args.debug
    )
    scraper.run()


if __name__ == "__main__":
    main()
