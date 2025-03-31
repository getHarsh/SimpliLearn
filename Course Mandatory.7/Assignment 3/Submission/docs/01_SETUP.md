# Environment Setup

This document outlines the setup process for the Automating Port Operations project environment.

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
cd automating-port-operations
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
- **scikit-learn** for model evaluation metrics
- **Pillow** for image processing

## Step 4: Dataset Preparation

### Download and Extract the Dataset

1. Download the boat classification dataset from the provided source (boat_type_classification_dataset.zip)
2. Extract the dataset to the project directory:

```bash
# Navigate to the project directory
cd automating-port-operations

# Extract the dataset
unzip boat_type_classification_dataset.zip
```

### Verify Dataset Structure

The dataset should have the following structure:

```
boat_type_classification_dataset/
├── buoy/
├── cruise_ship/
├── ferry_boat/
├── freight_boat/
├── gondola/
├── inflatable_boat/
├── kayak/
├── paper_boat/
└── sailboat/
```

Each subdirectory should contain the respective boat type images.

## Step 5: Set Up Jupyter Notebook

Launch Jupyter Notebook to run the analysis:

```bash
jupyter notebook
```

This will open a browser window. Navigate to and open the `Automating_Port_Operations.ipynb` file.

## Step 6: GPU Configuration (Optional but Recommended)

Training deep learning models, especially the MobileNetV2 model, will be significantly faster with GPU acceleration. If you have a compatible NVIDIA GPU, follow these steps:

1. Install CUDA and cuDNN compatible with your TensorFlow version
2. Install the GPU version of TensorFlow:

```bash
pip install tensorflow-gpu==2.10.0
```

3. Verify GPU is recognized by TensorFlow:

```python
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
```

## Step 7: Verify Setup

To verify that everything is set up correctly, run the first few cells of the notebook. If there are no errors, the environment is configured properly.

## Troubleshooting Common Issues

### TensorFlow Installation Problems

If you encounter issues with TensorFlow installation:

```bash
# Try installing a specific version compatible with your system
pip install tensorflow==2.10.0
```

For GPU support, follow the official TensorFlow GPU setup guide.

### Image Loading Issues

If you encounter problems loading images:

1. Check that the dataset path is correct in the notebook
2. Verify that Pillow is properly installed: `pip install Pillow`
3. Ensure the dataset has the expected directory structure

### Memory Errors

If you encounter memory errors during model training:

1. Reduce the batch size (default is 32)
2. Reduce image dimensions (though this may affect model performance)
3. Use a machine with more RAM or GPU memory

## Additional Setup Notes

### Environment Variables (Optional)

You may want to set these environment variables for TensorFlow:

```bash
# For better performance
export TF_ENABLE_ONEDNN_OPTS=1

# To hide TensorFlow warnings
export TF_CPP_MIN_LOG_LEVEL=2
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

## Next Steps

After setting up the environment, I proceeded to data exploration and preprocessing as described in the `02_DATA_WRANGLING.md` document. The notebook is structured to follow the complete workflow from data loading to model evaluation.