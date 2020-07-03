import unittest
import time
from datetime import datetime, timedelta
from dateutil import relativedelta
import sys
sys.path.append('..')
from dotnettimeparser import try_parse, exceptions

class TestTryParse(unittest.TestCase):

    def test_hanging_operator_error(self):
        time_string = 'Monday+8h+4d+'
        self.assertRaises(exceptions.HangingOperatorError, try_parse, time_string)
    
    def test_double_operator_error(self):
        time_string = 'Today++9h'
        self.assertRaises(exceptions.DoubleOperatorError, try_parse, time_string)
    
    def test_abstract_manipulation_error(self):
        time_string = '9h'
        self.assertRaises(exceptions.AbstractManipulationError, try_parse, time_string)

    def test_operation_on_absolute_datetime_error(self):
        time_string = 'today+9h-yesterday'
        self.assertRaises(exceptions.OperationWithBaseDatetimeError, try_parse, time_string)
        
    def test_now_special_character_error(self):
        time_string = '+8*'
        self.assertRaises(exceptions.NowCharacterError, try_parse, time_string)

    def test_datetime_parse(self):
        time_string = '1/1/2020'
        self.assertEqual(try_parse(time_string), datetime.strptime(time_string, "%m/%d/%Y"))

    def test_datetime_manipulation_parse(self):
        time_string = '1/1/2020+8d'
        self.assertEqual(try_parse(time_string), datetime.strptime('1/1/2020', "%m/%d/%Y") + timedelta(days = 8))

    def test_interval_relative_to_now(self):
        time_string = '-9h'
        func_return = try_parse(time_string)
        correct_return = datetime.now() - timedelta(hours = 9)
        self.assertAlmostEqual(time.mktime(func_return.timetuple()), time.mktime(correct_return.timetuple()), places = 0)

    def test_interval_relative_to_day_of_month(self):
        time_string = '04-2d+4h'
        correct_return = datetime(year = datetime.now().year, month = datetime.now().month, day = 4) + timedelta(days = -2, hours = 4)
        self.assertEqual(try_parse(time_string), correct_return)

    def test_interval_relative_to_today(self):
        time_string = '12:30pm'
        correct_return = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours = 12, minutes = 30)
        self.assertEqual(try_parse(time_string), correct_return)

if __name__ == '__main__':
    unittest.main()