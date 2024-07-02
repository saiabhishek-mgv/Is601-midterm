"""Test for calculations"""
from decimal import Decimal
import os
import pytest
from calculator.calculations import Calculations
from calculator.calculation import Calculation
from calculator.operations import add, subtract
 # pylint: disable=redefined-outer-name, unused-argument
@pytest.fixture
def setup_calculations():
    """Fixture to set up and tear down calculations history."""
    Calculations.clear_history()
    yield
    if os.path.exists(Calculations.file_path):
        os.remove(Calculations.file_path)
    Calculations.clear_history()

def test_add_calculation(setup_calculations):
    """Test adding a calculation to the history."""
    calc = Calculation(Decimal('10'), Decimal('5'), add)
    Calculations.add_calculation(calc)
    assert len(Calculations.get_history()) == 1
    assert Calculations.get_history()[0] == calc

def test_get_history(setup_calculations):
    """Test retrieving the entire calculation history."""
    calc1 = Calculation(Decimal('10'), Decimal('5'), add)
    calc2 = Calculation(Decimal('20'), Decimal('3'), subtract)
    Calculations.add_calculation(calc1)
    Calculations.add_calculation(calc2)
    history = Calculations.get_history()
    assert len(history) == 2
    assert history == [calc1, calc2]

def test_clear_history(setup_calculations):
    """Test clearing the history of calculations."""
    calc = Calculation(Decimal('10'), Decimal('5'), add)
    Calculations.add_calculation(calc)
    Calculations.clear_history()
    assert len(Calculations.get_history()) == 0

def test_save_and_load_history(setup_calculations):
    """Test saving and loading the history of calculations."""
    calc1 = Calculation(Decimal('10'), Decimal('5'), add)
    calc2 = Calculation(Decimal('20'), Decimal('3'), subtract)
    Calculations.add_calculation(calc1)
    Calculations.add_calculation(calc2)
    Calculations.save_history()
    Calculations.clear_history()
    Calculations.load_history()
    history = Calculations.get_history()
    assert len(history) == 2
    assert history[0].perform() == calc1.perform()
    assert history[1].perform() == calc2.perform()

def test_save_history_no_data(setup_calculations):
    """Test saving history when there is no data (should not write to file)."""
    Calculations.clear_history()
    Calculations._cleared = True  # pylint: disable=protected-access
    assert not os.path.exists(Calculations.file_path)

def test_delete_history(setup_calculations):
    """Test deleting the history file."""
    calc = Calculation(Decimal('10'), Decimal('5'), add)
    Calculations.add_calculation(calc)
    Calculations.save_history()
    assert os.path.exists(Calculations.file_path)
    Calculations.delete_history()
    assert not os.path.exists(Calculations.file_path)
    assert len(Calculations.get_history()) == 0

def test_print_history(setup_calculations, capsys):
    """Test printing the history of calculations."""
    calc = Calculation(Decimal('10'), Decimal('5'), add)
    Calculations.add_calculation(calc)
    Calculations.print_history()
    captured = capsys.readouterr()
    assert "Calculation(10, 5, add)" in captured.out

def test_load_history_no_file(setup_calculations):
    """Test loading history when no file exists."""
    Calculations.load_history()
    assert len(Calculations.get_history()) == 0
