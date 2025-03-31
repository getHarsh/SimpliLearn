"""
Data preprocessing utility functions for the Automating Port Operations project.
These functions handle loading, preprocessing, and visualizing image data.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory

def load_and_preprocess_data(dataset_path, img_height, img_width, batch_size, validation_split=0.2, test_split=0.2, seed=42):
    """
    Load and preprocess image data for model training and evaluation.
    
    Parameters:
    dataset_path (str): Path to the dataset directory
    img_height (int): Target image height
    img_width (int): Target image width
    batch_size (int): Batch size for dataset
    validation_split (float): Fraction of data to use for validation
    test_split (float): Fraction of data to use for testing
    seed (int): Random seed for reproducibility
    
    Returns:
    tuple: (train_ds, val_ds, test_ds, class_names)
    """
    try:
        # Check if dataset path exists
        if not os.path.exists(dataset_path):
            # Try to get from environment variable if path doesn't exist
            env_dataset_path = os.environ.get('PORT_OPERATIONS_DATASET')
            if env_dataset_path and os.path.exists(env_dataset_path):
                dataset_path = env_dataset_path
                print(f"Using dataset path from environment variable: {dataset_path}")
            else:
                raise ValueError(f"Dataset path {dataset_path} does not exist and no valid environment variable found")
        
        # Get class names
        class_names = []
        for item in sorted(os.listdir(dataset_path)):
            if os.path.isdir(os.path.join(dataset_path, item)):
                class_names.append(item)
        
        # Instead of trying to filter datasets, let's use a simpler approach:
        # Create a validation split first, then use the remainder for train/test
        
        # Create validation dataset - use 20% of data
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            dataset_path,
            validation_split=validation_split,
            subset="validation",
            seed=seed,
            image_size=(img_height, img_width),
            batch_size=batch_size,
            label_mode='categorical'
        )
        
        # Create a combined dataset for training and testing (80% of data)
        train_test_ds = tf.keras.preprocessing.image_dataset_from_directory(
            dataset_path,
            validation_split=validation_split,
            subset="training",
            seed=seed,
            image_size=(img_height, img_width),
            batch_size=batch_size,
            label_mode='categorical'
        )
        
        # Now split the 80% into train (80% of 80% = 64% of total) and test (20% of 80% = 16% of total)
        # Convert to a list so we can split it
        train_test_images = []
        train_test_labels = []
        
        for images, labels in train_test_ds:
            for i in range(len(images)):
                train_test_images.append(images[i])
                train_test_labels.append(labels[i])
        
        # Convert to numpy arrays for splitting
        train_test_images = np.array(train_test_images)
        train_test_labels = np.array(train_test_labels)
        
        # Shuffle with seed
        np.random.seed(seed)
        indices = np.random.permutation(len(train_test_images))
        train_test_images = train_test_images[indices]
        train_test_labels = train_test_labels[indices]
        
        # Calculate split index
        train_size = int(len(train_test_images) * 0.8)  # 80% for training, 20% for testing
        
        # Split into train and test
        train_images = train_test_images[:train_size]
        train_labels = train_test_labels[:train_size]
        test_images = train_test_images[train_size:]
        test_labels = train_test_labels[train_size:]
        
        # Create tf.data.Dataset from numpy arrays
        train_ds = tf.data.Dataset.from_tensor_slices((train_images, train_labels)).batch(batch_size)
        test_ds = tf.data.Dataset.from_tensor_slices((test_images, test_labels)).batch(batch_size)
        
        # Print dataset sizes
        print(f"Dataset split: {len(train_images)} training, {len(val_ds)*batch_size} validation, {len(test_images)} test images")
        
        # Apply normalization and optimization to all datasets
        train_ds = prepare_dataset(train_ds, cache=True, shuffle=True, augment=False)
        val_ds = prepare_dataset(val_ds, cache=True, shuffle=False, augment=False)
        test_ds = prepare_dataset(test_ds, cache=True, shuffle=False, augment=False)
        
        return train_ds, val_ds, test_ds, class_names
    
    except Exception as e:
        print(f"Error loading and preprocessing data: {str(e)}")
        raise

def prepare_dataset(dataset, cache=True, shuffle=False, augment=False, batch_size=None, prefetch=True):
    """
    Prepare a dataset with various optimization techniques.
    
    Parameters:
    dataset (tf.data.Dataset): The dataset to prepare
    cache (bool): Whether to cache the dataset
    shuffle (bool): Whether to shuffle the dataset
    augment (bool): Whether to apply data augmentation
    batch_size (int): Batch size (if rebatching is needed)
    prefetch (bool): Whether to prefetch the next batch
    
    Returns:
    tf.data.Dataset: The prepared dataset
    """
    try:
        # Apply normalization [0-1]
        normalization_layer = tf.keras.layers.Rescaling(1./255)
        dataset = dataset.map(lambda x, y: (normalization_layer(x), y), 
                              num_parallel_calls=tf.data.AUTOTUNE)
        
        # Apply augmentation if specified
        if augment:
            augmentation_model = data_augmentation()
            dataset = dataset.map(lambda x, y: (augmentation_model(x, training=True), y),
                                 num_parallel_calls=tf.data.AUTOTUNE)
        
        # Cache the dataset
        if cache:
            dataset = dataset.cache()
        
        # Shuffle if specified
        if shuffle:
            dataset = dataset.shuffle(buffer_size=1000)
        
        # Rebatch if specified
        if batch_size is not None:
            dataset = dataset.batch(batch_size)
        
        # Prefetch next batch while current batch is being processed
        if prefetch:
            dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
        
        return dataset
    
    except Exception as e:
        print(f"Error preparing dataset: {str(e)}")
        return dataset  # Return original dataset if error occurs

def visualize_data(dataset_path, categories, samples_per_class=3):
    """
    Visualize sample images from each category in the dataset.
    
    Parameters:
    dataset_path (str): Path to the dataset directory
    categories (list): List of category names
    samples_per_class (int): Number of sample images to display per class
    
    Returns:
    None (displays the plot)
    """
    try:
        plt.figure(figsize=(15, 12))
        
        for i, category in enumerate(sorted(categories)):
            category_path = os.path.join(dataset_path, category)
            if not os.path.isdir(category_path):
                continue
                
            images = os.listdir(category_path)
            images = [img for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if not images:
                continue
                
            # Select random samples
            samples = np.random.choice(images, min(samples_per_class, len(images)), replace=False)
            
            for j, sample in enumerate(samples):
                sample_path = os.path.join(category_path, sample)
                
                # Load and display the image
                img = plt.imread(sample_path)
                plt.subplot(len(categories), samples_per_class, i * samples_per_class + j + 1)
                plt.imshow(img)
                plt.title(f"{category}")
                plt.axis('off')
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error visualizing data: {str(e)}")

def data_augmentation():
    """
    Create a data augmentation model for training.
    
    Returns:
    tf.keras.Sequential: A sequential model with data augmentation layers
    """
    try:
        data_augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip('horizontal'),
            tf.keras.layers.RandomRotation(0.2),
            tf.keras.layers.RandomZoom(0.1),
            tf.keras.layers.RandomContrast(0.1),
            tf.keras.layers.RandomBrightness(0.1)
        ])
        
        return data_augmentation
    except Exception as e:
        print(f"Error creating data augmentation model: {str(e)}")
        # Return minimal augmentation if error occurs
        return tf.keras.Sequential([tf.keras.layers.RandomFlip('horizontal')])

def create_augmented_dataset(dataset, augment_factor=2):
    """
    Create an augmented dataset with multiple augmented versions of each image.
    
    Parameters:
    dataset (tf.data.Dataset): Original dataset
    augment_factor (int): Number of augmented versions to create for each image
    
    Returns:
    tf.data.Dataset: Augmented dataset
    """
    try:
        augmentation_model = data_augmentation()
        
        # Function to create augmented versions
        def augment_multiple(image, label):
            # Include the original image
            augmented_images = [image]
            augmented_labels = [label]
            
            # Create augmented versions
            for _ in range(augment_factor - 1):
                augmented_images.append(augmentation_model(image, training=True))
                augmented_labels.append(label)
            
            return tf.data.Dataset.from_tensor_slices((augmented_images, augmented_labels))
        
        # Create a dataset with augmented versions of each image
        augmented_dataset = dataset.flat_map(augment_multiple)
        
        return augmented_dataset
    except Exception as e:
        print(f"Error creating augmented dataset: {str(e)}")
        return dataset  # Return original dataset if error occurs

def get_dataset_info(dataset):
    """
    Get information about a TensorFlow dataset.
    
    Parameters:
    dataset (tf.data.Dataset): Dataset to analyze
    
    Returns:
    dict: Dictionary containing dataset information
    """
    try:
        # Count elements in the dataset
        element_count = 0
        batch_size = None
        
        for images, _ in dataset:
            if batch_size is None and hasattr(images, 'shape') and len(images.shape) > 0:
                batch_size = images.shape[0]
            element_count += 1
            
        # Calculate estimated samples
        if batch_size is not None:
            estimated_samples = element_count * batch_size
        else:
            estimated_samples = element_count
            
        return {
            "batch_count": element_count,
            "batch_size": batch_size,
            "estimated_samples": estimated_samples
        }
    except Exception as e:
        print(f"Error getting dataset info: {str(e)}")
        return {
            "batch_count": 0,
            "batch_size": None,
            "estimated_samples": 0
        }

def balance_dataset(dataset, class_names, oversampling=True):
    """
    Balance a dataset by oversampling minority classes or undersampling majority classes.
    
    Parameters:
    dataset (tf.data.Dataset): Dataset to balance
    class_names (list): List of class names
    oversampling (bool): If True, oversample minority classes; if False, undersample majority classes
    
    Returns:
    tf.data.Dataset: Balanced dataset
    """
    try:
        # Count samples per class
        class_counts = [0] * len(class_names)
        
        # Unbatch the dataset if it's batched
        unbatched_ds = dataset.unbatch() if hasattr(dataset, 'unbatch') else dataset
        
        # Count samples per class
        for _, label in unbatched_ds:
            class_idx = tf.argmax(label).numpy()
            class_counts[class_idx] += 1
        
        print("Class distribution before balancing:")
        for i, name in enumerate(class_names):
            print(f"{name}: {class_counts[i]} samples")
        
        if oversampling:
            # Oversample minority classes
            max_count = max(class_counts)
            balanced_datasets = []
            
            for class_idx, count in enumerate(class_counts):
                # Get samples of this class
                class_ds = unbatched_ds.filter(
                    lambda x, y: tf.equal(tf.argmax(y), class_idx)
                )
                
                # Determine how many times to repeat
                repeat_times = max_count // count + (1 if max_count % count > 0 else 0)
                
                # Repeat the dataset
                repeated_ds = class_ds.repeat(repeat_times)
                
                # Take exactly max_count samples
                balanced_datasets.append(repeated_ds.take(max_count))
            
            # Combine all balanced class datasets
            balanced_ds = balanced_datasets[0]
            for ds in balanced_datasets[1:]:
                balanced_ds = balanced_ds.concatenate(ds)
            
            # Shuffle the balanced dataset
            balanced_ds = balanced_ds.shuffle(buffer_size=max_count * len(class_names))
            
        else:
            # Undersample majority classes
            min_count = min(class_counts)
            balanced_datasets = []
            
            for class_idx, count in enumerate(class_counts):
                # Get samples of this class
                class_ds = unbatched_ds.filter(
                    lambda x, y: tf.equal(tf.argmax(y), class_idx)
                )
                
                # Take exactly min_count samples
                balanced_datasets.append(class_ds.take(min_count))
            
            # Combine all balanced class datasets
            balanced_ds = balanced_datasets[0]
            for ds in balanced_datasets[1:]:
                balanced_ds = balanced_ds.concatenate(ds)
            
            # Shuffle the balanced dataset
            balanced_ds = balanced_ds.shuffle(buffer_size=min_count * len(class_names))
        
        # Print new class distribution
        print("\nClass distribution after balancing:")
        # Calculate the expected balanced count
        balanced_count = max_count if oversampling else min_count
        for i, name in enumerate(class_names):
            print(f"{name}: {balanced_count} samples")
        
        return balanced_ds
    
    except Exception as e:
        print(f"Error balancing dataset: {str(e)}")
        return dataset  # Return original dataset if error occurs
