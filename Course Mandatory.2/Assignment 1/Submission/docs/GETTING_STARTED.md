# Getting Started with Demo Marketplace

This guide will help you set up and run the Demo Marketplace application.

## Quick Start

The setup script can run either the application or the test suite:

```bash
# Run the application (default)
./run.py

# Run the test suite
./run.py --test
# or
./run.py -t

# Run tests with verbose output
./run.py --test --verbose
# or
./run.py -t -v

# Clean build (removes virtual environment and starts fresh)
./run.py --deepbuild
# or
./run.py -d

# Clean build with tests
./run.py --test --deepbuild
# or
./run.py -t -d
```

The script will automatically handle everything for you!

## What the Setup Script Does

1. Detects your operating system and Python installation
2. Supports multiple Python environments:
   - Standard Python installation
   - Conda environment
   - Python3 vs Python command variations
3. Creates an isolated environment:
   - Uses conda if in a conda environment
   - Creates virtual environment otherwise
   - Falls back to virtualenv if venv fails
4. Installs dependencies:
   - Uses conda-forge channel in conda environments
   - Falls back to pip if conda install fails
   - Uses pip in standard virtual environments
5. Supports clean builds:
   - Can remove existing virtual environment
   - Creates fresh environment
   - Reinstalls all dependencies
6. Launches the application

On subsequent runs, it will detect the existing setup and launch directly.

## Manual Installation

If you prefer manual setup:

1. Ensure Python 3.7+ is installed
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   
   # Activate it on Unix-like systems
   source .venv/bin/activate
   
   # Activate it on Windows
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Demo Credentials

- Regular User:
  - Username: user1
  - Password: pass123
  - Username: user2
  - Password: pass456
- Admin User:
  - Username: admin
  - Password: admin123

## Running Tests

You can run tests in two ways:

1. Using the setup script (recommended):
   ```bash
   # Run tests
   ./run.py --test
   
   # Run tests with verbose output
   ./run.py --test --verbose
   ```

2. Manually with unittest:
   ```bash
   python3 -m unittest tests.py
   ```

## Supported Environments

- Windows: Python, Conda
- Mac/Linux: Python3, Python, Conda
- Automatically detects and uses the appropriate commands

## Next Steps

- Check out [MARKETPLACE.md](MARKETPLACE.md) for marketplace features and usage
- See [MODELS.md](MODELS.md) for data model documentation
- View [CODE_SETUP.md](CODE_SETUP.md) for code organization and development setup
