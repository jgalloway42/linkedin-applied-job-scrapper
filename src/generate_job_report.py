"""
LinkedIn Job Application Report Generator
Reads all Week_Ending_*.txt files from the reports directory and generates a cumulative bar chart.

Usage:
    conda activate LISCRAPE
    python generate_job_report.py

Requirements:
    - Conda environment: LISCRAPE
    - matplotlib package
"""

import os
import sys
import glob
from datetime import datetime
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def find_report_files(reports_dir):
    """Find all Week_Ending_*.txt files in the reports directory"""
    pattern = os.path.join(reports_dir, "Week_Ending_*.txt")
    files = glob.glob(pattern)
    return sorted(files)


def extract_week_ending_date(filename):
    """
    Extract the week ending date from filename

    Args:
        filename: Path like "reports/Week_Ending_2026_01_31.txt"

    Returns:
        datetime object representing the week ending date
    """
    basename = os.path.basename(filename)
    # Extract date pattern: Week_Ending_YYYY_MM_DD.txt
    match = re.search(r'Week_Ending_(\d{4})_(\d{2})_(\d{2})\.txt', basename)
    if match:
        year, month, day = match.groups()
        return datetime(int(year), int(month), int(day))
    return None


def count_jobs_in_file(filepath):
    """
    Count the number of job applications in a report file

    Args:
        filepath: Path to the report file

    Returns:
        int: Number of jobs (lines) in the file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Count non-empty lines
            return len([line for line in lines if line.strip()])
    except Exception as e:
        print(f"Error reading {filepath}: {str(e)}")
        return 0


def generate_cumulative_chart(reports_dir, output_dir):
    """
    Generate a cumulative bar chart of job applications by week

    Args:
        reports_dir: Directory containing the report files
        output_dir: Directory to save the chart
    """
    # Find all report files
    report_files = find_report_files(reports_dir)

    if not report_files:
        print(f"No Week_Ending_*.txt files found in {reports_dir}")
        return

    print(f"\nFound {len(report_files)} report file(s):")

    # Collect data from all files
    data = []
    for filepath in report_files:
        week_ending = extract_week_ending_date(filepath)
        if week_ending:
            job_count = count_jobs_in_file(filepath)
            data.append({
                'week_ending': week_ending,
                'job_count': job_count,
                'filename': os.path.basename(filepath)
            })
            print(f"  - {os.path.basename(filepath)}: {job_count} jobs")

    if not data:
        print("No valid data to plot")
        return

    # Sort by date
    data.sort(key=lambda x: x['week_ending'])

    # Extract data for plotting
    weeks = [d['week_ending'] for d in data]
    counts = [d['job_count'] for d in data]

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create bars
    bars = ax.bar(weeks, counts, width=5, color='#0077B5', edgecolor='black', linewidth=1.2)

    # Customize the chart
    ax.set_xlabel('Week Ending', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Job Applications', fontsize=12, fontweight='bold')
    ax.set_title('LinkedIn Job Applications by Week', fontsize=14, fontweight='bold', pad=20)

    # Format x-axis dates - place ticks exactly on the week-ending dates from filenames
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xticks(weeks)
    plt.xticks(rotation=45, ha='right')

    # Add value labels on top of bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)

    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')
    output_filename = f"job_applications_summary_{timestamp}.png"
    output_path = os.path.join(output_dir, output_filename)

    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Chart saved to: {output_path}")

    # Display summary statistics
    total_jobs = sum(counts)
    avg_jobs = total_jobs / len(counts) if counts else 0
    print(f"\n{'='*60}")
    print(f"SUMMARY STATISTICS")
    print(f"{'='*60}")
    print(f"Total weeks tracked: {len(weeks)}")
    print(f"Total job applications: {total_jobs}")
    print(f"Average per week: {avg_jobs:.1f}")
    if counts:
        print(f"Highest week: {max(counts)} applications")
        print(f"Lowest week: {min(counts)} applications")
    print(f"{'='*60}")

    # Optionally display the chart
    # plt.show()  # Uncomment if you want to display the chart interactively

    plt.close()


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
        print(f"✓ Running in conda environment: {conda_env}")


def main():
    """Main execution flow"""
    # Get project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Define directories
    reports_dir = os.path.join(project_root, "reports")
    figures_dir = os.path.join(reports_dir, "figures")

    print("\n" + "="*60)
    print("LinkedIn Job Application Report Generator")
    print("="*60)

    # Check conda environment
    check_conda_environment()

    print(f"Reports directory: {reports_dir}")
    print(f"Output directory: {figures_dir}")

    # Check if reports directory exists
    if not os.path.exists(reports_dir):
        print(f"\n✗ Reports directory not found: {reports_dir}")
        print("  Please run the LinkedIn scraper first to generate reports.")
        return

    # Generate the chart
    generate_cumulative_chart(reports_dir, figures_dir)

    print("\n" + "="*60)
    print("REPORT GENERATION COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
