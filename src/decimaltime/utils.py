
from .constants import *
import datetime as _datetime
import math as _math

def strftime():
    pass

def is_leap(year:int) -> bool:
    special_leaps = (3,7,11,15,20)
    if year <= 20:
        if year in special_leaps:
            return True
        return False
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def leap_years_since(year:int) -> int:
    """
    TODO: support other leap year rules
    1. Straight 4 - Leap years are every four years, starting at 3
    2. 4/100/400 - leap years are 3,7,11,15,20 and every 4 thereafter, except // 100, except // 400
    3. 4/128 - leap years are 3,7,11,15,20 and every four years thereafter, except // 128
    """
    if year <= 20:
        count = 0
        for y in range(1, year):
            if is_leap(y):
                count += 1
        return count
    else:
        y = year - 1
        return (y//4 - y//100 + y//400)

def check_date_fields(year:int, month: int | None, day:int):
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), year)
    if month is not None and not 1 <= month <= 12:
        raise ValueError('month must be in 1..12 or None')
    if not 1 <= day <= 30:
        raise ValueError('day must be in 1..30')
    return year, month, day

def check_time_fields(hour:int, minute:int, second:int, microsecond:int):
    if not 0 <= hour <= 9:
        raise ValueError('hour must be in 0..9', hour)
    if not 0 <= minute <= 99:
        raise ValueError('minute must be in 0..99', minute)
    if not 0 <= second <= 99:
        raise ValueError('second must be in 0..99', second)
    if not 0 <= microsecond <= 999999:
        raise ValueError('microsecond must be in 0..999999', microsecond)
    return hour, minute, second, microsecond

def fromtimestamp(t:float, tz=None):
        udt = _datetime.datetime.fromtimestamp(t, tz)
        fepoch = _datetime.datetime(year=1792, month=9, day=22, tzinfo=tz)
        if udt < fepoch:
            raise ValueError('cannot have a date before the start of the calendar')
        time_since_epoch = udt - fepoch

        #year = round(time_since_epoch.days / 365)
        year = _math.ceil(time_since_epoch.days / 365)
        year = year if year > 0 else 1
        y = year - 1
        days_before_year = (y * 365) + leap_years_since(year)
        days_since_year = time_since_epoch.days - days_before_year
        print(f"({time_since_epoch.days}) y{year}({time_since_epoch.days/365}) {days_before_year} {days_since_year}")
        #print(f"{time_since_epoch.days} - {days_before_year} == {time_since_epoch.days - days_before_year}")


        month = int(days_since_year // 30) + 1 
        # if we are Sansculottides (Complementary)
        if days_since_year >= 366:
            month = None
        print(f"m{month} {days_since_year // 30} and {days_since_year % 30}")

        day = int(days_since_year % 30) + 1

        seconds_since_midnight = time_since_epoch.seconds / 0.864
        hh = int(seconds_since_midnight / 10_000)
        mm = int((seconds_since_midnight / 100) % 100)
        ss = int(seconds_since_midnight % 100)
        d = (seconds_since_midnight - int(seconds_since_midnight)) * 1000

        us = int(d)# * 1_000_000

        return (year, month, day, hh, mm, ss, us, tz)

def cmperror(x, y):
    raise TypeError("can't compare '%s' to '%s'" % (
                    type(x).__name__, type(y).__name__))
