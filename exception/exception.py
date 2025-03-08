import sys 
import logging 
from utils.logger import logger 

class CustomException(Exception):
    """Custom Exception Class to log and handle errors"""

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = CustomException.get_detailed_error_message(error_message, error_detail)

        # Log the error message
        logger.error(self.error_message)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        """Extract detailed error information including line number and file name."""
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return f"Error in script [{file_name}] at line [{line_number}]: {error_message}"

    def __str__(self):
        return self.error_message

# Example usage
if __name__ == "__main__":
    try:
        x = 1 / 0  # Intentional error
    except Exception as e:
        raise CustomException(str(e), sys)
