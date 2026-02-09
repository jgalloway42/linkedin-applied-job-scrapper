"""
LinkedIn Job Application Scraper with Date Range Filtering
Extracts jobs you've applied to from LinkedIn and saves them with proper naming convention.

Usage:
    python linkedin_scraper.py --start-date 2026-01-25 --end-date 2026-01-31
    python linkedin_scraper.py --start-date 2026-01-25  # End date defaults to today
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
    def __init__(self, start_date=None, end_date=None):
        """
        Initialize scraper with date range
        
        Args:
            start_date: datetime object or string (YYYY-MM-DD) for start of range
            end_date: datetime object or string (YYYY-MM-DD) for end of range
        """
        self.driver = None
        
        # Parse dates
        if isinstance(start_date, str):
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        elif isinstance(start_date, datetime):
            self.start_date = start_date
        else:
            self.start_date = datetime.now() - timedelta(days=7)  # Default to last week
            
        if isinstance(end_date, str):
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        elif isinstance(end_date, datetime):
            self.end_date = end_date
        else:
            self.end_date = datetime.now()  # Default to today
            
        # Generate output filename using the end date (latest day of range)
        self.output_file = f"Week_Ending_{self.end_date.strftime('%Y_%m_%d')}.txt"
        
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
        """Scroll down to load all job cards (LinkedIn uses infinite scroll)"""
        print("\nLoading all jobs (this may take a moment)...")
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 30  # Increased for larger application histories
        
        while scroll_attempts < max_attempts:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                # No new content loaded, try one more time to be sure
                time.sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                
            last_height = new_height
            scroll_attempts += 1
            print(f"  Scroll attempt {scroll_attempts}...")
            
        print(f"✓ Finished loading (scrolled {scroll_attempts} times)")
        
    def parse_linkedin_date(self, date_text):
        """
        Parse LinkedIn's relative date format and return datetime object
        
        Args:
            date_text: String like "Applied 2 weeks ago" or "Applied yesterday"
            
        Returns:
            datetime object
        """
        if not date_text:
            return datetime.now()
            
        date_text = date_text.lower()
        
        # Handle "yesterday", "today"
        if "yesterday" in date_text:
            return datetime.now() - timedelta(days=1)
        if "today" in date_text or "just now" in date_text:
            return datetime.now()
            
        # Extract number and unit (hours, days, weeks, months)
        match = re.search(r'(\d+)\s+(hour|day|week|month)', date_text)
        
        if match:
            number = int(match.group(1))
            unit = match.group(2)
            
            if unit == 'hour':
                return datetime.now() - timedelta(hours=number)
            elif unit == 'day':
                return datetime.now() - timedelta(days=number)
            elif unit == 'week':
                return datetime.now() - timedelta(weeks=number)
            elif unit == 'month':
                return datetime.now() - timedelta(days=number*30)  # Approximate
        
        # Default to now if we can't parse
        return datetime.now()
        
    def is_date_in_range(self, date):
        """Check if a date falls within the specified range"""
        # Set time to start of day for comparison
        date_only = date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_only = self.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_only = self.end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        return start_only <= date_only <= end_only
        
    def extract_jobs(self):
        """Extract job application data from the page"""
        print("\nExtracting job data...")
        all_jobs = []
        filtered_jobs = []
        
        try:
            # Wait for job cards to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.reusable-search__result-container"))
            )
            
            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
            print(f"Found {len(job_cards)} total job applications")
            
            for idx, card in enumerate(job_cards, 1):
                try:
                    # Extract job title
                    title_element = card.find_element(By.CSS_SELECTOR, "span.entity-result__title-text a span[aria-hidden='true']")
                    job_title = title_element.text.strip()
                    
                    # Extract company name
                    company_element = card.find_element(By.CSS_SELECTOR, "span.entity-result__primary-subtitle")
                    company_name = company_element.text.strip()
                    
                    # Extract application date metadata
                    date_text = None
                    try:
                        metadata = card.find_elements(By.CSS_SELECTOR, "div.entity-result__metadata span")
                        for meta in metadata:
                            text = meta.text.strip()
                            if "Applied" in text or "ago" in text or "yesterday" in text.lower() or "today" in text.lower():
                                date_text = text
                                break
                    except:
                        pass
                    
                    # Parse the date
                    application_datetime = self.parse_linkedin_date(date_text)
                    
                    # Store all jobs
                    job_data = {
                        'date': application_datetime,
                        'date_str': application_datetime.strftime("%Y-%m-%d"),
                        'company': company_name,
                        'title': job_title,
                        'raw_date_text': date_text
                    }
                    all_jobs.append(job_data)
                    
                    # Filter by date range
                    if self.is_date_in_range(application_datetime):
                        filtered_jobs.append(job_data)
                        print(f"  ✓ {job_data['date_str']} - {company_name} - {job_title}")
                    else:
                        print(f"  ✗ {job_data['date_str']} - {company_name} - {job_title} (outside range)")
                    
                except Exception as e:
                    print(f"  Warning: Could not extract data from card {idx}: {str(e)}")
                    continue
                    
        except TimeoutException:
            print("✗ Could not find job cards. The page structure may have changed.")
            print("\nTrying alternative selectors...")
            self._try_alternative_selectors()
            
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
                    print(f"  Please update the code to use this selector")
                    # Print first element's HTML for inspection
                    if elements:
                        print(f"\n  First element classes: {elements[0].get_attribute('class')}")
            except Exception as e:
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
            self.scroll_to_load_all_jobs()
            jobs = self.extract_jobs()
            self.save_to_file(jobs)
            
        except KeyboardInterrupt:
            print("\n\n✗ Scraping interrupted by user.")
            
        except Exception as e:
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


def main():
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
    
    scraper = LinkedInJobScraper(
        start_date=args.start_date,
        end_date=args.end_date
    )
    scraper.run()


if __name__ == "__main__":
    main()
