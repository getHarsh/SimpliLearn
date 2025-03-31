# Marketing Campaign Analysis - Visualization

## Visualization Setup

### 1. Environment Configuration
```python
def configure_visualization_env():
    """Configure the visualization environment with consistent settings.
    Sets up matplotlib, seaborn, and plotly with predefined styles.
    """
    try:
        # Import required libraries
        import matplotlib.pyplot as plt
        import seaborn as sns
        import plotly.express as px
        
        # Set style configuration
        plt.style.use('seaborn')
        sns.set_style('whitegrid')
        
        # Define figure sizes
        plt.rcParams.update({
            'figure.figsize': [12, 6],
            'figure.dpi': 100,
            'figure.autolayout': True
        })
        
        # Set color palette
        colors = {
            'primary': '#2ecc71',
            'secondary': '#e74c3c',
            'accent1': '#3498db',
            'accent2': '#f1c40f',
            'accent3': '#9b59b6'
        }
        sns.set_palette(list(colors.values()))
        
        return colors
        
    except Exception as e:
        print(f"Error configuring visualization environment: {str(e)}")
        raise
```

### 2. Dashboard Components
```python
def define_visualization_components():
    """Define the structure and components of the visualization dashboard.
    
    Returns:
        dict: Dashboard component configuration
    """
    return {
        'product_analysis': {
            'components': ['revenue_comparison', 'category_relationships'],
            'metrics': ['total_revenue', 'market_share', 'growth_rate'],
            'filters': ['time_period', 'product_category', 'customer_segment']
        },
        'campaign_analysis': {
            'components': ['age_impact', 'geographic_performance'],
            'metrics': ['response_rate', 'conversion_rate', 'roi'],
            'filters': ['campaign_type', 'customer_age', 'location']
        },
        'demographic_analysis': {
            'components': ['family_spending', 'education_complaints'],
            'metrics': ['avg_spending', 'complaint_rate', 'satisfaction_score'],
            'filters': ['family_size', 'education_level', 'income_range']
        }
    }
```

## Product Analysis

### 1. Product Performance
```python
# My preferred visualization settings
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set my style preferences
plt.style.use('seaborn')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = [12, 6]

# Custom color palette I find effective
my_colors = ['#2ecc71', '#e74c3c', '#3498db', '#f1c40f', '#9b59b6']
sns.set_palette(my_colors)
```

### Product Performance Visualization
```python
# My approach to analyzing product performance

def analyze_product_revenue(df):
    """Analyze and visualize product revenue patterns.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Product revenue analysis including metrics and visualizations
    """
    try:
        # Validate input
        product_cols = [
            'MntWines', 'MntFruits', 'MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
        ]
        if not all(col in df.columns for col in product_cols):
            raise ValueError("Missing required product columns")
            
        # Calculate metrics
        revenue_metrics = {
            'total_revenue': df[product_cols].sum(),
            'avg_revenue': df[product_cols].mean(),
            'revenue_std': df[product_cols].std()
        }
        
        # Sort products by revenue
        product_revenue = revenue_metrics['total_revenue'].sort_values(ascending=True)
        
        # Calculate market share
        total_market = product_revenue.sum()
        market_share = (product_revenue / total_market * 100).round(2)
        
        # Create visualization
        plt.figure(figsize=(12, 6))
        bars = plt.barh(range(len(product_revenue)), product_revenue)
        
        # Format axis labels
        plt.yticks(
            range(len(product_revenue)),
            [col.replace('Mnt', '').replace('Prods', '') 
             for col in product_revenue.index]
        )
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            share = market_share.iloc[i]
            plt.text(
                width, bar.get_y() + bar.get_height()/2,
                f'${width:,.0f} ({share}%)',
                ha='left', va='center', fontweight='bold'
            )
        
        plt.title('Revenue and Market Share by Product Category')
        plt.xlabel('Total Revenue ($)')
        plt.tight_layout()
        plt.show()
        
        # Print summary
        print('Product Performance Summary:')
        summary_df = pd.DataFrame({
            'Revenue': revenue_metrics['total_revenue'],
            'Market_Share': market_share,
            'Avg_Revenue': revenue_metrics['avg_revenue'],
            'Std_Dev': revenue_metrics['revenue_std']
        }).round(2)
        print(summary_df)
        
        return {
            'revenue_metrics': revenue_metrics,
            'market_share': market_share,
            'summary': summary_df
        }
        
    except Exception as e:
        print(f"Error analyzing product revenue: {str(e)}")
        raise
```

### Age-Campaign Response Analysis
```python
# My analysis of age impact on campaigns

def analyze_age_campaign_response(df):
    """Analyze and visualize the relationship between age and campaign response.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Age-based campaign analysis results
    """
    try:
        # Validate age data
        if df['Age'].min() < 0 or df['Age'].max() > 100:
            raise ValueError("Invalid age values detected")
            
        # Create age groups
        age_bins = [0, 30, 45, 60, 100]
        age_labels = ['Young', 'Middle', 'Senior', 'Elderly']
        
        df['Age_Group'] = pd.cut(
            df['Age'],
            bins=age_bins,
            labels=age_labels
        )
        
        # Calculate metrics
        age_metrics = {
            'acceptance_rate': df.groupby('Age_Group')['Response'].mean(),
            'response_count': df.groupby('Age_Group')['Response'].sum(),
            'total_customers': df.groupby('Age_Group').size()
        }
        
        # Create dual visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Age distribution
        sns.histplot(
            data=df,
            x='Age',
            hue='Response',
            multiple='stack',
            ax=ax1
        )
        ax1.set_title('Age Distribution by Campaign Response')
        
        # Acceptance rates
        rates = age_metrics['acceptance_rate']
        bars = rates.plot(kind='bar', ax=ax2)
        ax2.set_title('Campaign Acceptance Rate by Age Group')
        ax2.set_ylabel('Acceptance Rate')
        
        # Add rate labels
        for i, rate in enumerate(rates):
            ax2.text(
                i, rate,
                f'{rate:.1%}',
                ha='center',
                va='bottom'
            )
        
        plt.tight_layout()
        plt.show()
        
        # Print summary
        print('Age Group Analysis Summary:')
        summary_df = pd.DataFrame({
            'Total_Customers': age_metrics['total_customers'],
            'Responses': age_metrics['response_count'],
            'Response_Rate': age_metrics['acceptance_rate'].round(3)
        })
        print(summary_df)
        
        return {
            'age_metrics': age_metrics,
            'summary': summary_df
        }
        
    except Exception as e:
        print(f"Error analyzing age response: {str(e)}")
        raise
    
    # Create dual visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Age distribution
    sns.histplot(data=df, x='Age', hue='Response',
                multiple='stack', ax=ax1)
    ax1.set_title('Age Distribution by Campaign Response')
    
    # Acceptance rates
    acceptance_rates.plot(kind='bar', ax=ax2)
    ax2.set_title('Campaign Acceptance Rate by Age Group')
    ax2.set_ylabel('Acceptance Rate')
    
    # Add rate labels
    for i, rate in enumerate(acceptance_rates):
        ax2.text(i, rate, f'{rate:.1%}',
                 ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Print statistical summary
    print('Acceptance Rate Summary:')
    print(acceptance_rates)
    
    return acceptance_rates
```

### Geographic Campaign Analysis
```python
# My analysis of regional campaign success

def analyze_regional_response(df):
    """Visualizing campaign success by country"""
    # Calculate response rates by country
    country_response = df.groupby('Country')['Response'].agg([
        'count',
        'sum',
        'mean'
    ]).sort_values('mean', ascending=False)
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Response count by country
    sns.barplot(data=df, x='Country', y='Response',
                estimator='count', ax=ax1)
    ax1.set_title('Number of Responses by Country')
    ax1.tick_params(axis='x', rotation=45)
    
    # Response rate by country
    sns.barplot(data=df, x='Country', y='Response',
                estimator='mean', ax=ax2)
    ax2.set_title('Response Rate by Country')
    ax2.set_ylabel('Acceptance Rate')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add rate labels
    for i, rate in enumerate(country_response['mean']):
        ax2.text(i, rate, f'{rate:.1%}',
                 ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print('Country Response Summary:')
    print(country_response)
    
    return country_response
```

### Family Size and Spending Analysis
```python
# My analysis of family size impact on spending

def visualize_product_performance(df):
    """Create product performance visualizations"""
    # Product revenue comparison
    product_cols = ['MntWines', 'MntFruits', 'MntMeatProducts',
                   'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    
    # Bar plot of product revenue
    plt.figure(figsize=(12, 6))
    product_revenue = df[product_cols].sum().sort_values(ascending=True)
    sns.barplot(x=product_revenue.values, y=product_revenue.index)
    plt.title('Product Revenue Comparison')
    plt.xlabel('Total Revenue')
    plt.show()
    
    # Product category relationships
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[product_cols].corr(), annot=True, cmap='coolwarm')
    plt.title('Product Category Correlations')
    plt.show()
```

## Campaign Analysis

### 1. Age Impact Analysis
```python
# Visualize age impact on campaign acceptance
def visualize_age_campaign(df):
    # Age distribution by campaign acceptance
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='AcceptedCmp5', y='Age', data=df)
    plt.title('Age Distribution by Campaign Acceptance')
    plt.show()
    
    # Age group acceptance rates
    df['Age_Group'] = pd.qcut(df['Age'], q=5)
    acceptance_by_age = df.groupby('Age_Group')['AcceptedCmp5'].mean()
    
    plt.figure(figsize=(12, 6))
    acceptance_by_age.plot(kind='bar')
    plt.title('Campaign Acceptance Rate by Age Group')
    plt.show()
```

### 2. Geographic Performance
```python
# Visualize campaign performance by country
def visualize_country_performance(df):
    # Country-wise acceptance rates
    country_acceptance = df.groupby('Country')['AcceptedCmp5'].agg(['count', 'mean'])
    
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=country_acceptance, x='count', y='mean', s=100)
    
    # Add country labels
    for idx, row in country_acceptance.iterrows():
        plt.annotate(idx, (row['count'], row['mean']))
    
    plt.title('Campaign Acceptance Rate vs Customer Count by Country')
    plt.xlabel('Number of Customers')
    plt.ylabel('Acceptance Rate')
    plt.show()
```

## Demographic Analysis

### 1. Family Spending Patterns
```python
# Analyze spending patterns based on family size
def analyze_family_spending_patterns(df):
    """Analyze and visualize spending patterns based on family size.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Family spending analysis results
    """
    try:
        # Validate input
        required_cols = [
            'Total_Children', 'Total_Spending',
            'MntWines', 'MntFruits', 'MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
        ]
        if not all(col in df.columns for col in required_cols):
            raise ValueError("Missing required columns")
            
        # Calculate metrics
        product_cols = [col for col in required_cols if col.startswith('Mnt')]
        metrics = {
            'avg_spending': df.groupby('Total_Children')[product_cols + ['Total_Spending']].mean(),
            'spending_std': df.groupby('Total_Children')[product_cols + ['Total_Spending']].std(),
            'customer_count': df.groupby('Total_Children').size()
        }
        
        # Correlation analysis
        correlations = {
            'spending_correlation': df['Total_Children'].corr(df['Total_Spending']),
            'category_correlations': df['Total_Children'].corr(df[product_cols])
        }
        
        # Create multi-view visualization
        fig = plt.figure(figsize=(15, 10))
        
        # Total spending by family size
        plt.subplot(221)
        sns.boxplot(x='Total_Children', y='Total_Spending', data=df)
        plt.title('Total Spending Distribution by Family Size')
        
        # Category spending patterns
        plt.subplot(222)
        metrics['avg_spending'][product_cols].plot(kind='bar')
        plt.title('Category Spending by Family Size')
        plt.legend(bbox_to_anchor=(1.05, 1), title='Product Category')
        plt.xticks(rotation=45)
        
        # Correlation analysis
        plt.subplot(223)
        sns.regplot(
            x='Total_Children',
            y='Total_Spending',
            data=df,
            scatter_kws={'alpha':0.5},
            line_kws={'color': 'red'}
        )
        plt.title(f'Spending vs Family Size (r={correlations["spending_correlation"]:.2f})')
        
        # Customer distribution
        plt.subplot(224)
        metrics['customer_count'].plot(kind='bar')
        plt.title('Number of Customers by Family Size')
        plt.xlabel('Number of Children')
        plt.ylabel('Customer Count')
        
        plt.tight_layout()
        plt.show()
        
        # Print summary
        print('Family Spending Analysis Summary:')
        summary_df = pd.DataFrame({
            'Avg_Spending': metrics['avg_spending']['Total_Spending'],
            'Std_Dev': metrics['spending_std']['Total_Spending'],
            'Customer_Count': metrics['customer_count']
        }).round(2)
        print(summary_df)
        
        return {
            'metrics': metrics,
            'correlations': correlations,
            'summary': summary_df
        }
        
    except Exception as e:
        print(f"Error analyzing family spending: {str(e)}")
        raise
```

### Customer Complaint Patterns
```python
# My analysis of education and complaints

def analyze_complaint_characteristics(df):
    """Analyze and visualize customer complaint patterns.
    
    Args:
        df (pd.DataFrame): Input marketing campaign dataset
        
    Returns:
        dict: Complaint analysis results and patterns
    """
    try:
        # Validate input
        if 'Complain' not in df.columns or 'Education' not in df.columns:
            raise ValueError("Missing required columns")
            
        # Calculate complaint metrics
        complaint_metrics = {
            'education_rates': df.groupby('Education')['Complain'].agg([
                'count',
                'sum',
                'mean'
            ]).sort_values('mean', ascending=False),
            'total_complaints': df['Complain'].sum(),
            'overall_rate': df['Complain'].mean()
        }
        
        # Analyze complainant characteristics
        complainant_profile = df[df['Complain'] == 1].agg({
            'Age': ['mean', 'std'],
            'Total_Spending': ['mean', 'std'],
            'Total_Children': ['mean', 'std']
        }).round(2)
        
        # Create multi-view visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Complaint distribution
        sns.countplot(
            data=df,
            x='Education',
            hue='Complain',
            ax=ax1,
            order=complaint_metrics['education_rates'].index
        )
        ax1.set_title('Complaints by Education Level')
        ax1.tick_params(axis='x', rotation=45)
        
        # Complaint rate comparison
        rates = complaint_metrics['education_rates']
        bars = rates['mean'].plot(kind='bar', ax=ax2)
        ax2.axhline(
            y=complaint_metrics['overall_rate'],
            color='red',
            linestyle='--',
            label=f'Overall Rate: {complaint_metrics["overall_rate"]:.1%}'
        )
        ax2.set_title('Complaint Rate by Education')
        ax2.set_ylabel('Complaint Rate')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend()
        
        # Add rate labels
        for i, rate in enumerate(rates['mean']):
            ax2.text(
                i, rate,
                f'{rate:.1%}',
                ha='center',
                va='bottom'
            )
        
        plt.tight_layout()
        plt.show()
        
        # Print summary
        print('Complaint Analysis Summary:')
        print(f"Overall Complaint Rate: {complaint_metrics['overall_rate']:.1%}")
        print(f"Total Complaints: {complaint_metrics['total_complaints']}\n")
        
        print('Complaint Rates by Education:')
        print(complaint_metrics['education_rates'])
        
        print('\nComplainant Profile (Mean ± Std):')
        print(complainant_profile)
        
        return {
            'metrics': complaint_metrics,
            'profile': complainant_profile
        }
        
    except Exception as e:
        print(f"Error analyzing complaints: {str(e)}")
        raise
    
    # Create multi-view analysis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Complaint distribution
    sns.countplot(data=df, x='Education', hue='Complain', ax=ax1)
    ax1.set_title('Complaints by Education Level')
    ax1.tick_params(axis='x', rotation=45)
    
    # Complaint rate
    complaint_rates['mean'].plot(kind='bar', ax=ax2)
    ax2.set_title('Complaint Rate by Education')
    ax2.set_ylabel('Complaint Rate')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add rate labels
    for i, rate in enumerate(complaint_rates['mean']):
        ax2.text(i, rate, f'{rate:.1%}',
                 ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Additional characteristics
    print('Complainant Profile:')
    profile = df[df['Complain'] == 1].describe()
    print(profile)
    
    return complaint_rates
```

### Dashboard Development Guide
```python
# Interactive Visualization
def create_dashboard():
    """Guide: How to present insights effectively?"""
    # Key metrics
    # Interactive elements
    # Filter options
    # Insight highlights
```

### Next Steps Framework
1. What patterns need investigation?
2. Which insights drive strategy?
3. How to present findings?
4. What recommendations follow?
