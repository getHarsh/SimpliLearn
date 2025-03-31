# Data Wrangling Process

This document details the data preprocessing steps I performed for the Automating Port Operations project to prepare the boat image dataset for deep learning model training.

## Overview of the Raw Data

The boat classification dataset contains 1,162 images across 9 different categories of boats. Each image is stored in its corresponding class directory. Before building the deep learning models, I needed to process these images to ensure they were in the appropriate format for model training.

## Step 1: Initial Dataset Exploration

I began by exploring the structure and contents of the dataset:

```python
# List the boat categories and count the number of images in each category
boat_categories = os.listdir(dataset_path)
if '.DS_Store' in boat_categories:  # Remove hidden files if present
    boat_categories.remove('.DS_Store')

print(f"Found {len(boat_categories)} categories of boats:")
for category in sorted(boat_categories):
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        num_images = len(os.listdir(category_path))
        print(f"- {category}: {num_images} images")

total_images = sum([len(os.listdir(os.path.join(dataset_path, cat))) for cat in boat_categories if os.path.isdir(os.path.join(dataset_path, cat))])
print(f"\nTotal number of images: {total_images}")
```

This exploration revealed:
- The distribution of images across the 9 boat categories
- Some class imbalance, with certain boat types having more images than others
- The total number of images available for training

## Step 2: Data Visualization

I visualized sample images from each category to better understand the dataset:

```python
# Visualize sample images from each category
visualize_data(dataset_path, boat_categories)
```

This visualization helped me identify:
- The visual characteristics of each boat type
- The variety of angles, lighting conditions, and backgrounds
- The quality and resolution of the images
- Potential challenges in distinguishing between similar boat types

## Step 3: Dataset Splitting Strategies

For this project, I implemented two different dataset splitting strategies as required:

### 3.1 Custom CNN Dataset Split (80:20)

For the custom CNN model, I split the dataset as follows:
- 80% training data (further split into training and validation)
- 20% testing data
- Random seed set to 43 for reproducibility

```python
train_ds, val_ds, test_ds, class_names = load_and_preprocess_data(
    dataset_path=dataset_path,
    img_height=img_height,
    img_width=img_width,
    batch_size=batch_size,
    validation_split=0.2,  # 20% of training data for validation
    test_split=0.2,  # 20% of all data for testing
    seed=43
)
```

### 3.2 MobileNetV2 Dataset Split (70:30)

For the MobileNetV2 transfer learning model, I used a different split:
- 70% training data (further split into training and validation)
- 30% testing data
- Random seed set to 1 for reproducibility

```python
mobilenet_train_ds, mobilenet_val_ds, mobilenet_test_ds, mobilenet_class_names = load_and_preprocess_data(
    dataset_path=dataset_path,
    img_height=img_height,
    img_width=img_width,
    batch_size=batch_size,
    validation_split=0.2,  # 20% of training data for validation
    test_split=0.3,  # 30% of all data for testing
    seed=1
)
```

## Step 4: Image Preprocessing

I performed several preprocessing steps to prepare the images for model training:

### 4.1 Image Resizing

All images were resized to 224×224 pixels, which is:
- A standard input size for many CNN architectures
- The required input size for MobileNetV2
- A good balance between detail preservation and computational efficiency

### 4.2 Pixel Normalization

I normalized the pixel values by scaling them from [0-255] to [0-1]:

```python
normalization_layer = tf.keras.layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y))
```

This normalization helps with:
- Faster convergence during training
- Numerical stability
- Consistent input scale for the model

### 4.3 Data Batching

I organized the data into batches of 32 images:

```python
batch_size = 32
```

Batching provides several benefits:
- More efficient use of GPU memory
- Faster training through parallel processing
- Better gradient estimates than single-sample updates

### 4.4 Data Prefetching and Caching

To optimize data pipeline performance, I implemented prefetching and caching:

```python
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)
```

These optimizations:
- Reduce disk I/O bottlenecks
- Enable the CPU to prepare data while the GPU is training
- Speed up the overall training process

## Step 5: Data Labels Preparation

For model training, I needed to prepare the labels in the appropriate format:

```python
# Using tf.keras.preprocessing.image_dataset_from_directory with categorical labels
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    validation_split=None,
    subset=None,
    seed=seed,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode='categorical'  # One-hot encoded labels
)
```

By setting `label_mode='categorical'`:
- Labels were converted to one-hot encoded vectors
- Format was appropriate for categorical crossentropy loss
- Each label vector had length equal to the number of classes (9)

## Step 6: Custom Data Loading Implementation

I implemented a custom data loading function to handle the specific requirements of this project:

```python
def load_and_preprocess_data(dataset_path, img_height, img_width, batch_size, validation_split, test_split, seed):
    # Implementation details in data_preprocessing.py
    ...
```

This function:
- Handles the custom dataset splitting requirements
- Applies consistent preprocessing across all data splits
- Ensures reproducibility through fixed random seeds
- Optimizes the data pipeline for training efficiency

## Step 7: Data Augmentation Preparation (Optional)

I prepared a data augmentation function that could be applied during training if needed:

```python
def data_augmentation():
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomContrast(0.1)
    ])
    
    return data_augmentation
```

This augmentation pipeline provides:
- Horizontal flipping to simulate different boat orientations
- Rotation to account for different viewing angles
- Zoom variations to simulate different distances
- Contrast adjustments to handle different lighting conditions

## Challenges and Solutions

Throughout the data wrangling process, I encountered and addressed several challenges:

### Challenge 1: Maintaining Dataset Integrity During Splitting

**Issue**: Ensuring that the dataset splits were correct and balanced.

**Solution**: I implemented a custom function that:
- Manually tracks images and their labels
- Applies random shuffling with a fixed seed
- Separates data into appropriate splits while maintaining class distribution

### Challenge 2: Efficient Data Pipeline

**Issue**: Loading and processing image data efficiently.

**Solution**: I optimized the data pipeline by:
- Using TensorFlow's data API for efficient batch processing
- Implementing caching to avoid redundant disk reads
- Using prefetching to overlap data preprocessing with model training

### Challenge 3: Consistent Preprocessing

**Issue**: Ensuring consistent preprocessing across both models.

**Solution**: I created a centralized preprocessing function that:
- Applies the same resizing and normalization to all images
- Uses the same batching strategy for all datasets
- Maintains consistent label encoding across all splits

## Final Dataset Characteristics

After completing all preprocessing steps, the final datasets had the following characteristics:

### For Custom CNN:
- Training set: Approximately 743 images (80% of data, minus validation)
- Validation set: Approximately 186 images (20% of training data)
- Test set: Approximately 233 images (20% of all data)
- Image dimensions: 224×224×3 (RGB)
- Pixel value range: [0-1]
- Label format: One-hot encoded vectors

### For MobileNetV2:
- Training set: Approximately 650 images (70% of data, minus validation)
- Validation set: Approximately 163 images (20% of training data)
- Test set: Approximately 349 images (30% of all data)
- Image dimensions: 224×224×3 (RGB)
- Pixel value range: [0-1]
- Label format: One-hot encoded vectors

These preprocessed datasets were now ready for model training and evaluation.