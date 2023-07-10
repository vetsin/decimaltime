
from decimaltime import _utils as utils


def test_leap_stuff():
    assert utils.is_leap(1) == False
    assert utils.is_leap(2) == False
    assert utils.is_leap(3) == True
    assert utils.is_leap(4) == False
    assert utils.is_leap(8) == False
    assert utils.is_leap(11) == True

    assert utils.leap_years_since(1) == 0
    assert utils.leap_years_since(10) == 2
    assert utils.leap_years_since(11) == 2
    assert utils.leap_years_since(12) == 3
    assert utils.leap_years_since(21) == 5 # 1812
    assert utils.leap_years_since(32) == 7 # 1823
    assert utils.leap_years_since(63) == 15 # 1854
    assert utils.leap_years_since(163) == 39 # 1954
    assert utils.leap_years_since(167) == 40 # 1959
    assert utils.leap_years_since(175) == 42 # 1967
    assert utils.leap_years_since(202) == 48 # 1993, aka our leap years start to differ

