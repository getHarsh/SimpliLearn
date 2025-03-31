# Approach to Automating Port Operations

## Overview

In this project, I developed a comprehensive approach to automate boat classification for Marina Pier Inc.'s operations at the San Francisco port. The challenge was to build reliable deep learning models that could accurately classify nine different types of boats, reducing human error in the classification process.

## Methodology

I structured my approach into several key phases:

### 1. Problem Understanding

First, I established a clear understanding of the problem:

- **Business Context**: Marina Pier Inc. needs to automate their port operations to eliminate human error in boat classification.
- **Technical Requirements**: Need for both a standard CNN model and a lightweight mobile-deployable solution.
- **Success Criteria**: High accuracy in classifying nine boat types while ensuring the mobile model is efficient.

### 2. Data Exploration and Assessment

I began with a thorough exploration of the dataset:

- **Dataset Composition**: 1,162 images across 9 boat categories
- **Class Distribution**: Examined the distribution of images across categories to identify any class imbalance
- **Image Characteristics**: Assessed image quality, size, and variation within each class

This exploration guided my preprocessing decisions and helped identify potential challenges, such as distinguishing between visually similar boat types.

### 3. Data Preprocessing Strategy

Based on the exploration phase, I implemented the following preprocessing steps:

- **Data Splitting**:
  - For the custom CNN: 80/20 train-test split with seed=43
  - For the MobileNetV2 model: 70/30 train-test split with seed=1

- **Image Preprocessing**:
  - Resized all images to 224x224 pixels to maintain consistency
  - Normalized pixel values to the range [0-1] for better model convergence
  - Organized data into batches of 32 images for efficient training

- **Data Loading Pipeline**:
  - Used TensorFlow's image_dataset_from_directory for efficient data loading
  - Implemented caching and prefetching to optimize training performance

### 4. Modeling Approach

I implemented two distinct modeling approaches:

#### 4.1 Custom CNN Model

Built a custom convolutional neural network from scratch:
- Two convolutional layers with 32 filters each, followed by max pooling
- Global average pooling to reduce spatial dimensions
- Two dense layers with 128 neurons each
- Output layer with 9 neurons (one for each boat class)

This model provides a baseline performance with a relatively simple architecture.

#### 4.2 MobileNetV2 Transfer Learning Model

Implemented a transfer learning approach using MobileNetV2:
- Used pre-trained MobileNetV2 (trained on ImageNet) as the base model
- Froze the base model's weights to preserve learned features
- Added custom classification layers on top:
  - Global average pooling
  - Dropout for regularization
  - Dense layers with batch normalization
  - Output layer for the 9 boat classes

This approach leverages the power of a pre-trained model while optimizing for mobile deployment.

### 5. Training Strategy

I employed different training strategies for each model:

#### 5.1 Custom CNN Training

- Trained for a fixed 20 epochs
- Used Adam optimizer and categorical crossentropy loss
- Monitored accuracy, precision, and recall metrics
- Analyzed learning curves to assess model performance

#### 5.2 MobileNetV2 Training

- Trained for up to 50 epochs with early stopping
- Monitored validation loss to prevent overfitting
- Implemented model checkpointing to save the best model
- Used the same optimizer and loss function as the custom CNN

### 6. Evaluation Methodology

I conducted a comprehensive evaluation of both models:

- **Performance Metrics**:
  - Accuracy: Overall correctness of classifications
  - Precision: Proportion of positive identifications that were correct
  - Recall: Proportion of actual positives that were identified correctly
  - Loss: Model's prediction error

- **Visual Analysis**:
  - Confusion matrices to identify classification patterns
  - Learning curves to analyze training progression
  - Comparative visualizations of model performance

- **Model Comparison**:
  - Direct comparison of all performance metrics
  - Analysis of model size and complexity
  - Assessment of mobile deployment potential

### 7. Technical Challenges and Solutions

Throughout the project, I encountered and addressed several challenges:

1. **Class Imbalance**:
   - **Challenge**: Some boat types had more images than others
   - **Solution**: Monitored class-specific metrics and considered weighted loss functions

2. **Model Optimization for Mobile**:
   - **Challenge**: Balancing model performance with size constraints
   - **Solution**: Used MobileNetV2 which is specifically designed for mobile applications

3. **Distinguishing Similar Boat Types**:
   - **Challenge**: Some boat categories have similar visual characteristics
   - **Solution**: Leveraged the feature extraction capabilities of MobileNetV2

4. **Limited Dataset Size**:
   - **Challenge**: Relatively small dataset for deep learning
   - **Solution**: Applied transfer learning to leverage pre-trained features

## Implementation Details

### Data Pipeline Implementation

I created a robust data pipeline using TensorFlow's data API:
- Implemented custom functions for loading and preprocessing images
- Ensured proper randomization during data splitting
- Applied normalization to standardize pixel values

### Model Implementation

For both models, I implemented:
- Clear architecture definitions following the project requirements
- Proper model compilation with appropriate metrics
- Effective training loops with progress monitoring
- Model saving functionality for future deployment

### Visualization Tools

I developed visualization functions for:
- Training history (loss and metrics over epochs)
- Confusion matrices for error analysis
- Sample image predictions for qualitative assessment
- Comparative model performance visualization

## Conclusion

My approach combined methodical data preprocessing, strategic model development, and comprehensive evaluation to create an effective boat classification system. The dual-model strategy provides Marina Pier Inc. with both a baseline model and an optimized mobile solution, allowing them to choose based on their specific deployment requirements.

The MobileNetV2 transfer learning approach proved superior in both accuracy and efficiency, demonstrating the power of leveraging pre-trained models even for specialized classification tasks like boat type identification.