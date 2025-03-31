# Lending Club Loan Default Prediction

## Project Overview

This project implements a deep learning model to predict whether a loan will default based on historical Lending Club data from 2007 to 2015. Using a neural network architecture built with TensorFlow and Keras, the model analyzes borrower characteristics, loan terms, and credit metrics to assess default risk.

## Business Context

For lending institutions like Lending Club, accurately predicting loan defaults is crucial for:

- Effective risk management
- Appropriate interest rate determination
- Portfolio optimization
- Reduced financial losses

This project addresses the challenge of identifying high-risk loans in a dataset with class imbalance (fewer defaults than fully paid loans).

## Repository Structure

```plaintext
Assignment 1/
└── Submission/
    ├── Lending_Club_Loan_Data_Analysis.ipynb   # Main notebook with complete code
    ├── README.md                          # Project documentation
    ├── docs/                              # Detailed documentation
    │   ├── 00_APPROACH.md                 # Methodology overview
    │   ├── 01_SETUP.md                    # Environment setup
    │   ├── 02_DATA_WRANGLING.md           # Data cleaning process
    │   ├── 03_DATA_ANALYSIS.md            # Exploratory analysis findings
    │   ├── 04_MODELING.md                 # Model specifications
    │   └── 05_EVALUATION.md               # Performance assessment
    ├── models/                            # Model artifacts
    │   ├── checkpoints/                   # Training checkpoints
    │   ├── final_model.h5                 # Saved trained model
    │   ├── model_history.pkl              # Training metrics history
    │   └── preprocessor.pkl               # Saved preprocessing pipeline
    ├── utils/                             # Utility scripts
    │   ├── data_preprocessing.py          # Data preparation functions
    │   └── model_utils.py                 # Model helper functions
    ├── run.sh                             # Shell setup script
    └── requirements.txt                   # Project dependencies
```

## Getting Started

### Quick Start

Run the shell script to quickly set up and launch the project:

This script will:

- Set up a Python virtual environment
- Install all required dependencies
- Locate the dataset automatically
- Launch Jupyter notebook with the project

```bash
chmod +x run.sh  # Make the script executable (first time only)
./run.sh
```

**Note about dataset loading**: The script can access the dataset from any location. If running the notebook manually, you may need to update the dataset path in the notebook.

### Advanced Options

The script offers additional options for advanced users:

```bash
./run.sh --help
```

Options include specifying a custom dataset location, port number, and more.

## Setup and Execution

### Requirements

- Python 3.8+
- TensorFlow 2.13.0
- Pandas 2.0.3
- Scikit-learn 1.3.0
- Imbalanced-learn 0.11.0
- Additional dependencies in requirements.txt

### Installation

1. Clone the repository

2. Run this setup script:

   ```bash
   brew install python@3.10
   chmod +x run.sh
   ./run.sh
   ```

### Dataset

The scripts automatically locate the `loan_data.csv` file. The dataset includes the following features:

- **credit.policy**: Meeting credit underwriting criteria (1=yes, 0=no)
- **purpose**: Loan purpose (credit card, debt consolidation, etc.)
- **int.rate**: Interest rate as a proportion
- **installment**: Monthly payment amount
- **log.annual.inc**: Log of borrower's annual income
- **dti**: Debt-to-income ratio
- **fico**: FICO credit score
- **days.with.cr.line**: Days with credit line
- **revol.bal**: Revolving balance
- **revol.util**: Revolving utilization rate
- **inq.last.6mths**: Inquiries in last 6 months
- **delinq.2yrs**: Delinquencies in past 2 years
- **pub.rec**: Public derogatory records
- **not.fully.paid**: Target variable (1=default, 0=fully paid)

## Model Details

- **Architecture**: Multi-layer neural network with decreasing layer widths (64→32→16→1)
- **Regularization**: BatchNormalization and Dropout layers to prevent overfitting
- **Class Imbalance Handling**: SMOTE oversampling technique
- **Evaluation Metrics**: AUC, Precision, Recall, and F1 Score
- **Feature Importance**: Analysis of key predictors of loan default

## Key Results

The model achieves:

- **AUC**: ~0.83
- **Accuracy**: ~80%
- **Precision** (Default class): ~48%
- **Recall** (Default class): ~38%

Interest rates, FICO scores, and certain loan purposes (especially small business loans) were identified as the strongest predictors of default risk.

## Future Improvements

- Incorporate additional features like employment history and macroeconomic indicators
- Explore ensemble methods combining deep learning with other algorithms
- Implement custom loss functions more heavily penalizing false negatives
- Develop an explainability layer for individual prediction interpretation