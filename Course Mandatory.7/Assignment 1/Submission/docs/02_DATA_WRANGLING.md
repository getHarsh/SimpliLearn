# Data Wrangling Process

This document outlines the comprehensive data cleaning, transformation, and preprocessing steps implemented for the Lending Club Loan Default Prediction project.

## Data Quality Assessment

### Missing Value Analysis

The initial data quality assessment involved checking for missing values in all columns:

```python
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_data = pd.concat([missing_values, missing_percentage], axis=1)
missing_data.columns = ['Missing Values', 'Percentage']
```

For columns with missing values, I implemented targeted strategies based on the nature of the feature:

- **Numerical Features**: Imputed with median values to minimize the impact of outliers
- **Categorical Features**: Filled with the most frequent category

### Outlier Detection and Treatment

I identified outliers using the Interquartile Range (IQR) method:

```python
for col in numerical_features:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
```

For extreme outliers that could negatively impact model performance:
- Values greater than the upper bound were capped at the upper bound
- Values less than the lower bound were set to the lower bound

This approach preserves the information that the value is extreme while reducing the skewing effect on the model.

## Data Transformation

### Categorical Variable Encoding

The primary categorical variable in this dataset is `purpose`, which indicates the reason for the loan. I applied One-Hot Encoding to transform these categories into binary features:

```python
categorical_cols = ['purpose']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_cols)
    ]
)
```

The `drop='first'` parameter was used to avoid the dummy variable trap, where one category is omitted as it can be inferred from the others.

### Numerical Feature Normalization

To ensure all numerical features contribute equally to the model and to improve training stability, I applied StandardScaler to normalize features:

```python
numerical_cols = [col for col in X.columns if col not in categorical_cols]
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols)
    ]
)
```

This transformation scales each feature to have a mean of 0 and standard deviation of 1, which is particularly important for deep learning models.

## Feature Engineering

### Correlation Analysis

I calculated a correlation matrix to identify highly correlated features:

```python
correlation_matrix = df.corr()
high_corr_features = set()
for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > 0.75:
            high_corr_features.add(correlation_matrix.columns[i])
```

Features with correlation coefficients exceeding 0.75 were identified for potential removal to reduce multicollinearity issues.

### Feature Selection

Based on the correlation analysis, I removed highly correlated features to simplify the model while preserving predictive power:

```python
df_processed = df.drop(columns=high_corr_features, errors='ignore')
```

The `errors='ignore'` parameter ensures the operation doesn't fail if some columns were already removed.

## Class Imbalance Handling

The target variable `not.fully.paid` showed significant class imbalance, with defaults (class 1) representing only a small portion of the dataset. To address this, I implemented Synthetic Minority Over-sampling Technique (SMOTE):

```python
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_preprocessed, y_train)
```

SMOTE creates synthetic examples of the minority class (defaults) by interpolating between existing minority class examples, resulting in a balanced training dataset.

## Preprocessing Pipeline

To ensure reproducibility and consistent application of transformations to both training and test data, I created a preprocessing pipeline:

```python
# Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(drop='first'), categorical_cols)
    ])

# Preprocess the data
X_train_preprocessed = preprocessor.fit_transform(X_train)
X_test_preprocessed = preprocessor.transform(X_test)

# Save the preprocessor for future use
with open('models/preprocessor.pkl', 'wb') as file:
    pickle.dump(preprocessor, file)
```

This pipeline ensures that:
1. All transformations are applied consistently
2. No information from the test set leaks into the training process
3. The same transformations can be applied to new data during model deployment

## Data Split Strategy

I implemented a stratified train-test split to maintain the same class distribution in both subsets:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

Using `stratify=y` ensures that both training and test sets have approximately the same proportion of loan defaults, which is crucial for reliable model evaluation.

## Final Preprocessed Dataset

The final preprocessed dataset includes:
- Encoded categorical variables
- Normalized numerical features
- Removed highly correlated features
- Balanced class distribution (in the training set)

This comprehensive preprocessing approach ensures the data is optimally prepared for training the deep learning model while addressing key challenges like class imbalance, multicollinearity, and feature scaling.
