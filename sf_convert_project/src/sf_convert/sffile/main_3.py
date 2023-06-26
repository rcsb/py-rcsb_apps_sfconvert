import os
import re
import sys

def is_space_line(str):
    return len(str) - str.count(' ')

def get_lines_from_file(inpfile):
    if not os.path.isfile(inpfile):
        print(f"Cannot open file ({inpfile}) in get_lines_from_file")
        return None, 0

    with open(inpfile, 'r') as fp:
        lines = [line for line in fp.readlines() if is_space_line(line) > 0]
        
    return lines, len(lines)

def pinfo_local(fout, format):
    print(format)
    fout.write(format + '\n')

def write_format(fout, format, key):
    len = len(format)
    if len < 1:
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
        3: "Data type are anomolous signal.",
        10: "Data type for MTZ file can be auto_converted."
    }
    pinfo_local(fout, keys.get(key, ""))

def rid_of_end_space(str):
    return str.rstrip()

def check_category(str):
    match = re.match(r"^_(\w+)\.(\w+)$", str)
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
        "n1": 0, "n2": 0, "n3": 0, "n4": 0, "n5": 0, "n6": 0, "n7": 0, "n8": 0, "n9": 0, "k1": 0, "k2": 0, "k3": 0, "m1": 0, "m2": 0, "mm1": 0, "nn7": 0, "kk7": 0
    }

def guess_sf_format(inpfile, format):
    line, nline = get_lines_from_file(inpfile)
    if nline < 2:
        print(f"Error! File ({inpfile}) is wrong! Too few lines ({nline})")
        sys.exit(0)

    outfile = "sf_format_guess.text"

    variables = initialize_variables()

    with open(outfile, "w") as fout:
        # your previous code logic goes here with adjustments to use helper functions
        # and refactored code...

    print("Results have been written to " + outfile)

guess_sf_format('input.txt', 'XXX')
