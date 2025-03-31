# Clustering Model Development

## 1. Feature Selection and Preparation

### 1.1 Select Features for Clustering
```python
def select_clustering_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select and prepare features for clustering.
    Per data dictionary:
    - acousticness: Acoustic confidence (0-1)
    - danceability: Dance suitability (0-1)
    - energy: Perceptual intensity (0-1)
    - instrumentalness: No vocal content prediction (0-1)
    - liveness: Audience presence (0-1)
    - loudness: Overall loudness (-60 to 0 dB)
    - speechiness: Spoken words presence (0-1)
    - tempo: BPM
    - valence: Musical positivity (0-1)
    - popularity: Song popularity (0-100)
    - duration_ms: Track length in milliseconds
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Selected features for clustering
    """
    # Select audio features
    audio_features = [
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
    ]
    
    # Add engineered features
    additional_features = [
        'popularity', 'duration_minutes', 'energy_to_loudness',
        'mood_score'
    ]
    
    selected_features = audio_features + additional_features
    
    return df[selected_features]
```

### 1.2 Optimal Cluster Determination
```python
def evaluate_clustering_metrics(X: np.ndarray, labels: np.ndarray) -> dict:
    """
    Evaluate clustering quality using multiple metrics.
    
    Parameters:
        X (np.ndarray): Feature matrix
        labels (np.ndarray): Cluster labels
        
    Returns:
        dict: Dictionary of clustering metrics
    """
    metrics = {
        'silhouette': silhouette_score(X, labels),
        'calinski_harabasz': calinski_harabasz_score(X, labels),
        'cluster_sizes': pd.Series(labels).value_counts().to_dict()
    }
    return metrics

def determine_optimal_clusters(X: np.ndarray,
                              cluster_range: range = N_CLUSTERS_RANGE) -> tuple:
    """
    Determine optimal number of clusters using elbow method and silhouette score.
    
    Parameters:
        X (np.ndarray): Scaled feature matrix
        max_clusters (int): Maximum number of clusters to try
        
    Returns:
        int: Optimal number of clusters
    """
    inertias = []
    silhouette_scores = []
    k_values = range(2, max_clusters + 1)
    
    for k in k_values:
        # Fit KMeans
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        
        # Calculate metrics
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))
    
    # Plot elbow curve
    plt.figure(figsize=(12, 5))
    
    # Inertia plot
    plt.subplot(1, 2, 1)
    plt.plot(k_values, inertias, 'bo-')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method')
    
    # Silhouette score plot
    plt.subplot(1, 2, 2)
    plt.plot(k_values, silhouette_scores, 'ro-')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Analysis')
    
    plt.tight_layout()
    plt.show()
    
    # Return k with highest silhouette score
    optimal_k = k_values[np.argmax(silhouette_scores)]
    print(f"\nOptimal number of clusters: {optimal_k}")
    print(f"Silhouette score: {max(silhouette_scores):.3f}")
    
    return optimal_k
```

### 1.3 Feature Scaling
```python
def scale_features_for_clustering(X: pd.DataFrame) -> np.ndarray:
    """
    Scale features for clustering.
    
    Parameters:
        X (pd.DataFrame): Feature matrix
        
    Returns:
        np.ndarray: Scaled features
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled
```

## 2. Dimensionality Reduction

### 2.1 PCA Transformation
```python
def apply_pca(X: np.ndarray,
              n_components: int = None) -> tuple:
    """
    Apply PCA for dimensionality reduction.
    
    Parameters:
        X (np.ndarray): Scaled feature matrix
        n_components (int): Number of components
        
    Returns:
        tuple: (transformed_data, pca_model)
    """
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    
    return X_pca, pca
```

### 2.2 UMAP Transformation
```python
def apply_umap(X: np.ndarray,
               n_neighbors: int = 15,
               min_dist: float = 0.1) -> tuple:
    """
    Apply UMAP for dimensionality reduction.
    
    Parameters:
        X (np.ndarray): Scaled feature matrix
        n_neighbors (int): Number of neighbors
        min_dist (float): Minimum distance
        
    Returns:
        tuple: (transformed_data, umap_model)
    """
    umap_model = UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        random_state=RANDOM_SEED
    )
    X_umap = umap_model.fit_transform(X)
    
    return X_umap, umap_model
```

## 3. Clustering Models

### 3.1 K-Means Clustering
```python
def perform_kmeans_clustering(X: np.ndarray,
                            n_clusters: int) -> tuple:
    """
    Perform K-means clustering.
    
    Parameters:
        X (np.ndarray): Feature matrix
        n_clusters (int): Number of clusters
        
    Returns:
        tuple: (cluster_labels, model)
    """
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=RANDOM_SEED
    )
    labels = kmeans.fit_predict(X)
    
    return labels, kmeans
```

### 3.2 HDBSCAN Clustering
```python
def perform_hdbscan_clustering(X: np.ndarray,
                             min_cluster_size: int = 50) -> tuple:
    """
    Perform HDBSCAN clustering.
    
    Parameters:
        X (np.ndarray): Feature matrix
        min_cluster_size (int): Minimum cluster size
        
    Returns:
        tuple: (cluster_labels, model)
    """
    hdbscan_model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=5
    )
    labels = hdbscan_model.fit_predict(X)
    
    return labels, hdbscan_model
```

## 4. Cluster Analysis

### 4.1 Cluster Visualization
```python
def plot_clusters_2d(X: np.ndarray,
                    labels: np.ndarray,
                    title: str) -> None:
    """
    Create 2D visualization of clusters.
    
    Parameters:
        X (np.ndarray): 2D feature matrix
        labels (np.ndarray): Cluster labels
        title (str): Plot title
    """
    plt.figure(figsize=(10, 8))
    
    scatter = plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
    plt.colorbar(scatter)
    
    plt.title(title)
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.show()
```

### 4.2 Cluster Characteristics
```python
def analyze_cluster_characteristics(df: pd.DataFrame,
                                 labels: np.ndarray,
                                 n_top: int = N_TOP_FEATURES) -> pd.DataFrame:
    """
    Analyze characteristics of each cluster.
    
    Parameters:
        df (pd.DataFrame): Original dataframe
        labels (np.ndarray): Cluster labels
        
    Returns:
        pd.DataFrame: Cluster statistics
    """
    df_with_clusters = df.copy()
    df_with_clusters['Cluster'] = labels
    
    # Calculate cluster statistics
    cluster_stats = df_with_clusters.groupby('Cluster').agg({
        'popularity': 'mean',
        'danceability': 'mean',
        'energy': 'mean',
        'valence': 'mean',
        'name': 'count'
    })
    
    cluster_stats.columns = [
        'Avg_Popularity', 'Avg_Danceability',
        'Avg_Energy', 'Avg_Valence', 'Size'
    ]
    
    return cluster_stats
```

## 5. Cluster Interpretation

### 5.1 Feature Importance Analysis
```python
def analyze_feature_importance(df: pd.DataFrame,
                             labels: np.ndarray) -> pd.DataFrame:
    """
    Analyze feature importance for each cluster.
    
    Parameters:
        df (pd.DataFrame): Original dataframe
        labels (np.ndarray): Cluster labels
        
    Returns:
        pd.DataFrame: Feature importance by cluster
    """
    df_with_clusters = df.copy()
    df_with_clusters['Cluster'] = labels
    
    # Calculate z-scores for each feature by cluster
    features = [
        'acousticness', 'danceability', 'energy',
        'instrumentalness', 'valence'
    ]
    
    feature_importance = pd.DataFrame()
    for cluster in np.unique(labels):
        cluster_data = df_with_clusters[df_with_clusters['Cluster'] == cluster]
        feature_means = cluster_data[features].mean()
        feature_stds = df_with_clusters[features].std()
        
        z_scores = (feature_means - df_with_clusters[features].mean()) / feature_stds
        feature_importance[f'Cluster_{cluster}'] = z_scores
    
    return feature_importance
```

### 5.2 Cluster Naming
```python
def name_clusters(feature_importance: pd.DataFrame) -> dict:
    """
    Generate descriptive names for clusters.
    
    Parameters:
        feature_importance (pd.DataFrame): Feature importance by cluster
        
    Returns:
        dict: Cluster names
    """
    cluster_names = {}
    
    for cluster in feature_importance.columns:
        # Get top features
        top_features = feature_importance[cluster].nlargest(2)
        
        # Generate name based on dominant features
        if top_features.iloc[0] > 1.0:
            primary_feature = top_features.index[0].replace('ness', '')
            if top_features.iloc[1] > 0.5:
                secondary_feature = top_features.index[1].replace('ness', '')
                name = f"{primary_feature.title()}-{secondary_feature.title()}"
            else:
                name = f"{primary_feature.title()}-Dominant"
        else:
            name = "Balanced"
            
        cluster_names[cluster] = name
    
    return cluster_names
```

## 6. Implementation Example
```python
# Load and prepare data
# Load and validate data
df = load_spotify_data(DATA_PATH)

# Check for invalid values
validation_results = validate_audio_features(df)
print("\nValidation Results:")
for feature, invalid_count in validation_results.items():
    if invalid_count > 0:
        print(f"WARNING: {feature} has {invalid_count} values outside valid range")

# Clean invalid values and prepare for clustering
df_clean = clean_invalid_values(df)
df_clean = prepare_data_for_clustering(df_clean)

# Select and scale features
X = select_clustering_features(df_clean)
X_scaled = scale_features_for_clustering(X)

# Apply dimensionality reduction
X_umap, umap_model = apply_umap(X_scaled)

# Perform clustering
labels_hdbscan, hdbscan_model = perform_hdbscan_clustering(X_umap)

# Visualize clusters
plot_clusters_2d(X_umap, labels_hdbscan, 'Song Clusters (HDBSCAN)')

# Analyze clusters
cluster_stats = analyze_cluster_characteristics(df_clean, labels_hdbscan)
print("\nCluster Statistics:\n", cluster_stats)

# Analyze feature importance
feature_importance = analyze_feature_importance(df_clean, labels_hdbscan)
cluster_names = name_clusters(feature_importance)
print("\nCluster Names:\n", cluster_names)
```

## 7. Cluster Descriptions and Use Cases

### Energy-Dance Cluster
- High energy and danceability
- Ideal for workout playlists
- Party and club music

### Acoustic-Instrumental Cluster
- High acousticness and instrumentalness
- Suitable for focus and study
- Background music for work

### Mood-Valence Cluster
- High valence and moderate energy
- Perfect for mood enhancement
- Feel-good playlists

### Balanced Cluster
- Moderate levels across features
- Versatile playlist additions
- General listening

## 8. Next Steps
1. Create playlist recommendations
2. Implement A/B testing
3. Monitor cluster stability
4. Refine clustering parameters
