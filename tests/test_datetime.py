from datetime import datetime
import decimaltime
import pytest
import time, os
from unittest import mock

@pytest.fixture(autouse=True)
def ensure_tz():
    time.tzset()
    yield


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
    assert then.tzinfo == None


def test_edge_epoch():

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


def test_basic_conversions():
    le = datetime(1971, 1, 1)
    #decimaltime.Datetime.fromdatetime(datetime(2020, 9, 25))
    dt = decimaltime.Datetime.fromdatetime(le)
    assert dt == le
    assert dt.year == 179
    assert dt.month == 4
    assert dt.day == 12


    
def test_basic_comparisons():
    first = decimaltime.Datetime(230, 1, 1)
    second = decimaltime.Datetime(230, 1, 2)
    third = decimaltime.Datetime(230, 1, 3)

    assert first == decimaltime.Datetime(230, 1, 1)
    assert first < second
    assert second > first
    assert third > first
    assert third >= first
    assert first >= first


@mock.patch.dict(os.environ, {"TZ": "UTC"})
def test_tz_things():
    assert os.environ['TZ'] == 'UTC'
    time.tzset()
    assert time.localtime() == time.gmtime(), 'expected local to be utc'

    now = decimaltime.Datetime.now()
    assert now.tzinfo == None

    utcnow = decimaltime.Datetime.utcnow()
    assert now != utcnow, 'should not have compared as one is tz marked'

    assert now == utcnow.replace(tzinfo=False)

    with pytest.raises(TypeError):
        now > utcnow





    