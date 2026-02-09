# Data Workflow Guide

Complete guide to managing data files and workflows in this project template, including the powerful DataCatalog system.

## Overview

This template provides a structured approach to data management with:
- **Organized directory structure** following data science best practices
- **DataCatalog system** for automatic file discovery and loading
- **Smart file operations** with metadata tracking
- **Flexible data workflows** from raw to processed

## Directory Structure

### Data Organization

```
data/
├── raw/           ← Original, immutable data dump
├── processed/     ← Final, canonical datasets for modeling  
├── interim/       ← Intermediate transformed data
└── external/      ← Data from third-party sources
```

### Directory Purposes

**`data/raw/`** - The original data
- Never edit files here
- Treat as read-only
- Keep original formats and naming
- Document data sources

**`data/processed/`** - Final datasets
- Clean, validated data ready for analysis
- Consistent column names and formats
- Documented transformations applied
- Analysis-ready structure

**`data/interim/`** - Work in progress
- Partially processed data
- Intermediate transformation steps
- Temporary working files
- Can be recreated from raw data

**`data/external/`** - Third-party data
- Reference datasets
- Market data, demographics
- External APIs downloads
- Supplement to your main data

## DataCatalog System

### Getting Started

The DataCatalog automatically discovers and manages data files:

```python
from generic.helpers import create_data_catalog

# Initialize catalog (scans all data directories)
catalog = create_data_catalog('.')

# View summary
display(catalog.summary())
```

### Core Features

**Automatic File Discovery**
```python
# Catalog scans these directories by default:
# data/raw/, data/processed/, data/interim/, data/external/

# Includes these file types:
# .csv, .xlsx, .json, .pkl, .parquet, .h5, .xls
```

**File Metadata Tracking**
- File sizes and modification dates
- Directory organization
- Path information
- Extension types

### Basic Operations

**Finding Files**
```python
# Search by name pattern
sales_files = catalog.find_files('sales')
print(sales_files)

# View all files
print(catalog.catalog)

# Get specific file path
file_path = catalog.get_path('dataset_name')
```

**Loading Files**
```python
# Smart loading - detects format automatically
df = catalog.load_file('my_dataset')  # Loads my_dataset.csv/xlsx/etc

# With parameters
df = catalog.load_file('excel_file', sheet_name='Sheet2')
df = catalog.load_file('csv_file', sep=';', encoding='utf-8')
```

**Supported Formats**
- **CSV**: `pd.read_csv()`
- **Excel**: `pd.read_excel()` (.xlsx, .xls)
- **JSON**: `pd.read_json()`
- **Pickle**: `pd.read_pickle()`
- **Parquet**: `pd.read_parquet()`
- **HDF5**: `pd.read_hdf()` (requires `key` parameter)

### Advanced Usage

**Custom Scanning**
```python
# Scan specific directories
catalog.scan_directory(
    subdirs=['raw', 'processed'],  # Only these directories
    file_types=['.csv', '.parquet']  # Only these formats
)

# Scan with custom file types
catalog.scan_directory(file_types=['.txt', '.log', '.dat'])
```

**File Operations**
```python
# Get file metadata
files_info = catalog.catalog[catalog.catalog['extension'] == '.csv']
large_files = catalog.catalog[catalog.catalog['size_mb'] > 10]
recent_files = catalog.catalog.sort_values('modified', ascending=False)
```

## Data Workflow Patterns

### Pattern 1: Linear Pipeline

**Raw → Processed**
```python
# 1. Load raw data
raw_df = catalog.load_file('raw_sales_data')

# 2. Clean and transform
processed_df = clean_data(raw_df)  # Your function

# 3. Save to processed
processed_df.to_csv(f"{processed_data}/clean_sales.csv", index=False)

# 4. Refresh catalog to see new file
catalog.scan_directory()
```

### Pattern 2: Multi-Step Pipeline

**Raw → Interim → Processed**
```python
# Step 1: Initial cleaning
raw_df = catalog.load_file('messy_data')
clean_df = initial_cleaning(raw_df)
clean_df.to_csv(f"{interim_data}/step1_clean.csv", index=False)

# Step 2: Feature engineering  
interim_df = catalog.load_file('step1_clean')
features_df = create_features(interim_df)
features_df.to_csv(f"{interim_data}/step2_features.csv", index=False)

# Step 3: Final dataset
final_df = catalog.load_file('step2_features')
model_ready = finalize_dataset(final_df)
model_ready.to_csv(f"{processed_data}/model_dataset.csv", index=False)
```

### Pattern 3: Multiple Sources

**Combining data from different sources**
```python
# Load multiple raw files
sales = catalog.load_file('sales_2023')
customers = catalog.load_file('customer_master')
products = catalog.load_file('product_catalog')

# Combine and enrich
enriched = sales.merge(customers, on='customer_id')
enriched = enriched.merge(products, on='product_id')

# Save combined dataset
enriched.to_csv(f"{processed_data}/enriched_sales.csv", index=False)
```

## File Naming Conventions

### Recommended Patterns

**Raw Data**
- `raw_[source]_[date].csv` (e.g., `raw_salesforce_20231201.csv`)
- `[system]_export_[timestamp].xlsx`
- Keep original names when possible

**Processed Data** 
- `[purpose]_[date_range].csv` (e.g., `sales_analysis_2023Q4.csv`)
- `model_dataset_v1.parquet`
- `features_[model_name].csv`

**Interim Files**
- `step1_[description].csv`
- `temp_[process]_[timestamp].pkl`
- `interim_[transformation].parquet`

### File Organization Tips

1. **Use descriptive names** - `sales_data.csv` not `data.csv`
2. **Include dates** - Help track data versions
3. **Version important files** - `dataset_v1.csv`, `dataset_v2.csv`
4. **Use consistent formats** - Prefer .parquet for large files, .csv for sharing

## Working with Large Files

### Memory-Efficient Loading

```python
# For large CSV files
chunks = pd.read_csv(f"{raw_data}/large_file.csv", chunksize=10000)
processed_chunks = [process_chunk(chunk) for chunk in chunks]
result = pd.concat(processed_chunks)
```

### Optimal File Formats

**For storage efficiency:**
- **Parquet**: Best compression, fast reading
- **HDF5**: Good for numeric data, partial loading
- **Pickle**: Python objects, but not portable

```python
# Save as parquet for better performance
df.to_parquet(f"{processed_data}/dataset.parquet")

# Load specific columns only
df_subset = pd.read_parquet(
    f"{processed_data}/dataset.parquet", 
    columns=['col1', 'col2']
)
```

## Data Validation

### Built-in Checks

```python
# Check data freshness
recent = catalog.catalog[
    catalog.catalog['modified'] > '2023-12-01'
]

# Find missing data files
expected_files = ['sales', 'customers', 'products']
missing = [f for f in expected_files if catalog.get_path(f) is None]
print(f"Missing files: {missing}")
```

### Custom Validation

```python
def validate_dataset(df, name):
    """Validate dataset meets requirements"""
    checks = {
        'not_empty': len(df) > 0,
        'no_all_null_columns': not df.isnull().all().any(),
        'reasonable_size': len(df) < 1_000_000  # Adjust as needed
    }
    
    failed = [check for check, passed in checks.items() if not passed]
    if failed:
        print(f"❌ {name} failed checks: {failed}")
    else:
        print(f"✅ {name} passed all checks")
    
    return len(failed) == 0

# Use in your workflow
df = catalog.load_file('my_dataset')
validate_dataset(df, 'my_dataset')
```

## Integration with Notebooks

### Template Integration

The template notebook automatically:
1. Initializes DataCatalog
2. Displays file summary
3. Sets up all path variables

```python
# Available in every notebook:
catalog          # Pre-loaded DataCatalog
raw_data        # Path to data/raw/
processed_data  # Path to data/processed/
interim_data    # Path to data/interim/
```

### Notebook Workflow

```python
# Cell 1: Standard setup (already in template)
from generic.notebook_setup import *

# Cell 2: Load your data
df = catalog.load_file('my_dataset')
print(f"Loaded {len(df)} rows")

# Cell 3: Start your analysis
df.head()
```

## Best Practices

### Data Management

1. **Keep raw data immutable** - Never modify files in `data/raw/`
2. **Document transformations** - Comment your cleaning steps
3. **Version important datasets** - Use meaningful file names
4. **Regular cleanup** - Remove unnecessary interim files

### Performance

1. **Use appropriate formats** - Parquet for large datasets
2. **Load only what you need** - Specify columns when possible
3. **Cache expensive operations** - Save intermediate results
4. **Monitor file sizes** - Use `catalog.summary()` to track growth

### Reproducibility

1. **Script your workflows** - Don't rely on manual steps
2. **Save processing code** - Put functions in `src/` modules
3. **Document data sources** - Include metadata and origins
4. **Use consistent environments** - Requirements.txt and conda

## Troubleshooting

### Common Issues

**"File not found in catalog"**
```python
# Refresh the catalog
catalog.scan_directory()

# Check if file exists with different name
catalog.find_files('partial_name')
```

**"Multiple files with same basename"**
```python
# Use full filename or directory filtering
matches = catalog.catalog[catalog.catalog['basename'] == 'data']
print(matches[['filename', 'directory', 'path']])
```

**"Can't load file format"**
```python
# Check supported formats
print("Supported:", ['.csv', '.xlsx', '.json', '.pkl', '.parquet', '.h5'])

# Use pandas directly for unsupported formats
import pandas as pd
df = pd.read_table(catalog.get_path('my_file'))
```

## Next Steps

- **Explore helpers**: Check `src/generic/helpers.py` for more utilities
- **Notebook guide**: See [`notebook-guide.md`](notebook-guide.md) for development tips  
- **Project structure**: Review project organization in main README
- **Advanced features**: Experiment with custom DataCatalog configurations