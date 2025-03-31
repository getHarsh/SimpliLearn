"""
Test module for the Demo Marketplace application.

This module contains unit tests for the core functionality of the marketplace.
"""

import unittest
from marketplace import DemoMarketplace
from models import User, Product, Category, CartItem, ShoppingCart

class TestDemoMarketplace(unittest.TestCase):
    """Test cases for DemoMarketplace class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.marketplace = DemoMarketplace()
        self.user_session = self.marketplace.login("user1", "pass123")
        self.admin_session = self.marketplace.login("admin", "admin123")
        
    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'user_session') and self.user_session:
            self.marketplace.logout(self.user_session)
        if hasattr(self, 'admin_session') and self.admin_session:
            self.marketplace.logout(self.admin_session)

    def test_welcome_message(self):
        """Test welcome message display."""
        message = self.marketplace.get_welcome_message()
        self.assertEqual(message, "Welcome to the Demo Marketplace")
    
    def test_authentication(self):
        """Test user authentication and session management."""
        # Test valid credentials
        session = self.marketplace.login("user1", "pass123")
        self.assertIsNotNone(session)
        
        # Test invalid credentials
        with self.assertRaises(ValueError):
            self.marketplace.login("user1", "wrongpass")
        
        # Test admin credentials
        admin_session = self.marketplace.login("admin", "admin123")
        self.assertIsNotNone(admin_session)
        self.assertTrue(self.marketplace.is_admin(admin_session))
        
        # Test admin with wrong credentials
        with self.assertRaises(ValueError):
            self.marketplace.login("admin", "wrongpass")
        
        # Test session invalidation
        self.marketplace.logout(session)
        with self.assertRaises(ValueError):
            self.marketplace.view_cart(session)
        
        # Test role validation
        with self.assertRaises(PermissionError):
            self.marketplace.add_product(self.user_session, "P5", "Test", "ELEC", 999.99)

    def test_product_management(self):
        """Test product catalog operations."""
        # Test user can't manage products
        with self.assertRaises(PermissionError):
            self.marketplace.add_product(self.user_session, "P5", "Test", "ELEC", 99.99)
        
        with self.assertRaises(PermissionError):
            self.marketplace.modify_product(self.user_session, "P1", "Test Product", "BOOT", 99.99)
        
        with self.assertRaises(PermissionError):
            self.marketplace.delete_product(self.user_session, "P1")
        
        # Test admin product operations
        initial_count = len(self.marketplace.products)
        
        # Add new product
        result = self.marketplace.add_product(
            self.admin_session, "P5", "Test Product", "BOOT", 999.99
        )
        self.assertIn("Added", result)
        self.assertEqual(len(self.marketplace.products), initial_count + 1)
        
        # Verify both admin and user can view products
        catalog = self.marketplace.view_catalog()
        self.assertIn("Test Product", catalog)
        
        # Modify product
        new_product_id = f"P{initial_count + 1}"
        result = self.marketplace.modify_product(
            self.admin_session, "P5", "Updated Product", "BOOT", 1099.99
        )
        self.assertIn("Modified", result)
        
        # Delete product
        result = self.marketplace.delete_product(self.admin_session, new_product_id)
        self.assertIn("Deleted", result)
        self.assertEqual(len(self.marketplace.products), initial_count)

    def test_category_management(self):
        """Test category operations."""
        # Test user can't manage categories
        with self.assertRaises(PermissionError):
            self.marketplace.add_category(self.user_session, "BOOK", "Books")
        
        with self.assertRaises(PermissionError):
            self.marketplace.delete_category(self.user_session, "BOOT")
        
        # Test admin category operations
        # Add new category
        result = self.marketplace.add_category(self.admin_session, "BOOK", "Books")
        self.assertIn("Added", result)
        
        # Add product to new category
        result = self.marketplace.add_product(
            self.admin_session, "P5", "Python Book", "BOOK", 499.99
        )
        self.assertIn("Added", result)
        
        # Verify catalog shows new category
        catalog = self.marketplace.view_catalog()
        self.assertIn("Books", catalog)
        self.assertIn("Python Book", catalog)
        
        # Try to delete non-empty category
        with self.assertRaises(ValueError):
            self.marketplace.delete_category(self.admin_session, "BOOK")
        
        # Delete product then category
        self.marketplace.delete_product(self.admin_session, "P5")
        result = self.marketplace.delete_category(self.admin_session, "BOOK")
        self.assertIn("Deleted", result)

    def test_cart_operations(self):
        """Test shopping cart operations."""
        # Test admin can't perform cart operations
        with self.assertRaises(PermissionError):
            self.marketplace.add_to_cart(self.admin_session, "P1", 2)
        
        with self.assertRaises(PermissionError):
            self.marketplace.view_cart(self.admin_session)
        
        # Test user cart operations
        # Add items
        result = self.marketplace.add_to_cart(self.user_session, "P1", 2)
        self.assertIn("Added", result)
        
        result = self.marketplace.add_to_cart(self.user_session, "P3", 1)
        self.assertIn("Added", result)
        
        # View cart
        cart = self.marketplace.view_cart(self.user_session)
        self.assertIn("Leather Boots", cart)
        self.assertIn("Denim Jacket", cart)
        
        # Update quantity
        result = self.marketplace.add_to_cart(self.user_session, "P1", 3)
        self.assertIn("Updated", result)
        
        # Remove items
        result = self.marketplace.remove_from_cart(self.user_session, "P1", 5)
        self.assertIn("Removed", result)
        
        result = self.marketplace.remove_from_cart(self.user_session, "P3", 1)
        self.assertIn("Removed", result)
        
        # Verify cart is empty
        cart = self.marketplace.view_cart(self.user_session)
        self.assertEqual(cart, "Cart is empty")

    def test_checkout_process(self):
        """Test checkout and payment processing."""
        # Add items to cart
        self.marketplace.add_to_cart(self.user_session, "P1", 2)
        self.marketplace.add_to_cart(self.user_session, "P2", 1)
        
        # Test invalid payment method
        with self.assertRaises(ValueError):
            self.marketplace.checkout(self.user_session, "InvalidMethod")
        
        # Test successful checkout with NetBanking
        result = self.marketplace.checkout(self.user_session, "NetBanking")
        self.assertIn("Redirecting", result)
        
        # Verify cart is empty after checkout
        cart = self.marketplace.view_cart(self.user_session)
        self.assertEqual(cart, "Cart is empty")
        
        # Add more items and test PayPal
        self.marketplace.add_to_cart(self.user_session, "P3", 1)
        result = self.marketplace.checkout(self.user_session, "PayPal")
        self.assertIn("Redirecting", result)
        
        # Add more items and test UPI
        self.marketplace.add_to_cart(self.user_session, "P4", 2)
        result = self.marketplace.checkout(self.user_session, "UPI")
        self.assertIn("portal", result)

    def test_error_handling(self):
        """Test error handling and edge cases."""
        # Test adding invalid product
        with self.assertRaises(ValueError):
            self.marketplace.add_to_cart(self.user_session, "InvalidProduct", 1)
        
        # Test adding invalid quantity
        with self.assertRaises(ValueError):
            self.marketplace.add_to_cart(self.user_session, "P1", 0)
            
        with self.assertRaises(ValueError):
            self.marketplace.add_to_cart(self.user_session, "P1", -1)
        
        # Test invalid session
        with self.assertRaises(PermissionError):
            self.marketplace.add_to_cart("invalid_session", "P1", 1)
        
        # Test checkout with empty cart
        with self.assertRaises(ValueError):
            self.marketplace.checkout(self.user_session, "NetBanking")
            
        # Test admin trying to use cart functions
        with self.assertRaises(PermissionError):
            self.marketplace.add_to_cart(self.admin_session, "P1", 1)
        with self.assertRaises(PermissionError):
            self.marketplace.remove_from_cart(self.admin_session, "P1", 1)
        with self.assertRaises(PermissionError):
            self.marketplace.view_cart(self.admin_session)
        with self.assertRaises(PermissionError):
            self.marketplace.checkout(self.admin_session, "UPI")
            
        # Test user trying to use admin functions
        with self.assertRaises(PermissionError):
            self.marketplace.add_product(self.user_session, "P5", "Test", "ELEC", 999.99)
        with self.assertRaises(PermissionError):
            self.marketplace.modify_product(self.user_session, "P1", "Test", "BOOT", 99.99)
        with self.assertRaises(PermissionError):
            self.marketplace.delete_product(self.user_session, "P1")
        with self.assertRaises(PermissionError):
            self.marketplace.add_category(self.user_session, "TEST", "Test Category")
        with self.assertRaises(PermissionError):
            self.marketplace.delete_category(self.user_session, "BOOT")
            
        # Test catalog viewing permissions
        # Both user and admin should be able to view catalog
        user_catalog = self.marketplace.view_catalog(self.user_session)
        admin_catalog = self.marketplace.view_catalog(self.admin_session)
        self.assertEqual(user_catalog, admin_catalog)
        
        # Test invalid payment method
        self.marketplace.add_to_cart(self.user_session, "P1", 1)
        with self.assertRaises(ValueError):
            self.marketplace.checkout(self.user_session, "InvalidMethod")

if __name__ == '__main__':
    unittest.main()
