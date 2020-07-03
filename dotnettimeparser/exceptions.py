class HangingOperatorError(Exception):
    def __init__(self, time_string):
        self.message = f"Cannot parse time_string, Hanging Operator '{time_string}'"
    def __str__(self):
        return self.message

class DoubleOperatorError(Exception):
    def __init__(self, time_string):
        self.message = f"Cannot parse time_string, Duplicate/Double Operator '{time_string}'"
    def __str__(self):
        return self.message

class AbstractManipulationError(Exception):
    def __init__(self, time_string):
        self.message = f"Cannot parse time string, Abstract Time Manipulation {time_string}"
    def __str__(self):
        return self.message

class OperationWithBaseDatetimeError(Exception):
    def __init__(self, time_string):
        self.message = f"Cannot parse time string, Operation on Absolute Timestamps {time_string}"
    def __str__(self):
        return self.message

class NowCharacterError(Exception):
    def __init__(self, time_string):
        self.message = f"Cannot parse time string, 'Now' Character w/ Context {time_string}"
    def __str__(self):
        return self.message

class UnhandledFormatError(Exception):
    def __init__(self, time_string):
        self.message = f"Cannot parse time string, Unhandled Format {time_string}"
    def __str__(self):
        return self.message