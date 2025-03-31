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
# Core data manipulation and analysis
import numpy as np
import pandas as pd

# Data visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')  # Set consistent style

# Machine Learning - Feature Processing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Machine Learning - Clustering
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score

# Statistics and correlation
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage

# Date handling
from datetime import datetime

# Utilities
import warnings
warnings.filterwarnings('ignore')  # Suppress warnings for clean notebook output
```

## 2. Data Loading and Initial Setup

### 2.1 Configuration Settings
```python
# Data paths and filenames
DATA_DIR = '../data'
CSV_PATH = f'{DATA_DIR}/rolling_stones_spotify.csv'
XLSX_PATH = f'{DATA_DIR}/data_dictionary.xlsx'
OUTPUT_DIR = '../output'

# Random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Data processing parameters
UNIT_RANGE_FEATURES = [
    'acousticness', 'danceability', 'energy',
    'instrumentalness', 'liveness', 'speechiness', 'valence'
]

SPECIAL_RANGES = {
    'loudness': (-60, 0),
    'popularity': (0, 100),
    'duration_ms': (0, float('inf'))
}

# Analysis parameters
POPULARITY_THRESHOLD = 70  # For popular song analysis
CORR_THRESHOLD = 0.7       # For feature correlation analysis

# Clustering parameters
N_CLUSTERS_RANGE = range(2, 11)  # Range for optimal cluster search
N_COMPONENTS = 3                 # For PCA visualization
N_TOP_FEATURES = 5              # Features to show in cluster profiles

# File paths
DATA_PATH = '../data/rolling_stones_spotify.csv'

# Visualization settings
plt.style.use('seaborn')
sns.set_palette("husl")
```

### 2.2 Data Loading Function
```python
def load_spotify_data(file_path: str) -> pd.DataFrame:
    """
    Load Rolling Stones Spotify data with appropriate data types.
    
    Parameters:
        file_path (str): Path to the Spotify data CSV file
        
    Returns:
        pd.DataFrame: Loaded dataframe with correct data types
    """
    # Define data types for columns
    dtypes = {
        'name': str,
        'album': str,
        'id': str,
        'uri': str,
        'track_number': int,
        'acousticness': float,
        'danceability': float,
        'energy': float,
        'instrumentalness': float,
        'liveness': float,
        'loudness': float,
        'speechiness': float,
        'tempo': float,
        'valence': float,
        'popularity': int,
        'duration_ms': int
    }
    
    # Read CSV with specified data types
    df = pd.read_csv(file_path, dtype=dtypes)
    
    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'])
    
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
        'name', 'album', 'release_date', 'track_number', 'id', 'uri',
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'speechiness', 'tempo', 'valence',
        'popularity', 'duration_ms'
    ]
    
    # Check for required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        print(f"Missing required columns: {missing_cols}")
        return False
    
    # Validate numeric features are within expected ranges
    range_validations = {
        'acousticness': (0, 1),
        'danceability': (0, 1),
        'energy': (0, 1),
        'instrumentalness': (0, 1),
        'liveness': (0, 1),
        'speechiness': (0, 1),
        'valence': (0, 1),
        'popularity': (0, 100)
    }
    
    for col, (min_val, max_val) in range_validations.items():
        if not df[col].between(min_val, max_val).all():
            print(f"Values out of range for {col}")
            return False
    
    return True
```

### 2.4 Feature Groups Definition
```python
# Define feature groups for analysis
AUDIO_FEATURES = [
    'acousticness', 'danceability', 'energy', 'instrumentalness',
    'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
]

METADATA_FEATURES = [
    'popularity', 'duration_ms', 'track_number'
]

CATEGORICAL_FEATURES = [
    'album'
]

TEMPORAL_FEATURES = [
    'release_date'
]
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
    print(df[AUDIO_FEATURES + METADATA_FEATURES].describe())
    print("\nAlbum Distribution:")
    print(df['album'].value_counts())
```

### 3.2 Data Loading Example
```python
# Load and validate data
df = load_spotify_data(DATA_PATH)
if validate_data_structure(df):
    get_data_overview(df)
else:
    raise ValueError("Data validation failed!")
```

## 4. Next Steps
After successfully setting up the environment and loading the data:
1. Proceed to data cleaning in `02_DATA_WRANGLING.md`
2. Follow the EDA process in `03_DATA_ANALYSIS.md`
3. Implement clustering in `04_MODELING.md`
