# SimpliLearn Course Materials

This repository contains materials and assignments for the SimpliLearn program, including datasets, notebooks, and project submissions.

## Repository Structure

The repository is organized by courses:

- **Course Mandatory.2 - Course Mandatory.9**: Each directory contains course-specific content

### Standard Directory Structure

Each course typically contains:
- **Assignments**: Contains problem statements and submission folders
- **Datasets**: Data files used in exercises and assignments
- **Demos**: Example implementations and demonstrations
- **Ebooks**: Reference materials
- **Instructor_Slides**: Presentation materials

### Assignment Structure

Each assignment submission contains:
- Main notebook (`.ipynb`)
- Documentation in the `docs/` directory
- Source code in the `source_code/` directory
- Evaluation metrics in the `evaluation/` directory
- Final report summarizing the project

## Git LFS

This repository uses Git Large File Storage (LFS) to handle large files. The following files are tracked with Git LFS:

- Large dataset files (CSV)
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
2. Clone the repository: `git clone https://github.com/YourUsername/SimpliLearn-Projects.git`
3. Pull LFS content: `git lfs pull`
