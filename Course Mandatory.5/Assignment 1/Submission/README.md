# Employee Turnover Analytics

## Project Overview
Analysis of employee turnover patterns at Portobello Tech using machine learning techniques to predict turnover risk and develop retention strategies.

## Project Structure
```
/
├── docs/
│   ├── 00_APPROACH.md       # Analysis methodology
│   ├── 01_SETUP.md          # Environment setup
│   ├── 02_DATA_WRANGLING.md # Data cleaning
│   ├── 03_DATA_ANALYSIS.md  # EDA
│   ├── 04_MODELING.md       # ML modeling
│   └── 05_FINDINGS.md       # Results
├── notebooks/
│   └── Employee_Turnover_Analysis.ipynb
└── requirements.txt
```

## Key Objectives
1. Data Quality Assessment
   - Check for missing values
   - Validate data integrity

2. Turnover Factor Analysis
   - Correlation analysis
   - Distribution analysis of key metrics
   - Employee project count analysis

3. Employee Clustering
   - K-means clustering (3 clusters)
   - Focus on satisfaction and evaluation
   - Cluster interpretation

4. Model Development
   - SMOTE for class imbalance
   - Feature preprocessing
   - 5-fold cross-validation
   - Multiple model comparison:
     * Logistic Regression
     * Random Forest
     * Gradient Boosting

5. Model Evaluation
   - ROC/AUC analysis
   - Confusion matrix analysis
   - Metric selection justification

6. Retention Strategy
   - Risk zone categorization
   - Zone-specific recommendations
   - Implementation guidelines

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
