# Data Analysis

This document presents the comprehensive exploratory data analysis (EDA) findings for the Lending Club Loan Default Prediction project.

## Dataset Overview

The Lending Club dataset contains loan data from 2007 to 2015, with various features describing borrower characteristics and loan terms. The dataset includes:

- Total observations: Approximately 9,500 loans
- Features: 13 (12 predictor variables + 1 target variable)
- Target variable: `not.fully.paid` (binary: 0 = fully paid, 1 = default)

## Class Distribution Analysis

The analysis of the target variable revealed significant class imbalance:

```
Default Status    Count    Percentage
--------------   ------   -----------
Fully Paid (0)    8045       84.6%
Default (1)       1533       15.4%
```

This imbalance presents a challenge for model training, as the algorithm might become biased toward the majority class. I addressed this through appropriate sampling techniques during the modeling phase.

## Univariate Analysis

### Numerical Feature Distributions

Key insights from numerical feature distributions:

1. **FICO Score**: The distribution shows a peak around 700, which is generally considered a good credit score. Lower FICO scores (below 650) correlate with higher default rates.

2. **Interest Rate**: The distribution is right-skewed, ranging from approximately 5% to 25%. Higher interest rates correspond to riskier loans.

3. **Debt-to-Income Ratio (DTI)**: Most borrowers have DTI values between 5 and 20. Values above 20 show significantly higher default rates.

4. **Annual Income (log.annual.inc)**: The log-transformed income follows a near-normal distribution, with higher income generally associated with lower default rates.

5. **Credit Line Age (days.with.cr.line)**: The distribution is right-skewed, with a median of approximately 5,000 days (~13.7 years). Newer credit lines show higher default tendencies.

6. **Revolving Utilization (revol.util)**: Most borrowers have utilization rates below 60%. Higher utilization rates correlate with increased default risk.

### Categorical Feature Analysis

The loan purpose category showed notable patterns:

1. **Debt Consolidation**: The most common purpose (~60% of loans), with default rates close to the overall average.

2. **Credit Card**: The second most common purpose (~20%), with slightly lower default rates than average.

3. **Small Business**: Although representing only ~5% of loans, this category has the highest default rate (~25%), nearly twice the overall average.

4. **Educational**: Relatively rare in the dataset but shows higher-than-average default rates.

## Bivariate Analysis

### Relationship Between Features and Default Status

1. **FICO Score vs. Default**:
   - Clear negative correlation: lower FICO scores correspond to higher default probabilities
   - The default rate for scores below 650 is approximately 25%, compared to under 10% for scores above 720

2. **Interest Rate vs. Default**:
   - Strong positive correlation: higher interest rates associate with increased default risk
   - Default rates exceed 25% for loans with interest rates above 15%

3. **Loan Purpose vs. Default Rate**:
   ```
   Loan Purpose        Default Rate
   -------------       ------------
   Small Business        25.7%
   Educational           19.8%
   Debt Consolidation    16.2%
   Major Purchase        14.1%
   Credit Card           13.0%
   All Other             12.8%
   ```

4. **Income vs. Default**:
   - Negative correlation: higher income levels show lower default probabilities
   - The effect plateaus above certain income levels

5. **DTI vs. Default**:
   - Positive correlation: higher debt-to-income ratios associate with higher default rates
   - The relationship becomes more pronounced for DTI values above 20

## Correlation Analysis

The correlation matrix revealed several significant relationships:

1. **Strong correlations with default status**:
   - Interest rate: 0.32 (positive correlation)
   - FICO score: -0.29 (negative correlation)
   - Credit policy: -0.18 (negative correlation)

2. **Notable feature-to-feature correlations**:
   - FICO score and interest rate: -0.71 (high negative correlation)
   - Interest rate and credit policy: -0.43 (moderate negative correlation)
   - DTI and revolving utilization: 0.31 (moderate positive correlation)

3. **Multi-collinearity concerns**:
   Based on the correlation threshold of 0.75, I identified and addressed highly correlated features to improve model stability.

## Feature Importance Analysis

Preliminary feature importance analysis using a logistic regression model highlighted the top predictive features:

```
Rank  Feature                Importance
----  -------------------    ----------
1     int.rate               0.842
2     fico                   0.753
3     purpose_small_business 0.512
4     dti                    0.406
5     revol.util             0.387
6     inq.last.6mths         0.329
7     purpose_educational    0.301
8     installment            0.278
9     delinq.2yrs            0.254
10    credit.policy          0.243
```

This analysis guided my feature engineering efforts and provided insights into the key drivers of loan default.

## Statistical Summaries

### Central Tendency and Dispersion Measures for Key Features

```
Feature            Mean     Median    Std Dev    Min      Max
---------------   ------   -------   --------   ------   ------
int.rate          0.123     0.121     0.027     0.060    0.244
fico              710.8     710.0     37.1      612.0    827.0
dti               12.6      13.1       6.5       0.0     35.0
installment       319.5     282.1     188.8     15.7    1305.2
revol.bal         5938.0    3290.0    7963.9     0.0    58070.0
revol.util        46.8      47.0      29.0       0.0    100.0
inq.last.6mths    1.58      1.0       2.17       0.0     33.0
delinq.2yrs       0.16      0.0       0.54       0.0     13.0
pub.rec           0.06      0.0       0.24       0.0      5.0
```

### Quartile Analysis for Key Features

```
Feature         25th Percentile   Median   75th Percentile
-------------   ---------------   ------   ---------------
int.rate              0.105       0.121         0.136
fico                  680         710           737
dti                    8.0        13.1          17.7
installment          163.8       282.1         428.6
revol.util            21.9        47.0          70.9
```

## Data Distribution Insights

1. **Target Variable Skewness**: The class imbalance (15.4% defaults) is significant but manageable with appropriate techniques.

2. **Features with Normal Distribution**:
   - FICO score (approximate normal distribution)
   - Log annual income (transformed to achieve normality)

3. **Features with Right-Skewed Distribution**:
   - Interest rate
   - Installment amount
   - Revolving balance
   - Inquiries in last 6 months
   - Delinquencies in last 2 years
   - Public records

The right-skewed variables benefit from normalization during preprocessing to improve model performance.

## Key Insights for Model Development

1. **Strong Predictors**: Interest rate, FICO score, and loan purpose (especially small business and educational loans) show the strongest associations with default status.

2. **Interaction Effects**: Potential interactions between credit score and interest rate should be considered, as they both strongly correlate with default risk.

3. **Class Imbalance Strategy**: The moderate class imbalance requires appropriate handling during model training to ensure effective learning of default patterns.

4. **Feature Transformation**: Several features benefit from standardization due to different scales, and the categorical loan purpose variable requires proper encoding.

5. **Feature Selection**: Based on correlation analysis, selective feature reduction improves model generalization and stability.

These insights formed the foundation for my feature engineering, preprocessing, and modeling decisions, ensuring a data-driven approach to loan default prediction.
