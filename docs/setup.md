# Setup Guide

Comprehensive guide for setting up your data science environment and getting the most out of this project template.

## Overview

This template uses conda for environment management and provides an automated setup script that handles most of the configuration for you. This guide covers both the automated approach and manual setup options.

## Prerequisites

### Required Software

1. **Miniconda or Anaconda**
   - Download from: https://docs.conda.io/en/latest/miniconda.html
   - Verify installation: `conda --version`

2. **Git** (for cloning and version control)
   - Download from: https://git-scm.com/
   - Verify installation: `git --version`

3. **Bash-compatible terminal**
   - **Linux/macOS**: Built-in terminal
   - **Windows**: Git Bash (installed with Git) or WSL

### System Requirements

- **Python**: 3.8+ (handled by conda)
- **Storage**: ~500MB for conda environment + your data
- **Memory**: 4GB+ RAM recommended for data analysis

## Automated Setup (Recommended)

### Step 1: Get the Project

```bash
# Option A: Clone if you have a git repository
git clone <your-repo-url>
cd project_template

# Option B: Download and extract ZIP
# Download ZIP from GitHub → Extract → Navigate to folder
cd path/to/project_template
```

### Step 2: Run Setup Script

```bash
bash scripts/env-setup.sh
```

**The script will:**
1. Prompt for environment name and Python version
2. Create conda environment
3. Create data directory structure
4. Install all packages from requirements.txt
5. Set up Jupyter kernel
6. Update requirements.txt with installed packages

**Example interaction:**
```
Please enter environment name:
my_analysis

Please enter Python version (e.g., 3.9, 3.10, 3.11) or press Enter for latest:
3.10

Creating: my_analysis with Python 3.10
```

### Step 3: Activate Environment

```bash
conda activate my_analysis
```

### Step 4: Verify Setup

```bash
# Check Python version
python --version

# Check installed packages
pip list | head -10

# Verify Jupyter kernel
jupyter kernelspec list
```

## Manual Setup

If you prefer manual control or the automated script doesn't work for your system:

### Create Environment

```bash
# Create conda environment
conda create -n my_project python=3.10 -y

# Activate environment
conda activate my_project

# Install Jupyter and basic tools
pip install ipykernel
python -m ipykernel install --user --name=my_project

# Install project dependencies
pip install -r requirements.txt
```

### Create Directory Structure

```bash
# Create data directories
mkdir -p data/{raw,processed,interim,external}

# Verify structure
ls -la data/
```

### Optional: Update Requirements

```bash
# Update requirements.txt with current packages
pip freeze > requirements.txt
```

## IDE Configuration

### Jupyter Notebook/Lab

1. **Start Jupyter**:
   ```bash
   conda activate my_project
   jupyter notebook  # or jupyter lab
   ```

2. **Select Kernel**: When opening notebooks, choose your project kernel (`my_project`)

3. **Verify Setup**: Run the first cell of the template notebook

### VS Code

1. **Install Python extension**
2. **Select interpreter**: 
   - Open Command Palette (Ctrl+Shift+P)
   - "Python: Select Interpreter"
   - Choose your conda environment
3. **Jupyter extension**: Install for .ipynb support

### PyCharm

1. **Add interpreter**:
   - File → Settings → Project → Python Interpreter
   - Add → Conda Environment → Existing
   - Select your environment path
2. **Enable Jupyter**: Available in Professional edition

## Troubleshooting

### Environment Issues

**"conda: command not found"**
```bash
# Add conda to PATH (Linux/macOS)
echo 'export PATH="~/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Windows: Use Anaconda Prompt instead of Command Prompt
# Or initialize Git Bash:
conda init bash
```

**"Environment already exists"**
```bash
# Remove existing environment
conda env remove -n my_project

# Or use a different name
conda create -n my_project_v2 python=3.10
```

### Package Installation Issues

**"Solving environment: failed"**
```bash
# Try with conda-forge channel
conda install -c conda-forge package_name

# Or use pip instead
pip install package_name
```

**"No module named 'package'"**
```bash
# Make sure environment is activated
conda activate my_project

# Reinstall package
pip install --upgrade package_name

# Check if package is in requirements.txt
grep package_name requirements.txt
```

### Script Execution Issues

**"Permission denied"**
```bash
chmod +x scripts/env-setup.sh
bash scripts/env-setup.sh
```

**"No such file or directory"**
```bash
# Make sure you're in project root
pwd
ls scripts/  # Should show env-setup.sh
```

### Path Issues

**Imports not working in notebooks**
1. Verify project structure matches template
2. Check first cell of template notebook runs without errors
3. Ensure `src` directory has `__init__.py` files

**Wrong paths in preamble.py**
- The preamble.py uses `__file__` for robust path detection
- If paths are wrong, check project directory structure
- Paths are relative to project root

## Advanced Configuration

### Custom Package Channels

Add to environment creation:
```bash
conda create -n my_project -c conda-forge -c pytorch python=3.10
```

### Development Tools

Optional additions for development:
```bash
pip install black flake8 pytest  # Code formatting and testing
pip install jupyterlab-lsp       # Enhanced Jupyter Lab
pip install nbstripout           # Clean notebooks for git
```

### Memory Optimization

For large datasets:
```python
# Add to notebook first cell
import pandas as pd
pd.options.mode.chained_assignment = None  # Disable warnings
pd.options.display.max_columns = 20       # Limit display
```

## Environment Management

### Multiple Projects

Each project should have its own environment:
```bash
conda create -n project1 python=3.10
conda create -n project2 python=3.9
```

### Environment Export/Import

Export current environment:
```bash
conda env export > environment.yml
```

Create from exported file:
```bash
conda env create -f environment.yml
```

### Cleanup

Remove unused environments:
```bash
# List environments
conda env list

# Remove environment
conda env remove -n old_project

# Clean conda cache
conda clean --all
```

## Next Steps

Once setup is complete:

1. **Test the template**: Open and run `notebooks/zz_template_notebook.ipynb`
2. **Add your data**: Place files in `data/raw/`
3. **Explore utilities**: Review `src/generic/helpers.py`
4. **Read workflow guide**: See [`data-workflow.md`](data-workflow.md)
5. **Start analyzing**: Create your first analysis notebook

## Getting Help

- **Template issues**: Check project documentation
- **Conda problems**: [Conda documentation](https://docs.conda.io/)
- **Python packages**: [PyPI documentation](https://pypi.org/)
- **Jupyter issues**: [Jupyter documentation](https://jupyter.org/documentation)