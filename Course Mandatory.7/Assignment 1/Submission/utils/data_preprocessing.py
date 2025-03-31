"""
Utility functions for data preprocessing in the Lending Club Loan Default Prediction project.
This module contains functions for cleaning, transforming, and preparing data for model training.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import pickle
import os


def handle_missing_values(df):
    """
    Handle missing values in the dataset.
    
    Parameters:
    df (pd.DataFrame): The input dataset
    
    Returns:
    pd.DataFrame: Dataset with handled missing values
    """
    # Make a copy to avoid modifying the original
    df_cleaned = df.copy()
    
    # For numerical columns, fill missing values with median
    numerical_cols = df_cleaned.select_dtypes(include=['number']).columns
    for col in numerical_cols:
        if df_cleaned[col].isnull().sum() > 0:
            median_value = df_cleaned[col].median()
            df_cleaned[col].fillna(median_value, inplace=True)
    
    # For categorical columns, fill missing values with mode
    categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_cleaned[col].isnull().sum() > 0:
            mode_value = df_cleaned[col].mode()[0]
            df_cleaned[col].fillna(mode_value, inplace=True)
    
    print("Missing values after handling:")
    print(df_cleaned.isnull().sum())
    
    return df_cleaned


def handle_outliers(df, numerical_cols, method='clip'):
    """
    Detect and handle outliers in numerical columns.
    
    Parameters:
    df (pd.DataFrame): The input dataset
    numerical_cols (list): List of numerical column names
    method (str): Method to handle outliers ('clip' or 'remove')
    
    Returns:
    pd.DataFrame: Dataset with handled outliers
    """
    df_processed = df.copy()
    
    for col in numerical_cols:
        Q1 = df_processed[col].quantile(0.25)
        Q3 = df_processed[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        if method == 'clip':
            # Cap outliers at boundaries
            df_processed[col] = df_processed[col].clip(lower=lower_bound, upper=upper_bound)
        elif method == 'remove':
            # Filter out outliers
            df_processed = df_processed[(df_processed[col] >= lower_bound) & 
                                       (df_processed[col] <= upper_bound)]
    
    return df_processed


def remove_highly_correlated_features(df, threshold=0.75):
    """
    Identify and remove highly correlated features.
    
    Parameters:
    df (pd.DataFrame): The input dataset
    threshold (float): Correlation threshold above which to remove features
    
    Returns:
    pd.DataFrame: Dataset with highly correlated features removed
    tuple: (correlation_matrix, set of removed features)
    """
    # Calculate correlation matrix
    correlation_matrix = df.corr()
    
    # Find features with correlation greater than the threshold
    high_corr_features = set()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) > threshold:
                colname = correlation_matrix.columns[i]
                high_corr_features.add(colname)
    
    # Remove highly correlated features
    df_processed = df.drop(columns=high_corr_features, errors='ignore')
    
    print(f"Removed {len(high_corr_features)} highly correlated features: {high_corr_features}")
    
    return df_processed, (correlation_matrix, high_corr_features)


def create_preprocessing_pipeline(numerical_cols, categorical_cols):
    """
    Create a preprocessing pipeline for numerical and categorical features.
    
    Parameters:
    numerical_cols (list): List of numerical column names
    categorical_cols (list): List of categorical column names
    
    Returns:
    ColumnTransformer: Preprocessing pipeline
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(drop='first'), categorical_cols)
        ])
    
    return preprocessor


def prepare_training_data(df, target_col='not.fully.paid', test_size=0.2, random_state=42, apply_smote=True):
    """
    Prepare data for model training, including train-test split and class balancing.
    
    Parameters:
    df (pd.DataFrame): The preprocessed dataset
    target_col (str): Name of the target column
    test_size (float): Proportion of data to use for testing
    random_state (int): Random seed for reproducibility
    apply_smote (bool): Whether to apply SMOTE to balance classes
    
    Returns:
    tuple: (X_train, X_test, y_train, y_test, X_train_balanced, y_train_balanced, preprocessor)
    """
    # Split features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['number']).columns.tolist()
    
    # Create preprocessing pipeline
    preprocessor = create_preprocessing_pipeline(numerical_cols, categorical_cols)
    
    # Apply preprocessing
    X_train_preprocessed = preprocessor.fit_transform(X_train)
    X_test_preprocessed = preprocessor.transform(X_test)
    
    # Apply SMOTE for class balancing if requested
    if apply_smote:
        smote = SMOTE(random_state=random_state)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train_preprocessed, y_train)
        
        print("Class distribution before SMOTE:")
        print(pd.Series(y_train).value_counts())
        print("\nClass distribution after SMOTE:")
        print(pd.Series(y_train_balanced).value_counts())
    else:
        X_train_balanced, y_train_balanced = X_train_preprocessed, y_train
    
    return X_train_preprocessed, X_test_preprocessed, y_train, y_test, X_train_balanced, y_train_balanced, preprocessor


def calculate_class_weights(y_train):
    """
    Calculate class weights for imbalanced data.
    
    Parameters:
    y_train (array-like): Training target values
    
    Returns:
    dict: Class weights dictionary
    """
    from sklearn.utils.class_weight import compute_class_weight
    
    classes = np.unique(y_train)
    class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
    class_weight_dict = {i: class_weights[i] for i in range(len(classes))}
    
    return class_weight_dict


def save_preprocessor(preprocessor, filepath='models/preprocessor.pkl'):
    """
    Save the preprocessing pipeline to disk.
    
    Parameters:
    preprocessor (ColumnTransformer): The fitted preprocessor
    filepath (str): Path to save the preprocessor
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        with open(filepath, 'wb') as file:
            pickle.dump(preprocessor, file)
        print(f"Preprocessor saved to {filepath}")
    except Exception as e:
        print(f"Error saving preprocessor: {e}")


def load_preprocessor(filepath='models/preprocessor.pkl'):
    """
    Load the preprocessing pipeline from disk.
    
    Parameters:
    filepath (str): Path to the saved preprocessor
    
    Returns:
    ColumnTransformer: The loaded preprocessor
    """
    try:
        with open(filepath, 'rb') as file:
            preprocessor = pickle.load(file)
        return preprocessor
    except FileNotFoundError:
        print(f"Preprocessor file not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error loading preprocessor: {e}")
        return None