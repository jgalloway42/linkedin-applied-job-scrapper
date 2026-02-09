"""
Batch Week Processor for LinkedIn Job Applications
Creates weekly reports for unemployment claims

This script helps you generate multiple weekly reports at once.
"""

from datetime import datetime, timedelta
import subprocess
import sys

def get_week_ranges(start_date, num_weeks):
    """
    Generate weekly date ranges
    
    Args:
        start_date: datetime object for the start
        num_weeks: number of weeks to generate
        
    Returns:
        List of tuples (week_start, week_end)
    """
    weeks = []
    current = start_date
    
    for i in range(num_weeks):
        week_start = current
        week_end = current + timedelta(days=6)  # Week is 7 days (0-6)
        weeks.append((week_start, week_end))
        current = week_end + timedelta(days=1)  # Start of next week
        
    return weeks

def run_scraper_for_week(start_date, end_date):
    """
    Run the LinkedIn scraper for a specific week
    
    Args:
        start_date: datetime object
        end_date: datetime object
    """
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    print(f"\n{'='*60}")
    print(f"Processing week: {start_str} to {end_str}")
    print(f"{'='*60}")
    
    cmd = [
        sys.executable,  # Use the same Python interpreter
        "linkedin_scraper.py",
        "--start-date", start_str,
        "--end-date", end_str
    ]
    
    subprocess.run(cmd)

def main():
    print("="*60)
    print("LINKEDIN JOB APPLICATION BATCH PROCESSOR")
    print("="*60)
    print("\nThis will help you generate multiple weekly reports.")
    print("You'll need to log in to LinkedIn only once.\n")
    
    # Get user input
    start_date_str = input("Enter the start date of the first week (YYYY-MM-DD): ").strip()
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD")
        return
    
    num_weeks_str = input("How many weeks do you want to process? ").strip()
    try:
        num_weeks = int(num_weeks_str)
        if num_weeks < 1:
            raise ValueError()
    except ValueError:
        print("Error: Please enter a positive number")
        return
    
    # Generate week ranges
    weeks = get_week_ranges(start_date, num_weeks)
    
    print(f"\n{'='*60}")
    print("WEEK RANGES TO PROCESS:")
    print(f"{'='*60}")
    for i, (start, end) in enumerate(weeks, 1):
        print(f"Week {i}: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
        print(f"  → Output: Week_Ending_{end.strftime('%Y_%m_%d')}.txt")
    
    print(f"\n{'='*60}")
    confirm = input("Process these weeks? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    # Process each week
    print(f"\n{'='*60}")
    print("STARTING BATCH PROCESSING")
    print(f"{'='*60}")
    print("\nNote: You only need to log in once. The browser will stay open.")
    print("Press Ctrl+C at any time to stop.\n")
    
    for i, (start, end) in enumerate(weeks, 1):
        print(f"\n\n### PROCESSING WEEK {i} of {num_weeks} ###")
        run_scraper_for_week(start, end)
    
    print(f"\n\n{'='*60}")
    print("BATCH PROCESSING COMPLETE!")
    print(f"{'='*60}")
    print(f"\nGenerated {num_weeks} weekly reports.")
    print("Check your current directory for the output files.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBatch processing interrupted by user.")
        sys.exit(0)
