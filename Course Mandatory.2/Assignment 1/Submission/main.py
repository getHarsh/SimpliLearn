"""
Main entry point for the Demo Marketplace application.

This module provides the command-line interface for interacting with the
marketplace functionality.
"""

from marketplace import DemoMarketplace

def main():
    """Main function implementing the command-line interface."""
    marketplace = DemoMarketplace()
    current_session = None
    
    print("Welcome to the Demo Marketplace!")
    
    while True:
        if not current_session:
            print("\nPlease login:")
            print("1. User Login")
            print("2. Admin Login")
            print("3. Exit")
            
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == "1" or choice == "2":
                    username = input("Username: ").strip()
                    password = input("Password: ").strip()
                    current_session = marketplace.login(username, password)
                    
                    if current_session:
                        print("Login successful!")
                    else:
                        print("Invalid credentials!")
                        
                elif choice == "3":
                    print("Thank you for visiting Demo Marketplace!")
                    break
                else:
                    print("Invalid choice!")
            except (EOFError, KeyboardInterrupt):
                print("\nProgram interrupted!")
                break
                
        else:
            is_admin = marketplace.is_admin_session(current_session)
            
            if is_admin:
                print("\nAdmin Menu:")
                print("1. View Catalog")
                print("2. Add Product")
                print("3. Modify Product")
                print("4. Delete Product")
                print("5. Add Category")
                print("6. Delete Category")
                print("7. Logout")
                
                try:
                    choice = input("\nEnter your choice (1-7): ").strip()
                    
                    if choice == "1":
                        print(marketplace.view_catalog())
                    elif choice == "2":
                        name = input("Product name: ").strip()
                        category_id = input("Category ID: ").strip().upper()
                        try:
                            price = float(input("Price: ").strip())
                            print(marketplace.add_product(current_session, name, category_id, price))
                        except ValueError:
                            print("Invalid price!")
                    elif choice == "3":
                        product_id = input("Product ID: ").strip().upper()
                        name = input("New name: ").strip()
                        category_id = input("New category ID: ").strip().upper()
                        try:
                            price = float(input("New price: ").strip())
                            print(marketplace.modify_product(current_session, product_id, name, category_id, price))
                        except ValueError:
                            print("Invalid price!")
                    elif choice == "4":
                        product_id = input("Product ID: ").strip().upper()
                        print(marketplace.delete_product(current_session, product_id))
                    elif choice == "5":
                        name = input("Category name: ").strip()
                        print(marketplace.add_category(current_session, name))
                    elif choice == "6":
                        print("\nAvailable Categories:")
                        print("-" * 40)
                        print(f"{'ID':<10} {'Name':<20}")
                        print("-" * 40)
                        for cat_id, category in marketplace.categories.items():
                            print(f"{cat_id:<10} {category.name:<20}")
                        print()
                        
                        category_id = input("Enter Category ID to delete: ").strip().upper()
                        try:
                            print(marketplace.delete_category(current_session, category_id))
                        except ValueError as e:
                            print(f"Error: {str(e)}")
                        except PermissionError as e:
                            print(f"Error: {str(e)}")
                        input("\nPress Enter to continue...")
                    elif choice == "7":
                        marketplace.logout(current_session)
                        current_session = None
                        print("Logged out successfully!")
                    else:
                        print("Invalid choice!")
                except (EOFError, KeyboardInterrupt):
                    print("\nOperation cancelled!")
                except Exception as e:
                    print(f"\nError: {str(e)}")
                    input("\nPress Enter to continue...")
                    
            else:
                print("\nUser Menu:")
                print("1. View Catalog")
                print("2. Add to Cart")
                print("3. Remove from Cart")
                print("4. View Cart")
                print("5. Checkout")
                print("6. Logout")
                
                try:
                    choice = input("\nEnter your choice (1-6): ").strip()
                    
                    if choice == "1":
                        print(marketplace.view_catalog())
                    elif choice == "2":
                        product_id = input("Product ID: ").strip().upper()
                        try:
                            quantity = int(input("Quantity: ").strip())
                            print(marketplace.add_to_cart(current_session, product_id, quantity))
                        except ValueError:
                            print("Invalid quantity!")
                    elif choice == "3":
                        product_id = input("Product ID: ").strip().upper()
                        try:
                            quantity = int(input("Quantity to remove: ").strip())
                            print(marketplace.remove_from_cart(current_session, product_id, quantity))
                        except ValueError:
                            print("Invalid quantity!")
                    elif choice == "4":
                        print(marketplace.view_cart(current_session))
                    elif choice == "5":
                        print("\nPayment Methods:")
                        print("1. UPI")
                        print("2. Net Banking")
                        print("3. PayPal")
                        print("4. Debit Card")
                        
                        payment_choice = input("\nSelect payment method (1-4): ").strip()
                        payment_methods = {
                            "1": "upi",
                            "2": "netbanking",
                            "3": "paypal",
                            "4": "debit"
                        }
                        
                        if payment_choice in payment_methods:
                            print(marketplace.checkout(current_session, payment_methods[payment_choice]))
                            print("Your order is successfully placed!")
                        else:
                            print("Invalid payment method!")
                    elif choice == "6":
                        marketplace.logout(current_session)
                        current_session = None
                        print("Logged out successfully!")
                    else:
                        print("Invalid choice!")
                except (EOFError, KeyboardInterrupt):
                    print("\nOperation cancelled!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Thank you for visiting Demo Marketplace!")
