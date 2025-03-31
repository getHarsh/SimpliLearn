# Environment Setup and Initial Configuration

## 1. Development Environment

### 1.1 Python Environment Setup
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On macOS/Linux:
source env/bin/activate
# On Windows:
.\env\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 1.2 Required Dependencies
```python
# Core data manipulation
import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc

# SMOTE for class imbalance
from imblearn.over_sampling import SMOTE
```

## 2. Data Loading and Initial Setup

### 2.1 Configuration Settings
```python
# Random seed for reproducibility
RANDOM_SEED = 123

# Model parameters
TEST_SIZE = 0.2
CV_FOLDS = 5
N_CLUSTERS = 3

# File paths
DATA_PATH = '../data/hr_data.csv'

# Visualization settings
plt.style.use('seaborn')
sns.set_palette("husl")
```

### 2.2 Data Loading Function
```python
def load_hr_data(file_path: str) -> pd.DataFrame:
    """
    Load HR analytics data with appropriate data types.
    
    Parameters:
        file_path (str): Path to the HR data CSV file
        
    Returns:
        pd.DataFrame: Loaded dataframe with correct data types
    """
    # Define data types for columns
    dtypes = {
        'satisfaction_level': float,
        'last_evaluation': float,
        'number_project': int,
        'average_montly_hours': int,
        'time_spend_company': int,
        'Work_accident': int,
        'left': int,
        'promotion_last_5years': int,
        'Department': 'category',
        'salary': 'category'
    }
    
    # Read CSV with specified data types
    df = pd.read_csv(file_path, dtype=dtypes)
    return df
```

### 2.3 Data Validation Function
```python
def validate_data_structure(df: pd.DataFrame) -> bool:
    """
    Validate the structure of loaded data.
    
    Parameters:
        df (pd.DataFrame): Input dataframe to validate
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    required_columns = [
        'satisfaction_level', 'last_evaluation', 'number_project',
        'average_montly_hours', 'time_spend_company', 'Work_accident',
        'left', 'promotion_last_5years', 'Department', 'salary'
    ]
    
    # Check for required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        print(f"Missing required columns: {missing_cols}")
        return False
    
    # Validate data types
    expected_types = {
        'satisfaction_level': ['float64', 'float32'],
        'last_evaluation': ['float64', 'float32'],
        'number_project': ['int64', 'int32'],
        'average_montly_hours': ['int64', 'int32'],
        'time_spend_company': ['int64', 'int32'],
        'Work_accident': ['int64', 'int32'],
        'left': ['int64', 'int32'],
        'promotion_last_5years': ['int64', 'int32']
    }
    
    for col, types in expected_types.items():
        if df[col].dtype.name not in types:
            print(f"Incorrect data type for {col}: {df[col].dtype}")
            return False
    
    return True
```

## 3. Initial Data Overview

### 3.1 Basic Data Inspection
```python
def get_data_overview(df: pd.DataFrame) -> None:
    """
    Print basic information about the dataset.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    print("\nDataset Shape:", df.shape)
    print("\nFeature Information:")
    print(df.info())
    print("\nNumerical Features Summary:")
    print(df.describe())
    print("\nCategorical Features Summary:")
    print(df.describe(include=['category']))
```

### 3.2 Data Loading Example
```python
# Load and validate data
df = load_hr_data(DATA_PATH)
if validate_data_structure(df):
    get_data_overview(df)
else:
    raise ValueError("Data validation failed!")
```

## 4. Next Steps
After successfully setting up the environment and loading the data:
1. Proceed to data quality checks in `02_DATA_WRANGLING.md`
2. Follow the EDA process in `03_DATA_ANALYSIS.md`
3. Implement modeling steps in `04_MODELING.md`
