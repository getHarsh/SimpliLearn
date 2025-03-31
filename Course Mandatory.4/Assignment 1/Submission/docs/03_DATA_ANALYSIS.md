# Statistical Analysis Study Notes - AAL Project

## Descriptive Statistics Analysis
*Personal Study Notes: Statistical Analysis*

### Analysis Approach
```markdown
## Analysis Framework

### Learning Goals
1. Master descriptive statistics
2. Understand performance metrics
3. Practice time series analysis
4. Develop business insights

### Key Methods Learned
- Central tendency (mean, median, mode)
- Spread measures (std, IQR)
- Distribution shapes (skewness)
- Time patterns (trends, cycles)
```

### Basic Statistics Framework

```python
def generate_time_reports(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Generate comprehensive time-based sales reports.
    
    Args:
        df: Input dataframe with sales data
        
    Returns:
        Dictionary containing weekly, monthly, and quarterly reports
    """
    try:
        reports = {}
        
        # Weekly Report
        weekly_metrics = df.groupby(['Week', 'Group']).agg({
            'Sales': ['sum', 'mean', 'count', 'std'],
            'Units': ['sum', 'mean']
        }).round(2)
        
        weekly_metrics.columns = ['Total_Sales', 'Avg_Sale', 'Transactions', 'Sales_Std',
                                'Total_Units', 'Avg_Units']
        reports['weekly'] = weekly_metrics
        
        # Monthly Report
        monthly_metrics = df.groupby(['Month', 'Group']).agg({
            'Sales': ['sum', 'mean', 'count', 'std'],
            'Units': ['sum', 'mean']
        }).round(2)
        
        monthly_metrics.columns = ['Total_Sales', 'Avg_Sale', 'Transactions', 'Sales_Std',
                                 'Total_Units', 'Avg_Units']
        reports['monthly'] = monthly_metrics
        
        # Quarterly Report
        quarterly_metrics = df.groupby(['Quarter', 'Group']).agg({
            'Sales': ['sum', 'mean', 'count', 'std'],
            'Units': ['sum', 'mean']
        }).round(2)
        
        quarterly_metrics.columns = ['Total_Sales', 'Avg_Sale', 'Transactions', 'Sales_Std',
                                   'Total_Units', 'Avg_Units']
        reports['quarterly'] = quarterly_metrics
        
        # Display Reports
        print("\nWeekly Performance Report:")
        print("-" * 50)
        display(reports['weekly'])
        
        print("\nMonthly Performance Report:")
        print("-" * 50)
        display(reports['monthly'])
        
        print("\nQuarterly Performance Report:")
        print("-" * 50)
        display(reports['quarterly'])
        
        return reports
        
    except Exception as e:
        print(f"Error generating time reports: {str(e)}")
        raise

# Generate reports
time_reports = generate_time_reports(df)

def analyze_distribution(df, columns=['Sales', 'Units']):
    """Perform comprehensive distribution analysis on numeric columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): Numeric columns to analyze
        
    Returns:
        tuple: (basic_stats, advanced_stats, distribution_tests)
    """
    try:
        # Validate input columns
        for col in columns:
            if col not in df.columns:
                raise ValueError(f"Column not found: {col}")
            if not np.issubdtype(df[col].dtype, np.number):
                raise ValueError(f"Column {col} is not numeric")
        
        # Basic descriptive statistics
        basic_stats = df[columns].describe()
        
        # Advanced distribution metrics
        adv_stats = pd.DataFrame(index=columns)
        
        for col in columns:
            data = df[col].dropna()
            
            # Shape metrics
            adv_stats.loc[col, 'Skewness'] = stats.skew(data)
            adv_stats.loc[col, 'Kurtosis'] = stats.kurtosis(data)
            
            # Spread metrics
            adv_stats.loc[col, 'IQR'] = np.percentile(data, 75) - np.percentile(data, 25)
            adv_stats.loc[col, 'CV'] = np.std(data) / np.mean(data) * 100
            
            # Additional metrics
            adv_stats.loc[col, 'Range'] = data.max() - data.min()
            adv_stats.loc[col, 'MAD'] = np.mean(np.abs(data - np.mean(data)))
        
        # Distribution tests
        dist_tests = pd.DataFrame(index=columns)
        
        for col in columns:
            data = df[col].dropna()
            
            # Normality tests
            _, p_value = stats.normaltest(data)
            dist_tests.loc[col, 'Normal_pvalue'] = p_value
            
            # Outlier detection (Z-score method)
            z_scores = np.abs(stats.zscore(data))
            dist_tests.loc[col, 'Outliers_zscore'] = np.sum(z_scores > 3)
            
            # Outlier detection (IQR method)
            Q1 = np.percentile(data, 25)
            Q3 = np.percentile(data, 75)
            IQR = Q3 - Q1
            outliers_iqr = np.sum((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR)))
            dist_tests.loc[col, 'Outliers_IQR'] = outliers_iqr
        
        # Display results
        print("Distribution Analysis Results:")
        print("-" * 50)
        
        print("\nBasic Statistics:")
        display(basic_stats)
        
        print("\nAdvanced Metrics:")
        display(adv_stats)
        
        print("\nDistribution Tests:")
        display(dist_tests)
        
        return basic_stats, adv_stats, dist_tests
        
    except Exception as e:
        print(f"Error in distribution analysis: {str(e)}")
        raise

# Perform distribution analysis
basic_stats, adv_stats, dist_tests = analyze_distribution(df)
```

### Performance Analysis Framework

```python
def analyze_performance(df, group_cols=['State', 'Group'], metric_cols=['Sales', 'Units']):
    """Analyze performance metrics across different groupings.
    
    Args:
        df (pd.DataFrame): Input dataframe
        group_cols (list): Columns to group by
        metric_cols (list): Metrics to analyze
        
    Returns:
        dict: Dictionary containing performance metrics
    """
    try:
        performance = {}
        
        # Validate inputs
        for col in group_cols + metric_cols:
            if col not in df.columns:
                raise ValueError(f"Column not found: {col}")
        
        # Define aggregation functions
        agg_funcs = {
            'sum': 'Total',
            'mean': 'Average',
            'count': 'Transactions',
            'std': 'Variability',
            'min': 'Minimum',
            'max': 'Maximum'
        }
        
        # Analyze each grouping
        for group_col in group_cols:
            metrics = {}
            
            # Basic metrics
            for metric_col in metric_cols:
                group_data = df.groupby(group_col)[metric_col].agg(list(agg_funcs.keys()))
                group_data = group_data.round(2)
                
                # Rename columns with meaningful names
                group_data.columns = [f"{agg_funcs[func]}_{metric_col}" for func in agg_funcs.keys()]
                
                metrics[metric_col] = group_data
            
            # Additional derived metrics
            group_summary = pd.DataFrame(index=df[group_col].unique())
            
            # Market share
            group_summary['Market_Share'] = (df.groupby(group_col)['Sales'].sum() / 
                                           df['Sales'].sum() * 100).round(2)
            
            # Average transaction value
            group_summary['Avg_Transaction'] = (df.groupby(group_col)['Sales'].sum() / 
                                              df.groupby(group_col)['Sales'].count()).round(2)
            
            # Growth potential (gap to leader)
            max_sales = df.groupby(group_col)['Sales'].sum().max()
            group_summary['Growth_Potential'] = ((max_sales - df.groupby(group_col)['Sales'].sum()) / 
                                               max_sales * 100).round(2)
            
            metrics['Summary'] = group_summary
            
            # Store all metrics
            performance[group_col] = metrics
        
        # Display results
        print("Performance Analysis Results:")
        print("-" * 50)
        
        for group_col, metrics in performance.items():
            print(f"\n{group_col} Analysis:")
            
            for metric_name, metric_data in metrics.items():
                print(f"\n{metric_name} Metrics:")
                display(metric_data.sort_values('Market_Share' if metric_name == 'Summary' 
                                               else f'Total_{metric_name}', ascending=False))
            
            # Identify leaders and opportunities
            top_performer = metrics['Summary']['Market_Share'].idxmax()
            growth_target = metrics['Summary']['Growth_Potential'].idxmax()
            
            print(f"\nKey Insights for {group_col}:")
            print(f"Market Leader: {top_performer} ({metrics['Summary'].loc[top_performer, 'Market_Share']:.1f}% share)")
            print(f"Growth Target: {growth_target} ({metrics['Summary'].loc[growth_target, 'Growth_Potential']:.1f}% potential)")
        
        return performance
        
    except Exception as e:
        print(f"Error in performance analysis: {str(e)}")
        raise

# Perform performance analysis
performance_metrics = analyze_performance(df)
```

### Time Series Analysis Framework

```python
def analyze_time_patterns(df, date_col='Date', metric_cols=['Sales', 'Units']):
    """Analyze temporal patterns in the data.
    
    Args:
        df (pd.DataFrame): Input dataframe
        date_col (str): Column containing datetime data
        metric_cols (list): Metrics to analyze over time
        
    Returns:
        dict: Dictionary containing temporal analysis results
    """
    try:
        # Validate inputs
        if date_col not in df.columns:
            raise ValueError(f"Date column not found: {date_col}")
            
        for col in metric_cols:
            if col not in df.columns:
                raise ValueError(f"Metric column not found: {col}")
        
        # Create working copy
        df = df.copy()
        
        # Ensure datetime format
        try:
            df[date_col] = pd.to_datetime(df[date_col])
        except Exception as e:
            raise ValueError(f"Error converting {date_col} to datetime: {str(e)}")
        
        # Extract time components
        time_components = {
            'Hour': df[date_col].dt.hour,
            'Day': df[date_col].dt.day,
            'Week': df[date_col].dt.isocalendar().week,
            'Month': df[date_col].dt.month,
            'Weekday': df[date_col].dt.day_name()
        }
        
        # Add components to dataframe
        for comp_name, comp_data in time_components.items():
            df[comp_name] = comp_data
        
        # Define analysis functions
        def analyze_component(data, component):
            # Basic metrics
            metrics = data.groupby(component).agg({
                **{col: ['sum', 'mean', 'count', 'std'] for col in metric_cols}
            }).round(2)
            
            # Add derived metrics
            total_sales = data['Sales'].sum()
            metrics['Sales_Share'] = (metrics[('Sales', 'sum')] / total_sales * 100).round(2)
            
            # Peak analysis
            peak_period = metrics['Sales_Share'].idxmax()
            peak_share = metrics['Sales_Share'].max()
            
            return metrics, peak_period, peak_share
        
        # Analyze each time component
        analysis = {}
        for comp_name in time_components.keys():
            metrics, peak, share = analyze_component(df, comp_name)
            
            analysis[comp_name] = {
                'metrics': metrics,
                'peak_period': peak,
                'peak_share': share
            }
        
        # Display results
        print("Temporal Analysis Results:")
        print("-" * 50)
        
        for comp_name, results in analysis.items():
            print(f"\n{comp_name} Analysis:")
            display(results['metrics'])
            print(f"Peak {comp_name}: {results['peak_period']} ({results['peak_share']:.1f}% of sales)")
            
            # Additional insights
            if comp_name == 'Hour':
                busy_hours = results['metrics'][results['metrics']['Sales_Share'] > 10].index
                print(f"Peak Hours: {list(busy_hours)}")
            elif comp_name == 'Weekday':
                weekend_share = results['metrics'].loc[['Saturday', 'Sunday'], 'Sales_Share'].sum()
                print(f"Weekend Share: {weekend_share:.1f}%")
        
        return analysis
        
    except Exception as e:
        print(f"Error in temporal analysis: {str(e)}")
        raise

# Perform temporal analysis
time_analysis = analyze_time_patterns(df)
```

### Analysis Learning Notes

```markdown
## Key Insights from Analysis

### 1. Distribution Study Notes
- Check mean vs median (skewness)
- Study spread patterns (variation)
- Note unusual patterns (outliers)

### 2. Performance Insights
- Document regional leaders
- Note demographic trends
- Identify growth markets

### 3. Time Pattern Notes
- Mark peak periods
- Track weekly cycles
- Monitor monthly growth

### 4. Business Applications
✓ Resource planning
✓ Marketing focus
✓ Stock management
✓ Staff scheduling
```

### Study Questions
1. Why is skewness important?
   - Impact on mean vs median
   - Pricing implications
   - Inventory decisions

2. Performance Metrics:
   - Revenue vs transaction count
   - Average sale importance
   - Variation impact

3. Time Analysis:
   - Cycle identification
   - Trend vs seasonality
   - Peak period management

### Next Steps
1. Prepare visualizations
2. Document findings
3. Draft recommendations
4. Review with course materials
