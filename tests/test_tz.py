import decimaltime
from datetime import timezone as _timezone
import pytz

def test_tz_deltas():
    now = decimaltime.Datetime.now(pytz.timezone('Europe/Berlin'))
    #now = decimaltime.Datetime.utcnow()
    print(repr(now.tzinfo))
    r = now.tzinfo
    print(dir(r))
    print(r.dst())
    print(repr(r._utcoffset))
    assert r == 1