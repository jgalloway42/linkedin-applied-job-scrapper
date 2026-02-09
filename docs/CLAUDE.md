# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive data science project template based on the cookiecutter-data-science structure. It provides a standardized framework with organized directories, powerful utilities, automated setup, and comprehensive documentation.

## Project Structure

### Core Architecture
- **src/**: Source code organized by functionality (all directories have __init__.py for proper Python packages)
  - **generic/**: Core utilities shared across the project
    - `preamble.py`: Standard imports, configurations, and robust path management for Jupyter notebooks
    - `helpers.py`: Comprehensive data science utility functions including DataCatalog system
  - **data_prep/**: Data preparation and cleaning modules
  - **features/**: Feature engineering modules
  - **models/**: Model training and evaluation modules
  - **visualization/**: Custom plotting and visualization functions

- **data/**: Data storage with cookiecutter-data-science structure (created by setup script)
  - `raw/`: Original, immutable data
  - `processed/`: Final datasets for modeling
  - `interim/`: Intermediate transformed data
  - `external/`: Third-party data sources

- **notebooks/**: Jupyter notebooks for analysis
  - `zz_template_notebook.ipynb`: Template with pre-configured setup and explicit imports

- **scripts/**: Setup and utility scripts
  - `env-setup.sh`: Automated environment setup script

- **docs/**: Comprehensive documentation
  - `setup.md`: Detailed environment setup guide
  - `data-workflow.md`: DataCatalog usage and data management patterns
  - `notebook-guide.md`: Notebook development best practices
  - `CLAUDE.md`: This file

- **reports/figures/**: Generated visualizations and figures
- **models/**: Trained models and model artifacts (now a proper Python package with __init__.py)

### Key Components

#### DataCatalog System (`src/generic/helpers.py`)
The project includes a sophisticated file discovery and data loading system:
- `DataCatalog` class for managing data files across directories
- Automatic file scanning and metadata collection
- Smart file loading with format detection (CSV, Excel, JSON, Pickle, Parquet, HDF5)
- File search and filtering capabilities

#### Notebook Template (`notebooks/zz_template_notebook.ipynb`)
Pre-configured notebook with:
- Explicit imports (no import * for clarity)
- Automatic DataCatalog initialization and file discovery
- Clean, documented setup in first cell
- Updated environment setup instructions

## Development Workflow

### Environment Setup
1. Run the environment setup script:
   ```bash
   bash scripts/env-setup.sh
   ```
   Note: Script moved to scripts/ directory for better organization
2. Follow prompts to create conda environment with specified Python version
3. The script automatically:
   - Creates data directories (raw/, processed/, interim/, external/)
   - Installs dependencies from requirements.txt
   - Sets up Jupyter kernel
   - Updates requirements.txt with installed packages

### Documentation System
The project includes comprehensive documentation:
- **README.md**: Project overview and quick navigation
- **QUICKSTART.md**: Get running in 3 steps
- **docs/setup.md**: Detailed setup with troubleshooting
- **docs/data-workflow.md**: Complete DataCatalog guide and data management patterns  
- **docs/notebook-guide.md**: Development best practices and optimization techniques

### Working with Data
- Use the DataCatalog system for file discovery: `catalog = create_data_catalog('.')`
- Access file paths programmatically: `catalog.get_path('filename')`
- Load files directly: `df = catalog.load_file('filename')`
- Search for files: `catalog.find_files('pattern')`

### Notebook Development
- Start with the template notebook for consistent setup
- The first cell uses explicit imports grouped by purpose:
  ```python
  # Core data science libraries
  from generic.preamble import np, pd, plt, sns
  # Data management and paths
  from generic.preamble import raw_data, processed_data, models_path
  from generic.helpers import create_data_catalog
  ```
- DataCatalog is pre-initialized and displays available files summary
- All src/ directories are proper Python packages with __init__.py files

## Dependencies

Core packages (requirements.txt):
- seaborn: Statistical visualization
- plotly: Interactive plotting  
- scikit-learn: Machine learning
- statsmodels: Statistical modeling

Standard data science stack is imported via preamble.py:
- numpy, pandas, matplotlib, seaborn
- joblib for model persistence  
- warnings management and display configurations
- Robust path management using pathlib and __file__

## File Organization Conventions

- Use descriptive filenames without spaces or special characters (Windows compatibility)
- Store raw data in data/raw/ (never modify)
- Place cleaned data in data/processed/
- Use data/interim/ for intermediate processing steps
- Save models in models/ directory (now a proper Python package)
- Generate figures in reports/figures/
- Keep setup scripts in scripts/ directory

## Windows Compatibility Notes

- All file paths use forward slashes or pathlib for cross-platform compatibility
- Avoid Unicode characters in file names and code comments
- Use UTF-8 encoding when reading/writing text files:
  ```python
  df.to_csv('file.csv', encoding='utf-8')
  pd.read_csv('file.csv', encoding='utf-8')
  ```
- Path handling in preamble.py uses pathlib for robust Windows support

## Utility Functions

The helpers.py module provides:
- **File Operations**: `walk_directory()`, `save_joblib()`, logging setup
- **Data Manipulation**: `search_columns()`, `filter_list()`, `flatten_list()`
- **Visualization**: `plot_df()`, `plotly_graph()` with caching and export options
- **DataCatalog**: Comprehensive data file management system

## Key Improvements Made

This template has been enhanced beyond basic cookiecutter-data-science with:
- **Automated setup**: Single script creates environment and directory structure
- **Smart file management**: DataCatalog system for automatic file discovery and loading
- **Clean notebook setup**: Explicit imports with pre-configured utilities
- **Comprehensive documentation**: Multi-level guides from quickstart to advanced usage
- **Proper package structure**: All directories have __init__.py files for clean imports
- **Windows compatibility**: Robust path handling and encoding considerations
- **Organized scripts**: Setup and utility scripts in dedicated scripts/ directory

## Development Commands

- **Environment setup**: `bash scripts/env-setup.sh`
- **Activate environment**: `conda activate [ENV_NAME]`
- **Start Jupyter**: `jupyter notebook` or `jupyter lab`
- **Template notebook**: `notebooks/zz_template_notebook.ipynb`

## Notes

- Project follows enhanced cookiecutter-data-science conventions
- No package.json, Makefile, or formal build system - this is a Python research template
- Environment management handled through conda and requirements.txt
- Focus on reproducible data science workflows rather than software engineering deployment
- All documentation avoids Unicode characters for Windows compatibility
- Path handling uses pathlib for cross-platform robustness