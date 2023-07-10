
import time as _time
import math as _math
import datetime as _datetime

from .constants import *
from .utils import *

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
        return "asdfasdf"

    @classmethod
    def fromtimestamp(cls, t:float, tz: _datetime.tzinfo | None =None) -> 'Datetime':
        'datetime from POSIX timestamp (aka from UNIX EPOCH)'
        return cls(*fromtimestamp(t, tz))

    @classmethod
    def fromdatetime(cls, dt:_datetime.datetime, tz: _datetime.tzinfo | None =None) -> 'Datetime':
        t = _datetime.datetime.timestamp(dt)
        print(t)
        return cls(*fromtimestamp(t, tz))
        
    @classmethod
    def now(cls, tz: str | _datetime.tzinfo | None = None) -> 'Datetime':
        "Construct a datetime from time.time() and optional time zone info."
        t = _time.time()
        if tz == 'UTC':
            return cls.fromtimestamp(t, _datetime.timezone.utc)
        else:
            return cls.fromtimestamp(t, tz)

    @classmethod
    def utcnow(cls) -> 'Datetime':
        "Construct a UTC datetime from time.time()."
        return cls.now(tz='UTC')

    def utcoffset(self) -> int:
        return self._tzinfo.utcoffset(None) if self._tzinfo else None

    def replace(self, year=None, month=None, day=None, hour=None,
                minute=None, second=None, microsecond=None, tzinfo=True,
                *, fold=None):
        """Return a new Datetime with new values for the specified fields."""
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond
        if tzinfo is True:
            tzinfo = self.tzinfo
        if fold is None:
            fold = self.fold
        return type(self)(year, month, day, hour, minute, second,
                          microsecond, tzinfo, fold=fold)

    def to_datetime(self) -> _datetime.datetime:
        pass

    # comparisons
    def __eq__(self, other):
        if isinstance(other, (Datetime, _datetime.datetime)):
            return self._cmp(other, allow_mixed=True) == 0
        return False

    def __le__(self, other):
        if isinstance(other, (Datetime, _datetime.datetime)):
            return self._cmp(other) <= 0
        cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, (Datetime, _datetime.datetime)):
            return self._cmp(other) < 0
        else:
            cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, (Datetime, _datetime.datetime)):
            return self._cmp(other) >= 0
        else:
            cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, (Datetime, _datetime.datetime)):
            return self._cmp(other) > 0
        else:
            cmperror(self, other)

    def _cmp(self, other, allow_mixed=False):
        if isinstance(other, _datetime.datetime):
            other = self.fromdatetime(other)
        mytz = self._tzinfo
        ottz = other._tzinfo
        myoff = otoff = None

        _cmp = lambda x,y: 0 if x == y else 1 if x > y else -1

        if mytz is ottz:
            base_compare = True
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            # Assume that allow_mixed means that we are called from __eq__
            if allow_mixed:
                if myoff != self.replace(fold=not self.fold).utcoffset():
                    return 2
                if otoff != other.replace(fold=not other.fold).utcoffset():
                    return 2
            base_compare = myoff == otoff

        if base_compare:
            return _cmp((self._year, self._month, self._day,
                         self._hour, self._minute, self._second,
                         self._microsecond),
                        (other._year, other._month, other._day,
                         other._hour, other._minute, other._second,
                         other._microsecond))
        if myoff is None or otoff is None:
            if allow_mixed:
                return 2 # arbitrary non-zero value
            else:
                raise TypeError("cannot compare naive and aware datetimes")
        # XXX What follows could be done more efficiently...
        diff = self - other     # this will take offsets into account
        if diff.days < 0:
            return -1
        return diff and 1 or 0