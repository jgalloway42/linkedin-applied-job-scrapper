# Generic Jupyter Notebook Imports and Setup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
import joblib
import sys
from pathlib import Path

warnings.filterwarnings('ignore')

# Configure matplotlib and pandas display options
plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (15,5)
pd.set_option('display.max_columns',50)
np.set_printoptions(precision=3)

# Path definitions - robust path calculation
# Find project root by looking for common project markers
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent  # Go up from src/generic/ to project root

raw_data = project_root / 'data' / 'raw'
processed_data = project_root / 'data' / 'processed'
interim_data = project_root / 'data' / 'interim'
external_data = project_root / 'data' / 'external'
models_path = project_root / 'models'
figures_path = project_root / 'reports' / 'figures'

# Convert to strings for compatibility
raw_data = str(raw_data)
processed_data = str(processed_data)
interim_data = str(interim_data)
external_data = str(external_data)
models_path = str(models_path)
figures_path = str(figures_path)