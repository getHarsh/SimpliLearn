# Marketing Campaign Analysis Project

## Project Overview
This analysis explores marketing mix concepts through the lens of the 4 P's:
- **People**: Demographics (birth year, education, income)
- **Product**: Expenditures (wine, fruits, gold)
- **Place**: Sales channels (website, store, catalog)
- **Promotion**: Campaign outcomes and effectiveness

## Project Objective
Conduct exploratory data analysis and hypothesis testing to understand factors influencing customer acquisition through marketing campaigns.

## Analysis Framework
The study follows a structured analytical approach, with each document building on insights from the previous ones:

1. **Analysis Approach** (`00_APPROACH.md` → `01_SETUP.md`)
   - Marketing mix framework understanding
   - Analysis strategy development
   - Expected outcomes definition
   - Links to initial data setup

2. **Data Setup** (`01_SETUP.md` → `02_DATA_WRANGLING.md`)
   - Date and income validation
   - Data quality assessment
   - Initial patterns identification
   - Preparation for data wrangling

3. **Data Processing** (`02_DATA_WRANGLING.md` → `03_DATA_ANALYSIS.md`)
   - Missing income imputation strategy
   - Feature engineering (children, age, spending)
   - Distribution analysis and outlier treatment
   - Variable encoding for statistical analysis

4. **Statistical Study** (`03_DATA_ANALYSIS.md` → `04_VISUALIZATION.md`)
   - Correlation analysis with visualizations
   - Hypothesis testing:
     * Age vs shopping channel preferences
     * Family size impact on online shopping
     * Channel cannibalization effects
     * Regional performance variations

5. **Visualization** (`04_VISUALIZATION.md` → `05_FINDINGS.md`)
   - Product performance visualization
   - Age-campaign correlation plots
   - Regional campaign success maps
   - Family size spending patterns
   - Education-complaint relationships

6. **Strategic Insights** (`05_FINDINGS.md` → Implementation)
   - Data-driven key findings
   - Marketing recommendations
   - Implementation roadmap
   - Success metrics definition

## Main Notebook
The `Marketing_Campaign_Analysis.ipynb` notebook contains the complete analysis workflow with detailed code implementations and study notes.

## Setup Instructions

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

4. Open `Marketing_Campaign_Analysis.ipynb` to start the analysis

## Project Structure
```
project/
├── docs/
│   ├── 00_APPROACH.md          # Marketing mix framework and strategy
│   ├── 01_SETUP.md             # Initial data validation and setup
│   ├── 02_DATA_WRANGLING.md    # Data cleaning and feature engineering
│   ├── 03_DATA_ANALYSIS.md     # Statistical analysis and testing
│   ├── 04_VISUALIZATION.md     # Data visualization and patterns
│   └── 05_FINDINGS.md          # Insights and recommendations
├── Marketing_Campaign_Analysis.ipynb  # Main analysis notebook
├── requirements.txt            # Project dependencies
└── README.md                  # Project documentation
```

## Study Notes
- Each markdown file contains personal study notes and learning insights
- Code sections include detailed implementation examples
- Visualizations are designed for clear business communication
- Findings focus on actionable recommendations

## Next Steps
1. Start with `00_APPROACH.md` to understand the marketing framework
2. Follow the documentation in sequential order
3. Execute the notebook cells as you progress
4. Review findings and implementation plan
5. Begin implementing recommendations
