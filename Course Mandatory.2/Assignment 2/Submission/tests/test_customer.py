"""
Test cases for customer module.

This module contains comprehensive tests for the customer functionality.
"""

import pytest
from datetime import datetime
from car_rental import CarRental, RentalMode
from customer import Customer

@pytest.fixture
def rental_system():
    """Create a car rental system for testing."""
    return CarRental(total_cars=10)

@pytest.fixture
def customer():
    """Create a customer for testing."""
    return Customer("C1", "John Doe")

def test_customer_creation(customer):
    """Test customer initialization."""
    assert customer.customer_id == "C1"
    assert customer.name == "John Doe"
    assert customer.current_rental is None

def test_request_cars(rental_system, customer):
    """Test requesting cars."""
    record = customer.request_cars(rental_system, 5, RentalMode.HOURLY)
    
    assert record.num_cars == 5
    assert record.rental_mode == RentalMode.HOURLY
    assert not record.returned
    assert customer.current_rental == record
    assert rental_system.available_cars == 5

def test_return_cars(rental_system, customer):
    """Test returning cars."""
    # First rent some cars
    customer.request_cars(rental_system, 5, RentalMode.HOURLY)
    
    # Return them
    bill, duration = customer.return_cars(rental_system, 5)
    
    assert isinstance(bill, float)
    assert isinstance(duration, datetime)
    assert customer.current_rental is None
    assert rental_system.available_cars == 10

def test_error_handling(rental_system, customer):
    """Test error handling in customer operations."""
    # Try to return cars without rental
    with pytest.raises(ValueError):
        customer.return_cars(rental_system, 5)
    
    # Try to rent more cars than available
    with pytest.raises(ValueError):
        customer.request_cars(rental_system, 11, RentalMode.HOURLY)
    
    # Rent and try to return wrong number
    customer.request_cars(rental_system, 5, RentalMode.HOURLY)
    with pytest.raises(ValueError):
        customer.return_cars(rental_system, 3)  # Wrong number of cars

def test_multiple_customers(rental_system):
    """Test multiple customers using the system."""
    customer1 = Customer("C1", "John Doe")
    customer2 = Customer("C2", "Jane Smith")
    
    # Both customers rent cars
    customer1.request_cars(rental_system, 3, RentalMode.HOURLY)
    customer2.request_cars(rental_system, 4, RentalMode.DAILY)
    
    assert rental_system.available_cars == 3  # 10 - 3 - 4
    
    # First customer returns cars
    customer1.return_cars(rental_system, 3)
    assert rental_system.available_cars == 6  # 3 + 3
    
    # Second customer returns cars
    customer2.return_cars(rental_system, 4)
    assert rental_system.available_cars == 10  # 6 + 4
