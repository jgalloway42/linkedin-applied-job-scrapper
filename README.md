# Data Science Project Template

A comprehensive, organized template for data science projects based on the cookiecutter-data-science structure. This template provides a standardized framework with powerful utilities, organized directories, and streamlined workflows.

## Key Features

### 🗂️ **Organized Project Structure**
- **`src/`** - Modular source code organized by functionality
- **`data/`** - Structured data storage (raw, processed, interim, external)
- **`notebooks/`** - Jupyter notebooks with pre-configured template
- **`models/`** - Trained models and artifacts
- **`reports/figures/`** - Generated visualizations

### 📊 **DataCatalog System**
- Automatic file discovery across data directories
- Smart file loading with format detection (CSV, Excel, JSON, Pickle, Parquet, HDF5)
- File search and filtering capabilities
- Metadata tracking (size, modification dates, paths)

### 📓 **Template Notebook**
- Pre-configured with all essential imports
- Automatic DataCatalog initialization
- Clean, explicit import structure
- Ready-to-use data science environment

### 🛠️ **Helpful Utilities**
- **Visualization functions** with caching and export options
- **File operations** with joblib serialization
- **Data manipulation helpers** for common tasks
- **Path management** with robust project root detection

## Quick Start

**Get up and running in 3 steps:**

1. **Clone/download this template**
2. **Run setup script**: `bash scripts/env-setup.sh`
3. **Start analyzing**: Open `notebooks/zz_template_notebook.ipynb`

👉 **See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions**

## Project Structure

```
├── README.md          ← Project overview (you are here)
├── QUICKSTART.md      ← Get started in minutes
├── requirements.txt   ← Python package dependencies
├── scripts/          
│   └── env-setup.sh   ← Environment setup script
├── data/             
│   ├── raw/           ← Original, immutable data
│   ├── processed/     ← Final datasets for modeling
│   ├── interim/       ← Intermediate transformed data
│   └── external/      ← Third-party data sources
├── notebooks/         
│   └── zz_template_notebook.ipynb  ← Pre-configured analysis template
├── src/               ← Source code for this project
│   ├── generic/       ← Core utilities and imports
│   ├── data_prep/     ← Data preparation modules
│   ├── features/      ← Feature engineering
│   ├── models/        ← Model training and evaluation
│   └── visualization/ ← Custom plotting functions
├── models/            ← Trained models and artifacts
├── reports/figures/   ← Generated visualizations
└── docs/              ← Detailed documentation and guides
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started immediately
- **[docs/](docs/)** - Comprehensive guides and documentation
- **[docs/CLAUDE.md](docs/CLAUDE.md)** - Guide for Claude Code AI assistant

## Based On

This template extends the proven [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science) structure with additional utilities and modern Python practices.

## Next Steps

1. 📖 Read the [QUICKSTART.md](QUICKSTART.md) guide
2. 🔧 Run the environment setup script
3. 📊 Explore the template notebook
4. 📚 Browse the [detailed documentation](docs/) for advanced usage