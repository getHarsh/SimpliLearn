# Marketplace Features

This document describes the features and functionality of the Demo Marketplace application.

## Authentication System

- Separate user and admin logins with session management
- Role-based access control with proper security checks
- Session tracking using unique session IDs

## Product Management

- Organized product catalog with categories
- Product attributes: ID, name, category, price

### Initial Categories
- Boots
- Coats
- Jackets
- Caps

### Sample Products
- Leather Boots (P1): ₹1,499.99
- Winter Coat (P2): ₹2,499.99
- Denim Jacket (P3): ₹999.99
- Baseball Cap (P4): ₹299.99

## Shopping Cart

- Add/remove items with quantity management
- View cart contents with item details
- Calculate running totals

## Payment Processing

Available payment methods:
- UPI
- Net Banking (default)
- PayPal

Each payment method provides appropriate redirection messages and handles the checkout process securely.

## Admin Controls

Administrators can:
- Add new products
- Modify existing products
- Delete products
- Add new categories
- Delete categories (only if they have no products)

All admin operations are protected and require proper authentication.

## Error Handling

The marketplace implements robust error handling:
- Permission errors for unauthorized access
- Validation errors for invalid inputs
- Descriptive error messages
- Proper exception handling

## Testing

All marketplace features are thoroughly tested:
- Authentication tests
- Product management tests
- Shopping cart tests
- Payment processing tests
- Admin operation tests
- Error handling tests

Run the test suite using:
```bash
./run.py --test
```

## Related Documentation

- See [GETTING_STARTED.md](GETTING_STARTED.md) for setup instructions
- Check [MODELS.md](MODELS.md) for data model details
- View [CODE_SETUP.md](CODE_SETUP.md) for development information
