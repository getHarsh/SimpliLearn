"""
Customer Module.

This module implements the customer functionality for the car rental system.
"""

from datetime import datetime
from typing import Optional, Tuple
from car_rental import CarRental, RentalMode, RentalRecord

class Customer:
    """Customer class for car rental system."""
    
    def __init__(self, customer_id: str, name: str):
        """Initialize customer.
        
        Args:
            customer_id: Unique identifier for the customer
            name: Customer's name
        """
        self.customer_id = customer_id
        self.name = name
        self.current_rental: Optional[RentalRecord] = None
    
    def request_cars(self, rental: CarRental, num_cars: int, mode: RentalMode) -> RentalRecord:
        """Request cars for rental.
        
        Args:
            rental: CarRental system instance
            num_cars: Number of cars to rent
            mode: Rental mode (hourly/daily/weekly)
            
        Returns:
            RentalRecord for the transaction
            
        Raises:
            ValueError: If rental request is invalid
        """
        self.current_rental = rental.rent_cars(self.customer_id, num_cars, mode)
        return self.current_rental
    
    def return_cars(self, rental: CarRental, num_cars: int) -> Tuple[float, datetime]:
        """Return rented cars.
        
        Args:
            rental: CarRental system instance
            num_cars: Number of cars to return
            
        Returns:
            Tuple of (bill_amount, rental_duration)
            
        Raises:
            ValueError: If return request is invalid
        """
        bill, duration = rental.return_cars(self.customer_id, num_cars)
        self.current_rental = None
        return bill, duration
