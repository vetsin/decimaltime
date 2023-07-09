
import time as _time
import math as _math
import datetime as _datetime

from .constants import *
from .utils import check_date_fields, check_time_fields, is_leap

class Datetime:

    def __new__(cls, year:int, month:int | None=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):
        check_date_fields(year, month, day)
        check_time_fields(hour, minute, second, microsecond)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._fold = fold
        return self

    # Read-only field accessors
    @property
    def year(self):
        """year (1-?)"""
        return self._year

    @property
    def month(self):
        """month (1-12 | None)"""
        return self._month

    @property
    def day(self):
        """year (1-?)"""
        return self._day

    @property
    def hour(self):
        """hour (0-9)"""
        return self._hour

    @property
    def minute(self):
        """minute (0-99)"""
        return self._minute

    @property
    def second(self):
        """second (0-99)"""
        return self._second

    @property
    def microsecond(self):
        """microsecond (0-999999)"""
        return self._microsecond

    @property
    def tzinfo(self):
        """timezone info object"""
        return self._tzinfo

    @property
    def fold(self):
        return self._fold

    def __repr__(self):
        """Convert to formal string, for repr()."""
        L = [self._year, self._month, self._day,  # These are never zero
             self._hour, self._minute, self._second, self._microsecond]
        if L[-1] == 0:
            del L[-1]
        if L[-1] == 0:
            del L[-1]
        s = "%s.%s(%s)" % (self.__class__.__module__,
                           self.__class__.__qualname__,
                           ", ".join(map(str, L)))
        if self._tzinfo is not None:
            assert s[-1:] == ")"
            s = s[:-1] + ", tzinfo=%r" % self._tzinfo + ")"
        if self._fold:
            assert s[-1:] == ")"
            s = s[:-1] + ", fold=1)"
        return s

    def __str__(self):
        "Convert to string, for str()."
        return self.isoformat(sep=' ')

    @classmethod
    def fromtimestamp(cls, t:float, tz=None):
        'datetime from POSIX timestamp (aka from UNIX EPOCH)'
        udt = _datetime.datetime.fromtimestamp(t, tz)
        fepoch = _datetime.datetime(year=1792, month=9, day=22, tzinfo=tz)
        if udt < fepoch:
            raise ValueError('cannot have a date before the start of the calendar')
        time_since_epoch = udt - fepoch

        print(f" uh {time_since_epoch.days}")
        year = round(time_since_epoch.days / 365)
        year = year if year > 0 else 1
        y = year - 1
        # TODO: support other leap year rules
        # 1. Straight 4 - Leap years are every four years, starting at 3
        # 2. 4/100/400 - leap years are 3,7,11,15,20 and every 4 thereafter, except // 100, except // 400
        # 3. 4/128 - leap years are 3,7,11,15,20 and every four years thereafter, except // 128
        special_leaps = (3,7,11,15,20)
        if y in special_leaps:
            days_before_year = y*365 + (special_leaps.index(y)+1)
        else:
            days_before_year = (y*365 + y//4 - y//100 + y//400)
        days_since_year = time_since_epoch.days - days_before_year


        month = int(days_since_year // 30) + 1 
        # if we are Sansculottides (Complementary)
        if 361 <= days_since_year <= 366:
            month = None

        day = int(days_since_year % 30) + 1

        seconds_since_midnight = time_since_epoch.seconds / 0.864
        hh = int(seconds_since_midnight / 10_000)
        mm = int((seconds_since_midnight / 100) % 100)
        ss = int(seconds_since_midnight % 100)
        d = (seconds_since_midnight - int(seconds_since_midnight)) * 1000
        us = int(d)# * 1_000_000

        return cls(year, month, day, hh, mm, ss, us, tz)
        








