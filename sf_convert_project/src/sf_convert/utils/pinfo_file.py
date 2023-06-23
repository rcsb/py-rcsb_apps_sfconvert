# def pinfo(str, default=0):
#     if default == 0:
#         print(str)
#     else:
#         # do something
#         pass

import os

def pinfo(str, default=0):
    if default == 0:
        print(str)
    elif default == 1:
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))), 'output')
        filename = "log.txt"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'a') as file:
            file.write(str + '\n')
    elif default == 2:
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))), 'output')
        filename = "log.txt"
        filepath = os.path.join(directory, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
    else:
        # Handle other cases here
        pass
