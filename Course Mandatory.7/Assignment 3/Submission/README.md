# Automating Port Operations

## Deep Learning - Course-End Project

### Project Overview

Marina Pier Inc. seeks to automate their operations at the San Francisco port by implementing a deep learning solution that can accurately identify different types of boats. This project aims to build a bias-free and error-free automatic reporting system that recognizes nine different types of boats, reducing human error in classification.

### Problem Statement

Marina Pier Inc. needs a reliable automatic system that can correctly classify the following boat types:

- Buoy
- Cruise_ship
- Ferry_boat
- Freight_boat
- Gondola
- Inflatable_boat
- Kayak
- Paper_boat
- Sailboat

As a deep learning engineer, I've built two CNN-based solutions:

1. A custom CNN network for boat classification
2. A lightweight transfer learning model using MobileNetV2 for mobile device deployment

### Dataset

The dataset contains 1,162 images across 9 boat categories. Each image is categorized into its respective class directory. The dataset exhibits some class imbalance, with certain boat types having more representation than others.

### Project Structure

```plaintext
Automating Port Operations/
└── Submission/
    ├── Automating_Port_Operations.ipynb      # Main notebook with complete code
    ├── README.md                             # Project documentation
    ├── docs/
    │   ├── 00_APPROACH.md                    # Methodology overview
    │   ├── 01_SETUP.md                       # Environment setup
    │   ├── 02_DATA_WRANGLING.md              # Data processing
    │   ├── 03_DATA_ANALYSIS.md               # Exploratory analysis findings
    │   ├── 04_MODELING.md                    # Model specifications
    │   └── 05_EVALUATION.md                  # Performance assessment
    ├── models/                               # Saved models and checkpoints
    │   ├── checkpoints/                      # Training checkpoints
    │   ├── cnn_boat_classifier.h5            # Custom CNN model
    │   ├── mobilenet_boat_classifier.h5      # MobileNetV2 model
    │   ├── cnn_history.pkl                   # Custom CNN training history
    │   └── mobilenet_history.pkl             # MobileNetV2 training history
    ├── utils/
    │   ├── data_preprocessing.py             # Data loading and preprocessing functions
    │   └── model_utils.py                    # Model building and evaluation functions
    ├── run.sh                                # Shell setup script
    └── requirements.txt                      # Project dependencies
```

### Key Findings

I implemented and compared two deep learning models for boat classification:

1. **Custom CNN Model**:
   - Simpler architecture with two convolutional layers
   - Moderate performance with approximately 85% accuracy on test data
   - Smaller model size suitable for basic applications

2. **MobileNetV2 Transfer Learning Model**:
   - Utilizes pre-trained weights from a model trained on millions of images
   - Superior performance with approximately 92% accuracy on test data
   - Optimized for mobile deployment while maintaining high accuracy
   - Includes early stopping to prevent overfitting

The MobileNetV2 model outperformed the custom CNN model in all evaluation metrics, demonstrating the power of transfer learning even with a relatively small dataset. This makes it the recommended solution for Marina Pier's automatic boat classification system.

### Implementation Steps

1. **Data Preparation**:
   - Split the dataset into training and testing sets
   - Applied data normalization (scaling pixel values to 0-1)
   - Loaded data in batches for efficient training

2. **Model Building**:
   - Created a custom CNN from scratch following the specified architecture
   - Implemented a transfer learning approach using MobileNetV2
   - Compiled models with appropriate loss functions and metrics

3. **Model Training**:
   - Trained the custom CNN for 20 epochs
   - Trained the MobileNetV2 model with early stopping monitoring validation loss
   - Plotted training metrics to analyze learning progression

4. **Evaluation and Comparison**:
   - Evaluated both models on test data
   - Created confusion matrices to analyze classification patterns
   - Generated detailed classification reports
   - Compared performance metrics between the two approaches

### Technologies Used

- Python 3.8+
- TensorFlow 2.10 and Keras
- MobileNetV2 (pre-trained on ImageNet)
- NumPy, Pandas, Matplotlib, and Seaborn for data processing and visualization
- Scikit-learn for model evaluation metrics

### Conclusion

The project demonstrates the effectiveness of transfer learning in scenarios with limited training data, where leveraging pre-trained models can significantly enhance performance compared to building models from scratch. For Marina Pier Inc.'s port operations, the MobileNetV2-based model offers the best balance of accuracy and efficiency, making it suitable for deployment on mobile devices used by port personnel.

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
   - MacOS/Linux: `export PORT_OPERATIONS_DATASET=path/to/boat_dataset_directory`
5. Run Jupyter: `jupyter notebook Automating_Port_Operations.ipynb`

### Troubleshooting

If you encounter any issues:

1. **Missing Dataset**:  
   - The script will search for the dataset in common locations
   - You can manually specify the dataset location with `export PORT_OPERATIONS_DATASET=/path/to/dataset`

2. **Dependency Issues**:
   - If TensorFlow installation fails, check the [official TensorFlow installation guide](https://www.tensorflow.org/install)
   - For other package issues, try installing them individually: `pip install <package-name>`

3. **Jupyter Server Issues**:
   - If Jupyter fails to start, try running `jupyter notebook` directly
   - Check Jupyter's installation with `jupyter --version`

4. **Image Loading Issues**:
   - If images don't load properly, ensure they are valid JPEG/PNG files
   - Try running the script with debug output: `DEBUG=1 ./run.sh`

The automatic boat classification system built using MobileNetV2 provides high accuracy while maintaining the efficiency needed for mobile deployment. This solution will help Marina Pier Inc. automate their port operations, reduce human error in boat classification, and implement a bias-free system for monitoring boat traffic at the San Francisco port.

The project demonstrates the effectiveness of transfer learning in scenarios with limited training data, where leveraging pre-trained models can significantly enhance performance compared to building models from scratch.
