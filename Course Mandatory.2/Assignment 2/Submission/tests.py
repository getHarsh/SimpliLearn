"""
Main test suite for the Car Rental System.

This module integrates all test cases and provides a unified test runner.
"""

import unittest
import pytest
from datetime import datetime, timedelta
from car_rental import CarRental, RentalMode, RentalRecord
from customer import Customer

class TestCarRental(unittest.TestCase):
    """Test cases for the car rental system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rental_system = CarRental(total_cars=10)
        self.customer = Customer("C1", "John Doe")
    
    def test_initial_state(self):
        """Test initial state of rental system."""
        self.assertEqual(self.rental_system.total_cars, 10)
        self.assertEqual(self.rental_system.available_cars, 10)
        self.assertEqual(self.rental_system.rental_records, {})
    
    def test_display_available_cars(self):
        """Test displaying available cars."""
        self.assertEqual(
            self.rental_system.display_available_cars(),
            "Available cars: 10 out of 10"
        )
    
    def test_validate_rental_request(self):
        """Test rental request validation."""
        # Valid request
        self.rental_system.validate_rental_request(5)
        
        # Invalid requests
        with self.assertRaises(ValueError):
            self.rental_system.validate_rental_request(0)  # Zero cars
        with self.assertRaises(ValueError):
            self.rental_system.validate_rental_request(-1)  # Negative cars
        with self.assertRaises(ValueError):
            self.rental_system.validate_rental_request(11)  # More than available
    
    def test_rent_cars(self):
        """Test renting cars."""
        record = self.rental_system.rent_cars("C1", 5, RentalMode.HOURLY)
        
        self.assertIsInstance(record, RentalRecord)
        self.assertEqual(record.num_cars, 5)
        self.assertEqual(record.rental_mode, RentalMode.HOURLY)
        self.assertFalse(record.returned)
        self.assertEqual(self.rental_system.available_cars, 5)
    
    def test_return_cars(self):
        """Test returning cars."""
        # First rent some cars
        self.rental_system.rent_cars("C1", 5, RentalMode.HOURLY)
        
        # Return them after a delay
        bill, duration = self.rental_system.return_cars("C1", 5)
        
        self.assertIsInstance(bill, float)
        self.assertIsInstance(duration, timedelta)
        self.assertEqual(self.rental_system.available_cars, 10)
    
    def test_customer_operations(self):
        """Test customer operations."""
        # Request cars
        record = self.customer.request_cars(self.rental_system, 5, RentalMode.HOURLY)
        self.assertEqual(record.num_cars, 5)
        self.assertEqual(self.rental_system.available_cars, 5)
        
        # Return cars
        bill, duration = self.customer.return_cars(self.rental_system, 5)
        self.assertIsInstance(bill, float)
        self.assertIsInstance(duration, datetime)
        self.assertEqual(self.rental_system.available_cars, 10)
    
    def test_billing_calculation(self):
        """Test billing calculations for different modes."""
        # Test hourly billing
        record = self.rental_system.rent_cars("C1", 1, RentalMode.HOURLY)
        record.rental_time = datetime.now() - timedelta(hours=2)
        bill, _ = self.rental_system.return_cars("C1", 1)
        self.assertTrue(95 <= bill <= 105)  # About 100 (50/hour * 2 hours)
        
        # Test daily billing
        record = self.rental_system.rent_cars("C2", 1, RentalMode.DAILY)
        record.rental_time = datetime.now() - timedelta(days=2)
        bill, _ = self.rental_system.return_cars("C2", 1)
        self.assertTrue(1550 <= bill <= 1650)  # About 1600 (800/day * 2 days)
        
        # Test weekly billing
        record = self.rental_system.rent_cars("C3", 1, RentalMode.WEEKLY)
        record.rental_time = datetime.now() - timedelta(weeks=2)
        bill, _ = self.rental_system.return_cars("C3", 1)
        self.assertTrue(7900 <= bill <= 8100)  # About 8000 (4000/week * 2 weeks)
    
    def test_error_handling(self):
        """Test error handling."""
        # Try to return cars without rental
        with self.assertRaises(ValueError):
            self.rental_system.return_cars("C1", 5)
        
        # Try to rent more cars than available
        with self.assertRaises(ValueError):
            self.customer.request_cars(self.rental_system, 11, RentalMode.HOURLY)
        
        # Rent and try to return wrong number
        self.customer.request_cars(self.rental_system, 5, RentalMode.HOURLY)
        with self.assertRaises(ValueError):
            self.customer.return_cars(self.rental_system, 3)  # Wrong number of cars

if __name__ == '__main__':
    unittest.main()
