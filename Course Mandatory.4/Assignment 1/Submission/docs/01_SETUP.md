# Data Setup and Initial Configuration - My Notes

## Library Setup Notes

### Essential Libraries I'm Using
```python
# Core data processing libraries (with versions from requirements.txt)
import pandas as pd         # Data frames (v1.3.3)
import numpy as np          # Arrays and math (v1.21.4)
from scipy import stats    # Statistics (v1.7.2)

# Visualization libraries (tested versions)
import matplotlib.pyplot as plt  # Base plotting (v3.4.3)
import seaborn as sns           # Statistical viz (v0.11.2)
import plotly.express as px     # Interactive plots (v5.3.1)
import plotly.graph_objects as go  # Custom viz

# Configure warnings for data quality alerts
import warnings
warnings.filterwarnings('always')  # Show all warnings during setup

# Visualization settings for consistency
plt.style.use('seaborn')        # Clean, modern look
sns.set_palette('husl')         # Color-blind friendly palette
plt.rcParams.update({
    'figure.figsize': [12, 6],  # Standard figure size
    'figure.dpi': 100,          # Clear resolution
    'axes.grid': True,          # Show grids by default
    'axes.spines.top': False,   # Remove top spine
    'axes.spines.right': False  # Remove right spine
})

# Pandas display settings for better analysis
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', 100)      # Reasonable row limit
pd.set_option('display.float_format', '{:.2f}'.format)  # 2 decimal places
```

## Project Context Notes

### Background Research
```markdown
# AAL Case Study Notes

## Company Profile (from assignment)
- Founded: 2000
- Industry: Retail Clothing
- Market: Australia-wide
- Unique aspect: Multi-demographic focus

## Analysis Goals (from requirements)
1. Revenue mapping by state
2. Growth program development
3. Data-backed expansion planning

## Data Coverage
- Timeline: Q4 2020 (3 months)
- Geography: All states
- Customer segments: Full range
- Key metrics: Sales, Units, Timing

## Expected Deliverables
1. Revenue analysis
2. Customer insights
3. Growth strategy
4. Improvement plans
```

## Data Loading Process

### Initial Data Check (Week 1 Best Practices)
```python
# Function to safely load and validate data
def load_sales_data(filepath='AusApparalSales4thQrt2020.csv'):
    """Load and perform initial validation of sales data.
    
    Args:
        filepath (str): Path to the sales data CSV file
        
    Returns:
        pd.DataFrame: Validated sales data
        
    Raises:
        FileNotFoundError: If the data file is not found
        pd.errors.EmptyDataError: If the file is empty
    """
    try:
        # Attempt to load the data
        df = pd.read_csv(filepath)
        
        # Validate basic data requirements
        if df.empty:
            raise ValueError("Dataset is empty")
            
        # Required columns for our analysis
        required_cols = ['Date', 'State', 'Sales', 'Units']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Display dataset overview
        print("Dataset Overview:")
        print("-" * 50)
        
        # Basic information
        print("\nDataset Info:")
        df.info()
        
        # Preview data
        print("\nFirst few rows:")
        display(df.head())
        
        # Numerical summary
        print("\nBasic Statistics:")
        display(df.describe())
        
        # Additional quality checks
        print("\nData Quality Checks:")
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print(f"Missing values:\n{df.isnull().sum()}")
        print(f"Duplicate rows: {df.duplicated().sum()}")
        
        return df
        
    except FileNotFoundError:
        print(f"Error: Data file '{filepath}' not found")
        raise
    except pd.errors.EmptyDataError:
        print(f"Error: Data file '{filepath}' is empty")
        raise
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

# Load the data with validation
df = load_sales_data()
```

### Notes to Self
1. Watch for:
   - Date format consistency
   - State name standardization
   - Sales value ranges
   - Group categorization

2. Potential Issues:
   - Missing timestamps
   - Invalid sales amounts
   - Inconsistent state codes
   - Wrong demographic labels

3. Next Steps:
   - Clean missing values
   - Normalize sales data
   - Format dates properly
   - Group validation
