#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for the setup script (run.py).
Tests environment detection, creation, and package installation.
"""

import os
import sys
import shutil
import unittest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock
from run import MarketplaceSetup

class TestMarketplaceSetup(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)
        
        # Create a mock requirements.txt
        self.requirements_path = Path(self.temp_dir) / 'requirements.txt'
        with open(self.requirements_path, 'w') as f:
            f.write('pytest\nrequests\n')

    def test_python_command_detection(self):
        """Test Python command detection logic."""
        # Test sys.executable path
        with patch('sys.executable', '/usr/bin/python3'), \
             patch('os.path.exists', return_value=True):
            setup = MarketplaceSetup()
            self.assertEqual(setup.python_cmd, '/usr/bin/python3')

        # Test python3 command
        with patch('sys.executable', None), \
             patch('os.path.exists', return_value=False), \
             patch('platform.system', return_value='Darwin'), \
             patch('shutil.which') as mock_which:
            mock_which.side_effect = lambda x: '/usr/bin/python3' if x == 'python3' else None
            setup = MarketplaceSetup()
            self.assertEqual(setup.python_cmd, 'python3')

        # Test python command
        with patch('sys.executable', None), \
             patch('os.path.exists', return_value=False), \
             patch('platform.system', return_value='Windows'), \
             patch('shutil.which') as mock_which:
            mock_which.side_effect = lambda x: 'C:\\Python39\\python.exe' if x == 'python' else None
            setup = MarketplaceSetup()
            self.assertEqual(setup.python_cmd, 'python')

    def test_conda_detection(self):
        """Test conda environment detection."""
        # Test conda installed via PATH
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            setup = MarketplaceSetup()
            self.assertTrue(setup._is_conda_environment())

        # Test conda environment via conda-meta
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            setup = MarketplaceSetup()
            self.assertTrue(setup._is_conda_environment())

        # Test no conda available
        with patch('subprocess.run') as mock_run, \
             patch('os.path.exists') as mock_exists:
            mock_run.side_effect = FileNotFoundError()
            mock_exists.return_value = False
            setup = MarketplaceSetup()
            self.assertFalse(setup._is_conda_environment())

    def test_virtual_env_creation(self):
        """Test virtual environment creation."""
        with patch('venv.create') as mock_create:
            setup = MarketplaceSetup()
            
            # Test successful creation
            mock_create.return_value = None
            setup.create_virtual_env()
            mock_create.assert_called_once()

            # Test fallback to virtualenv
            mock_create.side_effect = Exception("venv failed")
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                setup.create_virtual_env()
                self.assertEqual(mock_run.call_count, 2)  # pip install virtualenv + virtualenv create

    def test_requirements_installation(self):
        """Test requirements installation logic."""
        setup = MarketplaceSetup()
        
        # Test conda installation
        with patch.object(setup, 'using_conda', True):
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                setup.install_requirements()
                # Should try to install each package with conda
                self.assertGreaterEqual(mock_run.call_count, 2)
                
    def test_clean_environment(self):
        """Test virtual environment cleanup."""
        setup = MarketplaceSetup()
        
        # Test successful cleanup
        with patch('shutil.rmtree') as mock_rmtree, \
             patch.object(Path, 'exists', return_value=True):
            setup.clean_environment()
            mock_rmtree.assert_called_once_with(setup.venv_dir)
        
        # Test cleanup when environment doesn't exist
        with patch('shutil.rmtree') as mock_rmtree, \
             patch.object(Path, 'exists', return_value=False):
            setup.clean_environment()
            mock_rmtree.assert_not_called()
        
        # Test cleanup failure
        with patch('shutil.rmtree') as mock_rmtree, \
             patch.object(Path, 'exists', return_value=True), \
             self.assertRaises(SystemExit):
            mock_rmtree.side_effect = Exception("Cleanup failed")
            setup.clean_environment()
    
    def test_deep_build(self):
        """Test deep build functionality."""
        setup = MarketplaceSetup()
        
        # Test deep build with venv
        with patch.object(setup, 'using_conda', False), \
             patch.object(setup, 'clean_environment') as mock_clean, \
             patch.object(setup, 'create_virtual_env') as mock_create, \
             patch.object(setup, 'install_requirements') as mock_install, \
             patch.object(setup, 'run_tests') as mock_tests:
            setup.setup_and_run(deep_build=True, run_tests=True)
            mock_clean.assert_called_once()
            mock_create.assert_called_once()
            mock_install.assert_called_once()
            mock_tests.assert_called_once()
        
        # Test deep build with conda
        with patch.object(setup, 'using_conda', True), \
             patch.object(setup, 'clean_environment') as mock_clean, \
             patch.object(setup, 'create_virtual_env') as mock_create, \
             patch.object(setup, 'install_requirements') as mock_install, \
             patch.object(setup, 'run_application') as mock_run:
            setup.setup_and_run(deep_build=True)
            mock_clean.assert_not_called()  # Should not clean conda environment
            mock_create.assert_not_called()
            mock_install.assert_called_once()
            mock_run.assert_called_once()

        # Test pip installation
        with patch.object(setup, 'using_conda', False):
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                setup.install_requirements()
                # Should install all requirements at once with pip
                mock_run.assert_called_once()

    def test_error_handling(self):
        """Test error handling in commands."""
        setup = MarketplaceSetup()
        
        # Test command failure
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, 'test_cmd', output=b'test output', stderr=b'test error'
            )
            result = setup.run_command('test_cmd')
            self.assertFalse(result)

    def test_environment_detection(self):
        """Test environment detection logic."""
        with patch('subprocess.check_output') as mock_output:
            # Mock Python version check
            mock_output.return_value = b'Python 3.9.0\n'
            
            setup = MarketplaceSetup()
            
            # Mock run_command to avoid actual execution
            with patch.object(setup, 'run_command', return_value=True):
                # Test venv detection
                with patch.object(sys, 'prefix', str(setup.venv_dir)):
                    setup.setup_and_run()

                # Test conda detection
                with patch.object(setup, 'using_conda', True):
                    setup.setup_and_run()

if __name__ == '__main__':
    unittest.main()
