# Demo Marketplace

A comprehensive e-commerce application backend implementing role-based user management, product catalog, shopping cart, and payment processing functionality.

## Key Features

- **Authentication**: User and admin logins with session management
- **Product Management**: Organized catalog with categories
- **Shopping Cart**: Add/remove items, view contents, calculate totals
- **Payment Processing**: Multiple payment options (UPI, Net Banking, PayPal)
- **Admin Controls**: Product and category management

## Documentation

Detailed documentation is available in the `docs` directory:

- [Getting Started Guide](docs/GETTING_STARTED.md)
  - Installation instructions
  - Environment setup
  - Demo credentials
  - Running tests

- [Marketplace Features](docs/MARKETPLACE.md)
  - Feature details
  - Initial catalog
  - Payment methods
  - Admin operations

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

- Backend-only implementation
- No database connectivity required
- Focus on clean code and maintainability
- Comprehensive error handling
