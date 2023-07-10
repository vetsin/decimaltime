
class Date:
    """
    date type per the French Republican calendar
    """
    
    def __new__(clz, year:int, month:int=None, day:int=None):
        """immutable"""
        self = object.__new__(clz)
        self._year = year
        self._month = month
        self._day = day
        return self

    # Read-only field accessors
    @property
    def year(self) -> int:
        """year (1-9999)"""
        return self._year

    @property
    def month(self) -> int:
        """month (1-12)"""
        return self._month

    @property
    def day(self) -> int:
        """day (1-31)"""
        return self._day
