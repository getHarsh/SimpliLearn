# Using the Jupyter Notebook Interface

## Overview

The Car Rental System provides an interactive Jupyter Notebook interface (`car_rental_system.ipynb`) that allows you to:
- Run the system step by step
- See immediate results
- Experiment with different scenarios
- View rich output formatting

## Getting Started

1. Start the Notebook:
   ```bash
   ./run.py
   ```
   This will:
   - Set up the Python environment
   - Install required dependencies
   - Launch Jupyter Notebook in your default browser

2. If the notebook doesn't open automatically:
   ```bash
   jupyter notebook car_rental_system.ipynb
   ```

## Using the Notebook

1. **Running Cells**:
   - Click a cell to select it
   - Press `Shift + Enter` to run the cell
   - Wait for the output before proceeding

2. **Cell Types**:
   - **Documentation Cells**: Contain instructions and explanations
   - **Code Cells**: Contain Python code to run
   - **Output Cells**: Show results of code execution

3. **Workflow**:
   a. Run the import cell first
   b. Execute helper function cells
   c. Run the main application cell
   d. Follow the interactive prompts

## Common Issues

1. **Notebook Won't Start**:
   - Check if Jupyter is installed: `pip list | grep jupyter`
   - Verify Python version: `python --version`
   - Try running: `jupyter --version`

2. **Import Errors**:
   - Make sure you've run `./run.py --deepbuild` first
   - Check if all dependencies are installed
   - Restart the kernel if needed

3. **Kernel Issues**:
   - Use "Kernel > Restart" if cells seem stuck
   - Try "Kernel > Restart & Run All" for a fresh start

## Tips & Tricks

1. **Code Modification**:
   - Feel free to modify rental rates in the code
   - Experiment with different customer scenarios
   - Add print statements for debugging

2. **Saving State**:
   - The notebook maintains state between cells
   - Variables persist until kernel restart
   - Use this to track long-running rentals

3. **Rich Output**:
   - Bills are formatted for readability
   - Error messages include helpful context
   - System status is clearly displayed

## Example Workflow

1. Start a rental:
   ```python
   # Initialize system
   rental_system = CarRental(total_cars=5)
   customer = Customer("C1", "John Doe")

   # Rent 2 cars for an hour
   record = customer.request_cars(rental_system, 2, RentalMode.HOURLY)
   print(f"Rented {record.num_cars} cars at {record.rental_time}")
   ```

2. Return cars:
   ```python
   # Return the cars
   bill, duration = customer.return_cars(rental_system, 2)
   print(f"Bill amount: ₹{bill:.2f}")
   print(f"Rental duration: {duration}")
   ```

## Troubleshooting

If you encounter issues:

1. Check the Python environment:
   ```bash
   ./run.py --test
   ```

2. Verify Jupyter installation:
   ```bash
   ./run.py --check-jupyter
   ```

3. Clean and rebuild:
   ```bash
   ./run.py --deepbuild
   ```
