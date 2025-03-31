# Creating Song Cohorts

## Project Overview
Analysis of Rolling Stones songs on Spotify to create meaningful cohorts for enhanced music recommendations using clustering techniques.

## Project Structure
```
/
├── docs/
│   ├── 00_APPROACH.md       # Analysis methodology
│   ├── 01_SETUP.md          # Environment setup
│   ├── 02_DATA_WRANGLING.md # Data cleaning
│   ├── 03_DATA_ANALYSIS.md  # EDA
│   ├── 04_MODELING.md       # Clustering
│   └── 05_FINDINGS.md       # Results
├── notebooks/
│   └── Song_Cohort_Analysis.ipynb
└── requirements.txt
```

## Key Objectives
1. Data Inspection and Cleaning
   - Identify duplicates
   - Handle missing values
   - Check for erroneous entries
   - Outlier detection

2. Data Refinement
   - Feature validation
   - Data type conversions
   - Temporal data processing

3. Exploratory Analysis
   - Album popularity analysis
   - Feature pattern identification
   - Popularity correlation study
   - Audio feature relationships

4. Feature Engineering
   - Temporal feature processing
   - Audio feature normalization
   - Derived metrics creation

5. Dimensionality Reduction
   - Feature importance analysis
   - Technique selection
   - Implementation and validation

6. Cluster Analysis
   - Optimal cluster determination
   - Algorithm selection
   - Cluster characterization
   - Recommendation framework

## Setup Instructions
1. Create virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # Unix/macOS
   # or
   .\env\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Follow documentation in `/docs` directory

4. Execute notebook for analysis
