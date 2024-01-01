import logging
import os


class PInfoLogger:
    def __init__(self, log_file1_path, log_file2_path):
        """
        Initializes a new instance of the PInfoLogger class.

        Args:
            log_file1_path (str): The path to the first log file.
            log_file2_path (str): The path to the second log file.
        """
        self.log_file1 = log_file1_path
        self.log_file2 = log_file2_path

        self.clear_logs()  # Clear the logs if they already exist

        # Set up the loggers
        self.logger1 = self._setup_logger('Logger1', self.log_file1)
        self.logger2 = self._setup_logger('Logger2', self.log_file2)

    def _setup_logger(self, logger_name, log_file_path):
        """
        Sets up a logger with a file handler.

        Args:
            logger_name (str): The name of the logger.
            log_file_path (str): The path to the log file.

        Returns:
            logging.Logger: The configured logger.
        """
        logger = logging.getLogger(logger_name)
        handler = logging.FileHandler(log_file_path)
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)  # Log all messages
        return logger

    def clear_logs(self):
        """
        Clears the log files.
        """
        self._remove_if_exists(self.log_file1)
        self._remove_if_exists(self.log_file2)

    def _remove_if_exists(self, file_path):
        """
        Removes a file if it exists.

        Args:
            file_path (str): The path to the file.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"An error occurred while removing {file_path}: {e}")

    def pinfo(self, info, id):
        """
        Logs information and prints it to the console.

        Args:
            info (str): The information to log and print.
            id (int): The ID of the logger to use.

        Notes:
            - If the information contains "Warning" or "Error", it is logged to the first log file and printed to the console.
            - If the ID is 0, the information is logged to the second log file and printed to the console.
            - If the ID is 1, the information is logged to the second log file.
            - If the ID is 2, the information is only printed to the console.
        """
        if "Warning" in info or "Error" in info:
            self.logger1.info(info)  # Log to FTMP1.log
            print(info)  # Also print to console
        else:
            if id == 0:
                self.logger2.info(info)  # Log to FTMP2.log
                print(info)  # Also print to console
            elif id == 1:
                self.logger2.info(info)  # Log to FTMP2.log
            elif id == 2:
                print(info)  # Only print to console
