# def pinfo(str, default=0):
#     if default == 0:
#         print(str)
#     else:
#         # do something
#         pass

# import os

# def pinfo(str, default=0):
#     if default == 0:
#         print(str)
#     elif default == 1:
#         directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))), 'output')
#         filename = "log.txt"
#         filepath = os.path.join(directory, filename)
        
#         with open(filepath, 'a') as file:
#             file.write(str + '\n')
#     elif default == 2:
#         directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))), 'output')
#         filename = "log.txt"
#         filepath = os.path.join(directory, filename)
        
#         if os.path.exists(filepath):
#             os.remove(filepath)
#     else:
#         # Handle other cases here
#         pass

import logging
import os

# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths to the log files, relative to the current script's directory
log_file1 = os.path.join(script_dir, '../command_line/FTMP1.log')
log_file2 = os.path.join(script_dir, '../command_line/FTMP2.log')

# Remove the log files if they exist
def remove_if_exists(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"An error occurred while removing {file_path}: {e}")

remove_if_exists(log_file1)
remove_if_exists(log_file2)

# Set up the loggers
logger1 = logging.getLogger('Logger1')
handler1 = logging.FileHandler(log_file1)
handler1.setFormatter(logging.Formatter('%(message)s'))
logger1.addHandler(handler1)
logger1.setLevel(logging.INFO)  # Log all messages

logger2 = logging.getLogger('Logger2')
handler2 = logging.FileHandler(log_file2)
handler2.setFormatter(logging.Formatter('%(message)s'))
logger2.addHandler(handler2)
logger2.setLevel(logging.INFO)



# Function to log information
def pinfo(info, id):
    if "Warning" in info or "Error" in info:
        #logger1.warning(info)  # Log to FTMP1.log
        logger1.info(info)  # Log to FTMP1.log
        print(info)  # Also print to console
    else:
        if id == 0:
            logger2.info(info)  # Log to FTMP2.log
            print(info)  # Also print to console
        elif id == 1:
            logger2.info(info)  # Log to FTMP2.log
        elif id == 2:
            print(info)  # Only print to console
