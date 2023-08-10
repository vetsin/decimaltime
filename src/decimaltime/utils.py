
from typing import Tuple
from .constants import *
import datetime as _datetime
import math as _math
import roman

def wrap_strftime(decimaltime: 'Datetime', format:str):
    ret = ''
    it = iter(format)
    a = next(it, None)
    for b in it:
        if a == '%':
            match b:
                case 'A':
                    # full weekday name
                    ret += to_weekday(decimaltime.month, decimaltime.day).name
                case 'B':
                    # full month name
                    if decimaltime.month is not None:
                        ret += to_month(decimaltime.month).name
                case 'd':
                    # Day of the month as a decimal number [01..30]
                    ret += f"{decimaltime.day:02d}"
                #case 'D':
                #    # probably shouldnt have this one
                #    ret += f"{roman.toRoman(decimaltime.day)}"
                case 'H':
                    # hour [01..10]
                    ret += f"{decimaltime.hour:02d}"
                case 'j':
                    # day of the year [0..366]
                    ret += f"{decimaltime.day_of_year}"
                case 'm':
                    # month [00(Complementary)..12]
                    if decimaltime.month is None:
                        ret += '00'
                    else:
                        ret += f"{decimaltime.month:02d}"
                case 'M':
                    # minute [00..99]
                    ret += f"{decimaltime.minute:02d}"
                case 'S':
                    # second [00..99]
                    ret += f"{decimaltime.second:02d}"
                case 'w':
                    # Weekday as a decimal number [0(Decadi)..9].
                    ret += f"{decimaltime.day % 10}"
                case 'y':
                    # year as decimal
                    ret += f"{decimaltime.year}"
                case 'Y':
                    # year as roman numeral
                    ret += f"{roman.toRoman(decimaltime.year)}"
                #case 'z':
                #    pass
                case '%':
                    ret += '%'
                case _:
                    raise ValueError(f"Unknown format '{b}'")
                

            b = next(it, None)
        else:
            ret += a
        a = b
    if a:
        ret += a
    return ret

def to_month(month:int) -> Month:
    return Month(month)

def to_weekday(month:int | None, day:int) -> Weekday | ComplementaryWeekday:
    if month is None:
        return ComplementaryWeekday(day)
    return Weekday(_math.fmod(day, 10))

def is_leap_four(year:int) -> bool:
    if year <= 20:
        if year in SPECIAL_LEAPS:
            return True
        return False
    return year % 4 == 0

def is_leap_standard(year:int) -> bool:
    """The 4/100/400 rule"""
    if year <= 20:
        if year in SPECIAL_LEAPS:
            return True
        return False
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def is_leap_128(year:int) -> bool:
    if year <= 20:
        if year in SPECIAL_LEAPS:
            return True
        return False
    return year % 4 == 0 and year % 128 != 0

def is_leap(year:int, mode:LeapYearRule=LeapYearRule.Romme) -> bool:
    """
    1. Straight 4 - Leap years are every four years, starting at 3
    2. 4/100/400 - leap years are 3,7,11,15,20 and every 4 thereafter, except // 100, except // 400
    3. 4/128 - leap years are 3,7,11,15,20 and every four years thereafter, except // 128
    """
    match mode:
        case LeapYearRule.Romme:
            return is_leap_standard(year)
        case LeapYearRule.Goucher:
            return is_leap_128(year)
        case LeapYearRule.Straight4:
            return is_leap_four(year)

def leap_years_since(year:int) -> int:
    return sum([is_leap(y) for y in range(1, year+1)])

def days_in_year(year:int) -> int:
    return 366 if is_leap(year) else 365

def days_before_year(year:int) -> int:
    assert year > 0 and year < 10000, 'expected 0 < year < 10000'
    return sum([days_in_year(y) for y in range(1, year)])

def year_from_days(days:int) -> Tuple[int, int]:
    """
    :returns: (year, remainder_days)
    """
    return _year_from_days(days)

def _year_from_days(days, cumdays=0, year=0):
    year += 1
    days_this_year = days_in_year(year)
    if (cumdays + days_this_year) > days:
        return (year, days-cumdays)
    cumdays += days_this_year
    return _year_from_days(days, cumdays, year)

def check_date_fields(year:int, month: int | None, day:int):
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError(f"year '{year}' must be in {MINYEAR}..{MAXYEAR}", year)
    if month is not None and not 1 <= month <= 12:
        raise ValueError(f"month '{month}' must be in 1..12 or None")
    if not 1 <= day <= 30:
        raise ValueError(f"day '{day}' must be in 1..30")
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
        frac, t = _math.modf(t)
        us = round(frac * 1e6)
        if us >= 1000000:
            t += 1
            us -= 1000000
        elif us < 0:
            t -= 1
            us += 1000000

        udt = _datetime.datetime.fromtimestamp(t, tz)
        fepoch = _datetime.datetime(year=1792, month=9, day=22, tzinfo=tz)
        if udt < fepoch:
            raise ValueError('cannot have a date before the start of the calendar')
        time_since_epoch = udt - fepoch

        year, days = year_from_days(time_since_epoch.days)


        if days < 360:
            month = int(days // 30) + 1
        else:
            month = None

        if month is None:
            day = (days - 360)
        else:
            day = days - ((month-1) * 30)
        day += 1
        print(f"{days!r} year={year!r}, month={month!r}, day={day!r}")

        seconds_since_midnight = time_since_epoch.seconds / 0.864
        hh = int(seconds_since_midnight / 10_000)
        mm = int((seconds_since_midnight / 100) % 100)
        ss = int(seconds_since_midnight % 100)

        return (year, month, day, hh, mm, ss, us, tz)

def cmperror(x, y):
    raise TypeError("can't compare '%s' to '%s'" % (
                    type(x).__name__, type(y).__name__))
