# Data Wrangling and Preparation

## 1. Data Quality Checks

### 1.1 Missing Value Analysis
```python
def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Check for missing values in the dataset.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.Series: Missing value counts by column
    """
    missing_counts = df.isnull().sum()
    missing_percentages = (missing_counts / len(df)) * 100
    
    missing_info = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing Percentage': missing_percentages
    })
    
    return missing_info[missing_info['Missing Count'] > 0]
```

### 1.2 Data Type Validation
```python
def validate_feature_ranges(df: pd.DataFrame) -> dict:
    """
    Validate value ranges for numerical features.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Dictionary with validation results
    """
    validations = {
        'satisfaction_level': (0, 1),
        'last_evaluation': (0, 1),
        'number_project': (0, 50),  # Reasonable max projects
        'average_montly_hours': (0, 400),  # Reasonable max hours
        'time_spend_company': (0, 50),  # Reasonable max years
        'Work_accident': (0, 1),
        'left': (0, 1),
        'promotion_last_5years': (0, 1)
    }
    
    results = {}
    for column, (min_val, max_val) in validations.items():
        invalid_values = df[~df[column].between(min_val, max_val)]
        results[column] = len(invalid_values)
    
    return results
```

### 1.3 Categorical Data Validation
```python
def validate_categorical_values(df: pd.DataFrame) -> dict:
    """
    Check for unexpected values in categorical columns.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Dictionary with unique values for each categorical column
    """
    categorical_columns = ['Department', 'salary']
    
    return {
        col: df[col].unique().tolist()
        for col in categorical_columns
    }
```

## 2. Data Cleaning

### 2.1 Handle Missing Values
```python
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with handled missing values
    """
    # Create copy to avoid modifying original data
    df_clean = df.copy()
    
    # For numerical columns, fill with median
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numerical_columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    # For categorical columns, fill with mode
    categorical_columns = ['Department', 'salary']
    for col in categorical_columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    
    return df_clean
```

### 2.2 Handle Outliers
```python
def detect_outliers(df: pd.DataFrame, columns: list) -> dict:
    """
    Detect outliers using IQR method.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        columns (list): List of columns to check for outliers
        
    Returns:
        dict: Dictionary with outlier counts for each column
    """
    outliers = {}
    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers[column] = len(df[(df[column] < lower_bound) | 
                                (df[column] > upper_bound)])
    
    return outliers
```

## 3. Data Preparation for Modeling

### 3.1 Categorical Variable Processing
```python
def preprocess_categorical_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pre-process categorical variables as per requirement 4.1.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Processed dataframe
    """
    # Separate categorical and numeric variables
    categorical_vars = ['Department', 'salary']
    numeric_vars = df.select_dtypes(include=['int64', 'float64']).columns
    numeric_vars = [col for col in numeric_vars if col not in categorical_vars]
    
    # Apply get_dummies() to categorical variables
    df_encoded = pd.get_dummies(df, columns=categorical_vars)
    
    print("Categorical variables encoded:")
    print(f"Original shape: {df.shape}")
    print(f"Encoded shape: {df_encoded.shape}")
    
    return df_encoded

### 3.2 Train-Test Split and SMOTE Implementation
```python
def prepare_modeling_data(df: pd.DataFrame) -> tuple:
    """
    Prepare data for modeling including train-test split and SMOTE.
    Implementation of requirements 4.2 and 4.3.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        tuple: (X_train_balanced, X_test, y_train_balanced, y_test)
    """
    # Separate features and target
    X = df.drop('left', axis=1)
    y = df['left']
    
    # Requirement 4.2: Stratified split (80:20) with random_state=123
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=123,  # As per requirements
        stratify=y
    )
    
    print("Train-test split summary:")
    print(f"Training set shape: {X_train.shape}")
    print(f"Testing set shape: {X_test.shape}")
    
    # Requirement 4.3: Apply SMOTE to handle class imbalance
    smote = SMOTE(random_state=123)  # As per requirements
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    print("\nClass distribution before SMOTE:")
    print(pd.Series(y_train).value_counts(normalize=True))
    print("\nClass distribution after SMOTE:")
    print(pd.Series(y_train_balanced).value_counts(normalize=True))
    
    return X_train_balanced, X_test, y_train_balanced, y_test

## 4. Feature Engineering

### 3.1 Categorical Encoding
```python
def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categorical features using one-hot encoding.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with encoded categorical features
    """
    # Create dummy variables for Department and salary
    df_encoded = pd.get_dummies(df, columns=['Department', 'salary'], 
                              prefix=['dept', 'salary'])
    
    return df_encoded
```

### 3.2 Feature Scaling
```python
def scale_numerical_features(df: pd.DataFrame, 
                           exclude_cols: list = None) -> pd.DataFrame:
    """
    Scale numerical features using StandardScaler.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        exclude_cols (list): Columns to exclude from scaling
        
    Returns:
        pd.DataFrame: Dataframe with scaled features
    """
    if exclude_cols is None:
        exclude_cols = []
    
    # Select numerical columns for scaling
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
    cols_to_scale = [col for col in numerical_cols if col not in exclude_cols]
    
    # Scale features
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
    
    return df_scaled
```

## 4. Data Preparation for Modeling

### 4.1 Train-Test Split and SMOTE Implementation
```python
def prepare_data_for_modeling(df: pd.DataFrame) -> tuple:
    """
    Prepare data for modeling including train-test split and SMOTE.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        tuple: (X_train_balanced, X_test, y_train_balanced, y_test)
    """
    # Separate features and target
    X = df.drop('left', axis=1)
    y = df['left']
    
    # Step 4.2: Stratified split (80:20) with random_state=123
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=123,  # As per requirements
        stratify=y
    )
    
    # Step 4.3: Apply SMOTE to handle class imbalance
    smote = SMOTE(random_state=123)  # As per requirements
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    # Print class distribution before and after SMOTE
    print("Original class distribution:")
    print(y_train.value_counts(normalize=True))
    print("\nBalanced class distribution:")
    print(pd.Series(y_train_balanced).value_counts(normalize=True))
    
    return X_train_balanced, X_test, y_train_balanced, y_test
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    return X_resampled, y_resampled
```

## 5. Data Preparation Pipeline

### 5.1 Complete Pipeline
```python
def prepare_data_for_modeling(df: pd.DataFrame) -> tuple:
    """
    Complete data preparation pipeline.
    
    Parameters:
        df (pd.DataFrame): Raw input dataframe
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    # 1. Clean data
    df_clean = handle_missing_values(df)
    
    # 2. Encode categorical features
    df_encoded = encode_categorical_features(df_clean)
    
    # 3. Scale features
    df_scaled = scale_numerical_features(
        df_encoded, 
        exclude_cols=['left']
    )
    
    # 4. Split features and target
    X = df_scaled.drop('left', axis=1)
    y = df_scaled['left']
    
    # 5. Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=TEST_SIZE, 
        random_state=RANDOM_SEED,
        stratify=y
    )
    
    # 6. Apply SMOTE to training data
    X_train_resampled, y_train_resampled = apply_smote(X_train, y_train)
    
    return X_train_resampled, X_test, y_train_resampled, y_test
```

### 5.2 Usage Example
```python
# Load data
df = load_hr_data(DATA_PATH)

# Check data quality
missing_info = check_missing_values(df)
print("Missing Values:\n", missing_info)

range_validations = validate_feature_ranges(df)
print("\nFeature Range Validations:\n", range_validations)

categorical_values = validate_categorical_values(df)
print("\nCategorical Values:\n", categorical_values)

# Prepare data for modeling
X_train, X_test, y_train, y_test = prepare_data_for_modeling(df)
print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)
```

## 6. Next Steps
After completing data wrangling:
1. Proceed to exploratory data analysis in `03_DATA_ANALYSIS.md`
2. Use prepared data for modeling in `04_MODELING.md`
