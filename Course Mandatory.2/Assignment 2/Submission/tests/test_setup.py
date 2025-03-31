"""
Test setup and configuration.

This module contains test configuration and setup fixtures.
"""

import pytest
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def setup_test_env():
    """Set up test environment."""
    # Add any test environment setup here
    yield
    # Add any cleanup code here
