# Model Development and Evaluation

## 1. Model Training Framework (Requirements 5.1-5.3)

### 1.1 Model Creation and Training
```python
def create_and_train_models(X_train: pd.DataFrame,
                           y_train: pd.Series) -> dict:
    """
    Create and train the three required models.
    Implementation of requirements 5.1, 5.2, and 5.3.
    
    Parameters:
        X_train (pd.DataFrame): Training feature matrix
        y_train (pd.Series): Training target variable
        
    Returns:
        dict: Dictionary of trained models
    """
    # Initialize models with consistent random state
    models = {
        'Logistic Regression': LogisticRegression(random_state=123),
        'Random Forest': RandomForestClassifier(random_state=123),
        'Gradient Boosting': GradientBoostingClassifier(random_state=123)
    }
    
    # Train and evaluate each model with 5-fold CV
    for name, model in models.items():
        # Perform 5-fold cross-validation
        cv_results = cross_validate(
            model,
            X_train, y_train,
            cv=5,  # Exactly 5 folds as per requirement
            scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
            return_train_score=True
        )
        
        # Fit the model on full training data
        model.fit(X_train, y_train)
        
        # Store results
        models[name] = {
            'model': model,
            'cv_results': cv_results
        }
        
        # Print cross-validation results
        print(f"\n{name} - 5-fold CV Results:")
        print(f"Accuracy: {cv_results['test_accuracy'].mean():.3f} (+/- {cv_results['test_accuracy'].std()*2:.3f})")
        print(f"Precision: {cv_results['test_precision'].mean():.3f} (+/- {cv_results['test_precision'].std()*2:.3f})")
        print(f"Recall: {cv_results['test_recall'].mean():.3f} (+/- {cv_results['test_recall'].std()*2:.3f})")
        print(f"F1 Score: {cv_results['test_f1'].mean():.3f} (+/- {cv_results['test_f1'].std()*2:.3f})")
        print(f"ROC AUC: {cv_results['test_roc_auc'].mean():.3f} (+/- {cv_results['test_roc_auc'].std()*2:.3f})")
    
    return models
```

## 2. Model Evaluation (Requirements 6.1-6.3)

### 2.1 ROC/AUC Analysis
```python
def evaluate_models_roc_auc(models: dict,
                           X_test: pd.DataFrame,
                           y_test: pd.Series) -> dict:
    """
    Evaluate models using ROC/AUC analysis.
    Implementation of requirement 6.1.
    
    Parameters:
        models (dict): Dictionary of trained models
        X_test (pd.DataFrame): Test feature matrix
        y_test (pd.Series): Test target variable
        
    Returns:
        dict: AUC scores for each model
    """
    plt.figure(figsize=(10, 8))
    auc_scores = {}
    
    for name, model_dict in models.items():
        model = model_dict['model']
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate ROC curve
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        auc_score = auc(fpr, tpr)
        auc_scores[name] = auc_score
        
        # Plot ROC curve
        plt.plot(fpr, tpr, label=f'{name} (AUC = {auc_score:.3f})')
    
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves Comparison')
    plt.legend()
    plt.show()
    
    return auc_scores

### 2.2 Confusion Matrix Analysis
```python
def analyze_confusion_matrices(models: dict,
                             X_test: pd.DataFrame,
                             y_test: pd.Series) -> None:
    """
    Generate and analyze confusion matrices.
    Implementation of requirement 6.2.
    
    Parameters:
        models (dict): Dictionary of trained models
        X_test (pd.DataFrame): Test feature matrix
        y_test (pd.Series): Test target variable
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for (name, model_dict), ax in zip(models.items(), axes):
        model = model_dict['model']
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        sns.heatmap(cm, annot=True, fmt='d', ax=ax)
        ax.set_title(f'{name}\nConfusion Matrix')
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
    
    plt.tight_layout()
    plt.show()
    
    # Print classification reports
    for name, model_dict in models.items():
        model = model_dict['model']
        y_pred = model.predict(X_test)
        print(f"\n{name} Classification Report:")
        print(classification_report(y_test, y_pred))
```

## 3. Risk Assessment and Retention Strategies (Requirement 7)

### 3.1 Employee Risk Categorization
```python
def categorize_risk_zones(model: object,
                          X_test: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize employees into risk zones based on turnover probability.
    Implementation of requirement 7.1 and 7.2.
    
    Parameters:
        model: Best performing model
        X_test (pd.DataFrame): Test feature matrix
        
    Returns:
        pd.DataFrame: Risk categorization results
    """
    # Get turnover probabilities
    probabilities = model.predict_proba(X_test)[:, 1]
    
    # Create risk categories
    def get_risk_zone(prob):
        if prob < 0.2:
            return 'Safe Zone (Green)'
        elif prob < 0.6:
            return 'Low-Risk Zone (Yellow)'
        elif prob < 0.9:
            return 'Medium-Risk Zone (Orange)'
        else:
            return 'High-Risk Zone (Red)'
    
    # Add predictions to test data
    results = X_test.copy()
    results['Turnover_Probability'] = probabilities
    results['Risk_Zone'] = results['Turnover_Probability'].apply(get_risk_zone)
    
    # Calculate zone statistics
    zone_stats = results['Risk_Zone'].value_counts()
    print("\nRisk Zone Distribution:")
    print(zone_stats)
    
    # Suggest retention strategies
    strategies = {
        'Safe Zone (Green)': [
            'Maintain current engagement levels',
            'Regular feedback and recognition',
            'Career development opportunities'
        ],
        'Low-Risk Zone (Yellow)': [
            'Increase engagement through team activities',
            'Schedule regular check-ins',
            'Review workload and project distribution'
        ],
        'Medium-Risk Zone (Orange)': [
            'Immediate manager intervention',
            'Compensation and benefits review',
            'Address work-life balance concerns',
            'Provide additional training and support'
        ],
        'High-Risk Zone (Red)': [
            'Urgent retention plan implementation',
            'One-on-one meetings with senior management',
            'Immediate address of key pain points',
            'Consider role change or department transfer',
            'Implement personalized retention bonus'
        ]
    }
    
    print("\nRetention Strategies by Risk Zone:")
    for zone, strats in strategies.items():
        print(f"\n{zone}:")
        for i, strategy in enumerate(strats, 1):
            print(f"{i}. {strategy}")
    
    return results
```

## 1. Model Training Framework

### 1.1 Base Model Setup
```python
def create_model_pipeline(model_type: str) -> Pipeline:
    """
    Create a model pipeline with preprocessing steps.
    
    Parameters:
        model_type (str): Type of model to create
        
    Returns:
        Pipeline: Scikit-learn pipeline
    """
    if model_type == 'logistic':
        model = LogisticRegression(random_state=RANDOM_SEED)
    elif model_type == 'random_forest':
        model = RandomForestClassifier(random_state=RANDOM_SEED)
    elif model_type == 'gradient_boosting':
        model = GradientBoostingClassifier(random_state=RANDOM_SEED)
    else:
        raise ValueError("Unsupported model type")
    
    return model
```

### 1.2 Cross-Validation Framework
```python
def perform_cross_validation(model: BaseEstimator,
                           X: pd.DataFrame,
                           y: pd.Series) -> dict:
    """
    Perform 5-fold cross-validation.
    
    Parameters:
        model: Scikit-learn model
        X (pd.DataFrame): Feature matrix
        y (pd.Series): Target variable
        
    Returns:
        dict: Cross-validation results
    """
    # Define scoring metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': 'precision',
        'recall': 'recall',
        'f1': 'f1',
        'roc_auc': 'roc_auc'
    }
    
    # Perform cross-validation
    cv_results = cross_validate(
        model, X, y,
        cv=5,
        scoring=scoring,
        return_train_score=True
    )
    
    return cv_results
```

## 2. Model Training and Evaluation

### 2.1 Train Models
```python
def train_evaluate_models(X_train: pd.DataFrame,
                         X_test: pd.DataFrame,
                         y_train: pd.Series,
                         y_test: pd.Series) -> dict:
    """
    Train and evaluate multiple models.
    
    Parameters:
        X_train, X_test: Feature matrices
        y_train, y_test: Target variables
        
    Returns:
        dict: Model evaluation results
    """
    models = {
        'logistic': create_model_pipeline('logistic'),
        'random_forest': create_model_pipeline('random_forest'),
        'gradient_boosting': create_model_pipeline('gradient_boosting')
    }
    
    results = {}
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Get predictions
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        # Store results
        results[name] = {
            'model': model,
            'predictions': y_pred,
            'probabilities': y_prob,
            'cv_results': perform_cross_validation(model, X_train, y_train)
        }
    
    return results
```

### 2.2 Plot Classification Reports
```python
def plot_classification_report(y_true: np.ndarray,
                             y_pred: np.ndarray,
                             title: str) -> None:
    """
    Create visual classification report.
    
    Parameters:
        y_true (np.ndarray): True labels
        y_pred (np.ndarray): Predicted labels
        title (str): Plot title
    """
    # Get classification report
    report = classification_report(y_true, y_pred, output_dict=True)
    
    # Convert to dataframe
    df_report = pd.DataFrame(report).transpose()
    
    # Create heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_report.iloc[:-1, :-1], annot=True, cmap='Blues')
    plt.title(f'Classification Report: {title}')
    plt.show()
```

## 3. Model Comparison

### 3.1 ROC Curve Analysis
```python
def plot_roc_curves(results: dict,
                    y_test: pd.Series) -> None:
    """
    Plot ROC curves for all models.
    
    Parameters:
        results (dict): Model evaluation results
        y_test (pd.Series): True test labels
    """
    plt.figure(figsize=(10, 6))
    
    for name, result in results.items():
        # Calculate ROC curve
        fpr, tpr, _ = roc_curve(y_test, result['probabilities'])
        roc_auc = auc(fpr, tpr)
        
        # Plot ROC curve
        plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.2f})')
    
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves')
    plt.legend()
    plt.show()
```

### 3.2 Confusion Matrix Analysis
```python
def plot_confusion_matrices(results: dict,
                          y_test: pd.Series) -> None:
    """
    Plot confusion matrices for all models.
    
    Parameters:
        results (dict): Model evaluation results
        y_test (pd.Series): True test labels
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for (name, result), ax in zip(results.items(), axes):
        cm = confusion_matrix(y_test, result['predictions'])
        sns.heatmap(cm, annot=True, fmt='d', ax=ax)
        ax.set_title(f'Confusion Matrix: {name}')
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
    
    plt.tight_layout()
    plt.show()
```

## 4. Retention Strategy Development

### 4.1 Risk Score Calculation
```python
def calculate_risk_scores(model: BaseEstimator,
                         X: pd.DataFrame) -> pd.Series:
    """
    Calculate turnover risk scores.
    
    Parameters:
        model: Best performing model
        X (pd.DataFrame): Feature matrix
        
    Returns:
        pd.Series: Risk scores
    """
    # Get probability of turnover
    risk_scores = model.predict_proba(X)[:, 1]
    
    return pd.Series(risk_scores)
```

### 4.2 Risk Zone Classification
```python
def classify_risk_zones(risk_scores: pd.Series) -> pd.Series:
    """
    Classify employees into risk zones.
    
    Parameters:
        risk_scores (pd.Series): Turnover risk scores
        
    Returns:
        pd.Series: Risk zone classifications
    """
    conditions = [
        (risk_scores < 0.2),
        (risk_scores >= 0.2) & (risk_scores < 0.6),
        (risk_scores >= 0.6) & (risk_scores < 0.9),
        (risk_scores >= 0.9)
    ]
    
    choices = ['Safe', 'Low-Risk', 'Medium-Risk', 'High-Risk']
    
    return pd.Series(np.select(conditions, choices))
```

## 5. Implementation Example
```python
# Load and prepare data
df = load_hr_data(DATA_PATH)
X_train, X_test, y_train, y_test = prepare_data_for_modeling(df)

# Train and evaluate models
model_results = train_evaluate_models(X_train, X_test, y_train, y_test)

# Plot evaluation metrics
for name, result in model_results.items():
    plot_classification_report(y_test, result['predictions'], name)

# Compare models
plot_roc_curves(model_results, y_test)
plot_confusion_matrices(model_results, y_test)

# Select best model (example: gradient boosting)
best_model = model_results['gradient_boosting']['model']

# Calculate risk scores
risk_scores = calculate_risk_scores(best_model, X_test)
risk_zones = classify_risk_zones(risk_scores)

# Create employee risk profile
risk_profile = pd.DataFrame({
    'Risk_Score': risk_scores,
    'Risk_Zone': risk_zones
})
print("\nEmployee Risk Profile:\n", risk_profile.value_counts('Risk_Zone'))
```

## 6. Retention Strategies by Risk Zone

### Safe Zone (Score < 20%)
- Regular check-ins to maintain satisfaction
- Career development opportunities
- Recognition programs

### Low-Risk Zone (20% < Score < 60%)
- Targeted engagement surveys
- Skills development programs
- Performance feedback sessions

### Medium-Risk Zone (60% < Score < 90%)
- One-on-one meetings with managers
- Compensation review
- Work-life balance assessment
- Role adjustment if needed

### High-Risk Zone (Score > 90%)
- Immediate intervention
- Comprehensive retention plan
- Salary and benefits review
- Career path discussion
- Work environment assessment

## 7. Next Steps
1. Implement retention strategies
2. Monitor effectiveness
3. Regular model retraining
4. Feedback loop for strategy refinement
