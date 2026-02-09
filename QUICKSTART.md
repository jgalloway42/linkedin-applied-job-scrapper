# Quick Start Guide

Get your data science project up and running in minutes with this step-by-step guide.

## Prerequisites

Before you begin, make sure you have:

- **Miniconda or Anaconda** installed and available in your PATH
  - Test: Run `conda --version` in your terminal
  - If not installed: [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- **Bash-compatible terminal**:
  - **Windows**: Git Bash (recommended) or WSL
  - **Mac**: Terminal (built-in)
  - **Linux**: Terminal (built-in)
- **Jupyter** environment or IDE that can run .ipynb files

### Platform-Specific Notes

**Windows Users:**
- Use **Git Bash** for best compatibility with the setup script
- Avoid Command Prompt or PowerShell for the initial setup
- If conda isn't found, run `conda init bash` in Git Bash

**Mac/Linux Users:**
- Use your built-in Terminal application
- The setup script should work directly
- If you use pyenv or other Python managers, ensure conda takes precedence during setup

## Setup Steps

### Step 1: Get the Template
```bash
# Clone or download this repository
git clone <your-repo-url>
cd project_template
```

### Step 2: Run Environment Setup
```bash
# Run the automated setup script
bash scripts/env-setup.sh
```

The script will prompt you for:
- **Environment name** (e.g., `my_analysis`, `sales_project`)
- **Python version** (e.g., `3.10`, `3.11`, or press Enter for latest)

**What happens during setup:**
✅ Creates conda environment with specified Python version  
✅ Creates data directories (`data/raw/`, `data/processed/`, etc.)  
✅ Installs all required packages from `requirements.txt`  
✅ Sets up Jupyter kernel for the new environment  
✅ Updates `requirements.txt` with installed packages  

### Step 3: Activate Environment & Start Jupyter
```bash
# Activate your new environment
conda activate YOUR_ENV_NAME

# Start Jupyter (choose one)
jupyter notebook
# OR
jupyter lab
```

### Step 4: Open the Template Notebook
1. Navigate to `notebooks/zz_template_notebook.ipynb`
2. Run the first cell - it will:
   - Import all essential libraries (pandas, numpy, matplotlib, etc.)
   - Set up data paths
   - Initialize the DataCatalog
   - Display available data files

**You're ready to start analyzing! 🎉**

## What You Get

### Instant Access to:
- **`pd, np, plt, sns`** - Essential data science libraries
- **`catalog`** - Smart file discovery and loading system
- **Path variables** - `raw_data`, `processed_data`, `models_path`, etc.
- **Helper functions** - File operations, visualization, data manipulation

### Example Usage:
```python
# The first cell gives you everything you need:
df = pd.read_csv(f"{raw_data}/my_dataset.csv")

# OR use the DataCatalog:
df = catalog.load_file('my_dataset')  # Automatic format detection!

# Find files by name pattern:
catalog.find_files('sales')  # Shows all files with 'sales' in the name
```

## Troubleshooting

### "conda: command not found"
- **Windows**: Make sure you're using Git Bash, not Command Prompt/PowerShell
- **Mac/Linux**: Check if conda is in PATH: `echo $PATH | grep conda`
- **All OS**: Run `conda init bash` and restart your terminal

### "No such file or directory: scripts/env-setup.sh"
- Make sure you're in the project root directory
- Run `ls` (or `dir` on Windows) to confirm you can see the `scripts/` folder

### "Permission denied"
**Mac/Linux:**
```bash
chmod +x scripts/env-setup.sh
bash scripts/env-setup.sh
```
**Windows (Git Bash):**
```bash
bash scripts/env-setup.sh
```

### Environment activation issues
**All platforms:**
```bash
# Initialize conda for your shell
conda init bash  # Mac/Linux/Git Bash
conda init zsh   # Mac with zsh
conda init powershell  # Windows PowerShell (if using)

# Restart terminal, then try:
conda activate YOUR_ENV_NAME
```

### Python/conda conflicts
**Mac users with Homebrew or pyenv:**
```bash
# Temporarily prioritize conda
export PATH="/opt/miniconda3/bin:$PATH"  # or your conda path
conda activate YOUR_ENV_NAME
```

## Next Steps

Once you're set up:

1. **Add your data** to the `data/raw/` directory
2. **Run the template notebook** first cell to see your files
3. **Start your analysis** in cell 2 and beyond
4. **Explore the helpers** - check out `src/generic/helpers.py` for useful functions

## Need More Help?

- **📚 Detailed guides**: See the [`docs/`](docs/) directory
- **🛠️ Setup problems**: Check [`docs/setup.md`](docs/setup.md)
- **📊 DataCatalog usage**: See [`docs/data-workflow.md`](docs/data-workflow.md)
- **📓 Notebook tips**: Read [`docs/notebook-guide.md`](docs/notebook-guide.md)

Happy analyzing! 🚀