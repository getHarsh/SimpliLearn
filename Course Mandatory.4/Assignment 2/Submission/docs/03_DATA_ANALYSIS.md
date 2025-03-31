# Marketing Campaign Analysis - Statistical Analysis

## Correlation Analysis

### 1. Variable Relationships
```python
def create_correlation_matrix(df):
    """Generate and visualize correlation matrix for numerical variables.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        pd.DataFrame: Correlation matrix of numerical variables
    """
    try:
        # Select numerical columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        # Create correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Generate heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Matrix of Numerical Variables')
        plt.tight_layout()
        plt.show()
        
        return corr_matrix
        
    except Exception as e:
        print(f"Error generating correlation matrix: {str(e)}")
        raise
```

### 2. Key Relationships Analysis
```python
def analyze_key_relationships(df):
    """Analyze key variable relationships in the dataset.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Dictionary containing correlation analyses
    """
    try:
        # Age vs Shopping Channel
        channel_age_corr = {
            'Web': df['Age'].corr(df['NumWebPurchases']),
            'Store': df['Age'].corr(df['NumStorePurchases']),
            'Catalog': df['Age'].corr(df['NumCatalogPurchases'])
        }
        
        # Children vs Online Shopping
        children_web_corr = df['Total_Children'].corr(df['NumWebPurchases'])
        
        # Channel Cannibalization
        purchase_cols = ['NumWebPurchases', 'NumStorePurchases', 'NumCatalogPurchases']
        channel_corr = df[purchase_cols].corr()
        
        # Print summary
        print("Age-Channel Correlations:")
        for channel, corr in channel_age_corr.items():
            print(f"{channel}: {corr:.3f}")
            
        print(f"\nChildren-Web Correlation: {children_web_corr:.3f}")
        
        print("\nChannel Correlations:")
        print(channel_corr)
        
        return {
            'age_channel': channel_age_corr,
            'children_web': children_web_corr,
            'channel_cannibalization': channel_corr
        }
        
    except Exception as e:
        print(f"Error analyzing relationships: {str(e)}")
        raise
```

## Hypothesis Testing

### 1. Age vs Technology Proficiency
```python
# My analysis of age vs shopping channel preference

def test_age_tech_hypothesis(df):
    """Test hypothesis about age-based shopping channel preferences.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Test results including statistics and p-values
    """
    try:
        # Validate age data
        if df['Age'].min() < 0 or df['Age'].max() > 100:
            raise ValueError("Invalid age values detected")
            
        # Create age groups
        df['Age_Group'] = pd.cut(
            df['Age'],
            bins=[0, 30, 45, 60, 100],
            labels=['Young', 'Middle', 'Senior', 'Elderly']
        )
        
        # Calculate channel preferences
        channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
        preferences = df.groupby('Age_Group')[channel_cols].agg(['mean', 'std'])
        
        # Statistical tests
        results = {}
        for age_group in ['Young', 'Middle', 'Senior', 'Elderly']:
            mask = df['Age_Group'] == age_group
            if mask.sum() >= 2:  # Ensure enough samples
                t_stat, p_value = stats.ttest_ind(
                    df[mask]['NumStorePurchases'],
                    df[mask]['NumWebPurchases']
                )
                results[age_group] = {
                    't_statistic': t_stat,
                    'p_value': p_value
                }
        
        # Print summary
        print('Channel preferences by age group:')
        print(preferences)
        print('\nHypothesis test results:')
        for group, stats in results.items():
            print(f"{group}: t={stats['t_statistic']:.2f}, p={stats['p_value']:.4f}")
        
        # Visualize
        plt.figure(figsize=(12, 5))
        preferences['mean'].plot(kind='bar')
        plt.title('Shopping Channel Preference by Age Group')
        plt.xlabel('Age Group')
        plt.ylabel('Average Number of Purchases')
        plt.legend(title='Channel')
        plt.tight_layout()
        plt.show()
        
        return {
            'preferences': preferences,
            'test_results': results
        }
        
    except Exception as e:
        print(f"Error testing age-tech hypothesis: {str(e)}")
        raise
```

### Family Shopping Analysis
```python
# My analysis of family shopping behavior

def analyze_family_shopping(df):
    """Analyze shopping patterns based on family status.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Analysis results including statistics and test results
    """
    try:
        # Create family status
        df['Has_Children'] = df['Total_Children'] > 0
        
        # Channel comparison
        channels = ['NumWebPurchases', 'NumStorePurchases', 'NumCatalogPurchases']
        channel_stats = df.groupby('Has_Children')[channels].agg(['mean', 'std'])
        
        # Statistical tests
        test_results = {}
        for channel in channels:
            t_stat, p_value = stats.ttest_ind(
                df[df['Has_Children']][channel],
                df[~df['Has_Children']][channel]
            )
            test_results[channel] = {
                't_statistic': t_stat,
                'p_value': p_value
            }
        
        # Print summary
        print('Shopping patterns by family status:')
        print(channel_stats)
        print('\nHypothesis test results:')
        for channel, stats in test_results.items():
            print(f"{channel}: t={stats['t_statistic']:.2f}, p={stats['p_value']:.4f}")
        
        # Visualize
        plt.figure(figsize=(12, 5))
        sns.boxplot(data=df.melt(
            id_vars='Has_Children',
            value_vars=channels
        ), x='variable', y='value', hue='Has_Children')
        plt.title('Purchase Distribution by Channel and Family Status')
        plt.xlabel('Channel')
        plt.ylabel('Number of Purchases')
        plt.tight_layout()
        plt.show()
        
        return {
            'channel_statistics': channel_stats,
            'test_results': test_results
        }
        
    except Exception as e:
        print(f"Error analyzing family shopping: {str(e)}")
        raise
    
    # Statistical test
    t_stat, p_value = stats.ttest_ind(
        df[df['Has_Children']]['NumWebPurchases'],
        df[~df['Has_Children']]['NumWebPurchases']
    )
    
    print('Shopping patterns by family status:')
    print(channel_comparison)
    print(f'\nT-test results: stat={t_stat:.2f}, p={p_value:.4f}')
    
    # Visualize
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='Has_Children', y='NumWebPurchases', data=df)
    plt.title('Web Purchases by Family Status')
    plt.show()
```

### Channel Interaction Study
```python
# My analysis of channel cannibalization

def analyze_channel_relationships(df):
    """Testing for channel cannibalization"""
    # Calculate correlations
    channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
    correlations = df[channel_cols].corr()
    
    # Test significance
    from scipy.stats import pearsonr
    
    # Test web vs store relationship
    r_value, p_value = pearsonr(
        df['NumWebPurchases'],
        df['NumStorePurchases']
    )
    
    print('Channel correlations:')
    print(correlations)
    print(f'\nWeb-Store correlation: r={r_value:.2f}, p={p_value:.4f}')
    
    # Visualize relationships
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlations, annot=True, cmap='coolwarm')
    plt.title('Channel Correlation Heatmap')
    plt.show()
```

### Regional Performance Study
```python
# My analysis of US vs global performance

def analyze_regional_performance(df):
    """Testing US market performance"""
    # Create US vs Rest grouping
    df['Is_US'] = df['Country'] == 'US'
    
    # Compare total purchases
    purchase_comparison = df.groupby('Is_US')['Total_Purchases'].agg(['mean', 'std'])
    
    # Statistical test
    t_stat, p_value = stats.ttest_ind(
        df[df['Is_US']]['Total_Purchases'],
        df[~df['Is_US']]['Total_Purchases']
    )
    
    print('Purchase comparison by region:')
    print(purchase_comparison)
    print(f'\nT-test results: stat={t_stat:.2f}, p={p_value:.4f}')
    
    # Visualize
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='Is_US', y='Total_Purchases', data=df)
    plt.title('Total Purchases by Region')
    plt.show()
```

### Feature Correlation Study

# My analysis of variable relationships

## Statistical Analysis

### 1. Product Performance
```python
# Analyze product revenue
def analyze_product_performance(df):
    """Analyze performance metrics for each product category.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Product performance metrics and rankings
    """
    try:
        # Product columns
        product_cols = [
            'MntWines', 'MntFruits', 'MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
        ]
        
        # Validate data
        if any(df[product_cols].lt(0).any()):
            raise ValueError("Negative product values detected")
        
        # Calculate statistics
        product_stats = df[product_cols].agg([
            'count', 'mean', 'median', 'std', 'sum'
        ])
        
        # Calculate market share
        total_revenue = product_stats.loc['sum'].sum()
        market_share = (product_stats.loc['sum'] / total_revenue * 100)
        
        # Rank products
        rankings = {
            'by_revenue': product_stats.loc['sum'].sort_values(ascending=False),
            'by_volume': product_stats.loc['count'].sort_values(ascending=False),
            'market_share': market_share.sort_values(ascending=False)
        }
        
        # Print summary
        print("Product Performance Summary:")
        print("\nRevenue Rankings:")
        print(rankings['by_revenue'])
        print("\nMarket Share (%):")
        print(rankings['market_share'])
        
        # Visualize
        plt.figure(figsize=(12, 5))
        rankings['market_share'].plot(kind='bar')
        plt.title('Product Market Share')
        plt.xlabel('Product')
        plt.ylabel('Market Share (%)')
        plt.tight_layout()
        plt.show()
        
        return {
            'statistics': product_stats,
            'rankings': rankings
        }
        
    except Exception as e:
        print(f"Error analyzing product performance: {str(e)}")
        raise
```

### 2. Campaign Analysis
```python
# Analyze campaign acceptance patterns
def analyze_campaign_patterns(df):
    """Analyze patterns in campaign acceptance across different factors.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Campaign analysis results and correlations
    """
    try:
        # Campaign columns
        campaign_cols = [col for col in df.columns if col.startswith('AcceptedCmp')]
        
        # Age correlations
        age_correlations = {}
        for campaign in campaign_cols:
            age_correlations[campaign] = df['Age'].corr(df[campaign])
        
        # Geographic performance
        geo_performance = df.groupby('Country')[campaign_cols].agg([
            'mean', 'count'
        ]).round(3)
        
        # Response rate by education
        edu_response = df.groupby('Education')[campaign_cols].mean()
        
        # Print summary
        print("Campaign Analysis Summary:")
        print("\nAge Correlations:")
        for campaign, corr in age_correlations.items():
            print(f"{campaign}: {corr:.3f}")
        
        print("\nGeographic Performance:")
        print(geo_performance)
        
        # Visualize
        plt.figure(figsize=(12, 5))
        edu_response.plot(kind='bar')
        plt.title('Campaign Response Rate by Education Level')
        plt.xlabel('Education Level')
        plt.ylabel('Response Rate')
        plt.legend(title='Campaign')
        plt.tight_layout()
        plt.show()
        
        return {
            'age_correlations': age_correlations,
            'geographic_performance': geo_performance,
            'education_response': edu_response
        }
        
    except Exception as e:
        print(f"Error analyzing campaign patterns: {str(e)}")
        raise
```

### 3. Demographic Analysis
```python
# Analyze demographic patterns
def analyze_demographics(df):
    # Children vs spending correlation
    children_spending_corr = df['Total_Children'].corr(df['Total_Spending'])
    
    # Education vs complaints
    education_complaints = df.groupby('Education')['Complain'].mean()
    
    return {
        'children_spending': children_spending_corr,
        'education_complaints': education_complaints
    }
```

## Next Steps
1. What visualizations will help?
2. Which insights need focus?
3. How to present findings?
4. What recommendations follow?
