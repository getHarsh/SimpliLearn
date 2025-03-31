"""
Main entry point for the Car Rental System.

This module provides the command-line interface for the car rental system.
"""

from datetime import datetime
from car_rental import CarRental, RentalMode
from customer import Customer

def display_menu() -> None:
    """Display the main menu."""
    print("\nCar Rental System")
    print("1. View available cars")
    print("2. Rent cars (hourly)")
    print("3. Rent cars (daily)")
    print("4. Rent cars (weekly)")
    print("5. Return cars")
    print("6. Exit")

def format_bill(bill: float, duration) -> str:
    """Format the bill for display.
    
    Args:
        bill: Bill amount
        duration: Rental duration
        
    Returns:
        Formatted bill string
    """
    return f"""
    ===== Rental Bill =====
    Duration: {duration}
    Amount: ₹{bill:.2f}
    ====================
    """

def main() -> None:
    """Main function implementing the command-line interface."""
    rental_system = CarRental(total_cars=100)
    
    # For demo purposes, create a customer
    customer = Customer("C1", "John Doe")
    print(f"Welcome {customer.name}!")
    
    while True:
        try:
            display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                print(rental_system.display_available_cars())
                
            elif choice in ["2", "3", "4"]:
                num_cars = int(input("Enter number of cars to rent: "))
                
                mode = {
                    "2": RentalMode.HOURLY,
                    "3": RentalMode.DAILY,
                    "4": RentalMode.WEEKLY
                }[choice]
                
                record = customer.request_cars(rental_system, num_cars, mode)
                print(f"\nRented {num_cars} cars ({mode.value})")
                print(f"Rental start time: {record.rental_time}")
                
            elif choice == "5":
                if not customer.current_rental:
                    print("No active rentals found")
                    continue
                    
                num_cars = customer.current_rental.num_cars
                bill, duration = customer.return_cars(rental_system, num_cars)
                print(format_bill(bill, duration))
                
            elif choice == "6":
                print("Thank you for using our service!")
                break
                
            else:
                print("Invalid choice! Please try again.")
                
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
