"""
Model utility functions for the Automating Port Operations project.
These functions handle model building, evaluation, and visualization.
"""

import os
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models, applications
from sklearn.metrics import confusion_matrix, classification_report, precision_score, recall_score
from tqdm import tqdm
from IPython.display import Image, display

def build_custom_cnn(input_shape, num_classes):
    """
    Build a custom CNN model for boat classification.
    
    Parameters:
    input_shape (tuple): Input shape of the images (height, width, channels)
    num_classes (int): Number of boat classes
    
    Returns:
    tf.keras.Model: Compiled CNN model
    """
    model = models.Sequential([
        # First Conv2D block
        layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        
        # Second Conv2D block
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        
        # Global Average Pooling
        layers.GlobalAveragePooling2D(),
        
        # Dense layers
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        
        # Output layer
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def build_mobilenet_model(input_shape, num_classes):
    """
    Build a MobileNetV2-based model for boat classification using transfer learning.
    
    Parameters:
    input_shape (tuple): Input shape of the images (height, width, channels)
    num_classes (int): Number of boat classes
    
    Returns:
    tf.keras.Model: Compiled MobileNetV2-based model
    """
    # Load MobileNetV2 pre-trained on ImageNet without the top classification layer
    base_model = applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the base model layers
    base_model.trainable = False
    
    # Create the model
    model = models.Sequential([
        # Base model
        base_model,
        
        # Global Average Pooling
        layers.GlobalAveragePooling2D(),
        
        # Dropout
        layers.Dropout(0.2),
        
        # Dense layer with batch normalization
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        
        # Dropout
        layers.Dropout(0.1),
        
        # Dense layer with batch normalization
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        
        # Dropout
        layers.Dropout(0.1),
        
        # Output layer
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def plot_training_history(history, model_name="Model"):
    """
    Plot the training and validation loss and accuracy curves.
    
    Parameters:
    history: History object from model.fit()
    model_name (str): Name of the model for plot titles
    
    Returns:
    None (displays plots)
    """
    # Plot training & validation accuracy values
    plt.figure(figsize=(15, 5))
    
    # Plot accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title(f'{model_name} - Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Plot loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title(f'{model_name} - Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Plot precision and recall if available
    if 'precision' in history.history and 'recall' in history.history:
        plt.figure(figsize=(15, 5))
        
        # Plot precision
        plt.subplot(1, 2, 1)
        plt.plot(history.history['precision'])
        plt.plot(history.history['val_precision'])
        plt.title(f'{model_name} - Precision')
        plt.ylabel('Precision')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper left')
        plt.grid(True, alpha=0.3)
        
        # Plot recall
        plt.subplot(1, 2, 2)
        plt.plot(history.history['recall'])
        plt.plot(history.history['val_recall'])
        plt.title(f'{model_name} - Recall')
        plt.ylabel('Recall')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper left')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def evaluate_model(model, test_ds, class_names, **kwargs):
    """
    Evaluate a model on the test dataset and save evaluation artifacts.
    
    Parameters:
    model (keras.Model): Model to evaluate
    test_ds (tf.data.Dataset): Test dataset
    class_names (list): List of class names
    model_name (str): Name of the model (e.g., 'cnn', 'mobilenet')
    save_dir (str): Directory to save evaluation results
    
    Returns:
    tuple: (test_loss, test_accuracy, test_precision, test_recall, test_predictions, test_true_labels)
    """
    model_name = kwargs.get('model_name', 'model')
    save_dir = kwargs.get('save_dir', 'models')
    
    try:
        # Create directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        # Get timestamp for versioning
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Evaluate the model (get basic metrics)
        print(f"Evaluating {model_name} model...")
        result = model.evaluate(test_ds, verbose=0)
        
        # Handle different return formats in different TF versions
        if isinstance(result, list) and len(result) >= 4:
            test_loss, test_accuracy = result[0], result[1]
            # Some models may include precision and recall directly
            test_precision_direct = result[2] if len(result) > 2 else None
            test_recall_direct = result[3] if len(result) > 3 else None
        else:
            # Only loss and accuracy were returned
            if isinstance(result, list) and len(result) == 2:
                test_loss, test_accuracy = result
            else:
                test_loss, test_accuracy = result, 0
            test_precision_direct = None
            test_recall_direct = None
        
        print(f"Test Loss: {test_loss:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        
        # Generate predictions
        print("Generating predictions...")
        predictions = []
        true_labels = []
        
        # Use a progress bar for larger datasets
        total_batches = sum(1 for _ in test_ds)
        progress_bar = tqdm(test_ds, total=total_batches, desc=f"Predicting with {model_name}")
        
        for images, labels in progress_bar:
            batch_pred = model.predict(images, verbose=0)
            pred_labels = tf.argmax(batch_pred, axis=1).numpy()
            actual_labels = tf.argmax(labels, axis=1).numpy()
            
            predictions.extend(pred_labels)
            true_labels.extend(actual_labels)
        
        # Convert to numpy arrays for consistency
        predictions = np.array(predictions)
        true_labels = np.array(true_labels)
        
        # Calculate precision and recall using scikit-learn
        # Use our calculated metrics (more reliable across TF versions)
        test_precision = precision_score(true_labels, predictions, average='weighted')
        test_recall = recall_score(true_labels, predictions, average='weighted')
        
        # If we got direct metrics from the model, log both for comparison
        if test_precision_direct is not None:
            print(f"Model-reported Test Precision: {test_precision_direct:.4f}")
            print(f"Calculated Test Precision: {test_precision:.4f}")
        else:
            print(f"Test Precision: {test_precision:.4f}")
            
        if test_recall_direct is not None:
            print(f"Model-reported Test Recall: {test_recall_direct:.4f}")
            print(f"Calculated Test Recall: {test_recall:.4f}")
        else:
            print(f"Test Recall: {test_recall:.4f}")
        
        # Generate confusion matrix
        cm = confusion_matrix(true_labels, predictions)
        
        # Create confusion matrix visualization
        plt.figure(figsize=(12, 10))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title(f'Confusion Matrix - {model_name.title()} Model')
        plt.colorbar()
        
        # Add axis labels
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names, rotation=45, ha='right')
        plt.yticks(tick_marks, class_names)
        
        # Normalize the confusion matrix for percentage view
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        # Add text annotations
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, f"{cm[i, j]}\n({cm_norm[i, j]:.2f})",
                        horizontalalignment="center",
                        color="white" if cm[i, j] > thresh else "black")
        
        plt.tight_layout()
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # Save the confusion matrix to file with timestamp
        cm_filename = f"{save_dir}/{model_name}_confusion_matrix_{timestamp}.png"
        plt.savefig(cm_filename, dpi=300, bbox_inches='tight')
        plt.close()  # Close to free memory
        print(f"Confusion matrix saved to: {cm_filename}")
        
        # Generate and save classification report
        class_report = classification_report(true_labels, predictions, 
                                            target_names=class_names, 
                                            output_dict=True)
        
        # Display classification report
        print("\nClassification Report:")
        print(classification_report(true_labels, predictions, target_names=class_names))
        
        # Save the classification report as JSON
        report_filename = f"{save_dir}/{model_name}_classification_report_{timestamp}.json"
        with open(report_filename, 'w') as f:
            json.dump(class_report, f, indent=4)
        print(f"Classification report saved to: {report_filename}")
        
        # Save predictions for further analysis
        predictions_filename = f"{save_dir}/{model_name}_predictions_{timestamp}.npz"
        np.savez(predictions_filename, 
                predictions=predictions, 
                true_labels=true_labels,
                class_names=np.array(class_names))
        print(f"Predictions saved to: {predictions_filename}")
        
        # Save evaluation metrics
        metrics = {
            'loss': float(test_loss),
            'accuracy': float(test_accuracy),
            'precision': float(test_precision),
            'recall': float(test_recall),
            'timestamp': timestamp,
            'num_test_samples': len(true_labels)
        }
        
        metrics_filename = f"{save_dir}/{model_name}_metrics_{timestamp}.json"
        with open(metrics_filename, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(f"Metrics saved to: {metrics_filename}")
        
        # Display the confusion matrix from file (to avoid WebSocket issues)
        try:
            display(Image(cm_filename))
        except Exception as e:
            print(f"Note: Unable to display image inline. View the saved file at {cm_filename}")
            
        return test_loss, test_accuracy, test_precision, test_recall, predictions, true_labels
    
    except Exception as e:
        print(f"Error evaluating model: {str(e)}")
        import traceback
        traceback.print_exc()
        return 0, 0, 0, 0, [], []

def visualize_model_predictions(model, dataset, class_names, num_images=9):
    """
    Visualize model predictions on sample images from a dataset.
    
    Parameters:
    model: Trained keras model
    dataset: Dataset containing images and labels
    class_names (list): List of class names
    num_images (int): Number of images to visualize
    
    Returns:
    None (displays plot)
    """
    try:
        # Get a batch of images
        images, labels = next(iter(dataset))
        
        # Make predictions
        predictions = model.predict(images)
        pred_labels = tf.argmax(predictions, axis=1).numpy()
        true_labels = tf.argmax(labels, axis=1).numpy()
        
        # Display the images and predictions
        plt.figure(figsize=(15, 15))
        for i in range(min(num_images, len(images))):
            plt.subplot(3, 3, i+1)
            img = images[i].numpy()
            plt.imshow(img)
            
            color = 'green' if pred_labels[i] == true_labels[i] else 'red'
            title = f"True: {class_names[true_labels[i]]}\nPred: {class_names[pred_labels[i]]}"
            plt.title(title, color=color)
            plt.axis('off')
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error visualizing model predictions: {str(e)}")

def create_callbacks(checkpoint_dir='models/checkpoints', patience=10, monitor='val_accuracy'):
    """
    Create training callbacks for model checkpointing and early stopping.
    
    Parameters:
    checkpoint_dir (str): Directory to save model checkpoints
    patience (int): Number of epochs with no improvement after which training will stop
    monitor (str): Metric to monitor for early stopping and checkpoint saving
    
    Returns:
    list: List of callbacks
    """
    try:
        # Ensure checkpoint directory exists
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        # Create checkpoint callback
        checkpoint_path = os.path.join(checkpoint_dir, f"model-{{epoch:02d}}-{{val_accuracy:.4f}}.h5")
        checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            checkpoint_path, 
            monitor=monitor, 
            save_best_only=True,
            save_weights_only=False,
            mode='max',
            verbose=1
        )
        
        # Create early stopping callback
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor=monitor,
            patience=patience,
            restore_best_weights=True,
            mode='max',
            verbose=1
        )
        
        # Return list of callbacks
        return [checkpoint_callback, early_stopping]
    except Exception as e:
        print(f"Error creating callbacks: {str(e)}")
        # Return minimal set of callbacks if there's an error
        return [tf.keras.callbacks.EarlyStopping(patience=patience)]


def save_model(model, model_path, history=None, history_path=None):
    """
    Save a trained model and optionally its training history.
    
    Parameters:
    model (keras.Model): Trained model to save
    model_path (str): Path to save the model
    history (History, optional): Training history
    history_path (str, optional): Path to save the history
    
    Returns:
    bool: True if model was saved successfully
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save the model
        model.save(model_path)
        print(f"Model saved to {model_path}")
        
        # Save history if provided
        if history and history_path:
            os.makedirs(os.path.dirname(history_path), exist_ok=True)
            import pickle
            with open(history_path, 'wb') as f:
                pickle.dump(history.history, f)
            print(f"Training history saved to {history_path}")
            
        return True
    except Exception as e:
        print(f"Error saving model: {str(e)}")
        return False


def load_model(model_path, custom_objects=None):
    """
    Load a saved model.
    
    Parameters:
    model_path (str): Path to the saved model
    custom_objects (dict, optional): Dictionary mapping names to custom classes or functions
    
    Returns:
    keras.Model or None: Loaded model if successful, None otherwise
    """
    try:
        model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)
        print(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None
