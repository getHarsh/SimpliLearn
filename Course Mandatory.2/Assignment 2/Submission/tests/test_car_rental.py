"""
Test cases for car rental module.

This module contains comprehensive tests for the car rental system.
"""

import pytest
from datetime import datetime, timedelta
from car_rental import CarRental, RentalMode, RentalRecord

@pytest.fixture
def rental_system():
    """Create a car rental system for testing."""
    return CarRental(total_cars=10)

def test_initial_state(rental_system):
    """Test initial state of rental system."""
    assert rental_system.total_cars == 10
    assert rental_system.available_cars == 10
    assert rental_system.rental_records == {}

def test_display_available_cars(rental_system):
    """Test displaying available cars."""
    assert rental_system.display_available_cars() == "Available cars: 10 out of 10"

def test_validate_rental_request(rental_system):
    """Test rental request validation."""
    # Valid request
    rental_system.validate_rental_request(5)
    
    # Invalid requests
    with pytest.raises(ValueError):
        rental_system.validate_rental_request(0)  # Zero cars
    with pytest.raises(ValueError):
        rental_system.validate_rental_request(-1)  # Negative cars
    with pytest.raises(ValueError):
        rental_system.validate_rental_request(11)  # More than available

def test_rent_cars(rental_system):
    """Test renting cars."""
    record = rental_system.rent_cars("C1", 5, RentalMode.HOURLY)
    
    assert isinstance(record, RentalRecord)
    assert record.num_cars == 5
    assert record.rental_mode == RentalMode.HOURLY
    assert not record.returned
    assert rental_system.available_cars == 5

def test_return_cars(rental_system):
    """Test returning cars."""
    # First rent some cars
    rental_system.rent_cars("C1", 5, RentalMode.HOURLY)
    
    # Return them after a delay
    bill, duration = rental_system.return_cars("C1", 5)
    
    assert isinstance(bill, float)
    assert isinstance(duration, timedelta)
    assert rental_system.available_cars == 10

def test_multiple_rentals(rental_system):
    """Test multiple rental scenarios."""
    # Multiple rentals for same customer
    rental_system.rent_cars("C1", 2, RentalMode.HOURLY)
    rental_system.rent_cars("C1", 3, RentalMode.DAILY)
    
    assert len(rental_system.rental_records["C1"]) == 2
    assert rental_system.available_cars == 5

def test_error_cases(rental_system):
    """Test error handling."""
    # Try to return cars without rental
    with pytest.raises(ValueError):
        rental_system.return_cars("C1", 5)
    
    # Rent and try to return wrong number
    rental_system.rent_cars("C1", 5, RentalMode.HOURLY)
    with pytest.raises(ValueError):
        rental_system.return_cars("C1", 3)  # Wrong number of cars

def test_billing_calculation(rental_system):
    """Test billing calculations for different modes."""
    # Hourly rental
    record = rental_system.rent_cars("C1", 1, RentalMode.HOURLY)
    record.rental_time = datetime.now() - timedelta(hours=2)
    bill, _ = rental_system.return_cars("C1", 1)
    assert 95 <= bill <= 105  # About 100 (50/hour * 2 hours)
    
    # Daily rental
    record = rental_system.rent_cars("C2", 1, RentalMode.DAILY)
    record.rental_time = datetime.now() - timedelta(days=2)
    bill, _ = rental_system.return_cars("C2", 1)
    assert 1550 <= bill <= 1650  # About 1600 (800/day * 2 days)
    
    # Weekly rental
    record = rental_system.rent_cars("C3", 1, RentalMode.WEEKLY)
    record.rental_time = datetime.now() - timedelta(weeks=2)
    bill, _ = rental_system.return_cars("C3", 1)
    assert 7900 <= bill <= 8100  # About 8000 (4000/week * 2 weeks)
