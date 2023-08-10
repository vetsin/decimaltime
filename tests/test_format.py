from datetime import datetime
import decimaltime
import pytest
import time, os
from unittest import mock

@pytest.fixture(autouse=True)
def ensure_tz():
    time.tzset()
    yield


def test_days():
    # July 8, 2023
    t = 1688872423.0
    then = decimaltime.Datetime.fromtimestamp(t)

    assert then.strftime("x %A x") == "x Décadi x"
    assert then.strftime("%B") == "Messidor"
    assert then.strftime("%d") == "20"
    assert then.strftime("%H") == "08"
    assert then.strftime("%j") == "320"
    assert then.strftime("%S") == "85"
    assert then.strftime("%w") == "0"
    assert then.strftime("%y") == "231"
    assert then.strftime("%%") == "%"

    assert then.strftime("%d %B %Y") == "20 Messidor CCXXXI"

    assert then.strftime("%y‐%m‐%dT%H:%M:%S−07:00") == ""