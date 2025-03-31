"""
Data preprocessing utility functions for the Housing Loan Data Analysis project.
These functions handle data cleaning, feature engineering, and preparation for modeling.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns

def handle_missing_values(df):
    """
    Handle missing values in the dataset using appropriate strategies.
    
    Parameters:
    df (pandas.DataFrame): Input DataFrame with missing values
    
    Returns:
    pandas.DataFrame: DataFrame with missing values handled
    """
    # Create a copy to avoid modifying the original
    df_copy = df.copy()
    
    # Identify numerical and categorical columns
    numerical_cols = df_copy.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df_copy.select_dtypes(include=['object']).columns.tolist()
    
    # Handle missing values in numerical columns using median imputation
    if numerical_cols:
        num_imputer = SimpleImputer(strategy='median')
        df_copy[numerical_cols] = num_imputer.fit_transform(df_copy[numerical_cols])
    
    # Handle missing values in categorical columns using most frequent value
    if categorical_cols:
        for col in categorical_cols:
            if df_copy[col].isnull().sum() > 0:
                # Calculate the most frequent value
                most_freq = df_copy[col].mode()[0]
                # Impute missing values
                df_copy[col] = df_copy[col].fillna(most_freq)
    
    return df_copy

def handle_outliers(df, numerical_cols, method='iqr', threshold=1.5):
    """
    Handle outliers in numerical columns using IQR method or capping.
    
    Parameters:
    df (pandas.DataFrame): Input DataFrame
    numerical_cols (list): List of numerical column names to process
    method (str): Method to handle outliers ('iqr' or 'capping')
    threshold (float): Multiplier for IQR to determine outlier boundary
    
    Returns:
    pandas.DataFrame: DataFrame with outliers handled
    dict: Dictionary with info about outliers detected and processed
    """
    try:
        # Create a copy to avoid modifying the original
        df_copy = df.copy()
        
        # Dictionary to store outlier info
        outlier_info = {}
        
        for col in numerical_cols:
            if col not in df_copy.columns:
                print(f"Warning: Column '{col}' not found in DataFrame")
                continue
                
            # Calculate statistics before handling outliers
            stats_before = {
                'min': df_copy[col].min(),
                'max': df_copy[col].max(),
                'mean': df_copy[col].mean(),
                'std': df_copy[col].std()
            }
            
            if method == 'iqr':
                # IQR method (replace outliers with upper/lower bounds)
                Q1 = df_copy[col].quantile(0.25)
                Q3 = df_copy[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                # Count outliers
                lower_outliers = (df_copy[col] < lower_bound).sum()
                upper_outliers = (df_copy[col] > upper_bound).sum()
                
                # Replace outliers with bounds
                df_copy.loc[df_copy[col] < lower_bound, col] = lower_bound
                df_copy.loc[df_copy[col] > upper_bound, col] = upper_bound
                
            elif method == 'capping':
                # Capping method (cap at certain percentiles)
                lower_bound = df_copy[col].quantile(0.01)
                upper_bound = df_copy[col].quantile(0.99)
                
                # Count outliers
                lower_outliers = (df_copy[col] < lower_bound).sum()
                upper_outliers = (df_copy[col] > upper_bound).sum()
                
                # Cap values
                df_copy.loc[df_copy[col] < lower_bound, col] = lower_bound
                df_copy.loc[df_copy[col] > upper_bound, col] = upper_bound
            
            # Calculate statistics after handling outliers
            stats_after = {
                'min': df_copy[col].min(),
                'max': df_copy[col].max(),
                'mean': df_copy[col].mean(),
                'std': df_copy[col].std()
            }
            
            # Store outlier information
            outlier_info[col] = {
                'method': method,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'lower_outliers': lower_outliers,
                'upper_outliers': upper_outliers,
                'total_outliers': lower_outliers + upper_outliers,
                'stats_before': stats_before,
                'stats_after': stats_after
            }
        
        return df_copy, outlier_info
        
    except Exception as e:
        print(f"Error in handle_outliers: {str(e)}")
        return df.copy(), {}

def encode_categorical_features(df, categorical_cols):
    """
    Encode categorical features using one-hot encoding.
    
    Parameters:
    df (pandas.DataFrame): Input DataFrame
    categorical_cols (list): List of categorical column names
    
    Returns:
    tuple: (encoded_df, encoders_dict)
        - encoded_df: DataFrame with encoded categorical features
        - encoders_dict: Dictionary of encoders used for each column
    """
    # Create a copy to avoid modifying the original
    df_copy = df.copy()
    encoders_dict = {}
    
    # For each categorical column
    for col in categorical_cols:
        # Check if the column has only 2 unique values (binary)
        if df_copy[col].nunique() == 2:
            # Use Label Encoder for binary features
            le = LabelEncoder()
            df_copy[col] = le.fit_transform(df_copy[col])
            encoders_dict[col] = {'type': 'label', 'encoder': le}
        else:
            # Use One-Hot Encoder for multi-category features
            encoder = OneHotEncoder(sparse=False, drop='first')
            encoded_features = encoder.fit_transform(df_copy[[col]])
            
            # Create new feature names
            feature_names = [f"{col}_{category}" for category in encoder.categories_[0][1:]]
            
            # Create a temporary DataFrame with the encoded features
            encoded_df = pd.DataFrame(encoded_features, columns=feature_names, index=df_copy.index)
            
            # Add the encoded features to the original DataFrame
            df_copy = pd.concat([df_copy, encoded_df], axis=1)
            
            # Drop the original categorical column
            df_copy = df_copy.drop(col, axis=1)
            
            # Store the encoder
            encoders_dict[col] = {'type': 'onehot', 'encoder': encoder, 'feature_names': feature_names}
    
    return df_copy, encoders_dict

def calculate_correlation_matrix(df, numerical_cols):
    """
    Calculate the correlation matrix for numerical features.
    
    Parameters:
    df (pandas.DataFrame): Input DataFrame
    numerical_cols (list): List of numerical column names
    
    Returns:
    pandas.DataFrame: Correlation matrix
    """
    try:
        # Validate input columns
        valid_cols = [col for col in numerical_cols if col in df.columns]
        if len(valid_cols) != len(numerical_cols):
            missing = set(numerical_cols) - set(valid_cols)
            print(f"Warning: Some columns not found in DataFrame: {missing}")
        
        if not valid_cols:
            print("Error: No valid columns to calculate correlation")
            return pd.DataFrame()
            
        return df[valid_cols].corr()
    except Exception as e:
        print(f"Error calculating correlation matrix: {str(e)}")
        return pd.DataFrame()

def remove_highly_correlated_features(df, threshold=0.75, show_plot=True):
    """
    Identify and remove highly correlated features.
    
    Parameters:
    df (pandas.DataFrame): Input DataFrame
    threshold (float): Correlation threshold above which to remove features
    show_plot (bool): Whether to display the correlation heatmap
    
    Returns:
    tuple: (df_filtered, dropped_features, corr_matrix)
        - df_filtered: DataFrame with highly correlated features removed
        - dropped_features: List of features that were dropped
        - corr_matrix: Correlation matrix of numerical features
    """
    try:
        # Create a copy
        df_copy = df.copy()
        
        # Get numerical columns
        numerical_cols = df_copy.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        if len(numerical_cols) < 2:
            print("Not enough numerical columns for correlation analysis")
            return df_copy, [], pd.DataFrame()
        
        # Calculate correlation matrix
        corr_matrix = df_copy[numerical_cols].corr()
        
        if show_plot:
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
            plt.title(f'Correlation Matrix of Numerical Features')
            plt.tight_layout()
            plt.show()
        
        # Create a mask for the upper triangle
        upper_triangle = np.triu(corr_matrix, k=1)
        
        # Find feature pairs with correlation greater than the threshold
        high_corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(upper_triangle[i, j]) > threshold:
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    corr_value = upper_triangle[i, j]
                    high_corr_pairs.append((col1, col2, corr_value))
        
        # Features to potentially drop (those appearing in correlated pairs)
        potential_drops = set()
        for col1, col2, _ in high_corr_pairs:
            potential_drops.add(col1)
            potential_drops.add(col2)
        
        # For each highly correlated pair, decide which one to drop
        # Strategy: For each correlation group, keep the feature that has
        # the highest average correlation with target (if provided)
        features_to_drop = []
        
        # Process each correlation pair
        processed_cols = set()
        for col1, col2, corr_value in high_corr_pairs:
            if col1 in processed_cols or col2 in processed_cols:
                continue
                
            # Decide which one to drop - we'll drop the second column by default
            # This strategy can be improved with domain knowledge or correlation with target
            features_to_drop.append(col2)
            processed_cols.add(col1)
            processed_cols.add(col2)
            print(f"High correlation ({corr_value:.2f}) between '{col1}' and '{col2}'. Dropping '{col2}'")
        
        # Remove the selected features
        df_filtered = df_copy.drop(columns=features_to_drop)
        
        print(f"Removed {len(features_to_drop)} highly correlated features out of {len(numerical_cols)} numerical features")
        return df_filtered, features_to_drop, corr_matrix
        
    except Exception as e:
        print(f"Error in remove_highly_correlated_features: {str(e)}")
        return df.copy(), [], pd.DataFrame()


def create_preprocessing_pipeline(numerical_features, categorical_features):
    """
    Create a preprocessing pipeline for numerical and categorical features.
    
    Parameters:
    numerical_features (list): List of numerical feature names
    categorical_features (list): List of categorical feature names
    
    Returns:
    ColumnTransformer: Preprocessing pipeline
    """
    try:
        # Numerical preprocessing pipeline
        numerical_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        # Categorical preprocessing pipeline
        categorical_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(sparse=False, handle_unknown='ignore'))
        ])
        
        # Combine pipelines
        preprocessing_pipeline = ColumnTransformer(
            transformers=[
                ('num', numerical_pipeline, numerical_features),
                ('cat', categorical_pipeline, categorical_features)
            ],
            remainder='drop'  # Drop other columns not specified in the transformers
        )
        
        return preprocessing_pipeline
        
    except Exception as e:
        print(f"Error creating preprocessing pipeline: {str(e)}")
        return None


def prepare_training_data(X_train, y_train, X_test, y_test, numerical_features, categorical_features):
    """
    Prepare training and testing data using a preprocessing pipeline.
    
    Parameters:
    X_train (pandas.DataFrame): Training features
    y_train (pandas.Series): Training target
    X_test (pandas.DataFrame): Testing features
    y_test (pandas.Series): Testing target
    numerical_features (list): List of numerical feature names
    categorical_features (list): List of categorical feature names
    
    Returns:
    tuple: (X_train_processed, y_train, X_test_processed, y_test, preprocessing_pipeline)
    """
    try:
        # Create the preprocessing pipeline
        preprocessing_pipeline = create_preprocessing_pipeline(
            numerical_features, categorical_features
        )
        
        if preprocessing_pipeline is None:
            print("Failed to create preprocessing pipeline")
            return None, None, None, None, None
        
        # Fit and transform the training data
        X_train_processed = preprocessing_pipeline.fit_transform(X_train)
        
        # Transform the testing data
        X_test_processed = preprocessing_pipeline.transform(X_test)
        
        print(f"Processed training data shape: {X_train_processed.shape}")
        print(f"Processed testing data shape: {X_test_processed.shape}")
        
        return X_train_processed, y_train, X_test_processed, y_test, preprocessing_pipeline
        
    except Exception as e:
        print(f"Error preparing training data: {str(e)}")
        return None, None, None, None, None


def calculate_class_weights(y):
    """
    Calculate class weights for imbalanced datasets.
    
    Parameters:
    y (array-like): Target variable
    
    Returns:
    dict: Class weights dictionary
    """
    try:
        # Convert to numpy array if not already
        y_np = np.array(y)
        
        # Count of each class
        classes, counts = np.unique(y_np, return_counts=True)
        
        # Calculate weights
        n_samples = len(y_np)
        n_classes = len(classes)
        
        # Calculate weights inversely proportional to class frequencies
        weights = n_samples / (n_classes * counts)
        
        # Create dictionary mapping class to weight
        class_weights = {classes[i]: weights[i] for i in range(len(classes))}
        
        print("Class weights:")
        for cls, weight in class_weights.items():
            print(f"Class {cls}: {weight:.4f}")
        
        return class_weights
        
    except Exception as e:
        print(f"Error calculating class weights: {str(e)}")
        return None


def apply_smote(X_train, y_train, random_state=42):
    """
    Apply SMOTE to oversample the minority class.
    
    Parameters:
    X_train (array-like): Training features
    y_train (array-like): Training target
    random_state (int): Random state for reproducibility
    
    Returns:
    tuple: (X_resampled, y_resampled)
    """
    try:
        # Check if SMOTE can be applied
        class_counts = np.bincount(y_train)
        if min(class_counts) < 5:
            print("Warning: Not enough samples in minority class for SMOTE. Using original data.")
            return X_train, y_train
            
        # Apply SMOTE
        smote = SMOTE(random_state=random_state)
        X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
        
        # Print class distribution before and after
        before_counts = np.bincount(y_train)
        after_counts = np.bincount(y_resampled)
        
        print("Class distribution before SMOTE:")
        for i, count in enumerate(before_counts):
            print(f"Class {i}: {count} samples")
            
        print("\nClass distribution after SMOTE:")
        for i, count in enumerate(after_counts):
            print(f"Class {i}: {count} samples")
            
        return X_resampled, y_resampled
        
    except Exception as e:
        print(f"Error applying SMOTE: {str(e)}")
        return X_train, y_train