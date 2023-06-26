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
            "category_count": 0, "declare_count": 0, "hkl_count": 0, "space_group_count": 0, "crystal_mosaicity_count": 0,
            "other_count": 0, "long_line_count": 0, "simple_line_count": 0, "f_meas_count": 0, "i_meas_count": 0,
            "f_plus_count": 0, "f_minus_count": 0, "i_plus_count": 0, "i_minus_count": 0
        }

    def is_not_empty_line(self, string):
        return len(string) - string.count(' ')

    def get_non_empty_lines(self):
        if not os.path.isfile(self.input_file):
            print(f"Cannot open file ({self.input_file}) in get_non_empty_lines")
            return None, 0

        with open(self.input_file, 'r') as fp:
            lines = [line for line in fp.readlines() if self.is_not_empty_line(line) > 0]

        return lines, len(lines)

    def print_and_write(self, fout, message):
        print(message)
        fout.write(message + '\n')

    def write_format_and_key(self, fout, format, key):
        length = len(format)
        if length < 1:
            self.print_and_write(fout, "Sorry! Format cannot be predicted. Check input file!")
        else:
            fout.write("FORMAT=%s\n" % format)
            self.write_key(fout, key)
        fout.close()

    def write_key(self, fout, key):
        keys = {
            -1: "Data type cannot be predicted. Check input file!",
            -2: "Data type may be Amplitude(F), Check file to confirm!",
            0: "Data type is Intensity (I).",
            1: "Data type is Amplitude (F).",
            2: "Data type are both Amplitude (F) and Intensity (I).",
            3: "Data type are anomalous signal.",
            10: "Data type for MTZ file can be auto_converted."
        }
        self.print_and_write(fout, keys.get(key, ""))

    def remove_end_space(self, string):
        return string.rstrip()

    def check_category(self, string):
        match = re.match(r"^_(\w+)\.(\w+)$", string)
        if match and 1 <= len(match.group(1)) <= 150 and 1 <= len(match.group(2)) <= 150:
            return 1, match.group(1), match.group(2)
        else:
            return 0, "", ""

    def strcmp_case(self, s1, s2):
        return s1.lower() == s2.lower()

    def strncmp_case(self, s1, s2, n):
        return s1[:n].lower() == s2[:n].lower()

    def strstr_case(self, s1, s2):
        try:
            return s1.lower().index(s2.lower())
        except ValueError:
            return None

    def float_or_zero(self, value):
        try:
            return float(value)
        except ValueError:
            return 0

    def guess_sf_format(self):
        lines, num_lines = self.get_non_empty_lines()
        if num_lines < 2:
            print(f"Error! File ({self.input_file}) is wrong! Too few lines ({num_lines})")
            sys.exit(0)

        outfile = "sf_format_guess.text"

        with open(outfile, "w") as fout:
            self.process_lines(lines, fout)
            self.determine_format(fout)

        return self.format_value

    def process_lines(self, lines, fout):
        for i, line in enumerate(lines):
            if i == 0 and line[0:4] == 'MTZ ':
                self.variables["format"] = "MTZ"
                self.write_format_and_key(fout, "MTZ", 10)
                return

            parts = line.split(maxsplit=6)
            s1, s2, s3, s4, s5, s6 = (parts + [None] * 6)[:6]
            n = len(parts)

            s1 = self.remove_end_space(line)

            if self.check_category_line(s1):
                break
            elif self.is_declare_line(s1, line):
                self.handle_declare_line(line)
                if self.variables["category_count"] > 200 or self.variables["f_meas_count"] or self.variables["i_meas_count"] or self.variables["f_plus_count"]:
                    break
            elif self.is_hkl_line(s1):
                self.handle_hkl_line(line)
                if self.variables["hkl_count"] > 200:
                    break
            elif self.is_space_group_line(s1):
                self.handle_space_group_line(line)
                if self.variables["space_group_count"] > 4:
                    break
            elif self.is_crystal_mosaicity_line(s1):
                self.handle_crystal_mosaicity_line(line)
                if self.variables["crystal_mosaicity_count"] > 5:
                    break
            elif self.is_other_line(line):
                self.handle_other_line(line)
                if self.variables["other_count"] >= 200:
                    break
            elif self.is_long_line(line):
                self.handle_long_line(line)
                if self.variables["long_line_count"] > 5:
                    break
            elif self.is_simple_line(line):
                self.handle_simple_line(line)
                if self.variables["simple_line_count"] >= 200 and self.variables["simple_line_count"] == self.variables["f_minus_count"]:
                    break

    def check_category_line(self, s1):
        if s1[0] == '_' and '.' in s1:
            val, table, item = self.check_category(s1)
            if val:
                if not self.strcmp_case(table, "_refln"):
                    if not self.strcmp_case(item, "F_meas_au") or not self.strcmp_case(item, "F_meas"):
                        self.variables["f_meas_count"] = 1
                    elif not self.strcmp_case(item, "intensity_meas") or not self.strcmp_case(item, "F_squared_meas"):
                        self.variables["i_meas_count"] = 1
                    elif not self.strcmp_case(item, "pdbx_F_plus") or not self.strcmp_case(item, "pdbx_I_plus"):
                        self.variables["f_plus_count"] = 1
                if self.variables["category_count"] > 200 or self.variables["f_meas_count"] or self.variables["i_meas_count"] or self.variables["f_plus_count"]:
                    return True
            elif self.strncmp_case(s1, "_refln_", 7) == 0:
                if self.strcmp_case(s1, "_refln_F_meas"):
                    self.variables["f_meas_count"] = 1
                if self.strcmp_case(s1, "_refln_F_squared_meas"):
                    self.variables["i_meas_count"] = 1
                if self.variables["declare_count"] > 200 or self.variables["f_meas_count"] or self.variables["i_meas_count"]:
                    return True
        return False

    def is_declare_line(self, s1, line):
        return (self.strncmp_case(s1, "INDE", 4) == 0 or
                (self.strncmp_case(s1, "DECLare", 7) == 0 and self.strstr_case(line + 20, "RECIproca")))

    def handle_declare_line(self, line):
        if self.strstr_case(line, "FOBS=") or self.strstr_case(line, "FO=") or self.strstr_case(line, " F_") or self.strstr_case(line, "F="):
            self.variables["f_meas_count"] += 1
        if self.strstr_case(line, "IOBS=") or self.strstr_case(line, "IO=") or self.strstr_case(line, "I="):
            self.variables["i_meas_count"] += 1
        if self.strstr_case(line, " FOBS "):
            self.variables["f_plus_count"] += 1
        if self.variables["declare_count"] > 300:
            return True
        return False

    def is_hkl_line(self, s1):
        return self.strncmp_case(s1, "HKL", 3) == 0

    def handle_hkl_line(self, line):
        parts = line.split()
        if len(parts) >= 5:
            a = float(parts[4])
            if a < 0:
                self.variables["i_meas_count"] += 1
            if self.variables["hkl_count"] > 200:
                return True
        return False

    def is_space_group_line(self, s1):
        return (self.strncmp_case(s1, "!SPACE_GROUP_NUMBER=", 20) == 0 or
                self.strncmp_case(s1, "!UNIT_CELL_CONSTANTS=", 21) == 0 or
                self.strncmp_case(s1, "!ITEM_H=", 8) == 0 or
                self.strncmp_case(s1, "!ITEM_K=", 8) == 0 or
                self.strncmp_case(s1, "!ITEM_L=", 8) == 0)

    def handle_space_group_line(self, line):
        if self.variables["space_group_count"] > 4:
            return True
        return False

    def is_crystal_mosaicity_line(self, s1):
        return (self.strncmp_case(s1, "CRYSTAL_MOSAICITY=", 18) == 0 or
                self.strncmp_case(s1, "CRYSTAL_SPACEGROUP=", 19) == 0 or
                self.strncmp_case(s1, "CRYSTAL_UNIT_CELL=", 18) == 0 or
                self.strncmp_case(s1, "nH", 2) == 0 or
                self.strncmp_case(s1, "nK", 2) == 0 or
                self.strncmp_case(s1, "nL", 2) == 0)

    def handle_crystal_mosaicity_line(self, line):
        if self.variables["crystal_mosaicity_count"] > 5:
            return True
        return False

    def is_other_line(self, line):
        return (self.strncmp_case(line, "!SPACE_GROUP_NUMBER=", 20) == 0 or
                self.strncmp_case(line, "!UNIT_CELL_CONSTANTS=", 21) == 0 or
                self.strncmp_case(line, "!ITEM_H=", 8) == 0 or
                self.strncmp_case(line, "!ITEM_K=", 8) == 0 or
                self.strncmp_case(line, "!ITEM_L=", 8) == 0)

    def handle_other_line(self, line):
        if self.variables["other_count"] >= 200:
            return True
        return False

    def is_long_line(self, line):
        return len(line) > 150

    def handle_long_line(self, line):
        if self.variables["long_line_count"] > 5:
            return True
        return False

    def is_simple_line(self, line):
        return (len(line) == 28 or len(line) == 35 or len(line) == 44 or len(line) == 53)

    def handle_simple_line(self, line):
        if len(line) == 28 or len(line) == 35 or len(line) == 44 or len(line) == 53:
            self.variables["simple_line_count"] += 1
        if self.variables["f_minus_count"] > 2000:
            return True
        return False

    def determine_format(self, fout):
        if self.variables["category_count"] >= 4:
            self.handle_mmcif_or_cif(fout, "MMCIF")
        elif self.variables["declare_count"] >= 4:
            self.handle_mmcif_or_cif(fout, "CIF")
        elif self.variables["hkl_count"] >= 50 and self.variables["f_plus_count"] < 10:
            self.handle_cns_or_xplor(fout, "CNS")
        elif self.variables["hkl_count"] >= 50 and self.variables["f_plus_count"] > 10:
            self.write_format_and_key(fout, "xplor", 1)
            self.format_value = "xplor"
        elif self.variables["space_group_count"] >= 100:
            self.handle_tnt(fout)
        elif self.variables["crystal_mosaicity_count"] >= 5:
            self.write_format_and_key(fout, "XSCALE", 0)
            self.format_value = "XSCALE"
        elif self.variables["other_count"] >= 6:
            self.write_format_and_key(fout, "DTREK", 0)
            self.format_value = "DTREK"
        elif self.variables["long_line_count"] > 1 or (self.variables["simple_line_count"] >= 200 and self.variables["simple_line_count"] == self.variables["f_minus_count"]):
            self.write_format_and_key(fout, "HKL", 0)
            self.format_value = "HKL"
        elif self.variables["other_count"] >= 200:
            self.handle_shelx(fout)
        elif self.variables["long_line_count"] >= 200:
            self.write_format_and_key(fout, "SAINT", 0)
            self.format_value = "SAINT"
        else:
            self.write_format_and_key(fout, "", -1)

    def handle_mmcif_or_cif(self, fout, format_name):
        if self.variables["f_meas_count"] == 1 and self.variables["i_meas_count"] == 1:
            self.write_format_and_key(fout, format_name, 2)  # I&F
        elif self.variables["f_meas_count"] == 1 and self.variables["i_meas_count"] != 1:
            self.write_format_and_key(fout, format_name, 1)  # F
        elif self.variables["f_meas_count"] != 1 and self.variables["i_meas_count"] == 1:
            self.write_format_and_key(fout, format_name, 0)  # I
        elif self.variables["f_plus_count"] == 1:
            self.write_format_and_key(fout, format_name, 3)  # ano
        else:
            self.write_format_and_key(fout, format_name, -1)  # nothing

        self.format_value = format_name

    def handle_cns_or_xplor(self, fout, format_name):
        if self.variables["f_meas_count"] > 100 and self.variables["i_meas_count"] > 100:
            self.write_format_and_key(fout, format_name, 2)  # I&F
        elif self.variables["f_meas_count"] > 50 and self.variables["i_meas_count"] < 10:
            self.write_format_and_key(fout, format_name, 1)  # F
        elif self.variables["i_meas_count"] > 50 and self.variables["f_meas_count"] < 10:
            self.write_format_and_key(fout, format_name, 0)  # I
        else:
            self.write_format_and_key(fout, format_name, -1)  # nothing

        self.format_value = format_name

    def handle_tnt(self, fout):
        if self.variables["i_meas_count"] > 0:
            self.write_format_and_key(fout, "TNT", 0)
        else:
            self.write_format_and_key(fout, "TNT", -2)

        self.format_value = "TNT"

    def handle_shelx(self, fout):
        if self.variables["i_meas_count"] > 0:
            self.write_format_and_key(fout, "SHELX", 0)
        else:
            self.write_format_and_key(fout, "SHELX", -2)

        self.format_value = "SHELX"


def main():
    input_file = 'input.txt'
    guesser = SF_Guesser(input_file)
    format_value = guesser.guess_sf_format()
    print(f"Guessed format: {format_value}")


if __name__ == "__main__":
    main()