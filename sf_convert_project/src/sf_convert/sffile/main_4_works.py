import os
import re
import sys


def is_space_line(string):
    return len(string) - string.count(' ')


def get_lines_from_file(input_file):
    if not os.path.isfile(input_file):
        print(f"Cannot open file ({input_file}) in get_lines_from_file")
        return None, 0

    with open(input_file, 'r') as fp:
        lines = [line for line in fp.readlines() if is_space_line(line) > 0]

    return lines, len(lines)


def pinfo_local(fout, format):
    print(format)
    fout.write(format + '\n')


def write_format(fout, format, key):
    length = len(format)
    if length < 1:
        pinfo_local(fout, "Sorry! Format cannot be predicted. Check input file!")
    else:
        fout.write("FORMAT=%s\n" % format)
        write_key(fout, key)
    fout.close()


def write_key(fout, key):
    keys = {
        -1: "Data type cannot be predicted. Check input file!",
        -2: "Data type may be Amplitude(F), Check file to confirm!",
        0: "Data type is Intensity (I).",
        1: "Data type is Amplitude (F).",
        2: "Data type are both Amplitude (F) and Intensity (I).",
        3: "Data type are anomalous signal.",
        10: "Data type for MTZ file can be auto_converted."
    }
    pinfo_local(fout, keys.get(key, ""))


def rid_of_end_space(string):
    return string.rstrip()


def check_category(string):
    match = re.match(r"^_(\w+)\.(\w+)$", string)
    if match and 1 <= len(match.group(1)) <= 150 and 1 <= len(match.group(2)) <= 150:
        return 1, match.group(1), match.group(2)
    else:
        return 0, "", ""


def strcmp_case(s1, s2):
    return s1.lower() == s2.lower()


def strncmp_case(s1, s2, n):
    return s1[:n].lower() == s2[:n].lower()


def strstr_case(s1, s2):
    try:
        return s1.lower().index(s2.lower())
    except ValueError:
        return None


def float_or_zero(value):
    try:
        return float(value)
    except ValueError:
        return 0


def initialize_variables():
    return {
        "n1": 0, "n2": 0, "n3": 0, "n4": 0, "n5": 0, "n6": 0, "n7": 0, "n8": 0, "n9": 0, "k1": 0, "k2": 0, "k3": 0, "m1": 0,
        "m2": 0, "mm1": 0, "nn7": 0, "kk7": 0
    }

def guess_sf_format(input_file):
    lines, num_lines = get_lines_from_file(input_file)
    if num_lines < 2:
        print(f"Error! File ({input_file}) is wrong! Too few lines ({num_lines})")
        sys.exit(0)

    outfile = "sf_format_guess.text"

    variables = initialize_variables()

    format_value = None

    with open(outfile, "w") as fout:
        process_lines(lines, variables, fout)
        format_value = determine_format(variables, fout, format_value)

    return format_value

def process_lines(lines, variables, fout):
    for i, line in enumerate(lines):
        if i == 0 and line[0:4] == 'MTZ ':
            variables["format"] = "MTZ"
            write_format(fout, "MTZ", 10)
            return

        parts = line.split(maxsplit=6)
        s1, s2, s3, s4, s5, s6 = (parts + [None] * 6)[:6]
        n = len(parts)

        s1 = rid_of_end_space(line)

        if check_category_line(s1, variables):
            break
        elif is_declare_line(s1, line):
            handle_declare_line(line, variables)
            if variables["n1"] > 200 or variables["k1"] or variables["k2"] or variables["k3"]:
                break
        elif is_hkl_line(s1):
            handle_hkl_line(line, variables)
            if variables["n4"] > 200:
                break
        elif is_space_group_line(s1):
            handle_space_group_line(line, variables)
            if variables["n5"] > 4:
                break
        elif is_crystal_mosaicity_line(s1):
            handle_crystal_mosaicity_line(line, variables)
            if variables["n6"] > 5:
                break
        elif is_other_line(line):
            handle_other_line(line, variables)
            if variables["n8"] >= 200:
                break
        elif is_long_line(line):
            handle_long_line(line, variables)
            if variables["n9"] > 5:
                break
        elif is_simple_line(line):
            handle_simple_line(line, variables)
            if variables["nn7"] >= 200 and variables["nn7"] == variables["kk7"]:
                break


def check_category_line(s1, variables):
    if s1[0] == '_' and '.' in s1:
        val, table, item = check_category(s1)
        if val:
            if not strcmp_case(table, "_refln"):
                if not strcmp_case(item, "F_meas_au") or not strcmp_case(item, "F_meas"):
                    variables["k1"] = 1
                elif not strcmp_case(item, "intensity_meas") or not strcmp_case(item, "F_squared_meas"):
                    variables["k2"] = 1
                elif not strcmp_case(item, "pdbx_F_plus") or not strcmp_case(item, "pdbx_I_plus"):
                    variables["k3"] = 1
            if variables["n1"] > 200 or variables["k1"] or variables["k2"] or variables["k3"]:
                return True
        elif strncmp_case(s1, "_refln_", 7) == 0:
            if strcmp_case(s1, "_refln_F_meas"):
                variables["k1"] = 1
            if strcmp_case(s1, "_refln_F_squared_meas"):
                variables["k2"] = 1
            if variables["n2"] > 200 or variables["k1"] or variables["k2"]:
                return True
    return False


def is_declare_line(s1, line):
    return (strncmp_case(s1, "INDE", 4) == 0 or
            (strncmp_case(s1, "DECLare", 7) == 0 and strstr_case(line + 20, "RECIproca")))


def handle_declare_line(line, variables):
    if strstr_case(line, "FOBS=") or strstr_case(line, "FO=") or strstr_case(line, " F_") or strstr_case(line, "F="):
        variables["m1"] += 1
    if strstr_case(line, "IOBS=") or strstr_case(line, "IO=") or strstr_case(line, "I="):
        variables["m2"] += 1
    if strstr_case(line, " FOBS "):
        variables["mm1"] += 1
    if variables["n3"] > 300:
        return True
    return False


def is_hkl_line(s1):
    return strncmp_case(s1, "HKL", 3) == 0


def handle_hkl_line(line, variables):
    parts = line.split()
    if len(parts) >= 5:
        a = float(parts[4])
        if a < 0:
            variables["m2"] += 1
        if variables["n4"] > 200:
            return True
    return False


def is_space_group_line(s1):
    return (strncmp_case(s1, "!SPACE_GROUP_NUMBER=", 20) == 0 or
            strncmp_case(s1, "!UNIT_CELL_CONSTANTS=", 21) == 0 or
            strncmp_case(s1, "!ITEM_H=", 8) == 0 or
            strncmp_case(s1, "!ITEM_K=", 8) == 0 or
            strncmp_case(s1, "!ITEM_L=", 8) == 0)


def handle_space_group_line(line, variables):
    if variables["n5"] > 4:
        return True
    return False


def is_crystal_mosaicity_line(s1):
    return (strncmp_case(s1, "CRYSTAL_MOSAICITY=", 18) == 0 or
            strncmp_case(s1, "CRYSTAL_SPACEGROUP=", 19) == 0 or
            strncmp_case(s1, "CRYSTAL_UNIT_CELL=", 18) == 0 or
            strncmp_case(s1, "nH", 2) == 0 or
            strncmp_case(s1, "nK", 2) == 0 or
            strncmp_case(s1, "nL", 2) == 0)


def handle_crystal_mosaicity_line(line, variables):
    if variables["n6"] > 5:
        return True
    return False


def is_other_line(line):
    return (strncmp_case(line, "!SPACE_GROUP_NUMBER=", 20) == 0 or
            strncmp_case(line, "!UNIT_CELL_CONSTANTS=", 21) == 0 or
            strncmp_case(line, "!ITEM_H=", 8) == 0 or
            strncmp_case(line, "!ITEM_K=", 8) == 0 or
            strncmp_case(line, "!ITEM_L=", 8) == 0)


def handle_other_line(line, variables):
    if variables["n7"] >= 3:
        return True
    return False


def is_long_line(line):
    return len(line) > 150


def handle_long_line(line, variables):
    if variables["n9"] > 5:
        return True
    return False


def is_simple_line(line):
    return (len(line) == 28 or len(line) == 35 or len(line) == 44 or len(line) == 53)


def handle_simple_line(line, variables):
    if len(line) == 28 or len(line) == 35 or len(line) == 44 or len(line) == 53:
        variables["nn7"] += 1
    if variables["kk7"] > 2000:
        return True
    return False


def determine_format(variables, fout, format_value):
    if variables["n1"] >= 4:
        if variables["k1"] == 1 and variables["k2"] == 1:
            write_format(fout, "MMCIF", 2)  # I&F
        elif variables["k1"] == 1 and variables["k2"] != 1:
            write_format(fout, "MMCIF", 1)  # F
        elif variables["k1"] != 1 and variables["k2"] == 1:
            write_format(fout, "MMCIF", 0)  # I
        elif variables["k3"] == 1:
            write_format(fout, "MMCIF", 3)  # ano
        else:
            write_format(fout, "MMCIF", -1)  # nothing

        format_value = "MMCIF"
    elif variables["n2"] >= 4:
        if variables["k1"] == 1 and variables["k2"] == 1:
            write_format(fout, "CIF", 2)  # I&F
        elif variables["k1"] == 1 and variables["k2"] != 1:
            write_format(fout, "CIF", 1)  # F
        elif variables["k1"] != 1 and variables["k2"] == 1:
            write_format(fout, "CIF", 0)  # I
        else:
            write_format(fout, "CIF", -1)  # nothing

        format_value = "CIF"
    elif variables["n3"] >= 50 and variables["mm1"] < 10:
        if variables["m1"] > 100 and variables["m2"] > 100:
            write_format(fout, "CNS", 2)  # I&F
        elif variables["m1"] > 50 and variables["m2"] < 10:
            write_format(fout, "CNS", 1)  # F
        elif variables["m2"] > 50 and variables["m1"] < 10:
            write_format(fout, "CNS", 0)  # I
        else:
            write_format(fout, "CNS", -1)  # nothing

        format_value = "CNS"
    elif variables["n3"] >= 50 and variables["mm1"] > 10:
        write_format(fout, "xplor", 1)
        format_value = "xplor"
    elif variables["n4"] >= 100:
        if variables["m2"] > 0:
            write_format(fout, "TNT", 0)
        else:
            write_format(fout, "TNT", -2)

        format_value = "TNT"
    elif variables["n5"] >= 5:
        write_format(fout, "XSCALE", 0)
        format_value = "XSCALE"
    elif variables["n6"] >= 6:
        write_format(fout, "DTREK", 0)
        format_value = "DTREK"
    elif variables["n7"] > 1 or (variables["nn7"] >= 200 and variables["nn7"] == variables["kk7"]):
        write_format(fout, "HKL", 0)
        format_value = "HKL"
    elif variables["n8"] >= 200:
        if variables["m2"] > 0:
            write_format(fout, "SHELX", 0)
        else:
            write_format(fout, "SHELX", -2)

        format_value = "SHELX"
    elif variables["n9"] >= 200:
        write_format(fout, "SAINT", 0)
        format_value = "SAINT"
    else:
        write_format(fout, "", -1)

    return format_value


guess_sf_format('input.txt', 'XXX')
