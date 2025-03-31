# Model Specifications

This document details the deep learning model architectures, training processes, and implementation decisions for the Automating Port Operations project.

## Model Objectives

The primary objective was to build deep learning models that could accurately classify nine different types of boats for Marina Pier Inc.'s automated port operations. Specifically, I needed to develop:

1. A custom CNN model with a predefined architecture
2. A lightweight model using transfer learning (MobileNetV2) suitable for mobile deployment

## Model 1: Custom CNN Architecture

### Architecture Design

Following the project requirements, I implemented a custom CNN with the following architecture:

```python
def build_custom_cnn(input_shape, num_classes):
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
```

### Architecture Components Explained

1. **Input Layer**:
   - Shape: (224, 224, 3) - RGB images resized to 224×224 pixels
   - This standardized size ensures consistent processing

2. **Convolutional Blocks**:
   - Two identical convolutional blocks, each containing:
     - Conv2D layer with 32 filters and 3×3 kernel size
     - ReLU activation function
     - MaxPooling2D layer with 2×2 pool size
   - These blocks learn hierarchical features from the input images
   - The first block captures low-level features (edges, textures)
   - The second block captures more complex patterns

3. **Global Average Pooling**:
   - Replaces traditional flattening to reduce parameters
   - Makes the model more robust to spatial translations
   - Helps prevent overfitting by reducing parameters

4. **Dense Layers**:
   - Two fully connected layers with 128 neurons each
   - ReLU activation for non-linearity
   - These layers learn higher-level combinations of features

5. **Output Layer**:
   - Dense layer with 9 neurons (one for each boat class)
   - Softmax activation for probability distribution
   - Outputs sum to 1, representing class probabilities

### Model Compilation

The custom CNN was compiled with the following configuration:

```python
cnn_model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy', 
             tf.keras.metrics.Precision(name='precision'),
             tf.keras.metrics.Recall(name='recall')]
)
```

- **Optimizer**: Adam with default learning rate (0.001)
  - Combines benefits of AdaGrad and RMSProp
  - Adaptive learning rate for each parameter
  - Efficient for noisy gradients

- **Loss Function**: Categorical Crossentropy
  - Appropriate for multi-class classification with one-hot encoded labels
  - Measures the difference between predicted and actual distributions

- **Metrics**: 
  - Accuracy: Overall correct predictions
  - Precision: Proportion of positive identifications that were correct
  - Recall: Proportion of actual positives that were identified correctly

### Training Process

The custom CNN was trained with the following parameters:

```python
cnn_history = cnn_model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20,
    verbose=1
)
```

- **Training Data**: 80% of the dataset (minus validation)
- **Validation Data**: 20% of the training set
- **Epochs**: 20 (as specified in requirements)
- **Batch Size**: 32 (set during data preprocessing)

### Model Size and Complexity

The custom CNN has the following characteristics:
- Number of layers: 8 (2 Conv2D, 2 MaxPooling2D, 1 GlobalAveragePooling2D, 3 Dense)
- Total parameters: Approximately 303,000
- Model size: Approximately 1.2 MB

## Model 2: MobileNetV2 Transfer Learning Architecture

### Architecture Design

Following the project requirements, I implemented a transfer learning approach using MobileNetV2:

```python
def build_mobilenet_model(input_shape, num_classes):
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
```

### Architecture Components Explained

1. **Base Model**:
   - MobileNetV2 pre-trained on ImageNet
   - Designed specifically for mobile and edge devices
   - Uses depthwise separable convolutions for efficiency
   - Weights frozen to preserve learned features

2. **Global Average Pooling**:
   - Converts feature maps to a fixed-size vector
   - Reduces parameters while maintaining spatial information
   - Makes the model more robust to spatial translations

3. **Regularization Blocks**:
   - Three regularization blocks, each containing:
     - Dropout layer (0.2 for first, 0.1 for others)
     - Dense layer with ReLU activation
     - BatchNormalization layer
   - These blocks help prevent overfitting
   - Dropout randomly deactivates neurons during training
   - Batch normalization stabilizes and accelerates training

4. **Output Layer**:
   - Dense layer with 9 neurons (one for each boat class)
   - Softmax activation for probability distribution

### Model Compilation

The MobileNetV2 model was compiled with the same configuration as the custom CNN:

```python
mobilenet_model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy', 
             tf.keras.metrics.Precision(name='precision'),
             tf.keras.metrics.Recall(name='recall')]
)
```

### Training Process

The MobileNetV2 model was trained with more sophisticated training management:

```python
# Set up callbacks for early stopping and model checkpointing
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

checkpoint = ModelCheckpoint(
    'mobilenet_boat_classifier.h5',
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)

# Train the model
mobilenet_history = mobilenet_model.fit(
    mobilenet_train_ds,
    validation_data=mobilenet_val_ds,
    epochs=50,
    callbacks=[early_stopping, checkpoint],
    verbose=1
)
```

- **Training Data**: 70% of the dataset (minus validation)
- **Validation Data**: 20% of the training set
- **Maximum Epochs**: 50
- **Early Stopping**: Patience of 10 epochs monitoring validation loss
- **Model Checkpointing**: Saves the best model based on validation loss
- **Batch Size**: 32 (set during data preprocessing)

### Model Size and Complexity

The MobileNetV2-based model has the following characteristics:
- Base model: MobileNetV2 (frozen weights)
- Custom layers: 9 layers added on top
- Total parameters: Approximately 2.3 million (mostly in the base model)
- Trainable parameters: Approximately 400,000 (only in the added layers)
- Model size: Approximately 9 MB

### Transfer Learning Strategy

I implemented a feature extraction transfer learning approach:
- The base MobileNetV2 model was pre-trained on ImageNet (1.4 million images)
- All layers in the base model were frozen (weights not updated during training)
- Only the custom classification layers on top were trained
- This approach leverages the feature extraction capabilities of MobileNetV2
- Particularly effective for a dataset of limited size (~130 images per class)

## Training Management

### Learning Rate Strategy

For both models, I used the Adam optimizer with its default learning rate of 0.001. This adaptive optimizer adjusts learning rates automatically for each parameter, reducing the need for manual learning rate scheduling.

### Regularization Strategy

I implemented different regularization strategies for each model:

1. **Custom CNN**:
   - Minimal regularization due to smaller model size
   - Relies on the simplicity of the architecture to prevent overfitting

2. **MobileNetV2 Model**:
   - Dropout layers (0.2 and 0.1) to prevent co-adaptation of neurons
   - Batch normalization to stabilize learning and reduce internal covariate shift
   - Early stopping to prevent overfitting by monitoring validation loss

### Model Persistence

Both models were saved to disk for future use:

```python
# Save the custom CNN model
cnn_model.save('custom_cnn_boat_classifier.h5')

# MobileNetV2 model saved via ModelCheckpoint
```

This allows the models to be:
- Deployed without retraining
- Used for inference on new images
- Loaded for further fine-tuning if needed

## Implementation Challenges and Solutions

Throughout the modeling process, I encountered and addressed several challenges:

### Challenge 1: Limited Dataset Size

**Issue**: The dataset contains only ~130 images per class, which can lead to overfitting.

**Solution**:
- Implemented transfer learning with MobileNetV2
- Used regularization techniques (dropout, batch normalization)
- Applied early stopping to prevent overfitting

### Challenge 2: Model Optimization for Mobile

**Issue**: Ensuring the model is lightweight enough for mobile deployment while maintaining accuracy.

**Solution**:
- Selected MobileNetV2 as the base model (designed for mobile devices)
- Used a feature extraction approach to limit trainable parameters
- Implemented a careful balance of model capacity and efficiency

### Challenge 3: Training Stability

**Issue**: Neural networks can be unstable during training, especially with limited data.

**Solution**:
- Used batch normalization to stabilize training
- Implemented early stopping to capture the best model
- Monitored multiple metrics to ensure balanced performance

## Model Architecture Comparison

Here's a side-by-side comparison of the two model architectures:

| Feature | Custom CNN | MobileNetV2 Model |
|---------|------------|-------------------|
| Base Architecture | From scratch | Pre-trained MobileNetV2 |
| Conv Layers | 2 standard convolutions | Depthwise separable convolutions |
| Parameters | ~303,000 | ~2.3M (mostly frozen) |
| Trainable Parameters | ~303,000 | ~400,000 |
| Regularization | Minimal | Dropout + Batch Normalization |
| Training Strategy | Fixed 20 epochs | Up to 50 epochs with early stopping |
| Model Size | ~1.2 MB | ~9 MB |
| Mobile Optimization | Basic | Specifically designed for mobile |

## Conclusion

I implemented two different deep learning approaches for boat classification:

1. A simple custom CNN model following the specified architecture, providing a baseline approach with moderate complexity.

2. A MobileNetV2-based transfer learning model, leveraging pre-trained weights while maintaining efficiency for mobile deployment.

Both models follow the specific architectures required in the project specifications. The MobileNetV2 model includes additional regularization techniques and training management strategies to optimize performance given the limited dataset size.

The architectural decisions were informed by both the project requirements and the insights gained from exploratory data analysis. The transfer learning approach was particularly important given the limited dataset size, allowing the model to leverage features learned from millions of images on ImageNet.