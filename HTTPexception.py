
class HTTPexception(Exception):
    """ Exception raised for requests to sqlite database """
    
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        return f"{super().__str__()} (Error Code: {self.error_code})"