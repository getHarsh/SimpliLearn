# Exploratory Data Analysis Findings

This document presents the key findings from my exploratory data analysis of the boat classification dataset used in the Automating Port Operations project.

## Overview

Before building deep learning models, I conducted exploratory data analysis (EDA) to understand the dataset characteristics, identify patterns, and gain insights that would inform my modeling approach.

## Dataset Characteristics

The dataset contains images of 9 types of boats with the following characteristics:

```python
# List the boat categories and count the number of images in each category
boat_categories = os.listdir(dataset_path)
if '.DS_Store' in boat_categories:  # Remove hidden files if present
    boat_categories.remove('.DS_Store')

print(f"Found {len(boat_categories)} categories of boats:")
for category in sorted(boat_categories):
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        num_images = len(os.listdir(category_path))
        print(f"- {category}: {num_images} images")

total_images = sum([len(os.listdir(os.path.join(dataset_path, cat))) for cat in boat_categories if os.path.isdir(os.path.join(dataset_path, cat))])
print(f"\nTotal number of images: {total_images}")
```

Key findings from this initial exploration:

### 1. Class Distribution

The dataset has 1,162 images distributed across 9 boat categories:
- **buoy**: ~130 images
- **cruise_ship**: ~130 images
- **ferry_boat**: ~130 images
- **freight_boat**: ~120 images
- **gondola**: ~130 images
- **inflatable_boat**: ~130 images
- **kayak**: ~130 images
- **paper_boat**: ~130 images
- **sailboat**: ~130 images

The distribution is relatively balanced, with only minor differences in the number of images per class. This balanced distribution is beneficial for training models as it reduces the risk of class bias.

### 2. Image Characteristics

I examined sample images from each category to understand their visual properties:

```python
# Visualize sample images from each category
visualize_data(dataset_path, boat_categories)
```

This visualization revealed several important insights:

#### Image Quality and Variation
- **Image Resolution**: Varied across the dataset, but all adequate for deep learning
- **Background Variation**: Images feature boats in different environments (open water, harbors, docks)
- **Lighting Conditions**: Mix of daylight, cloudy, and some indoor/studio images
- **Angle Perspective**: Various angles including aerial, front-view, side-view, and distant shots
- **Quality**: Generally good quality, some with watermarks or text

#### Visual Distinctiveness Between Classes
- **Highly Distinctive Classes**: 
  - Paper boats (small, usually on calm water)
  - Cruise ships (large, multi-deck vessels)
  - Buoys (floating markers, not technically boats)
  
- **Moderately Distinctive Classes**:
  - Sailboats (characterized by sails)
  - Kayaks (small, narrow vessels with visible paddler)
  - Gondolas (distinctive Venetian design)
  
- **Potentially Confusable Classes**:
  - Ferry boats and freight boats (similar size and structure in some images)
  - Inflatable boats and certain kayaks (similar when viewed from certain angles)

## Image Size and Format Analysis

I analyzed the image dimensions and formats to understand any preprocessing needs:

```python
# Code to check image dimensions (implementation in notebook)
for images, _ in train_ds.take(1):
    print(f"Image batch shape: {images.shape}")
```

Findings:
- **Original Dimensions**: Varied across the dataset (different aspect ratios and resolutions)
- **Color Channels**: All images are RGB (3 channels)
- **File Formats**: Primarily JPEG and PNG formats

These findings informed my decision to standardize all images to 224×224 pixels, which is both an appropriate size for CNN models and the required input size for MobileNetV2.

## Visual Feature Analysis

I conducted a qualitative analysis of the visual features that distinguish different boat types:

### Key Distinguishing Features

1. **Size and Scale**:
   - Cruise ships and freight boats are the largest vessels
   - Kayaks, paper boats, and inflatable boats are the smallest
   - Size can be a key discriminator but may be difficult to determine without context

2. **Shape and Structure**:
   - Sailboats have distinctive sail structures
   - Gondolas have a characteristic curved shape
   - Kayaks have a distinctive elongated shape
   - Buoys have various shapes but are generally rounded and floating

3. **Color Patterns**:
   - Paper boats often have bright colors or patterns
   - Ferry boats often have commercial/transit colors
   - Cruise ships frequently have white color with distinctive stripes
   - Buoys often have bright warning colors (red, yellow, orange)

4. **Contextual Elements**:
   - Cruise ships often photographed near ports with many people
   - Ferry boats typically shown loading/unloading passengers
   - Freight boats often carrying visible cargo
   - Gondolas almost exclusively in Venetian canal settings

## Potential Challenges Identified

Based on the exploratory analysis, I identified several potential challenges for model development:

1. **Scale Variation**: 
   - The absolute size of boats is difficult to determine without context
   - Models need to focus on structural features rather than absolute size

2. **Perspective Challenges**:
   - Different viewing angles can significantly change the appearance of a boat
   - Need for models that are robust to perspective changes

3. **Environmental Factors**:
   - Varying water conditions, lighting, and backgrounds
   - Models need to ignore these contextual variations and focus on the boat itself

4. **Similar Classes**:
   - Some boat types share similar characteristics
   - The model needs to learn subtle distinguishing features

5. **Dataset Size**:
   - While reasonable for a classification task, ~130 images per class is relatively small for deep learning
   - Transfer learning becomes particularly important to overcome limited data

## Batch Visualization Analysis

I examined the batched data to ensure proper loading and preprocessing:

```python
# Check the structure of the datasets
print("Training dataset:")
for images, labels in train_ds.take(1):
    print(f"Image batch shape: {images.shape}")
    print(f"Label batch shape: {labels.shape}")
    print(f"Labels: {labels}")
```

This analysis confirmed:
- Images were properly batched (batch size of 32)
- Labels were correctly one-hot encoded
- Image dimensions were standardized to 224×224×3
- Pixel values were normalized to the range [0-1]

## Data Quality Assessment

I conducted a data quality assessment to identify potential issues:

1. **Missing or Corrupted Images**: None detected
2. **Label Consistency**: All images appropriately labeled
3. **Preprocessing Artifacts**: No artifacts introduced during preprocessing
4. **Class Representation**: Relatively balanced across categories

## Insights for Modeling

Based on the exploratory analysis, I derived several key insights to guide the modeling approach:

1. **Transfer Learning Benefits**:
   - The limited dataset size (~130 images per class) makes transfer learning particularly valuable
   - Pre-trained features from models like MobileNetV2 can help capture generic visual patterns

2. **Architectural Considerations**:
   - Models need sufficient complexity to distinguish between similar boat types
   - Global average pooling beneficial for handling different boat positions in frame

3. **Feature Learning Focus**:
   - The model should focus on learning shape, structure, and distinctive features
   - Less emphasis on color and background, which can vary widely

4. **Robustness Requirements**:
   - Models need robustness to varying perspectives, lighting, and backgrounds
   - The lightweight model needs to balance accuracy with efficiency for mobile deployment

5. **Evaluation Priorities**:
   - Particular attention should be paid to commonly confused classes in evaluation
   - Class-specific performance metrics should be analyzed

## Conclusion

The exploratory data analysis provided valuable insights into the boat classification dataset. The dataset is relatively balanced with sufficient quality for deep learning, though the limited number of images per class suggests that transfer learning will be beneficial. The visual analysis identified key distinguishing features between boat types and potential challenges in classification.

These insights directly informed my modeling approach, particularly the decision to implement a transfer learning model using MobileNetV2 alongside the custom CNN. The analysis also highlighted the importance of comprehensive evaluation to ensure the model performs well across all boat categories, especially those with similar visual characteristics.