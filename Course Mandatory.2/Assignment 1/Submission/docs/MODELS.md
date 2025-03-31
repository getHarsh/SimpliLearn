# Data Models

This document describes the data models used in the Demo Marketplace application.

## User Model

```python
class User:
    """Represents a user in the system."""
    def __init__(self, username: str, password: str, is_admin: bool = False)
```

- `username`: User's login name
- `password`: User's password (demo only, not secure)
- `is_admin`: Whether user has admin privileges
- Methods for session management

## Product Model

```python
class Product:
    """Represents a product in the catalog."""
    def __init__(self, product_id: str, name: str, category_id: str, price: float)
```

- `product_id`: Unique identifier (e.g., "P1")
- `name`: Product name
- `category_id`: Reference to category
- `price`: Product price in INR

## Category Model

```python
class Category:
    """Represents a product category."""
    def __init__(self, category_id: str, name: str)
```

- `category_id`: Unique identifier (e.g., "BOOT")
- `name`: Category name

## Shopping Cart Models

### CartItem

```python
class CartItem:
    """Represents an item in a shopping cart."""
    def __init__(self, product_id: str, quantity: int)
```

- `product_id`: Reference to product
- `quantity`: Number of items

### ShoppingCart

```python
class ShoppingCart:
    """Manages a user's shopping cart."""
    def __init__(self, session_id: str)
```

- `session_id`: Reference to user session
- `items`: List of CartItems

## Related Documentation

- See [GETTING_STARTED.md](GETTING_STARTED.md) for setup instructions
- Check [MARKETPLACE.md](MARKETPLACE.md) for feature details
- View [CODE_SETUP.md](CODE_SETUP.md) for development information
