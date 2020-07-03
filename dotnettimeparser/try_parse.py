from .exceptions import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
def try_parse(time_string):
    """String to datetime parser. Supports basic datetime (1/1/2020), relative references (Today),
    and intervals/time manipulations (+8h).

    :param time_string: arg1
    :type time_string: str
    
    :raises NowCharacterError: if arg1 contains '*' character along with other characters (Ex. '8*')
    :raises HangingOperatorError: if arg1 is terminated with an operator (Ex. Today+9h+)
    :raises DoubleOperatorError: if arg1 has back to back operators (Ex. Today+-8h)
    :raises AbstractReferenceError: if arg1 is only an interval segment and has no operator (Ex. '9y')
    :raises OperationWithBaseDatetime: if arg1 references an operation on two absolute datetimes (Ex. 1/1/2020 + Today)
    :raises UnhandledFormatError: if all of arg1 or segments of arg1 cannot be parsed

    :rtype: datetime.datetime
    :returns: arg1 parsed to datetime.datetime object
    """

    #Declare allowable operators
    operators = ['+', '-']

    #Define relative datetime and manipulation expressions
    base_keyed_monday = 'datetime.combine(datetime.today() - timedelta(days = (datetime.today().weekday() + 6 - 0) % 7 + 1), datetime.min.time())'
    base_keyed_tuesday = 'datetime.combine(datetime.today() - timedelta(days = (datetime.today().weekday() + 6 - 1) % 7 + 1), datetime.min.time())'
    base_keyed_wednseday = 'datetime.combine(datetime.today() - timedelta(days = (datetime.today().weekday() + 6 - 2) % 7 + 1), datetime.min.time())'
    base_keyed_thursday = 'datetime.combine(datetime.today() - timedelta(days = (datetime.today().weekday() + 6 - 3) % 7 + 1), datetime.min.time())'
    base_keyed_friday = 'datetime.combine(datetime.today() - timedelta(days = (datetime.today().weekday() + 6 - 4) % 7 + 1), datetime.min.time())'
    base_keyed_saturday = 'datetime.combine(datetime.today() - timedelta(days = (datetime.today().weekday() + 6 - 5) % 7 + 1), datetime.min.time())'
    base_keyed_sunday = 'datetime.combine(datetime.today() - timedelta(days = (datetime.today().weekday() + 6 - 6) % 7 + 1), datetime.min.time())'
    base_keyed_today = 'datetime.combine(datetime.today(), datetime.min.time())'
    base_keyed_yesterday = 'datetime.combine(datetime.today() - timedelta(days = 1), datetime.min.time())'
    base_keyed_now = 'datetime.now()'
    manipulation_keyed_hours = 'timedelta(hours = {})'
    manipulation_keyed_seconds = 'timedelta(seconds = {})'
    manipulation_keyed_minutes = 'timedelta(minutes = {})'
    manipulation_keyed_days = 'timedelta(days = {})'
    manipulation_keyed_years = 'relativedelta(years = {})'
    manipulation_keyed_milliseconds = 'timedelta(milliseconds = {})'

    #Declare parsable formats
    base_native_formats = [
        '%m/%d/%y',
        '%m/%d/%Y',
        '%m/%d/%y%H:%M:%S',
        '%m/%d/%Y%H:%M:%S',
        '%m/%d/%y%I:%M:%S%p',
        '%m/%d/%Y%I:%M:%S%p',
        '%m/%d/%y%H:%M',
        '%m/%d/%Y%H:%M',
        '%m/%d/%y%I:%M%p',
        '%m/%d/%Y%I:%M%p',
        '%m-%d-%y',
        '%m-%d-%y%H:%M:%S',
        '%m-%d-%Y%H:%M:%S',
        '%m-%d-%y%I:%M:%S%p',
        '%m-%d-%Y%I:%M:%S%p',
        '%m-%d-%y%H:%M',
        '%m-%d-%Y%H:%M',
        '%m-%d-%y%I:%M%p',
        '%m-%d-%Y%I:%M%p',
        '%x',
        '%x %X',
        '%c',
        '%a,%d%b%Y%H:%M:%S%Z',
        '%a,%d%b%Y%H:%M:%S',
        '%a,%d%b%Y%H:%M:',
        '%a,%d%b%Y',
        '%a,%d%b%y',]

    manipulation_native_formats = [
        '%H:%M',
        '%I:%M%p',
        '%I:%M:%S%p',
        '%I:%M %p',
        '%I:%M:%S %p',
        '%I:%M:%p',
        '%H:%M:%S',
        '%I:%M:%S:%p',]

    base_keyed_formats = {
        't': base_keyed_today,
        'today': base_keyed_today,
        'y': base_keyed_yesterday,
        'yesterday': base_keyed_yesterday,
        'mon': base_keyed_monday,
        'monday': base_keyed_monday,
        'tue': base_keyed_tuesday,
        'tuesday': base_keyed_tuesday,
        'wed': base_keyed_wednseday,
        'wednseday': base_keyed_wednseday,
        'thu': base_keyed_thursday,
        'thursday': base_keyed_thursday,
        'fri': base_keyed_friday,
        'friday': base_keyed_friday,
        'sat': base_keyed_saturday,
        'saturday': base_keyed_saturday,
        'sun': base_keyed_sunday,
        'sunday': base_keyed_sunday,}

    manipulation_keyed_formats = {
        'h': manipulation_keyed_hours,
        'hour': manipulation_keyed_hours,
        'hours': manipulation_keyed_hours,
        'hrs': manipulation_keyed_hours,
        'hr': manipulation_keyed_hours,
        'd': manipulation_keyed_days,
        'day': manipulation_keyed_days,
        'days': manipulation_keyed_days,
        'y': manipulation_keyed_years,
        'year': manipulation_keyed_years,
        'years': manipulation_keyed_years,
        'm': manipulation_keyed_minutes,
        'minute': manipulation_keyed_minutes,
        'minutes': manipulation_keyed_minutes,
        's': manipulation_keyed_seconds,
        'second': manipulation_keyed_seconds,
        'seconds': manipulation_keyed_seconds,
        'ms': manipulation_keyed_milliseconds,
        'millisecond': manipulation_keyed_milliseconds,
        'milliseconds': manipulation_keyed_milliseconds,}

    #Sub-parser for time manipulations
    def manipulation_parser(string):
        for format_ in manipulation_native_formats:
            try:
                manipulation = datetime.strptime(string, format_)
                return f'timedelta(hours = {manipulation.hour}, minutes = {manipulation.minute}, seconds = {manipulation.second})'
            except ValueError:
                pass
            except TypeError: #If segment is parsed to non str type can throw AttributeError on string.split()
                pass
        for format_ in manipulation_keyed_formats.keys():
            try:
                split = string.split(format_)
                if len(split) == 2:
                    if split[1] == '':
                        try:
                            value = float(split[0])
                            return manipulation_keyed_formats[format_].format(value)
                        except ValueError:
                            pass
            except AttributeError: #If segment is parsed to non str type, can throw AttributeError on string.split()
                pass
        return None

    #Sub-parser for base formats
    def base_parser(string):
        for format_ in base_native_formats:
            try:
                datetime.strptime(string, format_)
                return f"datetime.strptime('{string}', '{format_}')"
            except ValueError:
                pass
            except TypeError: #If segment is parsed to non str type can throw AttributeError on string.split()
                pass
        if string in base_keyed_formats.keys():
            return base_keyed_formats[string]
        return None

    #Sub-parser needed for clock format time references, always relative to today (Ex. 12:30PM = Today + 12:30PM)
    def base_timestamp_parser(string):
        for format_ in manipulation_native_formats:
            try:
                manipulation = datetime.strptime(string, format_)
                return base_keyed_today + '+' + f'timedelta(hours = {manipulation.hour}, minutes = {manipulation.minute}, seconds = {manipulation.second})'
            except ValueError:
                pass
            except TypeError:
                pass
        return None

    #Sub-parser needed for day_of_month time references, always relative to current month (Ex. 01 = 'Current Month' 1 2020)
    def day_of_month_parser(string):
        try:
            datetime.strptime(string, '%d')
            month = 'datetime.today().month'
            year = 'datetime.today().year'
            return f"datetime(month = {month}, year = {year}, day = {int(string)})"
        except ValueError:
            pass
        except TypeError:
            pass
        return None

    #Takes segments split on operators and builds expression to be evaluated
    def expression_combiner(time_string_list, time_string_operators, base = None):
        
        def manipulation(segment_list, time):
            for index, segment in enumerate(segment_list):
                manipulation = manipulation_parser(segment)
                if manipulation:
                    time = time + time_string_operators[index] + manipulation
                else:
                    raise UnhandledFormatError(segment)
            return time
        if base:
            time = base
            time = manipulation(time_string_list, time)
        else:
            time = base_parser(time_string_list[0])
            if time:
                time = manipulation(time_string_list[1::], time)
            else:
                raise UnhandledFormatError(time_string_list[0])
        return time
        
    #time_string checks
    def special_character_check(time_string):
        if time_string != '*' and '*' in time_string:
            raise NowCharacterError(time_string)

    def double_operator_check(time_string):
        previous = ''
        for index, operator in enumerate(time_string):
            if operator in operators and previous in operators and index > 0:
                raise DoubleOperatorError(time_string)
            previous = operator

    def hanging_operator_check(time_string):
        if time_string[-1] in operators:
            raise HangingOperatorError(time_string)

    def abstract_manipulation_check(time_string, time_string_list):
        is_manipulation = manipulation_parser(time_string_list[0])
        if is_manipulation is not None and time_string[0] not in operators:
            raise AbstractManipulationError(time_string)

    def absolute_datetime_check(time_string, time_string_list):
        for segment in time_string_list[1::]:
            is_base = base_parser(segment)
            is_manipulation = manipulation_parser(segment)
            if is_base is not None and is_manipulation is None:
                raise OperationWithBaseDatetimeError(time_string)
    
    #Simple format evalulators
    def is_base(time_string):
        base = base_parser(time_string)
        if base:
            return base
    
    def is_base_timestamp(time_string):
        base_timestamp = base_timestamp_parser(time_string)
        if base_timestamp:
            return base_timestamp
    
    def is_day_of_month(time_string):
        day_of_month = day_of_month_parser(time_string)
        if day_of_month:
            return day_of_month
    
    if not isinstance(time_string, str):
        raise TypeError(f"Input must by type 'str', type = '{type(time_string)}'")

    #Prep time_string, forces to match formats in case and spacing
    time_string = time_string.lower()
    time_string = time_string.strip()
    time_string = time_string.replace(' ', '')

    #Try simple formats before breaking apart string
    if time_string == '*' or time_string == '':
        return eval(base_keyed_now)
    try:
        return eval(is_base(time_string))
    except TypeError:
        pass
    try:
        return eval(is_base_timestamp(time_string))
    except TypeError:
        pass
    try:
        return eval(is_day_of_month(time_string))
    except TypeError:
        pass
    
    #Divide time_string into segments split on operators
    time_string_list = [time_string]
    for operator in operators:
        time_string_list = [segment for time_string in time_string_list for segment in time_string.split(operator) if segment]
    time_string_operators = []
    time_string_operators_index = []
    for index, operator in enumerate(time_string):
        if operator in operators:
            time_string_operators.append(operator)
            time_string_operators_index.append(index)
    
    #Run Checks
    special_character_check(time_string)
    hanging_operator_check(time_string)
    double_operator_check(time_string)
    abstract_manipulation_check(time_string, time_string_list)
    absolute_datetime_check(time_string, time_string_list)

    #Attempt to create combined expression to be evaluated
    day_of_month_base = day_of_month_parser(time_string_list[0])
    if 0 in time_string_operators_index: #(-8h) <- Operator at 0 position, base = 'Now'
        base = base_keyed_now
        time = expression_combiner(time_string_list, time_string_operators, base = base)
    elif day_of_month_base: #(01 + 8h) <- Special representation for day of month, base = Day Of Month
        base = day_of_month_base
        time = expression_combiner(time_string_list[1::], time_string_operators, base = base)
    else:
        time = expression_combiner(time_string_list, time_string_operators)
    return eval(time)