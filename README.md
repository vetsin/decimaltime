# decimaltime

Like datetime, but decimaltime -- aka using the French Revolutionary Calendar in which:

* There are 10 hours a day, 100 minutes an hour, and 100 seconds a minute
* There are 30 days a month
* There are 12 months a year
* The extra 5 (or 6) days are 'Complementary' monthless days

## Usage

```python
import decimaltime

now = decimaltime.Datetime.now()
print(now.strftime("%d %B %Y"))
```

`20 Messidor CCXXXI`