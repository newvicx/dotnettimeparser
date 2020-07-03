Overview
--------

This repository has the source code package for time a string parser that operates similarly to Microsoft .NET’s System.DateTime.TryParse function. A time string can contain a date, time, time zone information, and a relative interval. The time strings are parsed to a datetime.datetime object

The string has two parts, each of which is optional: the date time part and the interval part. The date time part can be "Today" (or "T"), "Yesterday" (or "Y"), a weekday name, or a gregorian date "1/1/2020” (or “1-1-2020”). "Today" and "Yesterday" are the beginning of the specified day at 0 hours local time. A weekday name (either full name or abbreviation) specifies the most current occurrence at 0 hours local time. For example if the current time is Tuesday, specifying a weekday of Wednesday would set the time to the beginning of the day six days ago.

When only the time portion of the date time part is specified, then the input is evaluated as the time offset of the current day. If a reference time is specified, then this would be the time offset relative to the day of the reference time.

Requirements
------------

* Python 3.6+

Installation
------------

### pip install

Install via pip

```posh
pip install dotnettimeparser
```

### Setuptools

Install via setuptools

```posh
python setup.py install
```

Documentation
-------------

### Importing

Import try\_parse function from dotnettimeparser

```python
from dotnettimeparser import try_parse
```

### Parameters and Returns

:param time\_string: arg1

:type time\_string: str

:rtype: datetime.datetime

:returns: arg1 parsed to datetime.datetime object

### Excpetions

* InputError: If time\_string contains special character “\*” (Now) along with other context - **Ex. "1/1/2020 - \*", “8h\*"**
* HangingOperatorError: If time\_string is terminated with an operator -** Ex. “1/1/2020 + 8h +”**
* DoubleOperatorError: If time\_string has back to back operators - **Ex. "Today+-8h”**
* AbstractReferenceError: If time\_string is only an interval segment and has no operator - **Ex. “9y"**
* OperationWithBaseDatetimeError: If time\_string references an operation on two absolute datetimes - **Ex. 1/1/2020 + Today**
* UnhandledFormatError: If all of time\_string or segments of time\_string cannot be parsed

### Usage

try\_parse accepts 1 argument, the string to be parsed

```python
parsed_string = try_parse('1/1/2020 + 2h - 4m')
```

The string is converted to a datetime.datetime object if successfully parsed, otherwise one of the above excpetions will be raised

### How it works

try\_parse attempts to create an expression which can be evaluated using python’s eval() function. This is to create consistency and predictability for the actual conversion from type: str to type: datetime.datetime. The evalulation of the expression is always the last operation in the function return. Therefore, for time\_strings which are relative to time = Now, the datetime object is always equivalent to...

Datetime Representation = Time At Function Call + User Defined Interval + Execution Time

If the execution time is known with precision down to the microsecond, the user can convert the evaluated Datetime Object to the time at function call by subtracting the execution time

The expression to be evaluated is constructed by iteratively building up N number of timedeltas (time manipulations) from a base timestamp. Therefore, the parsing occurs in 2 steps…

* Construct expression for base (Ex. “1/1/2020” = "datetime.strptime(“1/1/2020”, "%m/%d/%Y”)"
* Construct timedeltas (Ex. “+8h” = “+timedelta(hours = 8)”

The user can specify the base, or the base may be implicitly determined. For example, time\_string = “-8h” is equivalent to “8 hours ago from now”. Therefore, the base is implicitly determined to be “datetime.now()"

Additional Notes…

* The base timestamp can be a keyed value (“Today”, “Yesterday”, etc) or it can be a string in a format which can be evaluated by the datetime.strptime() function. Not every combination of keyed dates or formats are included in the package so if you come across a format which you feel should be parsable, add it yourself if you want, or let me know and I will add it to the distro.
* The intervals/time manipulations can also be keyed (“Hours", “Minutes", etc) or can also be a string in a format which can be evaluated by the datetime.strptime() function. Again if you come across something you feel should be in there, add it yourself, or let me know.

Examples
--------

* 
* "\*" (now)
* "-8h" (8 hours ago)
* "01" (first of current month)
* "Monday+8h"
* "Sat, 01 Nov 2008 19:35:00 GMT + 2y+5d-12h+30.55s"
* "Today" (Today at 00:00)
* "T-3d"
* "Yesterday + 03:45:30"