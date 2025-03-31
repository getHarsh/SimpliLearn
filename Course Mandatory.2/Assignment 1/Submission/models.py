"""
Models module for the Demo Marketplace application.

This module contains all the data models used in the application:
- User: Represents a user or admin in the system
- Product: Represents a product in the catalog
- Category: Represents a product category
- CartItem: Represents an item in a shopping cart
- ShoppingCart: Represents a user's shopping cart
"""

from typing import List, Optional
import uuid

class User:
    """
    Represents a user in the system.
    
    Attributes:
        username (str): User's username
        password (str): User's password (Note: In a real system, this would be hashed)
        is_admin (bool): Whether the user has admin privileges
        session_id (Optional[str]): Current session ID if user is logged in
    """
    
    def __init__(self, username: str, password: str, is_admin: bool = False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.session_id: Optional[str] = None

    def login(self) -> str:
        """Generate a new session ID for the user."""
        self.session_id = str(uuid.uuid4())
        return self.session_id

    def logout(self) -> None:
        """Clear the user's session ID."""
        self.session_id = None

class Product:
    """
    Represents a product in the catalog.
    
    Attributes:
        product_id (str): Unique identifier for the product
        name (str): Name of the product
        category_id (str): ID of the category this product belongs to
        price (float): Price of the product in rupees
    """
    
    def __init__(self, product_id: str, name: str, category_id: str, price: float):
        self.product_id = product_id
        self.name = name
        self.category_id = category_id
        self.price = price

class Category:
    """
    Represents a product category.
    
    Attributes:
        category_id (str): Unique identifier for the category
        name (str): Name of the category
    """
    
    def __init__(self, category_id: str, name: str):
        self.category_id = category_id
        self.name = name

class CartItem:
    """
    Represents an item in a shopping cart.
    
    Attributes:
        product_id (str): ID of the product
        quantity (int): Quantity of the product
    """
    
    def __init__(self, product_id: str, quantity: int):
        self.product_id = product_id
        self.quantity = quantity

class ShoppingCart:
    """
    Represents a user's shopping cart.
    
    Attributes:
        session_id (str): Session ID of the user who owns this cart
        items (List[CartItem]): List of items in the cart
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.items: List[CartItem] = []
