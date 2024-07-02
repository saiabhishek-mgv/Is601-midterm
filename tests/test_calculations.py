'''My Calculator Test'''

# Correct the import order by placing standard library imports before third-party library imports,
# adhering to PEP 8 guidelines for import ordering.
from decimal import Decimal
import pytest

# Import Calculation and Calculations classes from the calculator package,
# assuming these are the correct paths following Python's package and module naming conventions.
from calculator.calculation import Calculation
from calculator.calculations import Calculations

# Import arithmetic operation functions (add and subtract) to be tested.
from calculator.operations import add, subtract

# pytest.fixture is a decorator that marks a function as a fixture,
# a setup mechanism used by pytest to initialize a test environment.
# Here, it's used to define a fixture that prepares the test environment for calculations tests.
@pytest.fixture
def setup_calculations():
    """Clear history and add sample calculations for tests."""
    # Clear any existing calculation history to ensure a clean state for each test.
    Calculations.clear_history()
    # Add sample calculations to the history to set up a known state for testing.
    # These calculations represent typical use cases and allow tests to verify that
    # the history functionality is working as expected.
    Calculations.add_calculation(Calculation(Decimal('10'), Decimal('5'), add))
    Calculations.add_calculation(Calculation(Decimal('20'), Decimal('3'), subtract))


def test_get_history(setup_calculations):
    """Test retrieving the entire calculation history."""
    # Retrieve the calculation history.
    history = Calculations.get_history()
    # Assert that the history contains exactly 2 calculations,
    # which matches our setup in the setup_calculations fixture.
    assert len(history) == 2, "History does not contain the expected number of calculations"

def test_clear_history(setup_calculations):
    """Test clearing the entire calculation history."""
    # Clear the calculation history.
    Calculations.clear_history()
    # Assert that the history is empty by checking its length.
    assert len(Calculations.get_history()) == 0, "History was not cleared"

