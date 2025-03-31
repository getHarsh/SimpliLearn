"""
Core marketplace functionality module.

This module contains the DemoMarketplace class which implements all the core
business logic for the e-commerce application.
"""

from typing import Dict, List, Optional
from models import User, Product, Category, CartItem, ShoppingCart

class DemoMarketplace:
    """
    Main class implementing the e-commerce marketplace functionality.
    
    This class handles all core operations including:
    - User authentication and session management
    - Product and category management
    - Shopping cart operations
    - Checkout and payment processing
    
    The class maintains in-memory data structures for all entities as per
    the assignment requirements (no database connectivity required).
    """

    def __init__(self):
        """Initialize the marketplace with demo data."""
        self.welcome_message = "Welcome to the Demo Marketplace"
        
        # Initialize demo databases
        self.users: Dict[str, User] = {
            "user1": User("user1", "pass123"),
            "user2": User("user2", "pass456"),
            "admin": User("admin", "admin123", True)
        }
        
        self.categories: Dict[str, Category] = {
            "BOOT": Category("BOOT", "Boots"),
            "COAT": Category("COAT", "Coats"),
            "JACK": Category("JACK", "Jackets"),
            "CAPS": Category("CAPS", "Caps")
        }
        
        self.products: Dict[str, Product] = {
            "P1": Product("P1", "Leather Boots", "BOOT", 1499.99),
            "P2": Product("P2", "Winter Coat", "COAT", 2499.99),
            "P3": Product("P3", "Denim Jacket", "JACK", 999.99),
            "P4": Product("P4", "Baseball Cap", "CAPS", 299.99)
        }
        
        self.active_sessions: Dict[str, User] = {}
        self.shopping_carts: Dict[str, ShoppingCart] = {}
        
        # Available payment methods
        self.payment_methods = ["NetBanking", "PayPal", "UPI"]

    def get_welcome_message(self) -> str:
        """Return the welcome message."""
        return self.welcome_message

    def login(self, username: str, password: str) -> str:
        """
        Authenticate a user and create a session.
        
        Args:
            username: The user's username
            password: The user's password
            
        Returns:
            str: Session ID if login successful
            
        Raises:
            ValueError: If credentials are invalid
        """
        user = self.users.get(username)
        if user and user.password == password:
            session_id = user.login()
            self.active_sessions[session_id] = user
            return session_id
        raise ValueError("Invalid credentials")

    def logout(self, session_id: str) -> None:
        """
        End a user's session.
        
        Args:
            session_id: The session to end
        """
        if session_id in self.active_sessions:
            user = self.active_sessions[session_id]
            user.logout()
            del self.active_sessions[session_id]
            if session_id in self.shopping_carts:
                del self.shopping_carts[session_id]

    def is_admin(self, session_id: str) -> bool:
        """Check if the session belongs to an admin user."""
        user = self.active_sessions.get(session_id)
        return user and user.is_admin

    def is_admin_session(self, session_id: str) -> bool:
        """Check if the session belongs to an admin user."""
        return self.is_admin(session_id)

    def is_user_session(self, session_id: str) -> bool:
        """Check if the session belongs to a regular user."""
        user = self.active_sessions.get(session_id)
        return user and not user.is_admin

    def view_catalog(self, session_id: Optional[str] = None) -> str:
        """
        Generate a formatted string of the product catalog.
        
        Args:
            session_id: Optional session ID. If provided, verifies session is valid.
            
        Returns:
            str: Formatted catalog string
            
        Raises:
            ValueError: If session_id is provided but invalid
        """
        if session_id and session_id not in self.active_sessions:
            raise ValueError("Invalid session")
        output = "\nProduct Catalog:\n" + "-" * 60 + "\n"
        output += f"{'ID':<8} {'Name':<20} {'Category':<15} {'Price':>10}\n"
        output += "-" * 60 + "\n"
        
        for product in self.products.values():
            category = self.categories[product.category_id].name
            output += f"{product.product_id:<8} {product.name:<20} {category:<15} ₹{product.price:>9.2f}\n"
        
        return output

    def add_to_cart(self, session_id: str, product_id: str, quantity: int) -> str:
        """
        Add a product to the user's shopping cart.
        
        Args:
            session_id: User's session ID
            product_id: Product to add
            quantity: Quantity to add
            
        Returns:
            str: Status message
            
        Raises:
            PermissionError: If session is not a user session
            ValueError: If product not found or invalid quantity
        """
        if not self.is_user_session(session_id):
            raise PermissionError("Only users can add items to cart")
        
        if product_id not in self.products:
            raise ValueError("Product not found")
            
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        if session_id not in self.shopping_carts:
            self.shopping_carts[session_id] = ShoppingCart(session_id)
            
        cart = self.shopping_carts[session_id]
        
        for item in cart.items:
            if item.product_id == product_id:
                item.quantity += quantity
                return "Updated"
                
        cart.items.append(CartItem(product_id, quantity))
        return "Added"

    def remove_from_cart(self, session_id: str, product_id: str, quantity: int) -> str:
        """
        Remove a product from the user's shopping cart.
        
        Args:
            session_id: User's session ID
            product_id: Product to remove
            quantity: Quantity to remove
            
        Returns:
            str: Status message
            
        Raises:
            PermissionError: If session is not a user session
            ValueError: If product not found or invalid quantity
        """
        if not self.is_user_session(session_id):
            raise PermissionError("Only users can remove items from cart")
            
        if session_id not in self.shopping_carts:
            raise ValueError("Cart is empty")
            
        if product_id not in self.products:
            raise ValueError("Product not found")
            
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        cart = self.shopping_carts[session_id]
        
        for item in cart.items:
            if item.product_id == product_id:
                if quantity >= item.quantity:
                    cart.items.remove(item)
                else:
                    item.quantity -= quantity
                return "Removed"
                    
        raise ValueError("Product not found in cart")

    def view_cart(self, session_id: str) -> str:
        """
        Generate a formatted string of the user's shopping cart.
        
        Args:
            session_id: User's session ID
            
        Returns:
            str: Formatted cart string
            
        Raises:
            ValueError: If session is invalid
            PermissionError: If session is an admin session
        """
        if session_id not in self.active_sessions:
            raise ValueError("Invalid session")
            
        user = self.active_sessions[session_id]
        if user.is_admin:
            raise PermissionError("Admins cannot have shopping carts")
            
        if session_id not in self.shopping_carts or not self.shopping_carts[session_id].items:
            return "Cart is empty"
            
        cart = self.shopping_carts[session_id]
        output = "\nShopping Cart:\n" + "-" * 60 + "\n"
        output += f"{'Product':<20} {'Quantity':>8} {'Price':>10} {'Total':>10}\n"
        output += "-" * 60 + "\n"
        
        total = 0
        for item in cart.items:
            product = self.products[item.product_id]
            item_total = product.price * item.quantity
            total += item_total
            output += f"{product.name:<20} {item.quantity:>8} ₹{product.price:>9.2f} ₹{item_total:>9.2f}\n"
            
        output += "-" * 60 + "\n"
        output += f"{'Total:':<40} ₹{total:>9.2f}\n"
        
        return output

    def checkout(self, session_id: str, payment_method: str = "NetBanking") -> str:
        """
        Process checkout with the specified payment method.
        
        Args:
            session_id: User's session ID
            payment_method: Payment method to use
            
        Returns:
            str: Payment status message
            
        Raises:
            PermissionError: If session is not a user session
            ValueError: If cart is empty or payment method invalid
        """
        if not self.is_user_session(session_id):
            raise PermissionError("Only users can checkout")
            
        if session_id not in self.shopping_carts:
            raise ValueError("Cart is empty")
            
        cart = self.shopping_carts[session_id]
        if not cart.items:
            raise ValueError("Cart is empty")
            
        if payment_method not in self.payment_methods:
            raise ValueError(f"Invalid payment method. Available methods: {', '.join(self.payment_methods)}")
        
        total = sum(self.products[item.product_id].price * item.quantity for item in cart.items)
        
        # Clear cart after successful checkout
        del self.shopping_carts[session_id]
        
        if payment_method == "UPI":
            return f"You will be shortly redirected to the portal for Unified Payment Interface to make a payment of ₹{total:.2f}"
        elif payment_method == "PayPal":
            return f"Redirecting to PayPal for payment of ₹{total:.2f}"
        else:
            return f"Redirecting to Net Banking portal for payment of ₹{total:.2f}"

    def add_product(self, session_id: str, product_id: str, name: str, category_id: str, price: float) -> str:
        """
        Add a new product to the catalog (admin only).
        
        Args:
            session_id: Admin's session ID
            product_id: Unique product identifier
            name: Product name
            category_id: Category ID
            price: Product price
            
        Returns:
            str: Status message
            
        Raises:
            PermissionError: If session is not an admin session
            ValueError: If category invalid or price negative
        """
        if not self.is_admin_session(session_id):
            raise PermissionError("Only admin can add products")
            
        if category_id not in self.categories:
            raise ValueError("Invalid category")
            
        if price <= 0:
            raise ValueError("Price must be positive")
            
        if product_id in self.products:
            raise ValueError("Product ID already exists")
            
        self.products[product_id] = Product(product_id, name, category_id, price)
        return "Added"

    def modify_product(self, session_id: str, product_id: str, name: str, category_id: str, price: float) -> str:
        """
        Modify an existing product (admin only).
        
        Args:
            session_id: Admin's session ID
            product_id: Product to modify
            name: New name
            category_id: New category ID
            price: New price
            
        Returns:
            str: Status message
            
        Raises:
            PermissionError: If session is not an admin session
            ValueError: If product not found, category invalid, or price negative
        """
        if not self.is_admin_session(session_id):
            raise PermissionError("Only admin can modify products")
            
        if product_id not in self.products:
            raise ValueError("Product not found")
            
        if category_id not in self.categories:
            raise ValueError("Invalid category")
            
        if price <= 0:
            raise ValueError("Price must be positive")
            
        self.products[product_id] = Product(product_id, name, category_id, price)
        return "Modified"

    def delete_product(self, session_id: str, product_id: str) -> str:
        """
        Delete a product from the catalog (admin only).
        
        Args:
            session_id: Admin's session ID
            product_id: Product to delete
            
        Returns:
            str: Status message
            
        Raises:
            PermissionError: If session is not an admin session
            ValueError: If product not found
        """
        if not self.is_admin_session(session_id):
            raise PermissionError("Only admin can delete products")
            
        if product_id not in self.products:
            raise ValueError("Product not found")
            
        del self.products[product_id]
        return "Deleted"

    def add_category(self, session_id: str, category_id: str, name: str) -> str:
        """
        Add a new product category (admin only).
        
        Args:
            session_id: Admin's session ID
            category_id: Unique category identifier
            name: Category name
            
        Returns:
            str: Status message
            
        Raises:
            PermissionError: If session is not an admin session
            ValueError: If category already exists
        """
        if not self.is_admin_session(session_id):
            raise PermissionError("Only admin can add categories")
            
        if category_id in self.categories:
            raise ValueError("Category already exists")
            
        self.categories[category_id] = Category(category_id, name)
        return "Added"

    def delete_category(self, session_id: str, category_id: str) -> str:
        """
        Delete a product category (admin only).
        
        Args:
            session_id: Admin's session ID
            category_id: Category to delete
            
        Returns:
            str: Status message
            
        Raises:
            PermissionError: If session is not an admin session
            ValueError: If category not found or has products
        """
        if not self.is_admin_session(session_id):
            raise PermissionError("Only admin can delete categories")
            
        if category_id not in self.categories:
            raise ValueError("Category not found")
            
        # Check if category has products
        for product in self.products.values():
            if product.category_id == category_id:
                raise ValueError("Cannot delete category with existing products")
                
        del self.categories[category_id]
        return "Deleted"
