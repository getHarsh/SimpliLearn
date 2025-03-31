# Data Wrangling Study Notes - AAL Project

## Week 3 Review: Data Quality Assessment
*Data Cleaning Techniques*

### My Data Quality Checklist
```markdown
Learned from practice exercises:
1. Missing data detection ✓
2. Incorrect entry validation ✓
3. Numerical data scaling ✓
4. Data chunking strategy ✓

Key Tools:
- isna()/notna() for nulls
- normalize() for scaling
- groupby() for segmentation
```

## Missing Value Detection 

```python
def analyze_data_quality(df):
    """Perform comprehensive data quality analysis.
    
    Args:
        df (pd.DataFrame): Input dataframe to analyze
        
    Returns:
        dict: Dictionary containing quality metrics
    """
    try:
        quality_metrics = {}
        
        # Missing data analysis
        print("Missing Data Analysis:")
        print("-" * 50)
        
        # Calculate missing value metrics
        missing = df.isna().sum()
        valid = df.notna().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        
        # Store metrics
        quality_metrics['missing'] = missing
        quality_metrics['valid'] = valid
        quality_metrics['missing_pct'] = missing_pct
        
        # Display results
        print("\nMissing Data Summary:")
        for col in df.columns:
            print(f"{col}:")
            print(f"  Missing: {missing[col]} ({missing_pct[col]}%)")
            print(f"  Valid: {valid[col]}")
        
        # Duplicate analysis
        duplicates = df.duplicated()
        dup_count = duplicates.sum()
        dup_pct = (dup_count / len(df) * 100).round(2)
        
        quality_metrics['duplicates'] = dup_count
        quality_metrics['duplicate_pct'] = dup_pct
        
        print(f"\nDuplicate Records:")
        print(f"Count: {dup_count} ({dup_pct}% of data)")
        
        if dup_count > 0:
            print("\nExample Duplicates:")
            display(df[duplicates].head())
            
        return quality_metrics
        
    except Exception as e:
        print(f"Error in data quality analysis: {str(e)}")
        raise

# Run quality analysis
quality_metrics = analyze_data_quality(df)
```

## Data Cleaning Strategy 

```markdown
### My Cleaning Approach

1. Numerical Data (Sales/Units)
   - Using median for nulls 
   - Why? More robust than mean for skewed data
   
2. Categories (State/Group)
   - Mode imputation makes sense here
   - Preserves actual category values

3. Validation Checklist
   ✓ No duplicate sales records
   ✓ Q4 2020 dates only
   ✓ Positive sales values
   ✓ Valid Australian states
   ✓ Correct demographic labels
```

## Normalization Implementation (Week 4 Practice)

```python
def normalize_numeric_data(df, columns=['Sales', 'Units'], method='zscore'):
    """Normalize numeric columns using specified method.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): List of columns to normalize
        method (str): Normalization method ('zscore' or 'minmax')
        
    Returns:
        pd.DataFrame: DataFrame with added normalized columns
    """
    try:
        df = df.copy()  # Avoid modifying original
        
        def zscore_normalize(column):
            """Z-score normalization: (x - mean) / std"""
            return (column - column.mean()) / column.std()
        
        def minmax_normalize(column):
            """Min-max normalization: (x - min) / (max - min)"""
            return (column - column.min()) / (column.max() - column.min())
        
        
        # Select normalization function
        norm_func = zscore_normalize if method == 'zscore' else minmax_normalize
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns not found: {missing_cols}")
        
        # Apply normalization
        for col in columns:
            # Verify numeric
            if not np.issubdtype(df[col].dtype, np.number):
                raise ValueError(f"Column {col} is not numeric")
                
            # Check for infinite values
            if df[col].isin([np.inf, -np.inf]).any():
                print(f"Warning: Infinite values found in {col}")
                
            # Normalize and add new column
            df[f'{col}_normalized'] = norm_func(df[col])
        
        # Validation summary
        print(f"Normalization Summary ({method}):")
        print("-" * 50)
        
        for col in columns:
            orig = df[col]
            norm = df[f'{col}_normalized']
            
            print(f"\n{col}:")
            print(f"  Original - mean: {orig.mean():.2f}, std: {orig.std():.2f}")
            print(f"  Normalized - mean: {norm.mean():.2f}, std: {norm.std():.2f}")
        
        return df
        
    except Exception as e:
        print(f"Error in normalization: {str(e)}")
        raise

# Apply normalization with validation
df = normalize_numeric_data(df, method='zscore')
```

## GroupBy Analysis Practice 

```python
def perform_group_analysis(df, group_columns=['State', 'Group']):
    """Perform hierarchical group analysis on sales data.
    
    Args:
        df (pd.DataFrame): Input dataframe
        group_columns (list): Columns to group by
        
    Returns:
        dict: Dictionary containing various group metrics
    """
    try:
        metrics = {}
        
        # Define aggregation functions
        agg_funcs = {
            'Sales': ['sum', 'mean', 'count', 'std'],
            'Units': ['sum', 'mean', 'std']
        }
        
        # Single-level analysis
        for col in group_columns:
            if col not in df.columns:
                raise ValueError(f"Column not found: {col}")
                
            metrics[col] = df.groupby(col).agg(agg_funcs).round(2)
            
            # Add derived metrics
            metrics[f'{col}_summary'] = {
                'total_sales': df.groupby(col)['Sales'].sum().sum(),
                'avg_transaction': (df.groupby(col)['Sales'].sum() / 
                                  df.groupby(col)['Units'].sum()).round(2),
                'sales_concentration': (df.groupby(col)['Sales'].sum() / 
                                      df['Sales'].sum() * 100).round(2)
            }
        
        # Multi-level analysis
        metrics['combined'] = df.groupby(group_columns).agg(agg_funcs).round(2)
        
        # Display results
        print("Group Analysis Results:")
        print("-" * 50)
        
        for key, value in metrics.items():
            if isinstance(value, pd.DataFrame):
                print(f"\n{key.title()} Analysis:")
                display(value)
            elif isinstance(value, dict):
                print(f"\n{key.title()} Summary:")
                for metric, val in value.items():
                    print(f"  {metric}: {val}")
        
        return metrics
        
    except Exception as e:
        print(f"Error in group analysis: {str(e)}")
        raise

# Perform group analysis
group_metrics = perform_group_analysis(df)
```

## Key Learnings 

```markdown
### GroupBy Insights

1. Benefits Found:
   - Easy state/group analysis
   - Multi-level insights
   - Flexible aggregation

2. Important Patterns:
   - State performance varies
   - Clear demographic trends
   - Interesting combinations

3. Best Practices:
   ✓ Use hierarchical grouping
   ✓ Cross-tab when needed
   ✓ Keep detail level

4. Process Notes:
   1. Start broad (states)
   2. Go deeper (groups)
   3. Combine for insights
```

### Notes to Self
1. Remember to document cleaning steps
2. Keep original data backup
3. Validate after each step
4. Check business logic

### Next Steps
- Move to statistical analysis
- Prepare visualization data
- Document key findings
