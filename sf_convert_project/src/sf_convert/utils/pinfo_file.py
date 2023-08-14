import logging
import os

class PInfoLogger:
    def __init__(self, log_file1_path, log_file2_path):
        self.log_file1 = log_file1_path
        self.log_file2 = log_file2_path
        
        # Set up the loggers
        self.logger1 = self._setup_logger('Logger1', self.log_file1)
        self.logger2 = self._setup_logger('Logger2', self.log_file2)
    
    def _setup_logger(self, logger_name, log_file_path):
        logger = logging.getLogger(logger_name)
        handler = logging.FileHandler(log_file_path)
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)  # Log all messages
        return logger
    
    def clear_logs(self):
        self._remove_if_exists(self.log_file1)
        self._remove_if_exists(self.log_file2)

    def _remove_if_exists(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"An error occurred while removing {file_path}: {e}")

    def pinfo(self, info, id):
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

# Example usage:
# logger = PInfoLogger('path_to_log1.log', 'path_to_log2.log')
# logger.pinfo('This is an error', 0)
# logger.clear_logs()
