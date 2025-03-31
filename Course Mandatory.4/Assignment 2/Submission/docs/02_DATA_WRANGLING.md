# Marketing Campaign Analysis - Data Wrangling

## Data Preparation Framework

### 1. Data Loading and Initial Check
```python
def load_marketing_data(file_path='marketing_data.csv'):
    """Load and perform initial inspection of marketing data.
    
    Args:
        file_path (str): Path to the marketing data CSV file
        
    Returns:
        pd.DataFrame: Raw marketing campaign dataset
    """
    try:
        df = pd.read_csv(file_path)
        print("Dataset shape:", df.shape)
        print("\nData types:")
        print(df.dtypes)
        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise
```

### 2. Date Format Validation
```python
def validate_dates(df):
    """Validate and convert date fields in the dataset.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        pd.DataFrame: Dataset with validated dates
    """
    try:
        df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
        print("Date range:")
        print(f"Earliest date: {df['Dt_Customer'].min()}")
        print(f"Latest date: {df['Dt_Customer'].max()}")
        return df
    except Exception as e:
        print(f"Error validating dates: {str(e)}")
        raise
```

### 3. Missing Value Analysis
```python
# My approach to handling missing values

# First, understand the missing data patterns
def analyze_missing_data(df):
    """Analyze missing value patterns in the dataset.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Missing value statistics including total count and patterns
    """
    # Calculate missing value statistics
    total_missing = df.isnull().sum().sum()
    missing_by_col = df.isnull().sum()
    missing_patterns = df.isnull().sum(axis=1).value_counts()
    
    # Print summary
    print('Total missing values:', total_missing)
    print('\nMissing by column:')
    print(missing_by_col[missing_by_col > 0])
    print('\nMissing patterns:')
    print(missing_patterns)
    
    return {
        'total_missing': total_missing,
        'missing_by_column': missing_by_col[missing_by_col > 0].to_dict(),
        'missing_patterns': missing_patterns.to_dict()
    }

# Income imputation - my strategy
def impute_income(df):
    """My method for income imputation"""
    # Group by education and marital status
    income_means = df.groupby(['Education', 'Marital_Status'])['Income'].mean()
    print('Average income by group:')
    print(income_means)
    
    # Create imputation map
    impute_map = df.groupby(['Education', 'Marital_Status'])['Income'].transform('mean')
    
    # Apply imputation
    df['Income'] = df['Income'].fillna(impute_map)
    
    return df
    # What factors influence income?
    # How to maintain data distribution?
    return df

# Education and marital status cleaning
def clean_categories(df):
    """Guide: How to standardize categories?"""
    # Education categories
    # Marital status grouping
    return df
```

### Feature Creation - My Approach
```python
# Creating useful features for my analysis

def create_analysis_features(df):
    """Create derived features for analysis.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        pd.DataFrame: Dataset with additional derived features
    """
    # Family size
    df['Total_Children'] = df['Kidhome'] + df['Teenhome']
    
    # Customer age
    from datetime import datetime
    current_year = datetime.now().year
    df['Age'] = current_year - df['Year_Birth']
    
    # Total spending
    product_columns = [
        'MntWines', 'MntFruits', 'MntMeatProducts',
        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
    ]
    df['Total_Spending'] = df[product_columns].sum(axis=1)
    
    # Purchase channels
    purchase_columns = [
        'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases'
    ]
    df['Total_Purchases'] = df[purchase_columns].sum(axis=1)
    
    # Print summary statistics
    print('Feature Statistics:')
    for col in ['Total_Children', 'Age', 'Total_Spending', 'Total_Purchases']:
        print(f"\n{col}:")
        print(df[col].describe())
    
    return df
    
    return df
```

### Outlier Analysis - My Method
```python
# My approach to handling outliers

def analyze_outliers(df, columns):
    """Detect and analyze outliers in specified columns.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        columns (list): List of columns to analyze for outliers
        
    Returns:
        dict: Outlier statistics for each column
    """
    outlier_stats = {}
    
    for col in columns:
        # Calculate bounds
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Identify outliers
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        
        # Store statistics
        outlier_stats[col] = {
            'count': len(outliers),
            'percentage': (len(outliers)/len(df))*100,
            'bounds': {'lower': lower_bound, 'upper': upper_bound}
        }
        
        # Print summary
        print(f'\nOutliers in {col}:')
        print(f'Count: {outlier_stats[col]["count"]}')
        print(f'Percentage: {outlier_stats[col]["percentage"]:.2f}%')
        
        # Visualize
        plt.figure(figsize=(10, 4))
        plt.subplot(121)
        sns.boxplot(x=df[col])
        plt.title(f'Boxplot of {col}')
        
        plt.subplot(122)
        sns.histplot(df[col], bins=30)
        plt.title(f'Distribution of {col}')
        plt.tight_layout()
        plt.show()
    
    return outlier_stats

def treat_outliers(df, columns):
    """My outlier treatment strategy"""
    df_clean = df.copy()
    
    for col in columns:
        # Calculate bounds
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        # Cap outliers
        df_clean.loc[df_clean[col] < lower, col] = lower
        df_clean.loc[df_clean[col] > upper, col] = upper
        
        print(f'\nTreated outliers in {col}')
        print('Before vs After:')
        print(df[col].describe()[[['min', 'max']])
        print(df_clean[col].describe()[[['min', 'max']])
    
    return df_clean
```

### Variable Encoding - My Implementation

# My approach to encoding variables

## Feature Engineering

### 1. Derived Variables
```python
# Total children
df['Total_Children'] = df['Kidhome'] + df['Teenhome']

# Customer age
df['Age'] = current_year - df['Year_Birth']

# Total spending
spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
df['Total_Spending'] = df[spending_cols].sum(axis=1)

# Total purchases
df['Total_Purchases'] = df['NumWebPurchases'] + df['NumStorePurchases'] + df['NumCatalogPurchases']
```

### 2. Data Cleaning
```python
# Education category cleaning
def clean_education(df):
    """Standardize education categories in the dataset.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        pd.DataFrame: Dataset with standardized education categories
    """
    education_map = {
        'Basic': 'Basic',
        'Graduation': 'Graduate',
        '2n Cycle': 'Post Graduate',
        'Master': 'Post Graduate',
        'PhD': 'Post Graduate'
    }
    
    # Verify all categories are mapped
    unmapped = set(df['Education'].unique()) - set(education_map.keys())
    if unmapped:
        raise ValueError(f"Unmapped education categories found: {unmapped}")
    
    df['Education'] = df['Education'].map(education_map)
    print("\nEducation category counts:")
    print(df['Education'].value_counts())
    
    return df

# Marital status cleaning
def clean_marital_status(df):
    """Standardize marital status categories"""
    marital_map = {
        'Single': 'Single',
        'Divorced': 'Single',
        'Widow': 'Single',
        'Together': 'Partnered',
        'Married': 'Partnered'
    }
    df['Marital_Status'] = df['Marital_Status'].map(marital_map)
    return df
```

### 3. Outlier Treatment
```python
# Identify outliers using IQR method
def identify_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

# Handle outliers
def handle_outliers(df, column):
    """Cap outliers at Q1-1.5*IQR and Q3+1.5*IQR"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df[column] = df[column].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR)
    return df
```

### 4. Variable Encoding
```python
# Ordinal encoding for education
def encode_variables(df):
    """Encode categorical variables for analysis.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        pd.DataFrame: Dataset with encoded categorical variables
    """
    # Ordinal encoding for education
    education_order = ['Basic', 'Graduate', 'Post Graduate']
    df['Education_Encoded'] = pd.Categorical(
        df['Education'],
        categories=education_order,
        ordered=True
    ).codes
    
    # One-hot encoding for categorical variables
    categorical_cols = ['Marital_Status', 'Country']
    df_encoded = pd.get_dummies(
        df,
        columns=categorical_cols,
        prefix=categorical_cols
    )
    
    # Print encoding summary
    print("\nEducation encoding:")
    print(pd.crosstab(df['Education'], df['Education_Encoded']))
    
    print("\nNew encoded columns:")
    new_cols = [col for col in df_encoded.columns if col not in df.columns]
    print(new_cols)
    
    return df_encoded
```

## Data Validation

### 1. Post-Processing Checks
```python
# Verify derived variables
def validate_derived_vars(df):
    print("Derived variable statistics:")
    print(df[['Total_Children', 'Age', 'Total_Spending', 'Total_Purchases']].describe())

# Check encoded variables
def validate_encoding(df):
    print("\nEncoded variables check:")
    print(df.filter(regex='^(Marital_Status_|Education_)').head())
```

### 2. Final Data Quality Check
```python
# Comprehensive data quality report
def generate_quality_report(df):
    """Generate comprehensive data quality report.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Data quality metrics and statistics
    """
    report = {
        'missing_values': {
            'total': df.isnull().sum().sum(),
            'by_column': df.isnull().sum().to_dict()
        },
        'invalid_values': {
            'negative_spending': (df['Total_Spending'] < 0).sum(),
            'zero_spending': (df['Total_Spending'] == 0).sum(),
            'invalid_age': (df['Age'] < 18).sum(),
            'future_dates': (df['Dt_Customer'] > datetime.now()).sum()
        },
        'categorical_counts': {
            'education': df['Education'].value_counts().to_dict(),
            'marital_status': df['Marital_Status'].value_counts().to_dict()
        }
    }
    
    # Print summary
    print("Data Quality Report:")
    print(f"Total missing values: {report['missing_values']['total']}")
    print(f"Invalid ages: {report['invalid_values']['invalid_age']}")
    print(f"Zero spending records: {report['invalid_values']['zero_spending']}")
    
    return report
```

### Next Steps Guide
1. What statistical analysis is needed?
2. Which correlations to explore?
3. How to test hypotheses?
4. What visualizations will help?
