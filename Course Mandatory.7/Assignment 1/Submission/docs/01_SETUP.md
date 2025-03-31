
# Environment Setup and Configuration

This document outlines the detailed setup instructions for the Lending Club Loan Default Prediction project.

## Environment Configuration

### Virtual Environment Setup

1. Create a dedicated Python virtual environment:

```bash
# Using venv
python -m venv lending_club_env

# Activate the environment
# On Windows
lending_club_env\Scripts\activate
# On macOS/Linux
source lending_club_env/bin/activate
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies

All required libraries and versions are specified in the `requirements.txt` file:

```
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
seaborn==0.12.2
scikit-learn==1.3.0
tensorflow==2.13.0
imbalanced-learn==0.11.0
jupyter==1.0.0
notebook==6.5.5
```

## Data Access and Configuration

### Dataset Retrieval

1. The Lending Club dataset should be placed in the project root directory as `loan_data.csv`.

2. Expected dataset columns:
   - credit.policy
   - purpose (categorical)
   - int.rate
   - installment
   - log.annual.inc
   - dti
   - fico
   - days.with.cr.line
   - revol.bal
   - revol.util
   - inq.last.6mths
   - delinq.2yrs
   - pub.rec
   - not.fully.paid (target variable)

### Directory Structure

Ensure the following directory structure is created:

```
Assignment 1/
└── Submission/
    ├── Lending_Club_Loan_Analysis.ipynb
    ├── loan_data.csv
    ├── README.md
    ├── docs/
    │   ├── 00_APPROACH.md
    │   ├── 01_SETUP.md
    │   ├── 02_DATA_WRANGLING.md
    │   ├── 03_DATA_ANALYSIS.md
    │   ├── 04_MODELING.md
    │   └── 05_EVALUATION.md
    ├── models/
    │   ├── checkpoints/
    │   ├── final_model.h5
    │   ├── model_history.pkl
    │   └── preprocessor.pkl
    ├── utils/
    │   ├── data_preprocessing.py
    │   └── model_utils.py
    └── requirements.txt
```

The notebook will automatically create necessary directories if they don't exist.

## Configuration Parameters

### Model Hyperparameters

The deep learning model uses the following parameters:

- Input layer: Matches preprocessed feature dimensions
- Hidden layers: 64, 32, and 16 neurons with ReLU activation
- Output layer: 1 neuron with sigmoid activation
- Batch normalization after each hidden layer
- Dropout rates: 0.3 (first layer), 0.2 (second layer)
- Optimizer: Adam with default learning rate (0.001)
- Loss function: Binary cross-entropy
- Batch size: 32
- Maximum epochs: 50 (with early stopping)

### Training Parameters

- Random seed: 42 (for reproducibility)
- Train-test split: 80-20
- Validation split: 20% of training data
- Early stopping patience: 10 epochs
- Model checkpoint: Save best model based on validation AUC

## Verification Steps

1. Confirm environment setup with a version check:

```python
import tensorflow as tf
import pandas as pd
import numpy as np
import sklearn

print(f"TensorFlow version: {tf.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"Scikit-learn version: {sklearn.__version__}")
```

2. Verify GPU availability (if applicable):

```python
print("GPU Available: ", tf.config.list_physical_devices('GPU'))
```

3. Test data loading:

```python
import pandas as pd
df = pd.read_csv('loan_data.csv')
print(f"Dataset loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns")
```

## Troubleshooting

- **TensorFlow installation issues**: If facing errors, try installing with specific version constraints: `pip install tensorflow==2.13.0`

- **Memory limitations**: If encountering memory issues during model training, reduce batch size or simplify model architecture

- **SMOTE errors**: If SMOTE implementation fails on high-dimensional data, consider reducing features through feature selection before applying SMOTE
