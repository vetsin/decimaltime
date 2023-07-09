from datetime import datetime
import decimaltime
import pytest

def test_from_timestamp():
    # July 8, 2023
    t = 1688872423.0
    then = decimaltime.Datetime.fromtimestamp(t)
    assert then
    assert then.year == 231
    assert then.month == 10
    assert then.day == 20
    assert then.hour == 8
    assert then.minute == 42
    assert then.second == 85

def test_edge_cases():
    datetime(1971, 1, 1, 0, 0, 0)

    t = datetime.timestamp(datetime(year=1792, month=9, day=22))
    then = decimaltime.Datetime.fromtimestamp(t)
    assert then.year == 1
    assert then.month == 1
    assert then.day == 1

    t = datetime.timestamp(datetime(year=1792, month=9, day=23))
    then = decimaltime.Datetime.fromtimestamp(t)
    assert then.day == 2 

    t = datetime.timestamp(datetime(year=1792, month=9, day=21))
    with pytest.raises(ValueError):
        then = decimaltime.Datetime.fromtimestamp(t)
    