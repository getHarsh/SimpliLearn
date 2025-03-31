# Data Wrangling and Preparation

## 1. Data Loading

### 1.1 Load Data Sources
```python
def load_data_sources(csv_path: str, xlsx_path: str) -> tuple:
    """
    Load data from both CSV and XLSX sources.
    
    Parameters:
        csv_path (str): Path to Rolling Stones Spotify CSV
        xlsx_path (str): Path to data dictionary XLSX
        
    Returns:
        tuple: (spotify_df, data_dict_df)
    """
    # Load Spotify data
    spotify_df = pd.read_csv(csv_path)
    
    # Load data dictionary
    data_dict_df = pd.read_excel(xlsx_path)
    
    return spotify_df, data_dict_df
```

### 1.2 Process Dates and Track Numbers
```python
def process_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process release dates and track numbers.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Processed dataframe
    """
    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    # Extract year for analysis
    df['release_year'] = df['release_date'].dt.year
    
    # Ensure track_number is integer
    df['track_number'] = df['track_number'].astype(int)
    
    return df
```

## 2. Initial Data Inspection

### 1.1 Missing Value Analysis
```python
def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check for missing values in the dataset.
    
    Parameters:
        df (pd.DataFrame): Input dataframe with columns as defined in data dictionary
        
    Returns:
        pd.DataFrame: Missing value information
    """
    missing_counts = df.isnull().sum()
    missing_percentages = (missing_counts / len(df)) * 100
    
    missing_info = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing Percentage': missing_percentages
    })
    
    return missing_info[missing_info['Missing Count'] > 0]
```

### 1.2 Duplicate Detection
```python
def check_duplicates(df: pd.DataFrame) -> dict:
    """
    Check for duplicate entries in the dataset.
    Per data dictionary: id and uri are unique identifiers for each track.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Dictionary with duplicate information
    """
    results = {
        'full_duplicates': len(df[df.duplicated()]),
        'song_duplicates': len(df[df.duplicated(subset=['name', 'album'])]),
        'id_duplicates': len(df[df.duplicated(subset=['id'])]),  # Should be 0
        'uri_duplicates': len(df[df.duplicated(subset=['uri'])))  # Should be 0
    }
    
    return results
```

### 1.3 Data Validation
```python
def clean_invalid_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean invalid values by clipping them to valid ranges.
    Uses ranges from data dictionary.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with cleaned values
    """
    # Unit range features (0-1)
    unit_range_features = [
        'acousticness', 'danceability', 'energy',
        'instrumentalness', 'liveness', 'speechiness', 'valence'
    ]
    
    for feature in unit_range_features:
        df[feature] = df[feature].clip(lower=0, upper=1)
    
    # Special ranges
    df['loudness'] = df['loudness'].clip(lower=-60, upper=0)
    df['popularity'] = df['popularity'].clip(lower=0, upper=100)
    df['duration_ms'] = df['duration_ms'].clip(lower=0)
    
    return df

def validate_audio_features(df: pd.DataFrame) -> dict:
    """
    Validate features according to data dictionary ranges:
    - acousticness: 0.0 to 1.0 (confidence of acoustic nature)
    - danceability: 0.0 to 1.0 (suitability for dancing)
    - energy: 0.0 to 1.0 (perceptual intensity)
    - instrumentalness: 0.0 to 1.0 (predicts no vocal content)
    - liveness: 0.0 to 1.0 (> 0.8 indicates live performance)
    - speechiness: 0.0 to 1.0 (spoken word detection)
    - valence: 0.0 to 1.0 (musical positivity)
    - popularity: 0 to 100 (song popularity score)
    - duration_ms: > 0 (track duration in milliseconds)
    - loudness: -60 to 0 dB (overall track loudness)
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Number of invalid values for each feature
    """
    # Define valid ranges for each feature from data dictionary
    range_validations = {
        'acousticness': (0, 1),
        'danceability': (0, 1),
        'energy': (0, 1),
        'instrumentalness': (0, 1),
        'liveness': (0, 1),
        'speechiness': (0, 1),
        'valence': (0, 1),
        'popularity': (0, 100),
        'duration_ms': (0, float('inf')),  # Must be positive
        'loudness': (-60, 0)  # Typical range in dB
    }
    
    # Check each feature for invalid values
    results = {}
    for feature, (min_val, max_val) in range_validations.items():
        invalid_count = len(df[~df[feature].between(min_val, max_val)])
        results[feature] = invalid_count
    
    return results
    """
    Validate audio feature ranges.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Validation results for each feature
    """
    range_validations = {
        'acousticness': (0, 1),
        'danceability': (0, 1),
        'energy': (0, 1),
        'instrumentalness': (0, 1),
        'liveness': (0, 1),
        'speechiness': (0, 1),
        'valence': (0, 1),
        'popularity': (0, 100),
        'duration_ms': (0, float('inf')),
        'loudness': (-60, 0)
    }
    
    results = {}
    for feature, (min_val, max_val) in range_validations.items():
        invalid_count = len(df[~df[feature].between(min_val, max_val)])
        results[feature] = invalid_count
    
    return results
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
        pd.DataFrame: Cleaned dataframe
    """
    df_clean = df.copy()
    
    # Handle missing audio features with median
    audio_features = [
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
    ]
    
    for feature in audio_features:
        df_clean[feature] = df_clean[feature].fillna(df_clean[feature].median())
    
    # Handle missing metadata
    df_clean['popularity'] = df_clean['popularity'].fillna(0)
    df_clean['track_number'] = df_clean['track_number'].fillna(0)
    
    # Drop rows with missing essential information
    essential_cols = ['name', 'album', 'id', 'uri']
    df_clean = df_clean.dropna(subset=essential_cols)
    
    return df_clean
```

### 2.2 Handle Duplicates
```python
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate entries from the dataset.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with duplicates removed
    """
    # Remove exact duplicates
    df_unique = df.drop_duplicates()
    
    # Remove duplicates based on ID (keeping first occurrence)
    df_unique = df_unique.drop_duplicates(subset=['id'], keep='first')
    
    return df_unique
```

### 2.3 Handle Outliers
```python
def handle_outliers(df: pd.DataFrame, features: list) -> pd.DataFrame:
    """
    Handle outliers using IQR method.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        features (list): List of features to check for outliers
        
    Returns:
        pd.DataFrame: Dataframe with handled outliers
    """
    df_clean = df.copy()
    
    for feature in features:
        Q1 = df_clean[feature].quantile(0.25)
        Q3 = df_clean[feature].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Cap outliers at bounds instead of removing
        df_clean[feature] = df_clean[feature].clip(lower_bound, upper_bound)
    
    return df_clean
```

## 3. Feature Engineering

### 3.1 Temporal Features
```python
def create_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create temporal features from release_date.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with additional temporal features
    """
    df_temp = df.copy()
    
    # Extract temporal components
    df_temp['release_year'] = df_temp['release_date'].dt.year
    df_temp['release_decade'] = (df_temp['release_year'] // 10) * 10
    df_temp['years_since_release'] = (
        pd.Timestamp.now().year - df_temp['release_year']
    )
    
    return df_temp
```

### 3.2 Audio Feature Engineering
```python
def engineer_audio_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create engineered features from audio characteristics.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with engineered features
    """
    df_eng = df.copy()
    
    # Create composite features
    df_eng['energy_to_loudness'] = df_eng['energy'] / df_eng['loudness'].abs()
    df_eng['duration_minutes'] = df_eng['duration_ms'] / 60000
    df_eng['is_instrumental'] = df_eng['instrumentalness'].apply(
        lambda x: 1 if x > 0.5 else 0
    )
    df_eng['mood_score'] = (df_eng['valence'] + df_eng['energy']) / 2
    
    return df_eng
```

## 4. Feature Scaling and Transformation

### 4.1 Scale Features
```python
def scale_features(df: pd.DataFrame, 
                  features_to_scale: list) -> pd.DataFrame:
    """
    Scale selected features using StandardScaler.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        features_to_scale (list): Features to be scaled
        
    Returns:
        pd.DataFrame: Dataframe with scaled features
    """
    df_scaled = df.copy()
    
    scaler = StandardScaler()
    df_scaled[features_to_scale] = scaler.fit_transform(df[features_to_scale])
    
    return df_scaled
```

## 5. Data Preparation Pipeline

### 5.1 Complete Pipeline
```python
def prepare_data_for_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Complete data preparation pipeline for analysis and clustering.
    
    Steps:
    1. Process dates and track numbers
    2. Handle missing values
    3. Clean invalid values
    4. Create engineered features:
       - duration_minutes: Convert ms to minutes
       - energy_to_loudness: Energy normalized by loudness
       - mood_score: Composite of valence and energy
       - release_year: Extract from release_date
    
    Parameters:
        df (pd.DataFrame): Raw input dataframe
        
    Returns:
        pd.DataFrame: Cleaned and prepared dataframe
    """
    # Process metadata
    df = process_metadata(df)
    
    # Handle missing and invalid values
    df = handle_missing_values(df)
    df = clean_invalid_values(df)
    
    # Create engineered features
    df['duration_minutes'] = df['duration_ms'] / 60000
    df['energy_to_loudness'] = df['energy'] / abs(df['loudness'])
    df['mood_score'] = (df['valence'] + df['energy']) / 2
    
    return df
    Complete data preparation pipeline.
    
    Parameters:
        df (pd.DataFrame): Raw input dataframe
        
    Returns:
        pd.DataFrame: Processed dataframe ready for clustering
    """
    # 1. Clean data
    df_clean = handle_missing_values(df)
    df_clean = remove_duplicates(df_clean)
    
    # 2. Handle outliers in audio features
    audio_features = [
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
    ]
    df_clean = handle_outliers(df_clean, audio_features)
    
    # 3. Create engineered features
    df_engineered = create_temporal_features(df_clean)
    df_engineered = engineer_audio_features(df_engineered)
    
    # 4. Scale features
    features_to_scale = audio_features + ['duration_ms', 'popularity']
    df_scaled = scale_features(df_engineered, features_to_scale)
    
    return df_scaled
```

### 5.2 Usage Example
```python
# Load data
df = load_spotify_data(DATA_PATH)

# Check data quality
missing_info = check_missing_values(df)
print("Missing Values:\n", missing_info)

duplicate_info = check_duplicates(df)
print("\nDuplicates:\n", duplicate_info)

validation_results = validate_audio_features(df)
print("\nFeature Validation:\n", validation_results)

# Prepare data for clustering
df_prepared = prepare_data_for_clustering(df)
print("\nPrepared Data Shape:", df_prepared.shape)
```

## 6. Next Steps
After completing data wrangling:
1. Proceed to exploratory data analysis in `03_DATA_ANALYSIS.md`
2. Use prepared data for clustering in `04_MODELING.md`
