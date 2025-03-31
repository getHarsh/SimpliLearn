
"""
Model utility functions for the Housing Loan Data Analysis project.
These functions handle model building, training, and evaluation.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, 
    roc_auc_score, precision_recall_curve, auc
)
import pickle
import os

def build_model(input_dim, dropout_rate1=0.3, dropout_rate2=0.2):
    """
    Build a deep learning model for housing loan default prediction.
    
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
    
    # Print model summary
    model.summary()
    
    return model

def calculate_sensitivity(y_true, y_pred):
    """
    Calculate sensitivity (recall) for the positive class.
    
    Parameters:
    y_true (array-like): True labels
    y_pred (array-like): Predicted labels
    
    Returns:
    float: Sensitivity (recall) score
    """
    # Calculate confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    
    # Calculate sensitivity (recall)
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    return sensitivity

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


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model with focus on housing loan default prediction metrics.
    
    Parameters:
    model (keras.Model): The trained model
    X_test (array-like): Test features
    y_test (array-like): Test target
    
    Returns:
    dict: Dictionary of evaluation metrics
    """
    # Generate predictions
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype('int32').flatten()
    
    # Calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    # Calculate metrics
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    f1 = 2 * (precision * sensitivity) / (precision + sensitivity) if (precision + sensitivity) > 0 else 0
    
    # Calculate ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
    roc_auc = auc(fpr, tpr)
    
    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Housing Loan Default Prediction - Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Print additional metrics
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Sensitivity (Recall): {sensitivity:.4f}")
    print(f"Specificity: {specificity:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"ROC AUC: {roc_auc:.4f}")
    
    # Plot ROC curve
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Housing Loan Default Prediction - ROC Curve')
    plt.legend(loc="lower right")
    plt.show()
    
    # Store metrics in dictionary
    metrics = {
        'confusion_matrix': cm,
        'accuracy': accuracy,
        'sensitivity': sensitivity,
        'specificity': specificity,
        'precision': precision,
        'f1': f1,
        'roc_auc': roc_auc,
        'fpr': fpr,
        'tpr': tpr
    }
    
    return metrics