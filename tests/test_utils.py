
from decimaltime import _utils as utils

from calendar import isleap


def test_is_leap():
    """
    The leap years are French years 3, 7, 11, 15, 20, and every four years thereafter 
    except if the French year is divisible by 100 it must also be divisible by 400 to be a leap year. 
    """
    should_be_true = [3, 7, 11, 15, 20, 24, 28]
    real_year = lambda x: x + 1792
    for i in range(0, 30):
        if i in should_be_true:
            assert utils.is_leap(i) is True, f"Expected {i} to be a leap year"
        else:
            assert utils.is_leap(i) is False, f"Did not expect {i} to be a leap"

    assert utils.is_leap(100) is False
    assert utils.is_leap(400)
    assert utils.is_leap(500) is False
    assert utils.is_leap(800)

    assert isleap(real_year(24)) is True



    assert utils.days_in_year(1) == 365
    assert utils.days_in_year(3) == 366

    assert utils.leap_years_since(1) == 0
    assert utils.leap_years_since(2) == 0
    assert utils.leap_years_since(3) == 1 
    assert utils.leap_years_since(10) == 2
    assert utils.leap_years_since(11) == 3
    assert utils.leap_years_since(12) == 3
    assert utils.leap_years_since(21) == 5 # 1812
    assert utils.leap_years_since(32) == 8 # 1823
    assert utils.leap_years_since(63) == 15 # 1854
    assert utils.leap_years_since(163) == 39 # 1954
    assert utils.leap_years_since(167) == 40 # 1959
    assert utils.leap_years_since(175) == 42 # 1967
    assert utils.leap_years_since(202) == 48 # 1993



