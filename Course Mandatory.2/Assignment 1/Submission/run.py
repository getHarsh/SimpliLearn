#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup and run script for Demo Marketplace application.
Handles OS detection, virtual environment setup, and application launching.
"""

import os
import sys
import platform
import subprocess
import venv
import shutil
from pathlib import Path
from typing import Optional, Tuple

class MarketplaceSetup:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.script_dir = Path(__file__).parent.absolute()
        self.venv_dir = self.script_dir / '.venv'
        
        # Detect Python installation
        self.python_cmd = self._detect_python_command()
        self.using_conda = self._is_conda_environment()
        
        # Set platform-specific variables
        if self.os_type == 'windows':
            self.venv_python = self.venv_dir / 'Scripts' / 'python.exe'
            self.venv_pip = self.venv_dir / 'Scripts' / 'pip.exe'
        else:
            self.venv_python = self.venv_dir / 'bin' / 'python'
            self.venv_pip = self.venv_dir / 'bin' / 'pip'
            
    def _detect_python_command(self) -> str:
        """Detect the appropriate Python command to use."""
        # Use sys.executable as the default Python command
        if sys.executable and os.path.exists(sys.executable):
            return sys.executable
            
        # Try python3 first on Unix-like systems
        if self.os_type != 'windows':
            if self._check_command('python3'):
                return 'python3'
        
        # Try python on all systems
        if self._check_command('python'):
            return 'python'
        
        # If we're in a conda environment, use that python
        if self._is_conda_environment():
            conda_python = os.path.join(sys.prefix, 'python')
            if os.path.exists(conda_python):
                return conda_python
            
        # Default to python3 as a last resort
        return 'python3'
    
    def _is_conda_environment(self) -> bool:
        """Check if we're in a conda environment or conda is available."""
        # First check if we're in a conda environment
        if os.path.exists(os.path.join(sys.prefix, 'conda-meta')):
            return True
            
        # Then check if conda is available in PATH
        try:
            subprocess.run(['conda', '--version'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, 
                          check=True)
            return True
        except:
            return False
    
    def _check_command(self, cmd: str) -> bool:
        """Check if a command exists."""
        return shutil.which(cmd) is not None
    
    def _get_pip_command(self) -> Tuple[str, list]:
        """Get the appropriate pip command and any extra args."""
        if self.using_conda:
            return 'conda', ['install', '--yes', '-c', 'conda-forge']
        else:
            if self.os_type == 'windows':
                return str(self.venv_pip), []
            else:
                return str(self.venv_pip), []
    
    def _run_pip(self, args: list) -> bool:
        """Run pip with given arguments."""
        pip_cmd, extra_args = self._get_pip_command()
        cmd = [pip_cmd] + extra_args + args
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def run_command(self, cmd: str, check: bool = True, shell: bool = True) -> bool:
        """Run a command and handle exceptions."""
        try:
            # Run the command with direct output to terminal
            result = subprocess.run(cmd, check=check, shell=shell,
                                  text=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {cmd}")
            print(f"Error details: {str(e)}")
            return False

    def check_python_version(self):
        """Check if Python version is compatible."""
        if sys.version_info < (3, 7):
            print("Error: Python 3.7 or higher is required")
            sys.exit(1)

    def create_virtual_env(self):
        """Create virtual environment if it doesn't exist."""
        if self.using_conda:
            # If we're already in a conda environment, use that
            print("Using existing conda environment")
            return
            
        if not self.venv_dir.exists():
            print("Creating virtual environment...")
            try:
                # Try to create venv with built-in venv module
                venv.create(self.venv_dir, with_pip=True)
                print("Virtual environment created successfully")
                
                # Get the correct pip command
                if self.os_type == 'windows':
                    pip_cmd = str(self.venv_dir / 'Scripts' / 'pip.exe')
                else:
                    pip_cmd = str(self.venv_dir / 'bin' / 'pip')
                
                # Upgrade pip in the new environment
                cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip']
                subprocess.run(cmd, check=True)
                
            except Exception as e:
                print(f"Error creating virtual environment: {str(e)}")
                # Try using virtualenv if venv fails
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', 'virtualenv'], check=True)
                    subprocess.run([sys.executable, '-m', 'virtualenv', str(self.venv_dir)], check=True)
                    print("Virtual environment created using virtualenv")
                except Exception as e:
                    print(f"Failed to create virtual environment: {str(e)}")
                    sys.exit(1)
        else:
            print("Virtual environment already exists")

    def install_requirements(self):
        """Install required packages in virtual environment."""
        requirements_file = self.script_dir / 'requirements.txt'
        if not requirements_file.exists():
            print("Error: requirements.txt not found")
            sys.exit(1)
            
        # Ensure jupyter is installed
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'jupyter'], check=True)
            print("Jupyter installation successful")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install Jupyter: {str(e)}")
            
        print("Installing requirements...")
        if self.using_conda:
            # Read requirements and install with conda
            with open(requirements_file) as f:
                for line in f:
                    package = line.strip()
                    if package and not package.startswith('#'):
                        try:
                            subprocess.run(['conda', 'install', '--yes', '-c', 'conda-forge', package], check=True)
                        except subprocess.CalledProcessError:
                            # Try pip if conda install fails
                            try:
                                subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
                            except subprocess.CalledProcessError as e:
                                print(f"Failed to install {package}: {str(e)}")
                                sys.exit(1)
        else:
            # Use pip for regular virtual environment
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to install requirements: {str(e)}")
                sys.exit(1)

    def run_tests(self, verbose: bool = True):
        """Run the test suite."""
        tests_file = self.script_dir / 'tests.py'
        if tests_file.exists():
            print("\nRunning test suite...\n")
            cmd = [str(self.venv_python), '-m', 'unittest', 'tests.py']
            if verbose:
                cmd.insert(3, '-v')
            try:
                subprocess.run(cmd, check=True)
                print("\nAll tests passed!")
            except subprocess.CalledProcessError:
                print("\nSome tests failed.")
                sys.exit(1)
        else:
            print("Error: tests.py not found")
            sys.exit(1)

    def check_jupyter_installation(self) -> bool:
        """Check if Jupyter is properly installed."""
        try:
            # Check jupyter command
            subprocess.run([self.venv_python, '-m', 'jupyter', '--version'], 
                         check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def verify_notebook_setup(self) -> bool:
        """Verify notebook environment is properly set up."""
        try:
            # Check notebook dependencies
            subprocess.run([self.venv_python, '-c', 
                          'import notebook, jupyter_client, jupyter_core'], 
                         check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def install_jupyter(self) -> bool:
        """Install Jupyter and its dependencies."""
        try:
            print("Installing Jupyter and dependencies...")
            packages = ['jupyter', 'notebook', 'ipykernel']
            for package in packages:
                subprocess.run([self.venv_python, '-m', 'pip', 'install', package], 
                             check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing Jupyter: {str(e)}")
            return False

    def run_jupyter(self):
        """Run the Jupyter Notebook interface with enhanced error handling."""
        notebook_file = self.script_dir / 'car_rental_system.ipynb'
        
        if not notebook_file.exists():
            print("Error: car_rental_system.ipynb not found")
            sys.exit(1)

        # Check Jupyter installation
        if not self.check_jupyter_installation():
            print("Jupyter not found. Attempting to install...")
            if not self.install_jupyter():
                print("Failed to install Jupyter. Falling back to CLI interface...")
                return self.run_cli()

        # Verify notebook setup
        if not self.verify_notebook_setup():
            print("Notebook environment not properly set up.")
            print("Attempting to fix installation...")
            if not self.install_jupyter():
                print("Failed to set up notebook environment. Falling back to CLI interface...")
                return self.run_cli()

        print("\nStarting Jupyter Notebook interface...")
        try:
            # Try to start the notebook server
            cmd = f'"{self.venv_python}" -m jupyter notebook "{notebook_file}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print("Error starting Jupyter Notebook:")
                print(result.stderr)
                print("\nTroubleshooting steps:")
                print("1. Try running: jupyter notebook --debug")
                print("2. Check if port 8888 is available")
                print("3. Verify browser settings")
                print("\nFalling back to CLI interface...")
                return self.run_cli()
                
        except Exception as e:
            print(f"Unexpected error starting Jupyter: {str(e)}")
            print("Falling back to CLI interface...")
            return self.run_cli()

    def run_cli(self):
        """Run the CLI interface."""
        main_file = self.script_dir / 'main.py'
        if main_file.exists():
            print("\nStarting Car Rental System (CLI Interface)...\n")
            cmd = f'"{self.venv_python}" "{main_file}"'
            return self.run_command(cmd)
        else:
            print("Error: main.py not found")
            sys.exit(1)

    def run_application(self):
        """Run the car rental application."""
        # Try Jupyter first
        notebook_file = self.script_dir / 'car_rental_system.ipynb'
        if notebook_file.exists():
            print("\nStarting Car Rental System (Jupyter Interface)...\n")
            return self.run_jupyter()
        
        # Fall back to CLI if notebook not found
        print("\nJupyter Notebook not found, falling back to CLI interface...\n")
        return self.run_cli()

    def clean_environment(self):
        """Clean up the virtual environment."""
        if self.venv_dir.exists():
            print("\nCleaning virtual environment...")
            try:
                shutil.rmtree(self.venv_dir)
                print("Virtual environment cleaned successfully")
            except Exception as e:
                print(f"Error cleaning virtual environment: {str(e)}")
                sys.exit(1)
    
    def setup_and_run(self, run_tests: bool = False, deep_build: bool = False):
        """Main setup and run sequence."""
        print(f"Detected OS: {self.os_type}")
        print(f"Python command: {self.python_cmd}")
        print(f"Environment type: {'conda' if self.using_conda else 'venv'}")
        
        self.check_python_version()
        
        if deep_build and not self.using_conda:
            self.clean_environment()
        
        # Try to run directly first if not doing a deep build
        if not deep_build:
            try:
                if run_tests:
                    print("Attempting to run tests directly...")
                    return self.run_tests()
                else:
                    print("Attempting to run application directly...")
                    return self.run_application()
            except Exception as e:
                print(f"Direct run failed: {str(e)}\nSetting up environment...")
            
        # If direct run fails or doing deep build, try conda or virtualenv
        if self.using_conda:
            print("Using conda environment...")
            self.install_requirements()
        else:
            print("Setting up virtual environment...")
            self.create_virtual_env()
            self.install_requirements()
            
        # Run tests or application
        if run_tests:
            self.run_tests()
        else:
            self.run_application()

if __name__ == "__main__":
    try:
        import argparse
        parser = argparse.ArgumentParser(description='Car Rental System Setup and Run Script')
        parser.add_argument('--test', '-t', action='store_true',
                          help='Run test suite instead of application')
        parser.add_argument('--verbose', '-v', action='store_true',
                          help='Show verbose output in test mode')
        parser.add_argument('--deepbuild', '-d', action='store_true',
                          help='Clean virtual environment and do a fresh build')
        args = parser.parse_args()
        
        setup = MarketplaceSetup()
        setup.setup_and_run(run_tests=args.test, deep_build=args.deepbuild)
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)
