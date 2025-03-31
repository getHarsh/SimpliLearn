# SimpliLearn Course Materials

## Disclaimer and License

I'm sharing this repository for **educational purposes only**. These materials were used to help a friend complete the SimpliLearn program assignments.

### Course Materials Disclaimer

**Important**: All course content, problem statements, datasets, and instructional materials are the intellectual property of SimpliLearn. I do not claim ownership of these materials, and they are included here solely for educational reference. These course materials are provided "as-is" without any warranty or license from me.

### Code Submissions License

My code submissions and solutions within this repository are provided under the MIT License (see license section below).

I assume no liability for any use of this code or materials. If you choose to use any part of this repository, you do so at your own risk and responsibility.

## About This Repository

This is my personal collection of assignments and project materials from the SimpliLearn program. I've organized everything by course and implemented solutions for various data science, ML, and GenAI challenges.

## Repository Structure

I've organized the repository by courses:

- **Course Mandatory.2 - Course Mandatory.9**: Each directory contains course-specific content

### Standard Directory Structure

Each course typically contains:
- **Assignments**: Problem statements and my submission folders
- **Datasets**: Data files used in exercises and assignments
- **Demos**: Example implementations and demonstrations
- **Ebooks**: Reference materials
- **Instructor_Slides**: Presentation materials

### Assignment Structure

My assignment submissions typically include:
- Main notebook (`.ipynb`)
- Documentation in the `docs/` directory
- Source code in the `source_code/` directory
- Evaluation metrics in the `evaluation/` directory
- Final report summarizing the project

## Git LFS

I've set up this repository with Git Large File Storage (LFS) to handle large files that exceed GitHub's 100MB file size limit.

### Large Files Included

I've specifically configured Git LFS to track these large CSV files that would otherwise exceed GitHub's limits:

- `Course Mandatory.7/Datasets_October/House_Loan_Data_Analysis_dataset/loan_data.csv` (158MB)
- `Course Mandatory.5/Datasets/Lesson_08_Recommender_Systems/8.08_User_Based_Collaborative_Filtering/rating.csv` (106MB)
- `Course Mandatory.7/Datasets_October/Lesson_03_Artificial_Neural_Network/3.04_Perceptron_Based_Classification_Model/mnist_train.csv` (105MB)

These files are commented in the `.gitignore` file for documentation purposes only but are fully included in the repository through Git LFS handling.

### Other File Types Tracked with LFS

I've also configured Git LFS to track these file types that might exceed GitHub's limits:

- Model files (H5, HDF5)
- Serialized objects (pickle, pkl)
- Parquet files

## Course Highlights

### Course Mandatory.8: GenAI
- **Assignment 1**: Virtual Project Management Consultant
- **Assignment 2**: ChatGPT-Based Interactive Storytelling

### Course Mandatory.9: Capstone
- Historical Structures Classification project

## Setup Instructions

To clone this repository and work with the large files:

1. Ensure Git LFS is installed: `brew install git-lfs`
2. Clone the repository: `git clone https://github.com/getHarsh/SimpliLearn.git`
3. Pull LFS content: `git lfs pull`

## MIT License (Applies to My Code Only)

Copyright (c) 2025 Harsh

This license applies **only** to my original code submissions and solutions in this repository, not to any SimpliLearn course materials, problem statements, datasets, or instructional content.

Permission is hereby granted, free of charge, to any person obtaining a copy of my code submissions (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
