# Exploratory Data Analysis

## 1. Album Analysis

### 1.1 Popular Songs by Album
```python
def analyze_album_popularity(df: pd.DataFrame, 
                           popularity_threshold: int = 70) -> pd.DataFrame:
    """
    Analyze album popularity based on popular songs.
    Per data dictionary: popularity ranges from 0 to 100.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        popularity_threshold (int): Threshold for popular songs (0-100)
        
    Returns:
        pd.DataFrame: Album popularity statistics with columns:
        - Total_Songs: Number of songs in album
        - Avg_Popularity: Mean popularity score
        - Max_Popularity: Highest popularity score
        - Popular_Songs: Count of songs above threshold
    """
    album_stats = df.groupby('album').agg({
        'name': 'count',
        'popularity': ['mean', 'max', 
                      lambda x: sum(x >= popularity_threshold)]
    })
    
    album_stats.columns = ['Total_Songs', 'Avg_Popularity', 
                          'Max_Popularity', 'Popular_Songs']
    
    return album_stats.sort_values('Popular_Songs', ascending=False)
```

### 1.2 Top Album Recommendations
```python
def get_top_album_recommendations(df: pd.DataFrame, n_recommendations: int = 2) -> pd.DataFrame:
    """
    Get top album recommendations based on popularity metrics.
    Per data dictionary: popularity ranges from 0 to 100.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        n_recommendations (int): Number of albums to recommend
        
    Returns:
        pd.DataFrame: Top album recommendations with metrics
    """
    # Calculate album metrics
    album_metrics = df.groupby('album').agg({
        'name': 'count',
        'popularity': ['mean', 'std', 'max',
                      lambda x: sum(x >= 70)]
    }).round(2)
    
    # Rename columns
    album_metrics.columns = ['Total_Songs', 'Avg_Popularity', 
                           'Popularity_Std', 'Max_Popularity',
                           'Popular_Songs']
    
    # Calculate popularity score
    album_metrics['Score'] = (0.4 * album_metrics['Avg_Popularity'] +
                            0.4 * album_metrics['Popular_Songs'] +
                            0.2 * album_metrics['Max_Popularity'])
    
    # Get top recommendations
    recommendations = album_metrics.nlargest(n_recommendations, 'Score')
    
    return recommendations
```

### 1.3 Visualize Album Performance
```python
def plot_album_performance(df: pd.DataFrame) -> None:
    """
    Create visualization of album performance.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(15, 6))
    
    # Calculate average popularity by album
    album_popularity = df.groupby('album')['popularity'].mean().sort_values()
    
    # Create bar plot
    album_popularity.plot(kind='bar')
    plt.title('Average Song Popularity by Album')
    plt.xlabel('Album')
    plt.ylabel('Average Popularity')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()
```

## 2. Feature Pattern Analysis

### 2.1 Audio Feature Distributions
```python
def plot_audio_feature_distributions(df: pd.DataFrame) -> None:
    """
    Plot distributions of audio features.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    audio_features = [
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'speechiness', 'valence'
    ]
    
    # Create subplot grid
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    axes = axes.ravel()
    
    # Plot each feature distribution
    for idx, feature in enumerate(audio_features):
        sns.histplot(data=df, x=feature, ax=axes[idx])
        axes[idx].set_title(f'{feature.capitalize()} Distribution')
    
    plt.tight_layout()
    plt.show()
```

### 2.2 Feature Correlations and Popularity
```python
def analyze_feature_correlations(df: pd.DataFrame, threshold: float = CORR_THRESHOLD) -> tuple:
    """
    Analyze correlations between audio features and their relationship with popularity.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        threshold (float): Correlation threshold for feature selection
        
    Returns:
        tuple: (correlation_matrix, highly_correlated_pairs)
    """
    # Select features including popularity
    features = UNIT_RANGE_FEATURES + ['loudness', 'tempo', 'popularity']
    
    # Calculate correlation matrix
    corr_matrix = df[features].corr()
    
    # Find highly correlated pairs
    highly_corr = []
    for i in range(len(features)):
        for j in range(i+1, len(features)):
            if abs(corr_matrix.iloc[i,j]) >= threshold:
                highly_corr.append({
                    'feature1': features[i],
                    'feature2': features[j],
                    'correlation': corr_matrix.iloc[i,j]
                })
    
    # Plot correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Feature Correlation Matrix')
    plt.show()
    
    # Plot feature vs popularity
    plt.figure(figsize=(15, 5))
    for i, feature in enumerate(features[:-1], 1):
        plt.subplot(2, 5, i)
        plt.scatter(df[feature], df['popularity'], alpha=0.5)
        plt.xlabel(feature)
        plt.ylabel('popularity')
        plt.title(f'{feature} vs Popularity')
    plt.tight_layout()
    plt.show()
    
    return corr_matrix, pd.DataFrame(highly_corr)
```

## 3. Temporal Analysis

### 3.1 Evolution of Audio Features and Popularity
```python
def analyze_temporal_patterns(df: pd.DataFrame) -> None:
    """
    Analyze how audio features and popularity evolved over time.
    
    Parameters:
        df (pd.DataFrame): Input dataframe with release_year
    """
    # Select features for temporal analysis
    features = UNIT_RANGE_FEATURES + ['popularity']
    
    # Calculate yearly averages
    yearly_avg = df.groupby('release_year')[features].mean()
    
    # Plot feature evolution
    plt.figure(figsize=(15, 10))
    
    # Audio features trends
    plt.subplot(2, 1, 1)
    for feature in UNIT_RANGE_FEATURES:
        plt.plot(yearly_avg.index, yearly_avg[feature], 
                 marker='o', label=feature)
    plt.title('Evolution of Audio Features Over Time')
    plt.xlabel('Release Year')
    plt.ylabel('Average Value')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Popularity trend
    plt.subplot(2, 1, 2)
    plt.plot(yearly_avg.index, yearly_avg['popularity'], 
             marker='o', color='red', linewidth=2)
    plt.title('Song Popularity Over Time')
    plt.xlabel('Release Year')
    plt.ylabel('Average Popularity')
    
    plt.tight_layout()
    plt.show()
    
    # Print significant trends
    trends = {}
    for feature in features:
        correlation = stats.pearsonr(yearly_avg.index, yearly_avg[feature])[0]
        trends[feature] = correlation
    
    print("\nSignificant Temporal Trends:")
    for feature, correlation in sorted(trends.items(), 
                                     key=lambda x: abs(x[1]), 
                                     reverse=True):
        print(f"{feature}: {correlation:.3f}")
```python
def analyze_feature_correlations(df: pd.DataFrame, threshold: float = CORR_THRESHOLD) -> tuple:
    """
    Analyze correlations between audio features to inform feature selection.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        threshold (float): Correlation threshold for feature selection
        
    Returns:
        tuple: (correlation_matrix, highly_correlated_pairs)
    """
    # Select features for correlation analysis
    features = UNIT_RANGE_FEATURES + ['loudness', 'tempo', 'popularity']
    
    # Calculate correlation matrix
    corr_matrix = df[features].corr()
    
    # Find highly correlated pairs
    highly_corr = []
    for i in range(len(features)):
        for j in range(i+1, len(features)):
            if abs(corr_matrix.iloc[i,j]) >= threshold:
                highly_corr.append({
                    'feature1': features[i],
                    'feature2': features[j],
                    'correlation': corr_matrix.iloc[i,j]
                })
    
    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Feature Correlation Matrix')
    plt.show()
    
    return corr_matrix, pd.DataFrame(highly_corr)

def prepare_features_for_clustering(df: pd.DataFrame) -> tuple:
    """
    Prepare features for clustering by:
    1. Selecting relevant features
    2. Handling correlations
    3. Scaling features
    4. Reducing dimensionality
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        tuple: (scaled_features, pca_features, feature_importance)
    """
    # Select features
    features = UNIT_RANGE_FEATURES + ['loudness', 'tempo', 'popularity', 
                                    'duration_minutes', 'energy_to_loudness', 
                                    'mood_score']
    X = df[features]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=features)
    
    # Apply PCA
    pca = PCA(n_components=N_COMPONENTS)
    X_pca = pca.fit_transform(X_scaled)
    
    # Calculate feature importance
    feature_importance = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(N_COMPONENTS)],
        index=features
    )
    
    return X_scaled, X_pca, feature_importance

def analyze_temporal_patterns(df: pd.DataFrame) -> None:
    """
    Analyze how audio features evolved over time.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    audio_features = [
        'acousticness', 'danceability', 'energy', 'valence'
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()
    
    for idx, feature in enumerate(audio_features):
        sns.regplot(data=df, x='release_year', y=feature, ax=axes[idx])
        axes[idx].set_title(f'{feature.capitalize()} Evolution Over Time')
    
    plt.tight_layout()
    plt.show()
```

### 3.2 Popularity Trends
```python
def analyze_popularity_trends(df: pd.DataFrame) -> None:
    """
    Analyze song popularity trends over time.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    plt.figure(figsize=(12, 6))
    
    # Calculate average popularity by year
    yearly_popularity = df.groupby('release_year')['popularity'].mean()
    
    # Create line plot
    yearly_popularity.plot(marker='o')
    plt.title('Average Song Popularity by Release Year')
    plt.xlabel('Release Year')
    plt.ylabel('Average Popularity')
    
    plt.grid(True)
    plt.show()
```

## 4. Feature Relationships

### 4.1 Popularity vs Audio Features
```python
def analyze_popularity_factors(df: pd.DataFrame) -> None:
    """
    Analyze relationship between popularity and audio features.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    audio_features = [
        'acousticness', 'danceability', 'energy', 'valence'
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()
    
    for idx, feature in enumerate(audio_features):
        sns.scatterplot(data=df, x=feature, y='popularity', ax=axes[idx])
        axes[idx].set_title(f'Popularity vs {feature.capitalize()}')
    
    plt.tight_layout()
    plt.show()
```

### 4.2 Feature Pair Analysis
```python
def analyze_feature_pairs(df: pd.DataFrame) -> None:
    """
    Create pairplot of main audio features.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
    """
    features = [
        'danceability', 'energy', 'valence', 'popularity'
    ]
    
    sns.pairplot(df[features])
    plt.suptitle('Relationships Between Key Features', y=1.02)
    plt.show()
```

## 5. Dimensionality Reduction Analysis

### 5.1 PCA Analysis
```python
def perform_pca_analysis(df: pd.DataFrame) -> tuple:
    """
    Perform PCA on audio features.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        tuple: (transformed_data, explained_variance_ratio)
    """
    audio_features = [
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
    ]
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[audio_features])
    
    # Apply PCA
    pca = PCA()
    X_pca = pca.fit_transform(X_scaled)
    
    return X_pca, pca.explained_variance_ratio_
```

### 5.2 Visualize PCA Results
```python
def plot_pca_results(explained_variance_ratio: np.ndarray) -> None:
    """
    Visualize PCA results.
    
    Parameters:
        explained_variance_ratio (np.ndarray): Explained variance ratios
    """
    plt.figure(figsize=(10, 6))
    
    # Calculate cumulative variance
    cumulative_variance = np.cumsum(explained_variance_ratio)
    
    # Create plot
    plt.plot(range(1, len(explained_variance_ratio) + 1),
             cumulative_variance, 'bo-')
    plt.axhline(y=0.9, color='r', linestyle='--')
    
    plt.title('Cumulative Explained Variance Ratio')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.grid(True)
    
    plt.show()
```

## 6. Usage Example
```python
# Load and prepare data
df = load_spotify_data(DATA_PATH)
df_clean = prepare_data_for_clustering(df)

# Album analysis
album_stats = analyze_album_popularity(df_clean)
print("Album Statistics:\n", album_stats.head())
plot_album_performance(df_clean)

# Feature analysis
plot_audio_feature_distributions(df_clean)
analyze_feature_correlations(df_clean)

# Temporal analysis
analyze_temporal_patterns(df_clean)
analyze_popularity_trends(df_clean)

# Feature relationships
analyze_popularity_factors(df_clean)
analyze_feature_pairs(df_clean)

# Dimensionality reduction
X_pca, variance_ratio = perform_pca_analysis(df_clean)
plot_pca_results(variance_ratio)
```

## 7. Next Steps
After completing exploratory data analysis:
1. Use insights to guide feature selection for clustering
2. Proceed to cluster analysis in `04_MODELING.md`
