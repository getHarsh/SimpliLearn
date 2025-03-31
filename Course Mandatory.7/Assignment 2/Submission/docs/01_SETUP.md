# Environment Setup

This document outlines the setup process for the House Loan Data Analysis project environment.

## Prerequisites

Before beginning, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Jupyter Notebook or JupyterLab

## Step 1: Clone or Download the Project

First, obtain the project files either by cloning the repository or downloading the project folder.

```bash
# If using git
git clone [repository-url]
cd house-loan-data-analysis
```

## Step 2: Set Up a Virtual Environment (Recommended)

I recommend creating a virtual environment to avoid conflicts with other Python projects.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

All required libraries are listed in the `requirements.txt` file. Install them using pip:

```bash
pip install -r requirements.txt
```

The key dependencies include:
- **numpy** and **pandas** for data manipulation
- **matplotlib** and **seaborn** for data visualization
- **tensorflow** and **keras** for building deep learning models
- **scikit-learn** for data preprocessing and evaluation metrics
- **imbalanced-learn** for handling class imbalance (SMOTE)

## Step 4: Set Up Jupyter Notebook

Launch Jupyter Notebook to run the analysis:

```bash
jupyter notebook
```

This will open a browser window. Navigate to and open the `House_Loan_Data_Analysis.ipynb` file.

## Step 5: Data Preparation

Ensure the loan data file is placed in the project directory. The notebook assumes the dataset is named `loan_data.csv` and is located in the same directory as the notebook.

## Step 6: Verify Setup

To verify that everything is set up correctly, run the first few cells of the notebook. If there are no errors, the environment is configured properly.

## Troubleshooting Common Issues

### TensorFlow Installation Problems

If you encounter issues with TensorFlow installation:

```bash
# Try installing a specific version compatible with your system
pip install tensorflow==2.10.0
```

For GPU support, follow the official TensorFlow GPU setup guide.

### Import Errors

If you encounter import errors for custom modules:

```python
# Add this to your notebook if the utils modules aren't found
import sys
sys.path.append('./utils')
```

### Memory Issues

If you encounter memory issues when running the notebook:

1. Reduce batch size in the model training section
2. Process the data in chunks if working with a very large dataset
3. Consider using a machine with more RAM or using Google Colab

## Additional Setup Notes

### GPU Acceleration

For faster model training, you can use GPU acceleration if you have a compatible NVIDIA GPU. Additional setup is required for this:

1. Install CUDA and cuDNN compatible with your TensorFlow version
2. Install the GPU version of TensorFlow:
   ```bash
   pip install tensorflow-gpu==2.10.0
   ```

### Jupyter Extensions (Optional)

I found these Jupyter extensions helpful for this project:

```bash
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

Enable helpful extensions like:
- Table of Contents
- Variable Inspector
- ExecuteTime (to track cell execution time)

## Version Control

If you're using version control:

1. Initialize a git repository if not already done:
   ```bash
   git init
   ```

2. Create a `.gitignore` file to exclude unnecessary files:
   ```
   venv/
   __pycache__/
   .ipynb_checkpoints/
   *.h5
   *.csv
   ```

3. Make initial commit:
   ```bash
   git add .
   git commit -m "Initial project setup"
   ```

## Next Steps

After setting up the environment, proceed to the data wrangling phase described in `02_DATA_WRANGLING.md`.
