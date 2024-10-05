import sys
import os

# Dynamically add the root project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.logger import logging



def error_message_detail(error, error_detail:sys):
    _, _, exc_tb =  sys.exc_info()   
    # error_detail.exc_info() is a function from the sys module that returns a tuple of three values related to the current exception 
    # The first two values (represented by _ here) are the exception type and the exception instance, which are not used in this case.
    # exc_tb, is the traceback object, which contains information about where the error occurred in the code 
    # (e.g., file name, line number, etc.).

    file_name = os.path.relpath(exc_tb.tb_frame.f_code.co_filename, os.getcwd())
    # exc_tb.tb_frame:the frame in which the exception occurred.
    # f_code is the code that caused the exception.
    # co_filename is an attribute that holds the name of the file where the error occurred.

    error_message = f'Error occured in python script name {file_name} line number {exc_tb.tb_lineno} error_message {str(error)}'
    # str(error)—the string representation of the error object, which contains details about what went wrong.

    return error_message
     

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):

        super().__init__(error_message)
        # This calls the constructor of the parent class (Exception), passing error_message to it. 
        # This ensures that the basic functionality of the Exception class is still present.

        self.error_message = error_message_detail(error_message, error_detail = error_detail)

    def __str__(self):
        return self.error_message



