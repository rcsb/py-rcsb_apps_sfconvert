import os
import logging

# Assuming logger1 and logger2 are already defined
# and are logging to 'FTMP1.log' and 'FTMP2.log', respectively

def get_sf_info(diagfile):
    # Check if diagfile is not empty
    # if os.path.exists(diagfile):
    with open('../command_line/FTMP1.log', 'r') as fr1:
        content = fr1.read().strip()
        if len(content) == 0:
            with open(diagfile, 'w') as fw1:
                fw1.write("No Error/Warning messages were found.\n")

    # Delete sf_information.cif if it exists and open it for writing
    if os.path.exists('../command_line/sf_information.cif'):
        os.remove('../command_line/sf_information.cif')

    with open('../command_line/sf_information.cif', 'w') as fw, open('../command_line/FTMP1.log', 'r') as fr1, open('../command_line/FTMP2.log', 'r') as fr2:
        # Write headers
        fw.write("data_info\n\n")
        fw.write("_sf_convert.error\n;\n")

        # Write content of 'FTMP1.log'
        for line in fr1:
            fw.write(line)
        fw.write(";\n\n")

        # Write another header
        fw.write("_sf_convert.sf_information\n;\n")

        # Write content of 'FTMP2.log'
        for line in fr2:
            fw.write(line)
        fw.write(";\n")

    print("\nThe SF information is written in file = sf_information.cif\n")
