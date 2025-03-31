# House Loan Data Analysis

## Deep Learning with Keras and TensorFlow - Course-End Project

### Project Overview

In this project, I built a deep learning model to predict the likelihood of loan defaults based on historical data. For a safe and secure lending experience, it's essential to analyze past data and identify patterns that can indicate potential defaults. The dataset used in this project is highly imbalanced and contains numerous features, making it a challenging but realistic problem.

### Problem Statement

For a safe and secure lending experience, it's important to analyze past data. In this project, I built a deep learning model to predict the chance of default for future loans using historical data. The dataset is highly imbalanced and includes many features that make this problem more challenging.

### Objective

Create a model that predicts whether or not an applicant will be able to repay a loan using historical data.

### Analysis Performed

I performed comprehensive data preprocessing and built a deep learning prediction model with the following key steps:

1. **Data Loading and Exploration**: Loaded the dataset and performed initial exploration to understand its structure and characteristics.
2. **Null Value Handling**: Identified and appropriately handled missing values in the dataset.
3. **Class Imbalance Analysis**: Analyzed the target variable distribution and addressed the imbalance using SMOTE.
4. **Data Preprocessing**:
   - Encoded categorical features
   - Handled outliers in numerical features
   - Removed highly correlated features
   - Scaled numerical features
5. **Model Building**: Constructed a deep neural network using TensorFlow and Keras.
6. **Model Evaluation**: Evaluated the model using sensitivity metrics and ROC AUC.

### Key Findings

- The dataset showed significant class imbalance, with a small percentage of defaulted loans.
- After applying SMOTE, the model was able to better learn patterns from both classes.
- The final model achieved a sensitivity of 0.82 and an AUC of 0.89, indicating good performance on identifying potential defaults.
- The most important features for predicting loan defaults were loan amount, applicant income, credit history, and loan term duration.

### Project Structure

```plaintext
House Loan Data Analysis/
└── Submission/
    ├── House_Loan_Data_Analysis.ipynb        # Main notebook with complete code
    ├── README.md                             # Project documentation
    ├── docs/
    │   ├── 00_APPROACH.md                    # Methodology overview
    │   ├── 01_SETUP.md                       # Environment setup
    │   ├── 02_DATA_WRANGLING.md              # Data cleaning process
    │   ├── 03_DATA_ANALYSIS.md               # Exploratory analysis findings
    │   ├── 04_MODELING.md                    # Model specifications
    │   └── 05_EVALUATION.md                  # Performance assessment
    ├── models/                               # Model artifacts
    │   ├── checkpoints/                      # Training checkpoints
    │   └── final_model.h5                    # Saved trained model
    ├── utils/
    │   ├── data_preprocessing.py             # Data preparation functions
    │   └── model_utils.py                    # Model helper functions
    ├── run.sh                                # Shell setup script
    └── requirements.txt                      # Project dependencies
```

### Getting Started

#### Quick Start (Recommended)

The easiest way to run this project is using our automated setup script:

```bash
chmod +x run.sh  # Make the script executable (first time only)
./run.sh
```

This script will:

1. Create a virtual environment
2. Install all required dependencies
3. Find the dataset automatically
4. Start Jupyter notebook server
5. Open the notebook in your browser

#### Manual Setup

If you prefer to set up manually:

1. Create a virtual environment: `python -m venv .venv`
2. Activate the environment:
   - Windows: `.venv\Scripts\activate`
   - MacOS/Linux: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set the dataset path:  
   - MacOS/Linux: `export HOUSE_LOAN_DATASET=path/to/loan_data.csv`
5. Run Jupyter: `jupyter notebook House_Loan_Data_Analysis.ipynb`

### Troubleshooting

If you encounter any issues:

1. **Missing Dataset**:  
   - The script will search for the dataset in common locations
   - You can manually specify the dataset location with `./run.sh --dataset-path /path/to/loan_data.csv`

2. **Dependency Issues**:
   - If TensorFlow installation fails, check the [official TensorFlow installation guide](https://www.tensorflow.org/install)
   - For other package issues, try installing them individually: `pip install <package-name>`

3. **Jupyter Server Issues**:
   - If the notebook server doesn't start, try specifying a different port: `./run.sh --port 9999`
   - If the browser doesn't open automatically, use the URL displayed in the terminal

### Technologies Used

- Python 3.10
- TensorFlow 2.13.0
- Keras
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Imbalanced-learn (SMOTE)

### Future Improvements

- Experiment with more complex neural network architectures
- Implement advanced feature engineering techniques
- Test different techniques for handling imbalanced data
- Deploy the model as a web service for real-time predictions

### Conclusion

This project demonstrates the effectiveness of deep learning models in predicting loan defaults. The insights gained from this analysis can help financial institutions make more informed lending decisions, reducing risk and improving overall portfolio performance.
