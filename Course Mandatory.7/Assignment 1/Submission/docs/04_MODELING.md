# Modeling Methodology

This document outlines the detailed modeling approach for the Lending Club Loan Default Prediction project, including architectural decisions, hyperparameter selection, and training strategies.

## Model Architecture Specification

I implemented a multi-layer neural network using TensorFlow and Keras with the following architecture:

```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(input_dim,)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
```

### Layer-by-Layer Breakdown

1. **Input Layer**:
   - Input shape dynamically determined based on the number of preprocessed features
   - Accommodates both numerical features and one-hot encoded categorical variables

2. **First Hidden Layer**:
   - 64 neurons with ReLU activation function
   - BatchNormalization for training stability
   - Dropout (0.3) for regularization to prevent overfitting

3. **Second Hidden Layer**:
   - 32 neurons with ReLU activation
   - BatchNormalization for improved convergence
   - Dropout (0.2) with reduced rate as deeper layers need less regularization

4. **Third Hidden Layer**:
   - 16 neurons with ReLU activation
   - No dropout to preserve information flow near the output

5. **Output Layer**:
   - Single neuron with sigmoid activation
   - Produces probability of loan default (0 to 1)

### Architectural Decisions Rationale

1. **Decreasing Layer Width**: The progressive reduction in neurons (64→32→16→1) follows the bottleneck principle, which helps the model learn hierarchical representations while reducing overfitting risk.

2. **ReLU Activation**: Chosen for hidden layers due to:
   - Computational efficiency
   - Mitigation of the vanishing gradient problem
   - Sparse activation properties that improve model generalization

3. **Batch Normalization**: Implemented after dense layers to:
   - Accelerate training by allowing higher learning rates
   - Reduce internal covariate shift
   - Act as a mild regularizer

4. **Dropout Implementation**: Decreasing dropout rates across layers (0.3→0.2→0) allow:
   - Stronger regularization in earlier layers with more parameters
   - Preservation of learned features in deeper layers

5. **Sigmoid Output**: Appropriate for binary classification, providing probability interpretation of default risk.

## Hyperparameter Selection

### Optimizer Configuration

I selected the Adam optimizer with the following configuration:

```python
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=[
        tf.keras.metrics.AUC(),
        tf.keras.metrics.Precision(),
        tf.keras.metrics.Recall()
    ]
)
```

**Rationale for Adam selection**:
- Adaptive learning rate capabilities
- Momentum-based approach that works well with noisy gradients
- Effective convergence properties for classification problems
- Good performance with default settings (learning_rate=0.001, beta_1=0.9, beta_2=0.999)

### Loss Function

Binary cross-entropy was chosen as the loss function because:
- It is specifically designed for binary classification problems
- It provides appropriate gradients for probability predictions
- It penalizes confident wrong predictions more heavily

### Evaluation Metrics

The model was evaluated using multiple metrics:

1. **Area Under the ROC Curve (AUC)**:
   - Primary metric due to robustness to class imbalance
   - Measures model's ability to rank positive examples higher than negative ones
   - Scale-invariant and threshold-invariant

2. **Precision**:
   - Measures proportion of correct positive predictions
   - Important for understanding false positive rate
   - Relevant when minimizing false defaults is important

3. **Recall**:
   - Measures proportion of actual positives correctly identified
   - Critical for capturing as many default cases as possible
   - Helps assess model's sensitivity to the minority class

### Training Configuration

Training parameters were selected based on empirical testing and domain knowledge:

```python
history = model.fit(
    X_train_balanced,
    y_train_balanced,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    callbacks=[checkpoint_callback, early_stopping],
    verbose=1
)
```

**Parameter rationale**:
- **Batch size (32)**: Provides a good balance between computational efficiency and gradient noise
- **Maximum epochs (50)**: Sufficient upper bound for convergence with early stopping
- **Validation split (0.2)**: Reserves 20% of training data for validation without touching test set
- **Early stopping patience (10)**: Prevents overfitting while allowing sufficient exploration

## Handling Class Imbalance

I implemented two complementary approaches to address class imbalance:

### 1. Synthetic Minority Over-sampling Technique (SMOTE)

```python
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_preprocessed, y_train)
```

**SMOTE strategy rationale**:
- Creates synthetic examples of the minority class
- Avoids simple duplication of minority samples
- Improves model's ability to learn decision boundaries for the default class
- Applied only to training data to maintain test set integrity

### 2. Class Weights (Alternative Approach)

```python
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}
```

**Class weighting rationale**:
- Penalizes misclassification of minority class samples more heavily
- Keeps all original data without synthetic generation
- Can be combined with SMOTE for enhanced performance

I primarily implemented SMOTE but included class weights as an alternative approach for performance comparison.

## Model Complexity Considerations

The model architecture balances complexity and performance:

1. **Parameter Count**:
   - First dense layer: input_dim × 64 + 64 (weights + biases)
   - Second dense layer: 64 × 32 + 32
   - Third dense layer: 32 × 16 + 16
   - Output layer: 16 × 1 + 1
   - Total parameters: Approximately 5,000-8,000 depending on input features

2. **Regularization Strength**:
   - Dropout rates (0.3, 0.2) were carefully tuned to provide sufficient regularization without losing critical information
   - BatchNormalization adds stability and mild regularization effect

3. **Early Stopping**:
   - Prevents overfitting by monitoring validation performance
   - Automatically selects optimal training duration

4. **Model Checkpointing**:
   - Saves the best model based on validation AUC
   - Ensures optimal model generalization

```python
checkpoint_path = "models/checkpoints/model-{epoch:02d}-{val_auc:.2f}.h5"
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    checkpoint_path, 
    monitor='val_auc', 
    save_best_only=True,
    save_weights_only=False,
    mode='max',
    verbose=1
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_auc',
    patience=10,
    restore_best_weights=True,
    mode='max'
)
```

## Training Methodology

The training process followed these steps:

1. **Data Preparation**:
   - Apply preprocessing pipeline to training data
   - Generate balanced dataset using SMOTE
   - Reserve validation subset for performance monitoring

2. **Model Initialization**:
   - Initialize weights with glorot_uniform (Xavier) initialization
   - Configure optimizer and loss function

3. **Training Loop**:
   - Process data in batches of 32 samples
   - Update weights using backpropagation
   - Monitor validation performance after each epoch
   - Save checkpoints of the best-performing model
   - Terminate training when validation performance plateaus

4. **Model Selection**:
   - Restore weights from the best checkpoint based on validation AUC
   - Evaluate final model on the test set

## Optimization Strategies

### Learning Rate Schedule

While I used the default Adam learning rate (0.001), I implemented early stopping to automatically determine the optimal training duration:

```python
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_auc',
    patience=10,
    restore_best_weights=True,
    mode='max'
)
```

This approach:
- Starts with a suitable learning rate for efficient initial training
- Stops training when diminishing returns are observed
- Restores weights from the best-performing epoch

### Batch Normalization

Batch normalization was applied after each hidden layer to:
- Normalize activations within each mini-batch
- Reduce internal covariate shift
- Allow faster and more stable training

### Gradient Clipping

While not explicitly implemented, Adam's adaptive learning rate properties help manage gradient scaling issues that might otherwise require clipping.

## Model Persistence Framework

I implemented a robust model persistence framework to ensure reproducibility:

```python
# Save the final model
model.save('models/final_model.h5')

# Save the training history
with open('models/model_history.pkl', 'wb') as file:
    pickle.dump(history.history, file)

# Save the preprocessor for consistent transformations
with open('models/preprocessor.pkl', 'wb') as file:
    pickle.dump(preprocessor, file)
```

This framework enables:
- Complete model restoration for inference
- Consistent preprocessing of new data
- Analysis of training dynamics through saved history
- Application of the same transformations to new data

The combination of these modeling decisions created a robust, balanced approach to loan default prediction, addressing the challenges of class imbalance while maintaining model generalization capabilities.
