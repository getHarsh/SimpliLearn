"""
Car Rental Module.

This module implements the core functionality for the car rental system.
It handles car rentals, returns, and billing.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class RentalMode(Enum):
    """Rental mode options."""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"

@dataclass
class RentalRate:
    """Rental rates for different modes."""
    hourly: float = 50.0  # Per hour rate
    daily: float = 800.0  # Per day rate
    weekly: float = 4000.0  # Per week rate

@dataclass
class RentalRecord:
    """Record of a car rental."""
    rental_time: datetime
    rental_mode: RentalMode
    num_cars: int
    returned: bool = False
    return_time: Optional[datetime] = None
    bill_amount: Optional[float] = None

class CarRental:
    """Main class for car rental operations."""
    
    def __init__(self, total_cars: int = 100):
        """Initialize car rental system.
        
        Args:
            total_cars: Total number of cars in inventory
        """
        self.total_cars = total_cars
        self.available_cars = total_cars
        self.rental_records: Dict[str, List[RentalRecord]] = {}
        self.rental_rates = RentalRate()
    
    def display_available_cars(self) -> str:
        """Display number of cars available for rent."""
        return f"Available cars: {self.available_cars} out of {self.total_cars}"
    
    def validate_rental_request(self, num_cars: int) -> None:
        """Validate a rental request.
        
        Args:
            num_cars: Number of cars requested
            
        Raises:
            ValueError: If request is invalid
        """
        if num_cars <= 0:
            raise ValueError("Number of cars must be positive")
        if num_cars > self.available_cars:
            raise ValueError(f"Sorry, only {self.available_cars} cars are available")
    
    def rent_cars(self, customer_id: str, num_cars: int, mode: RentalMode) -> RentalRecord:
        """Rent cars to a customer.
        
        Args:
            customer_id: Customer's unique identifier
            num_cars: Number of cars to rent
            mode: Rental mode (hourly/daily/weekly)
            
        Returns:
            RentalRecord for the transaction
            
        Raises:
            ValueError: If rental request is invalid
        """
        self.validate_rental_request(num_cars)
        
        record = RentalRecord(
            rental_time=datetime.now(),
            rental_mode=mode,
            num_cars=num_cars
        )
        
        if customer_id not in self.rental_records:
            self.rental_records[customer_id] = []
        
        self.rental_records[customer_id].append(record)
        self.available_cars -= num_cars
        
        return record
    
    def return_cars(self, customer_id: str, num_cars: int) -> Tuple[float, timedelta]:
        """Process car returns and generate bill.
        
        Args:
            customer_id: Customer's unique identifier
            num_cars: Number of cars being returned
            
        Returns:
            Tuple of (bill_amount, rental_duration)
            
        Raises:
            ValueError: If return request is invalid
        """
        if customer_id not in self.rental_records:
            raise ValueError("No rental record found for this customer")
            
        active_rentals = [r for r in self.rental_records[customer_id] if not r.returned]
        if not active_rentals:
            raise ValueError("No active rentals found for this customer")
            
        # For simplicity, assume we're returning cars from the latest rental
        rental = active_rentals[-1]
        if num_cars != rental.num_cars:
            raise ValueError(f"Please return all {rental.num_cars} cars from this rental")
            
        return_time = datetime.now()
        duration = return_time - rental.rental_time
        
        # Calculate bill based on rental mode
        if rental.rental_mode == RentalMode.HOURLY:
            hours = duration.total_seconds() / 3600
            bill = hours * self.rental_rates.hourly * num_cars
        elif rental.rental_mode == RentalMode.DAILY:
            days = duration.total_seconds() / (24 * 3600)
            bill = days * self.rental_rates.daily * num_cars
        else:  # Weekly
            weeks = duration.total_seconds() / (7 * 24 * 3600)
            bill = weeks * self.rental_rates.weekly * num_cars
            
        rental.returned = True
        rental.return_time = return_time
        rental.bill_amount = bill
        self.available_cars += num_cars
        
        return bill, duration
