# Notebook Development Guide

Best practices and patterns for effective Jupyter notebook development using this project template.

## Overview

This template provides a structured approach to notebook development with pre-configured setup, organized workflows, and integration with the project's utilities. This guide covers everything from getting started to advanced development patterns.

## Template Notebook Structure

### First Cell: Setup

The template notebook (`notebooks/zz_template_notebook.ipynb`) includes a pre-configured first cell:

```python
%load_ext autoreload
%autoreload 2
import sys
sys.path.append('../src')

# Core data science libraries
from generic.preamble import np, pd, plt, sns
# Data management and paths
from generic.preamble import raw_data, processed_data, models_path
from generic.helpers import create_data_catalog

# Initialize and display data catalog
catalog = create_data_catalog('..')
if not catalog.catalog.empty:
    display(catalog.summary())
else:
    print("No data files found in standard directories")
```

**What this gives you:**
- **Auto-reload** - Changes to source code automatically update
- **Essential libraries** - pandas, numpy, matplotlib, seaborn
- **Path variables** - Direct access to data directories
- **DataCatalog** - Smart file discovery and loading
- **Immediate feedback** - See available data files right away

## Notebook Organization Patterns

### Pattern 1: Exploratory Analysis

**Recommended structure for data exploration:**

```
Cell 1: Setup (template cell)
Cell 2: Load and inspect data
Cell 3: Data quality assessment
Cell 4: Univariate analysis
Cell 5: Bivariate analysis
Cell 6: Key findings summary
```

**Example:**
```python
# Cell 2: Load and inspect
df = catalog.load_file('my_dataset')
print(f"Shape: {df.shape}")
df.head()

# Cell 3: Data quality
print("Missing values:")
print(df.isnull().sum())
print("\nData types:")
print(df.dtypes)

# Cell 4: Univariate analysis
df.describe()
plt.figure(figsize=(12, 8))
df.hist(bins=20)
plt.tight_layout()

# Cell 5: Relationships
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

# Cell 6: Summary
print("Key findings:")
print("- Dataset has X observations and Y features")
print("- Missing data in columns: ...")
print("- Strong correlations between: ...")
```

### Pattern 2: Data Processing Pipeline

**For data cleaning and transformation:**

```
Cell 1: Setup (template cell)
Cell 2: Load raw data
Cell 3: Data cleaning functions
Cell 4: Apply transformations
Cell 5: Quality checks
Cell 6: Save processed data
```

### Pattern 3: Model Development

**For machine learning workflows:**

```
Cell 1: Setup (template cell)
Cell 2: Load processed data
Cell 3: Feature engineering
Cell 4: Train/test split
Cell 5: Model training
Cell 6: Evaluation
Cell 7: Save model
```

## Working with the DataCatalog

### Loading Different File Types

```python
# CSV files
df = catalog.load_file('sales_data')

# Excel with specific sheet
df = catalog.load_file('excel_data', sheet_name='Sheet2')

# JSON with specific orientation
df = catalog.load_file('json_data', orient='records')

# Parquet files (fast loading)
df = catalog.load_file('large_dataset')  # .parquet extension
```

### Finding and Exploring Files

```python
# Search for files by pattern
sales_files = catalog.find_files('sales')
print("Sales-related files:")
display(sales_files)

# View file metadata
large_files = catalog.catalog[catalog.catalog['size_mb'] > 10]
print("Large files (>10MB):")
display(large_files)

# Recent files
recent = catalog.catalog.sort_values('modified', ascending=False).head()
display(recent)
```

### Working with Multiple Files

```python
# Load and combine multiple files
q1_sales = catalog.load_file('sales_q1')
q2_sales = catalog.load_file('sales_q2')
q3_sales = catalog.load_file('sales_q3')
q4_sales = catalog.load_file('sales_q4')

# Combine quarterly data
annual_sales = pd.concat([q1_sales, q2_sales, q3_sales, q4_sales])
print(f"Combined dataset: {annual_sales.shape}")
```

## Path Management

### Using Predefined Paths

```python
# Available path variables from first cell:
raw_data        # data/raw/
processed_data  # data/processed/ 
interim_data    # data/interim/
external_data   # data/external/
models_path     # models/
figures_path    # reports/figures/

# Usage examples:
raw_file = f"{raw_data}/original_dataset.csv"
df = pd.read_csv(raw_file)

# Save processed data
df_clean.to_csv(f"{processed_data}/cleaned_dataset.csv", index=False)

# Save figures
plt.savefig(f"{figures_path}/analysis_plot.png", dpi=300, bbox_inches='tight')
```

### Custom Path Operations

```python
from pathlib import Path

# Create subdirectories for organization
analysis_dir = Path(figures_path) / "analysis_plots"
analysis_dir.mkdir(exist_ok=True)

# Save with timestamp
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
plt.savefig(analysis_dir / f"correlation_matrix_{timestamp}.png")
```

## Visualization Best Practices

### Using Template Helpers

```python
from generic.helpers import plot_df, plotly_graph

# Quick matplotlib plots with caching
plot_df(
    data=df, 
    cols_list=['col1', 'col2', 'col3'],
    save_to_path=f"{figures_path}/time_series.png",
    figsize=(15, 10)
)

# Interactive plotly graphs
plotly_graph(
    df=df,
    cols_to_graph=['metric1', 'metric2'],
    save_to_path=f"{figures_path}/interactive_plot.html"
)
```

### Custom Visualization Patterns

```python
# Set consistent style
plt.style.use('ggplot')  # Already set in preamble
plt.rcParams['figure.figsize'] = (12, 8)

# Create reusable plotting functions
def plot_distribution(data, column, title=None):
    """Plot distribution with both histogram and box plot"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Histogram
    ax1.hist(data[column], bins=30, alpha=0.7)
    ax1.set_title(f"{title or column} - Distribution")
    ax1.set_xlabel(column)
    
    # Box plot
    ax2.boxplot(data[column].dropna())
    ax2.set_title(f"{title or column} - Box Plot")
    
    plt.tight_layout()
    return fig

# Use the function
fig = plot_distribution(df, 'sales_amount', 'Monthly Sales')
plt.savefig(f"{figures_path}/sales_distribution.png")
```

## Code Organization

### When to Move Code to Modules

**Keep in notebooks:**
- Exploratory analysis
- One-off visualizations
- Experimental code
- Results presentation

**Move to `src/` modules:**
- Reusable functions (use 3+ times)
- Data cleaning pipelines
- Complex calculations
- Model training code

### Example: Refactoring to Modules

**Before (in notebook):**
```python
# Cell with data cleaning code
def clean_sales_data(df):
    # 20 lines of cleaning logic
    return clean_df

def calculate_metrics(df):
    # 15 lines of calculation
    return metrics_df

# Apply functions
clean_df = clean_sales_data(raw_df)
metrics_df = calculate_metrics(clean_df)
```

**After (moved to module):**

Create `src/data_prep/sales_cleaning.py`:
```python
import pandas as pd

def clean_sales_data(df):
    """Clean and standardize sales data"""
    # 20 lines of cleaning logic
    return clean_df

def calculate_metrics(df):
    """Calculate key sales metrics"""
    # 15 lines of calculation
    return metrics_df
```

**Updated notebook:**
```python
# Import your custom module
from data_prep.sales_cleaning import clean_sales_data, calculate_metrics

# Use functions (much cleaner)
clean_df = clean_sales_data(raw_df)
metrics_df = calculate_metrics(clean_df)
```

## Reproducibility Best Practices

### Documentation

```python
# Cell with markdown documentation
"""
# Sales Analysis - Q4 2023

**Objective:** Analyze Q4 sales performance and identify key trends

**Data Sources:**
- sales_q4_2023.csv: Raw sales transactions
- customer_master.xlsx: Customer demographics
- product_catalog.json: Product information

**Key Assumptions:**
- Revenue recognition follows GAAP standards
- Returns are excluded from analysis
- Currency is USD unless specified

**Last Updated:** 2023-12-15
"""
```

### Version Control

```python
# Track data versions
DATA_VERSION = "2023-12-01"
MODEL_VERSION = "v1.2"

print(f"Running analysis with data version: {DATA_VERSION}")
print(f"Using model version: {MODEL_VERSION}")

# Save with versioning
output_file = f"{processed_data}/analysis_results_{DATA_VERSION}.csv"
results_df.to_csv(output_file, index=False)
```

### Reproducible Workflows

```python
# Set random seeds for reproducibility
np.random.seed(42)

# Log key parameters
PARAMS = {
    'train_size': 0.8,
    'random_state': 42,
    'model_type': 'random_forest',
    'n_estimators': 100
}

print("Analysis parameters:")
for key, value in PARAMS.items():
    print(f"  {key}: {value}")
```

## Performance Optimization

### Memory Management

```python
# Check memory usage
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

# Optimize data types
def optimize_dtypes(df):
    """Optimize DataFrame memory usage"""
    for col in df.select_dtypes(include=['int']).columns:
        if df[col].min() >= 0 and df[col].max() <= 255:
            df[col] = df[col].astype('uint8')
        elif df[col].min() >= -128 and df[col].max() <= 127:
            df[col] = df[col].astype('int8')
    return df

df_optimized = optimize_dtypes(df)
```

### Efficient Data Loading

```python
# Load only needed columns
needed_cols = ['date', 'sales', 'region', 'product']
df = catalog.load_file('large_dataset', usecols=needed_cols)

# Load data in chunks for large files
def process_large_file(filename, chunksize=10000):
    chunks = []
    for chunk in pd.read_csv(f"{raw_data}/{filename}", chunksize=chunksize):
        # Process each chunk
        processed_chunk = process_chunk(chunk)
        chunks.append(processed_chunk)
    return pd.concat(chunks, ignore_index=True)
```

## Notebook Maintenance

### Regular Cleanup

```python
# Clear output periodically
# Jupyter: Cell → All Output → Clear

# Remove unused variables
del large_dataframe, temporary_results

# Check current memory usage
import gc
gc.collect()
```

### Cell Organization

1. **Keep cells focused** - One concept per cell
2. **Use markdown cells** - Document your thinking
3. **Restart and run all** - Test reproducibility regularly
4. **Remove experimental code** - Clean up before committing

### Error Handling

```python
try:
    df = catalog.load_file('important_dataset')
    print(f"✅ Loaded {len(df)} records")
except FileNotFoundError:
    print("❌ Dataset not found - check data directory")
    # Fallback or alternative data source
except Exception as e:
    print(f"❌ Error loading data: {e}")
    # Handle gracefully
```

## Advanced Techniques

### Interactive Widgets

```python
import ipywidgets as widgets
from IPython.display import display

# Interactive column selector
column_widget = widgets.Dropdown(
    options=list(df.columns),
    description='Column:'
)

def plot_column(column):
    plt.figure(figsize=(10, 6))
    df[column].hist(bins=30)
    plt.title(f'Distribution of {column}')
    plt.show()

# Connect widget to function
interactive_plot = widgets.interactive(plot_column, column=column_widget)
display(interactive_plot)
```

### Progress Tracking

```python
from tqdm import tqdm
tqdm.pandas()  # Enable progress bars for pandas operations

# Progress bar for apply operations
df['processed'] = df.progress_apply(lambda x: complex_function(x), axis=1)

# Manual progress tracking
results = []
for i, item in enumerate(tqdm(large_list)):
    result = process_item(item)
    results.append(result)
```

## Troubleshooting

### Common Issues

**"Module not found" errors:**
```python
# Make sure first cell ran successfully
import sys
print(sys.path)  # Should include '../src'

# Restart kernel if needed
# Jupyter: Kernel → Restart
```

**Memory issues:**
```python
# Check DataFrame memory usage
df.info(memory_usage='deep')

# Use more efficient data types
df['category'] = df['category'].astype('category')
```

**Import errors after refactoring:**
```python
# Reload modules after changes
import importlib
import my_module
importlib.reload(my_module)
```

## Next Steps

- **Practice patterns**: Try different notebook organization approaches
- **Explore helpers**: Discover more utilities in `src/generic/helpers.py`
- **Build modules**: Move reusable code to appropriate `src/` directories
- **Share notebooks**: Clean and document before sharing with team
- **Advanced features**: Explore Jupyter extensions and widgets for enhanced functionality

## Resources

- **Data workflow**: See [`data-workflow.md`](data-workflow.md) for DataCatalog details
- **Setup guide**: Check [`setup.md`](setup.md) for environment issues
- **Project structure**: Review main README for overall organization