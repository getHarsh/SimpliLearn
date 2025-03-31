"""
Utility functions for model building, training, and evaluation in the Lending Club Loan Default Prediction project.
This module contains functions for creating models, training, evaluation, and visualization.
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, 
    roc_auc_score, precision_recall_curve, auc
)
import pickle
import os


def build_model(input_dim, dropout_rate1=0.3, dropout_rate2=0.2):
    """
    Build a deep learning model for loan default prediction.
    
    Parameters:
    input_dim (int): Input dimension (number of features)
    dropout_rate1 (float): Dropout rate for first layer
    dropout_rate2 (float): Dropout rate for second layer
    
    Returns:
    keras.Sequential: Compiled model
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(dropout_rate1),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(dropout_rate2),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=[
            tf.keras.metrics.AUC(),
            tf.keras.metrics.Precision(),
            tf.keras.metrics.Recall()
        ]
    )
    
    return model


def create_callbacks(checkpoint_dir='models/checkpoints'):
    """
    Create training callbacks for model checkpointing and early stopping.
    
    Parameters:
    checkpoint_dir (str): Directory to save model checkpoints
    
    Returns:
    list: List of callbacks
    """
    # Ensure checkpoint directory exists
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    # Create checkpoint callback
    checkpoint_path = os.path.join(checkpoint_dir, "model-{epoch:02d}-{val_auc:.2f}.h5")
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        checkpoint_path, 
        monitor='val_auc', 
        save_best_only=True,
        save_weights_only=False,
        mode='max',
        verbose=1
    )
    
    # Create early stopping callback
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_auc',
        patience=10,
        restore_best_weights=True,
        mode='max'
    )
    
    return [checkpoint_callback, early_stopping]


def train_model(model, X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, 
                callbacks=None, class_weight=None, save_dir='models'):
    """
    Train the model and save training history.
    
    Parameters:
    model (keras.Model): The model to train
    X_train (array-like): Training features
    y_train (array-like): Training target
    epochs (int): Maximum number of epochs
    batch_size (int): Batch size
    validation_split (float): Proportion of training data to use for validation
    callbacks (list): List of callbacks
    class_weight (dict): Optional class weights for imbalanced data
    save_dir (str): Directory to save model and history
    
    Returns:
    tuple: (trained model, training history)
    """
    # Ensure directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Train the model
    history = model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        callbacks=callbacks,
        class_weight=class_weight,
        verbose=1
    )
    
    # Save the final model
    model_path = os.path.join(save_dir, 'final_model.h5')
    try:
        model.save(model_path)
        print(f"Model saved to {model_path}")
    except Exception as e:
        print(f"Error saving model: {e}")
    
    # Save the training history
    history_path = os.path.join(save_dir, 'model_history.pkl')
    try:
        with open(history_path, 'wb') as file:
            pickle.dump(history.history, file)
        print(f"Training history saved to {history_path}")
    except Exception as e:
        print(f"Error saving training history: {e}")
    
    return model, history


def plot_training_history(history):
    """
    Plot the training and validation metrics.
    
    Parameters:
    history (History): Keras training history object
    """
    if not history or not hasattr(history, 'history'):
        print("No valid training history provided")
        return
        
    plt.figure(figsize=(15, 5))
    
    # Plot loss
    plt.subplot(1, 3, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    if 'val_loss' in history.history:
        plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    # Plot AUC
    plt.subplot(1, 3, 2)
    if 'auc' in history.history:
        plt.plot(history.history['auc'], label='Training AUC')
    if 'val_auc' in history.history:
        plt.plot(history.history['val_auc'], label='Validation AUC')
    plt.title('Training and Validation AUC')
    plt.xlabel('Epoch')
    plt.ylabel('AUC')
    plt.legend()
    
    # Plot Precision and Recall
    plt.subplot(1, 3, 3)
    if 'precision' in history.history:
        plt.plot(history.history['precision'], label='Precision')
    if 'recall' in history.history:
        plt.plot(history.history['recall'], label='Recall')
    plt.title('Precision and Recall')
    plt.xlabel('Epoch')
    plt.ylabel('Score')
    plt.legend()
    
    plt.tight_layout()
    plt.show()


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model and generate various performance metrics and visualizations.
    
    Parameters:
    model (keras.Model): The trained model
    X_test (array-like): Test features
    y_test (array-like): Test target
    
    Returns:
    dict: Dictionary of evaluation metrics
    """
    if model is None:
        print("No model provided for evaluation")
        return {}
    
    # Get predictions
    try:
        y_pred_prob = model.predict(X_test)
        y_pred_classes = (y_pred_prob > 0.5).astype(int).flatten()
    except Exception as e:
        print(f"Error making predictions: {e}")
        return {}
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred_classes)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()
    
    # Classification Report
    cr = classification_report(y_test, y_pred_classes)
    print("\nClassification Report:")
    print(cr)
    
    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()
    
    # Precision-Recall Curve
    precision, recall, _ = precision_recall_curve(y_test, y_pred_prob)
    pr_auc = auc(recall, precision)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='green', lw=2, label=f'PR curve (area = {pr_auc:.2f})')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.show()
    
    # Compile metrics
    metrics = {
        'accuracy': (y_pred_classes == y_test).mean(),
        'auc': roc_auc,
        'pr_auc': pr_auc
    }
    
    return metrics


def analyze_feature_importance(model, feature_names, top_n=10):
    """
    Analyze feature importance using model weights.
    Note: This is a simple approach; more sophisticated methods exist.
    
    Parameters:
    model (keras.Model): The trained model
    feature_names (list): List of feature names
    top_n (int): Number of top features to display
    
    Returns:
    pd.DataFrame: Feature importance DataFrame
    """
    if model is None:
        print("No model provided for feature importance analysis")
        return pd.DataFrame()
        
    # Get weights from the first layer
    try:
        weights = model.layers[0].get_weights()[0]
    except (IndexError, AttributeError) as e:
        print(f"Error accessing model weights: {e}")
        return pd.DataFrame()
    
    # Calculate absolute importance as the sum of absolute weights for each feature
    importance = np.sum(np.abs(weights), axis=1)
    
    # Create DataFrame with feature names and importance
    feature_importance = pd.DataFrame({
        'Feature': feature_names[:len(importance)],  # Ensure lengths match
        'Importance': importance
    })
    
    # Sort by importance
    feature_importance = feature_importance.sort_values('Importance', ascending=False)
    
    # Plot top features
    plt.figure(figsize=(10, 6))
    top_features = feature_importance.head(min(top_n, len(feature_importance)))
    plt.barh(top_features['Feature'], top_features['Importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title(f'Top {min(top_n, len(feature_importance))} Features by Importance')
    plt.gca().invert_yaxis()  # Display highest importance at the top
    plt.tight_layout()
    plt.show()
    
    return feature_importance


def threshold_analysis(model, X_test, y_test, thresholds=None):
    """
    Analyze model performance across different classification thresholds.
    
    Parameters:
    model (keras.Model): The trained model
    X_test (array-like): Test features
    y_test (array-like): Test target
    thresholds (list): List of threshold values to evaluate (default: [0.3, 0.4, 0.5, 0.6, 0.7])
    
    Returns:
    pd.DataFrame: Dataframe of threshold performance metrics
    """
    if model is None:
        print("No model provided for threshold analysis")
        return pd.DataFrame()
        
    if thresholds is None:
        thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
    
    # Get predictions
    try:
        y_pred_prob = model.predict(X_test).flatten()
    except Exception as e:
        print(f"Error making predictions: {e}")
        return pd.DataFrame()
    
    # Initialize results list
    results = []
    
    # Evaluate each threshold
    for threshold in thresholds:
        y_pred = (y_pred_prob >= threshold).astype(int)
        
        # Calculate metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Store results
        results.append({
            'threshold': threshold,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        })
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['threshold'], results_df['accuracy'], marker='o', label='Accuracy')
    plt.plot(results_df['threshold'], results_df['precision'], marker='s', label='Precision')
    plt.plot(results_df['threshold'], results_df['recall'], marker='^', label='Recall')
    plt.plot(results_df['threshold'], results_df['f1_score'], marker='d', label='F1 Score')
    plt.title('Performance Metrics at Different Thresholds')
    plt.xlabel('Threshold')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return results_df


def save_model(model, filepath='models/final_model.h5'):
    """
    Save the trained model to disk.
    
    Parameters:
    model (keras.Model): The trained model
    filepath (str): Path to save the model
    """
    if model is None:
        print("No model provided to save")
        return
        
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        model.save(filepath)
        print(f"Model saved to {filepath}")
    except Exception as e:
        print(f"Error saving model: {e}")


def load_model(filepath='models/final_model.h5'):
    """
    Load the trained model from disk.
    
    Parameters:
    filepath (str): Path to the saved model
    
    Returns:
    keras.Model: The loaded model
    """
    try:
        model = tf.keras.models.load_model(filepath)
        print(f"Model loaded successfully from {filepath}")
        return model
    except FileNotFoundError:
        print(f"Model file not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None