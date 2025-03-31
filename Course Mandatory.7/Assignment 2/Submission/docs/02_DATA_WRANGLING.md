# Data Wrangling Process

This document details the data cleaning and preprocessing steps I undertook for the House Loan Data Analysis project.

## Overview of the Raw Data

The initial dataset contained loan application information with various features about applicants and their loan history. Before building any predictive models, I needed to clean and transform this data to make it suitable for analysis.

## Step 1: Loading and Initial Assessment

I began by loading the dataset and performing an initial assessment:

```python
df = pd.read_csv('loan_data.csv')
print(f"Dataset shape: {df.shape}")
df.info()
df.head()
```

This initial examination revealed the overall structure of the data, including:
- Total number of records and features
- Data types of each column
- Presence of missing values
- Sample records to understand the nature of the data

## Step 2: Handling Missing Values

Missing values were a significant concern in this dataset. I identified all columns with null values:

```python
null_values = df.isnull().sum()
null_percentages = (null_values / len(df)) * 100
```

I addressed missing values using different strategies based on the nature of each feature:

### Numerical Features
- For most numerical columns, I used median imputation as it's robust to outliers
- For some time-based numerical features, I used forward fill or backward fill where appropriate

### Categorical Features
- For categorical columns, I used mode imputation (most frequent value)
- For columns with high percentage of missing values (>30%), I considered creating a "Missing" category

I implemented these strategies using the custom utility function `handle_missing_values()`:

```python
df_cleaned = handle_missing_values(df)
```

## Step 3: Handling Outliers

Outliers can significantly impact model training, especially in financial data. I detected and handled outliers in numerical features using the IQR (Interquartile Range) method:

1. Calculated Q1 (25th percentile) and Q3 (75th percentile)
2. Defined the IQR as Q3 - Q1
3. Identified outliers as values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR
4. Capped outliers at these boundaries

This approach preserved the overall distribution while minimizing the impact of extreme values:

```python
df_cleaned = handle_outliers(df_cleaned, numerical_cols)
```

## Step 4: Feature Engineering

I engineered new features to potentially improve model performance:

### Derived Features
- Calculated debt-to-income ratios
- Created age-based categories
- Derived features from date columns (loan age, time since last credit inquiry, etc.)

### Feature Transformation
- Applied log transformation to highly skewed numerical features
- Binned continuous variables where appropriate

## Step 5: Handling Categorical Variables

I encoded categorical variables to make them suitable for the deep learning model:

1. For binary categorical variables (2 categories), I used Label Encoding:
   ```python
   le = LabelEncoder()
   df_cleaned['binary_cat_col'] = le.fit_transform(df_cleaned['binary_cat_col'])
   ```

2. For multi-class categorical variables (>2 categories), I used One-Hot Encoding:
   ```python
   # One-hot encoding with dropping the first category
   encoded_features, encoders = encode_categorical_features(df_cleaned, categorical_cols)
   ```

## Step 6: Feature Selection

To reduce dimensionality and improve model performance, I:

1. Calculated the correlation matrix for numerical features
2. Identified and removed highly correlated features (threshold > 0.75)
   ```python
   to_drop = identify_high_correlation_features(corr_matrix, threshold=0.75)
   df_cleaned = df_cleaned.drop(columns=to_drop)
   ```

3. Kept only the most informative features based on statistical tests and domain knowledge

## Step 7: Handling Class Imbalance

The target variable ('TARGET') showed significant class imbalance:

1. I first quantified the imbalance:
   ```python
   target_counts = df_cleaned['TARGET'].value_counts()
   target_percentages = (target_counts / len(df_cleaned)) * 100
   ```

2. I addressed this imbalance during model training using SMOTE (Synthetic Minority Over-sampling Technique):
   ```python
   smote = SMOTE(random_state=42)
   X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
   ```

## Step 8: Feature Scaling

For the deep learning model to work effectively, I scaled the numerical features:

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_balanced)
X_test_scaled = scaler.transform(X_test)
```

This ensures all features have mean=0 and standard deviation=1, preventing features with larger scales from dominating the model training.

## Step 9: Train-Test Split

I split the data into training and testing sets:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

Using `stratify=y` ensured that both training and testing sets maintained the same class distribution as the original dataset.

## Data Quality Assurance

Throughout the process, I performed quality checks:
- Verified that missing values were properly handled
- Confirmed that categorical encodings were properly applied
- Ensured that the dimensionality of the data was appropriate
- Validated that the class distribution was improved after applying SMOTE

## Challenges and Solutions

1. **High Cardinality Categories**
   - Some categorical features had many unique values
   - Solution: Grouped less frequent categories into an "Other" category

2. **Skewed Numerical Distributions**
   - Many numerical features were highly skewed
   - Solution: Applied log transformations to normalize distributions

3. **Temporal Features**
   - Date-related features required special handling
   - Solution: Extracted meaningful components like month, year, and day of week

## Final Dataset Characteristics

After all preprocessing steps, the final dataset had:
- No missing values
- Appropriately scaled numerical features
- Properly encoded categorical features
- Reduced feature dimensionality (after removing highly correlated features)
- Balanced class distribution in the training set (after SMOTE)

This clean, processed dataset was now ready for model development.