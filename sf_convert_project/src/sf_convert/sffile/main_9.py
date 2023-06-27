import os
import re
import sys

class SF_Guesser:
    def __init__(self, input_file):
        self.input_file = input_file
        self.variables = self.initialize_variables()
        self.format_value = None

    def initialize_variables(self):
        return {
            "category_count": 0, "declare_count": 0, "hkl_count": 0, "space_group_count": 0, 
            "crystal_mosaicity_count": 0, "other_count": 0, "long_line_count": 0, "simple_line_count": 0, 
            "f_meas_count": 0, "i_meas_count": 0, "f_plus_count": 0, "f_minus_count": 0, 
            "i_plus_count": 0, "i_minus_count": 0, "format": ""
        }

    # ... Rest of your code ...

    def determine_format(self, fout):
        format_checkers = [
            (self.check_mmcif_or_cif, "MMCIF"),
            (self.check_declare, "CIF"),
            (self.check_cns_or_xplor, "CNS"),
            (self.check_xplor, "xplor"),
            (self.check_space_group, None),
            (self.check_crystal_mosaicity, "XSCALE"),
            (self.check_other, "DTREK"),
            (self.check_long_line, "HKL"),
            (self.check_other_200, None),
            (self.check_long_line_200, "SAINT")
        ]

        for checker, format_name in format_checkers:
            if checker():
                self.format_value = format_name
                self.write_format_and_key(fout, format_name, self.get_key_for_format())
                break
        else:
            self.write_format_and_key(fout, "", -1)

    # Format checker methods
    def check_mmcif_or_cif(self):
        return self.variables["category_count"] >= 4

    def check_declare(self):
        return self.variables["declare_count"] >= 4

    def check_cns_or_xplor(self):
        return self.variables["hkl_count"] >= 50 and self.variables["f_plus_count"] < 10

    def check_xplor(self):
        return self.variables["hkl_count"] >= 50 and self.variables["f_plus_count"] > 10

    def check_space_group(self):
        return self.variables["space_group_count"] >= 100

    def check_crystal_mosaicity(self):
        return self.variables["crystal_mosaicity_count"] >= 5

    def check_other(self):
        return self.variables["other_count"] >= 6

    def check_long_line(self):
        return self.variables["long_line_count"] > 1 or (self.variables["simple_line_count"] >= 200 and self.variables["simple_line_count"] == self.variables["f_minus_count"])

    def check_other_200(self):
        return self.variables["other_count"] >= 200

    def check_long_line_200(self):
        return self.variables["long_line_count"] >= 200

    # Method to get key for the detected format
    def get_key_for_format(self):
        if self.format_value in ["MMCIF", "CIF"]:
            return self.get_key_for_mmcif_cif()
        elif self.format_value == "CNS":
            return self.get_key_for_cns()
        elif self.format_value == "XSCALE" or self.format_value == "DTREK" or self.format_value == "HKL":
            return 0
        else:
            return -1

    # Methods to get keys for specific formats
    def get_key_for_mmcif_cif(self):
        if self.variables["f_meas_count"] >= 5:
            return 1
        elif self.variables["i_meas_count"] >= 5:
            return 0
        else:
            return -1

    def get_key_for_cns(self):
        if self.variables["f_plus_count"] >= 10:
            return 1
        elif self.variables["i_plus_count"] >= 10:
            return 0
        else:
            return -1

    # Method to write the determined format and its key into file
    def write_format_and_key(self, fout, format_name, key):
        fout.write("The determined format is " + format_name + "\n")
        fout.write("The determined key is " + str(key) + "\n")

if __name__ == "__main__":
    input_file = sys.argv[1]
    sf_guesser = SF_Guesser(input_file)
    with open('output.txt', 'w') as fout:
        sf_guesser.determine_format(fout)
