def is_space_line(str):
    """
    Checks if a line is a space line. Returns 0 if it is, otherwise returns the number of non-space characters.
    """
    n = 0
    len = len(str)
    for i in range(len):
        if str[i].isspace():
            continue
        n += 1
    return n

def get_lines_from_file(inpfile):
    """
    Reads lines from a file and returns a list of non-empty lines. 
    """
    if not os.path.isfile(inpfile):
        print(f"Cannot open file ({inpfile}) in get_lines_from_file")
        return None, 0

    with open(inpfile, 'r') as fp:
        lines = fp.readlines()

    all_line = []
    for line in lines:
        if is_space_line(line) <= 0:
            continue
        all_line.append(line)

    return all_line, len(all_line)

def pinfo_local(fout, format):
    """
    Prints the format string to the console and writes it to the file.
    """
    print(format)
    fout.write(format + '\n')

def write_format(fout, format, key):
    """
    Writes the given format string to the file and prints a message based on the given key.
    """
    len = len(format)
    if len < 1:
        pinfo_local(fout, "Sorry! Format cannot be predicted. Check input file!")
    else:
        fout.write("FORMAT=%s\n" % format)

        if key == -1:
            pinfo_local(fout, "Data type cannot be predicted. Check input file!")
        elif key == -2:
            pinfo_local(fout, "Data type may be Amplitude(F), Check file to confirm!")
        elif key == 0:
            pinfo_local(fout, "Data type is Intensity (I).")
        elif key == 1:
            pinfo_local(fout, "Data type is Amplitude (F).")
        elif key == 2:
            pinfo_local(fout, "Data type are both Amplitude (F) and Intensity (I).")
        elif key == 3:
            pinfo_local(fout, "Data type are anomolous signal.")
        elif key == 10:
            pinfo_local(fout, "Data type for MTZ file can be auto_converted.")
            
    fout.close()

def rid_of_end_space(str):
    i = 0
    n = 0
    length = len(str)

    for i in range(length - 1, -1, -1):
        if str[i].isspace():
            n += 1
        else:
            break

    str = str[:length - n]
    if str[length - n - 1].iscntrl():
        str = str[:length - n - 1]

    return str

def check_category(str):
    category = ""
    item = ""

    match = re.match(r"^_(\w+)\.(\w+)$", str)
    if match and 1 <= len(match.group(1)) <= 150 and 1 <= len(match.group(2)) <= 150:
        category = match.group(1)
        item = match.group(2)
        return 1, category, item
    else:
        return 0, category, item

def strcmp_case(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()

    if s1 == s2:
        return 0
    elif s1 < s2:
        return 1
    else:  # s1 > s2
        return -1

def strncmp_case(s1, s2, n):
    s1 = s1[:n].lower()
    s2 = s2[:n].lower()

    if s1 == s2:
        return 0
    elif s1 < s2:
        return 1
    else:  # s1 > s2
        return -1
    
def strstr_case(s1, s2):
    try:
        return s1.lower().index(s2.lower())
    except ValueError:
        return None

def float_or_zero(value):
    try:
        float(value)
        return float(value)
    except ValueError:
        return 0

def check_format_conditions(n, k, m, mm):
    """
    Checks conditions for different formats and returns a tuple with format name and key.
    """
    if n >= 4:
        if k[1] == 1 and k[2] == 1:
            return "MMCIF", 2  # I&F
        elif k[1] == 1 and k[2] != 1:
            return "MMCIF", 1  # F
        elif k[1] != 1 and k[2] == 1:
            return "MMCIF", 0  # I
        elif k[3] == 1:
            return "MMCIF", 3  # ano
        else:
            return "MMCIF", -1  # nothing
    elif m[1] > 100 and m[2] > 100:
        return "CNS", 2  # I&F
    elif m[1] > 50 and m[2] < 10:
        return "CNS", 1  # F
    elif m[2] > 50 and m[1] < 10:
        return "CNS", 0  # I
    elif mm > 10:
        return "xplor", 1
    else:
        return None, None

def write_format_to_file(fout, format, key):
    """
    Writes the format string and a corresponding message to the file.
    """
    if not format:
        print("Sorry! Format cannot be predicted. Check input file!")
        fout.write("Sorry! Format cannot be predicted. Check input file!\n")
    else:
        fout.write(f"FORMAT={format}\n")

        message_dict = {
            -2: "Data type may be Amplitude(F), Check file to confirm!",
            -1: "Data type cannot be predicted. Check input file!",
            0: "Data type is Intensity (I).",
            1: "Data type is Amplitude (F).",
            2: "Data type are both Amplitude (F) and Intensity (I).",
            3: "Data type are anomolous signal.",
            10: "Data type for MTZ file can be auto_converted.",
        }

        message = message_dict.get(key, "")
        if message:
            print(message)
            fout.write(message + "\n")
    fout.close()

def guess_sf_format(inpfile, format):
    line, nline = get_lines_from_file(inpfile)
    if nline < 2:
        print(f"Error! File ({inpfile}) is wrong! Too few lines ({nline})")
        sys.exit(0)

    outfile = "sf_format_guess.text"

    with open(outfile, "w") as fout:
        for i in range(nline):
            format_name = check_format_conditions(line[i], i, nline)
            if format_name:
                write_format_to_file(fout, format_name)
                format = format_name
                return format
    return None
