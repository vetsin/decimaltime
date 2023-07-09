import pytest
import decimaltime

def test_a_date():
    # 20 Messidor CCXXXI
    d = decimaltime.Date(year=231, month=10, day=20)
    assert d
    assert d.year == 231
    assert d.month == 10
    assert d.day == 20