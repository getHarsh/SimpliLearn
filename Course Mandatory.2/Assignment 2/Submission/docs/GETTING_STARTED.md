# Getting Started Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone or download the repository
2. Navigate to the project directory

## Environment Setup

The project uses a virtual environment to manage dependencies. The `run.py` script will handle this automatically, but if you need to set it up manually:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

```bash
# Using run.py (recommended)
./run.py

# Manual execution
python3 main.py
```

## Running Tests

```bash
# Using run.py
./run.py --test

# Manual test execution
python3 -m pytest tests/
```

## Project Structure

```
.
├── README.md
├── docs/
│   ├── GETTING_STARTED.md
│   ├── FEATURES.md
│   ├── MODELS.md
│   └── CODE_SETUP.md
├── main.py
├── models.py
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── requirements.txt
└── run.py
```
