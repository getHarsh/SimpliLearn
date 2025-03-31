# Assignment 2: Online Car Rental Platform

A Python-based car rental platform that allows customers to rent cars on hourly, daily, or weekly basis. The system manages inventory, handles rentals, and generates bills automatically.

## Key Features

- Multiple rental modes:
  - Hourly (₹50/hour)
  - Daily (₹800/day)
  - Weekly (₹4000/week)
- Real-time inventory management
- Automated billing system
- Customer request handling
- Flexible car quantity selection

## Project Structure

```
.
├── car_rental.py         # Core rental system logic
├── customer.py           # Customer management
├── car_rental_system.ipynb  # Main interactive interface
├── main.py              # CLI interface
├── run.py               # Build system
├── requirements.txt     # Dependencies
├── tests/               # Test suite
└── docs/                # Documentation
```

## Documentation

Detailed documentation is available in the `docs` directory:

- [Getting Started Guide](docs/GETTING_STARTED.md)
  - Installation instructions
  - Environment setup
  - Running tests

- [Jupyter Guide](docs/JUPYTER_GUIDE.md)
  - Using the notebook interface
  - Interactive examples
  - Troubleshooting

- [Features](docs/FEATURES.md)
  - Feature details
  - Usage examples

- [Data Models](docs/MODELS.md)
  - Model documentation
  - Class descriptions
  - Field details

- [Code Setup](docs/CODE_SETUP.md)
  - Project structure
  - Development guidelines
  - Error handling

## Quick Start

The project includes a build system (`run.py`) that handles setup, dependencies, and execution:

```bash
# Run the application
./run.py

# Run the test suite
./run.py --test

# Clean build (removes virtual environment and starts fresh)
./run.py --deepbuild

# Clean build with tests
./run.py --test --deepbuild
```

The script will automatically set up your environment and run the requested component.

## Notes

- Focus on clean code and maintainability
- Comprehensive error handling
- Test-driven development approach
