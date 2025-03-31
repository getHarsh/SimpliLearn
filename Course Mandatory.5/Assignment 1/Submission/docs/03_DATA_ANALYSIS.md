# Exploratory Data Analysis

## 1. Correlation Analysis (Requirement 2.1)

### 1.1 Correlation Heatmap
```python
def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    """
    Create correlation heatmap for numerical features.
    Implementation of requirement 2.1.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    # Select numerical columns
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    # Calculate correlation matrix
    corr_matrix = df[numerical_cols].corr()
    
    # Create heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, 
                annot=True,
                cmap='coolwarm',
                center=0,
                fmt='.2f',
                square=True)
    plt.title('Correlation Matrix of Numerical Features')
    plt.tight_layout()
    plt.show()
    
    # Print strongest correlations with turnover
    print("\nStrongest correlations with employee turnover:")
    turnover_corr = corr_matrix['left'].sort_values(ascending=False)
    print(turnover_corr)
```

## 2. Distribution Analysis (Requirement 2.2)

### 2.1 Employee Satisfaction Distribution
```python
def plot_satisfaction_distribution(df: pd.DataFrame) -> None:
    """
    Analyze distribution of employee satisfaction.
    Implementation of requirement 2.2.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(12, 6))
    
    # Create distribution plot
    sns.histplot(data=df, x='satisfaction_level', hue='left', 
                multiple="layer", bins=30)
    
    plt.title('Distribution of Employee Satisfaction by Turnover Status')
    plt.xlabel('Satisfaction Level')
    plt.ylabel('Count')
    plt.legend(title='Left Company', labels=['No', 'Yes'])
    
    # Add summary statistics
    print("\nSatisfaction Level Statistics by Turnover Status:")
    print(df.groupby('left')['satisfaction_level'].describe())
```

### 2.2 Employee Evaluation Distribution
```python
def plot_evaluation_distribution(df: pd.DataFrame) -> None:
    """
    Analyze distribution of employee evaluations.
    Implementation of requirement 2.2.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(12, 6))
    
    # Create distribution plot
    sns.histplot(data=df, x='last_evaluation', hue='left', 
                multiple="layer", bins=30)
    
    plt.title('Distribution of Last Evaluation by Turnover Status')
    plt.xlabel('Evaluation Score')
    plt.ylabel('Count')
    plt.legend(title='Left Company', labels=['No', 'Yes'])
    
    # Add summary statistics
    print("\nEvaluation Score Statistics by Turnover Status:")
    print(df.groupby('left')['last_evaluation'].describe())
```

### 2.3 Monthly Hours Distribution
```python
def plot_hours_distribution(df: pd.DataFrame) -> None:
    """
    Analyze distribution of monthly hours.
    Implementation of requirement 2.2.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(12, 6))
    
    # Create distribution plot
    sns.histplot(data=df, x='average_montly_hours', hue='left', 
                multiple="layer", bins=30)
    
    plt.title('Distribution of Average Monthly Hours by Turnover Status')
    plt.xlabel('Average Monthly Hours')
    plt.ylabel('Count')
    plt.legend(title='Left Company', labels=['No', 'Yes'])
    
    # Add summary statistics
    print("\nMonthly Hours Statistics by Turnover Status:")
    print(df.groupby('left')['average_montly_hours'].describe())
```

### 2.4 Project Count Analysis (Requirement 2.3)
```python
def analyze_project_turnover(df: pd.DataFrame) -> None:
    """
    Analyze project count distribution for employees who left vs stayed.
    Implementation of requirement 2.3.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(12, 6))
    
    # Create bar plot with hue for left vs stayed
    sns.countplot(data=df, x='number_project', hue='left')
    
    plt.title('Project Count Distribution: Left vs Stayed')
    plt.xlabel('Number of Projects')
    plt.ylabel('Count of Employees')
    plt.legend(title='Employee Status', labels=['Stayed', 'Left'])
    
    # Add count labels on bars
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', 
                          (p.get_x() + p.get_width()/2., p.get_height()),
                          ha='center', va='bottom')
    
    plt.show()
    
    # Print detailed statistics
    stats = df.groupby(['number_project', 'left']).size().unstack(fill_value=0)
    stats.columns = ['Stayed', 'Left']
    stats['Turnover Rate'] = (stats['Left'] / (stats['Stayed'] + stats['Left'])).round(3)
    
    print("\nProject Count Analysis:")
    print(stats)
    
    # Print key findings
    high_turnover = stats[stats['Turnover Rate'] > 0.2]
    print("\nProjects with High Turnover (>20%):")
    print(high_turnover)
```

## 3. Clustering Analysis of Departed Employees (Requirements 3.1-3.3)

### 3.1 K-means Clustering Implementation
```python
def cluster_departed_employees(df: pd.DataFrame) -> dict:
    """
    Perform K-means clustering of employees who left based on satisfaction and evaluation.
    Implementation of requirements 3.1, 3.2, and 3.3.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Clustering results and analysis
    """
    # 3.1: Select relevant data
    departed = df[df['left'] == 1]
    X = departed[['satisfaction_level', 'last_evaluation']]
    
    # 3.2: Perform K-means clustering with 3 clusters
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X)
    
    # Visualize clusters
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(X['satisfaction_level'], 
                         X['last_evaluation'],
                         c=clusters,
                         cmap='viridis')
    
    # Plot cluster centers
    plt.scatter(kmeans.cluster_centers_[:, 0],
                kmeans.cluster_centers_[:, 1],
                marker='x',
                s=200,
                linewidths=3,
                color='r',
                label='Centroids')
    
    plt.colorbar(scatter)
    plt.title('Clusters of Employees Who Left')
    plt.xlabel('Satisfaction Level')
    plt.ylabel('Last Evaluation')
    plt.legend()
    plt.show()
    
    # 3.3: Analyze cluster characteristics
    cluster_data = X.copy()
    cluster_data['Cluster'] = clusters
    
    # Calculate cluster statistics
    stats = cluster_data.groupby('Cluster').agg({
        'satisfaction_level': ['mean', 'min', 'max'],
        'last_evaluation': ['mean', 'min', 'max'],
        'Cluster': 'size'
    })
    
    # Define cluster profiles based on satisfaction and evaluation
    profiles = {
        0: 'Overworked High Performers: High evaluation scores but low satisfaction',
        1: 'Dissatisfied Low Performers: Low evaluation scores and low satisfaction',
        2: 'Satisfied Average Performers: Moderate evaluation and satisfaction levels'
    }
    
    print("\nCluster Statistics:")
    print(stats)
    print("\nCluster Profiles:")
    for cluster, profile in profiles.items():
        print(f"\nCluster {cluster}: {profile}")
        print(f"Size: {sum(clusters == cluster)} employees")
    
    return {
        'statistics': stats,
        'profiles': profiles,
        'labels': clusters
    }```

## 1. Correlation Analysis

### 1.1 Correlation Heatmap
```python
def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    """
    Create correlation heatmap for numerical features.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    # Select numerical columns
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    # Calculate correlation matrix
    corr_matrix = df[numerical_cols].corr()
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Numerical Features')
    plt.tight_layout()
    plt.show()
```

### 1.2 Feature Correlation with Turnover
```python
def analyze_turnover_correlation(df: pd.DataFrame) -> pd.Series:
    """
    Analyze correlation between features and turnover.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.Series: Sorted correlations with turnover
    """
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
    correlations = df[numerical_cols].corr()['left'].sort_values(ascending=False)
    
    return correlations
```

## 2. Distribution Analysis

### 2.1 Employee Satisfaction Distribution
```python
def plot_satisfaction_distribution(df: pd.DataFrame) -> None:
    """
    Plot distribution of employee satisfaction levels.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(10, 6))
    
    # Overall distribution
    sns.histplot(data=df, x='satisfaction_level', bins=30)
    plt.title('Distribution of Employee Satisfaction Levels')
    plt.xlabel('Satisfaction Level')
    plt.ylabel('Count')
    plt.show()
    
    # Distribution by turnover status
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='satisfaction_level', hue='left', common_norm=False)
    plt.title('Satisfaction Distribution by Turnover Status')
    plt.xlabel('Satisfaction Level')
    plt.ylabel('Density')
    plt.show()
```

### 2.2 Employee Evaluation Distribution
```python
def plot_evaluation_distribution(df: pd.DataFrame) -> None:
    """
    Plot distribution of employee evaluation scores.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(10, 6))
    
    # Overall distribution
    sns.histplot(data=df, x='last_evaluation', bins=30)
    plt.title('Distribution of Employee Evaluation Scores')
    plt.xlabel('Evaluation Score')
    plt.ylabel('Count')
    plt.show()
    
    # Distribution by turnover status
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='last_evaluation', hue='left', common_norm=False)
    plt.title('Evaluation Distribution by Turnover Status')
    plt.xlabel('Evaluation Score')
    plt.ylabel('Density')
    plt.show()
```

### 2.3 Monthly Hours Distribution
```python
def plot_monthly_hours_distribution(df: pd.DataFrame) -> None:
    """
    Plot distribution of average monthly hours.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(10, 6))
    
    # Overall distribution
    sns.histplot(data=df, x='average_montly_hours', bins=30)
    plt.title('Distribution of Average Monthly Hours')
    plt.xlabel('Monthly Hours')
    plt.ylabel('Count')
    plt.show()
    
    # Distribution by turnover status
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='average_montly_hours', hue='left', common_norm=False)
    plt.title('Monthly Hours Distribution by Turnover Status')
    plt.xlabel('Monthly Hours')
    plt.ylabel('Density')
    plt.show()
```

## 3. Project Count Analysis

### 3.1 Project Count Distribution
```python
def analyze_project_distribution(df: pd.DataFrame) -> None:
    """
    Analyze and plot project count distribution.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(12, 6))
    
    # Create bar plot
    sns.countplot(data=df, x='number_project', hue='left')
    plt.title('Project Count Distribution by Turnover Status')
    plt.xlabel('Number of Projects')
    plt.ylabel('Count')
    
    # Add percentage labels
    total = len(df)
    for p in plt.gca().patches:
        percentage = f'{100 * p.get_height() / total:.1f}%'
        x = p.get_x() + p.get_width() / 2
        y = p.get_height()
        plt.gca().annotate(percentage, (x, y), ha='center', va='bottom')
    
    plt.show()
```

## 4. Employee Clustering Analysis

### 4.1 K-means Clustering
```python
def perform_kmeans_clustering(df: pd.DataFrame) -> tuple:
    """
    Perform K-means clustering on employees who left.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        tuple: (cluster_labels, cluster_centers)
    """
    # Filter employees who left
    left_employees = df[df['left'] == 1]
    
    # Select features for clustering
    features = ['satisfaction_level', 'last_evaluation']
    X = left_employees[features]
    
    # Perform clustering
    kmeans = KMeans(n_clusters=3, random_state=RANDOM_SEED)
    cluster_labels = kmeans.fit_predict(X)
    
    return cluster_labels, kmeans.cluster_centers_
```

### 4.2 Visualize Clusters
```python
def plot_employee_clusters(df: pd.DataFrame, 
                         labels: np.ndarray, 
                         centers: np.ndarray) -> None:
    """
    Visualize employee clusters.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        labels (np.ndarray): Cluster labels
        centers (np.ndarray): Cluster centers
    """
    # Filter employees who left
    left_employees = df[df['left'] == 1]
    
    # Create scatter plot
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(left_employees['satisfaction_level'],
                        left_employees['last_evaluation'],
                        c=labels,
                        cmap='viridis')
    
    # Plot cluster centers
    plt.scatter(centers[:, 0], centers[:, 1], 
               c='red', marker='x', s=200, linewidths=3,
               label='Cluster Centers')
    
    plt.title('Employee Clusters Based on Satisfaction and Evaluation')
    plt.xlabel('Satisfaction Level')
    plt.ylabel('Last Evaluation Score')
    plt.legend(*scatter.legend_elements(), title="Clusters")
    plt.show()
```

## 5. Additional Insights

### 5.1 Department Analysis
```python
def analyze_departments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze turnover rates by department.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Department-wise turnover statistics
    """
    dept_stats = df.groupby('Department').agg({
        'left': ['count', 'mean'],
        'satisfaction_level': 'mean',
        'last_evaluation': 'mean'
    })
    
    dept_stats.columns = ['Total_Employees', 'Turnover_Rate', 
                         'Avg_Satisfaction', 'Avg_Evaluation']
    return dept_stats.sort_values('Turnover_Rate', ascending=False)
```

### 5.2 Salary Impact Analysis
```python
def analyze_salary_impact(df: pd.DataFrame) -> None:
    """
    Analyze impact of salary on turnover.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(10, 6))
    
    # Calculate turnover rate by salary level
    salary_turnover = df.groupby('salary')['left'].mean().sort_values()
    
    # Create bar plot
    salary_turnover.plot(kind='bar')
    plt.title('Turnover Rate by Salary Level')
    plt.xlabel('Salary Level')
    plt.ylabel('Turnover Rate')
    
    # Add percentage labels
    for i, v in enumerate(salary_turnover):
        plt.text(i, v, f'{v:.1%}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
```

## 6. Usage Example
```python
# Load and prepare data
df = load_hr_data(DATA_PATH)
df_clean = handle_missing_values(df)

# Correlation analysis
plot_correlation_heatmap(df_clean)
correlations = analyze_turnover_correlation(df_clean)
print("Feature Correlations with Turnover:\n", correlations)

# Distribution analysis
plot_satisfaction_distribution(df_clean)
plot_evaluation_distribution(df_clean)
plot_monthly_hours_distribution(df_clean)

# Project count analysis
analyze_project_distribution(df_clean)

# Clustering analysis
labels, centers = perform_kmeans_clustering(df_clean)
plot_employee_clusters(df_clean, labels, centers)

# Additional insights
dept_stats = analyze_departments(df_clean)
print("\nDepartment Statistics:\n", dept_stats)
analyze_salary_impact(df_clean)
```

## 7. Next Steps
After completing exploratory data analysis:
1. Use insights to guide feature selection for modeling
2. Proceed to model development in `04_MODELING.md`
