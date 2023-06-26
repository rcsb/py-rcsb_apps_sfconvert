# import argparse
# from sf_convert_project.src.sf_convert.sffile.sf_file import SFFile
# from sf_convert_project.src.sf_convert.utils.pinfo_file import pinfo
# from sf_convert_project.src.sf_convert.utils.checksffile import CheckSfFile
import os
import sys
import re

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

def guess_sf_format(inpfile, format):


    line, nline = get_lines_from_file(inpfile)
    if nline < 2:
        print(f"Error! File ({inpfile}) is wrong! Too few lines ({nline})")
        #pinfo(f"Error! File ({inpfile}) is wrong! Too few lines ({nline})", pinfo_value)
        sys.exit(0)

    outfile = "sf_format_guess.text"

    n1 = 0  # guess mmCIF
    n2 = 0  # guess CIF
    n3 = 0  # guess CNS (MAIN)
    n4 = 0  # guess TNT
    n5 = 0  # guess XSCALE based on head
    n6 = 0  # guess d*TREK based on head
    n7 = 0  # guess HKL/SCALEPACK based on head or columns
    n8 = 0  # guess shelx
    n9 = 0  # guess saint
    k1 = 0
    k2 = 0
    k3 = 0
    m1 = 0
    m2 = 0
    table = ""
    item = ""
    mm1 = 0
    nn7 = 0
    kk7 = 0
    with open(outfile, "w") as fout:

        for i in range(nline):
            if i == 0 and line[i][0] == 'M' and line[i][1] == 'T' and line[i][2] == 'Z' and line[i][3] == ' ':
                write_format(fout, "MTZ", 10)
                format = "MTZ"
                return

            parts = line[i].split(maxsplit=6)

            # Filling up to six variables with None if no value was found.
            str, s2, s3, s4, s5, s6 = (parts + [None]*6)[:6]

            n = len(parts)

            str = rid_of_end_space(line[i])

            if str[0] == '_' and '.' in str:
                val, table, item = check_category(str)
                if val:
                    if not strcmp_case(table, "_refln"):
                        if not strcmp_case(item, "F_meas_au") or not strcmp_case(item, "F_meas"):
                            k1 = 1
                        elif not strcmp_case(item, "intensity_meas") or not strcmp_case(item, "F_squared_meas"):
                            k2 = 1
                        elif not strcmp_case(item, "pdbx_F_plus") or not strcmp_case(item, "pdbx_I_plus"):
                            k3 = 1
                    if n1 > 200 or k1 or k2 or k3:
                        break
                elif strncmp_case(str, "_refln_", 7) == 0:
                    if strcmp_case(str, "_refln_F_meas"):
                        k1 = 1
                    if strcmp_case(str, "_refln_F_squared_meas"):
                        k2 = 1
                    if n2 > 200 or k1 or k2:
                        break
            elif strncmp_case(str, "INDE", 4) == 0 or (strncmp_case(str, "DECLare", 7) == 0 and strstr_case(line[i] + 20, "RECIproca")):
                if strstr_case(line[i], "FOBS=") or strstr_case(line[i], "FO=") or strstr_case(line[i], " F_") or strstr_case(line[i], "F="):
                    m1 += 1
                if strstr_case(line[i], "IOBS=") or strstr_case(line[i], "IO=") or strstr_case(line[i], "I="):
                    m2 += 1
                if strstr_case(line[i], " FOBS "):
                    mm1 += 1
                if n3 > 300:
                    break
            elif strstr_case(line[i], "FOBS=") or strstr_case(line[i], "FO=") or strstr_case(line[i], "F="):
                n3 += 1
                if m1 > 300:
                    break
            elif strstr_case(line[i], "IOBS=") or strstr_case(line[i], " IO=") or strstr_case(line[i], " I="):
                n3 += 1
                if m2 > 300:
                    break
            elif strncmp_case(str, "HKL", 3) == 0:
                #sscanf(line[i], "%*s%*s%*s%*s%f", &a)
                parts = line[i].split()
                if len(parts) >= 5:
                    a = float(parts[4])
                    if a < 0:
                        m2 += 1
                    if n4 > 200:
                        break
            elif strncmp_case(str, "!SPACE_GROUP_NUMBER=", 20) == 0 or strncmp_case(str, "!UNIT_CELL_CONSTANTS=", 21) == 0 or strncmp_case(str, "!ITEM_H=", 8) == 0 or strncmp_case(str, "!ITEM_K=", 8) == 0 or strncmp_case(str, "!ITEM_L=", 8) == 0:
                if n5 > 4:
                    break
            elif strncmp_case(str, "CRYSTAL_MOSAICITY=", 18) == 0 or strncmp_case(str, "CRYSTAL_SPACEGROUP=", 19) == 0 or strncmp_case(str, "CRYSTAL_UNIT_CELL=", 18) == 0 or strncmp_case(str, "nH", 2) == 0 or strncmp_case(str, "nK", 2) == 0 or strncmp_case(str, "nL", 2) == 0:
                if n6 > 5:
                    break
            elif (i == 0 and str == "1" and n == 1) or (i == 1 and (str == "-985" or str == "-987") and n == 1) or (i == 2 and '.' in str and len(line[i]) > 60 and n == 6):
                if n7 >= 3:
                    break
            elif i > 50 and len(line[i]) == 32:
                #strncpy(s1, line[i] + 12, 8)
                s1 = line[i][12:12+8]
                #s1[8] = '\0'
                s1 = s1[:8]
                if float_or_zero(s1) < 0:
                    m2 += 1
                n8 += 1
            elif i > 50 and len(line[i]) > 150:
                if n9 > 5:
                    break

            if i > 50 and not strchr(line[i], ','):
                if len(line[i]) == 28 or len(line[i]) == 35 or len(line[i]) == 44 or len(line[i]) == 53:
                    nn7 += 1
                if kk7 > 2000:
                    break

        if n1 >= 4:
            if k1 == 1 and k2 == 1:
                write_format(fout, "MMCIF", 2)  # I&F
            elif k1 == 1 and k2 != 1:
                write_format(fout, "MMCIF", 1)  # F
            elif k1 != 1 and k2 == 1:
                write_format(fout, "MMCIF", 0)  # I
            elif k3 == 1:
                write_format(fout, "MMCIF", 3)  # ano
            else:
                write_format(fout, "MMCIF", -1)  # nothing

            format = "MMCIF"
        elif n2 >= 4:
            if k1 == 1 and k2 == 1:
                write_format(fout, "CIF", 2)  # I&F
            elif k1 == 1 and k2 != 1:
                write_format(fout, "CIF", 1)  # F
            elif k1 != 1 and k2 == 1:
                write_format(fout, "CIF", 0)  # I
            else:
                write_format(fout, "CIF", -1)  # nothing

            format = "CIF"
        elif n3 >= 50 and mm1 < 10:
            if m1 > 100 and m2 > 100:
                write_format(fout, "CNS", 2)  # I&F
            elif m1 > 50 and m2 < 10:
                write_format(fout, "CNS", 1)  # F
            elif m2 > 50 and m1 < 10:
                write_format(fout, "CNS", 0)  # I
            else:
                write_format(fout, "CNS", -1)  # nothing

            format = "CNS"
        elif n3 >= 50 and mm1 > 10:
            write_format(fout, "xplor", 1)
            format = "xplor"
        elif n4 >= 100:
            if m2 > 0:
                write_format(fout, "TNT", 0)
            else:
                write_format(fout, "TNT", -2)

            format = "TNT"
        elif n5 >= 5:
            write_format(fout, "XSCALE", 0)
            format = "XSCALE"
        elif n6 >= 6:
            write_format(fout, "DTREK", 0)
            format = "DTREK"
        elif n7 > 1 or (nn7 >= 200 and nn7 == kk7):
            write_format(fout, "HKL", 0)
            format = "HKL"
        elif n8 >= 200:
            if m2 > 0:
                write_format(fout, "SHELX", 0)
            else:
                write_format(fout, "SHELX", -2)
            
            format = "SHELX"
        elif n9 >= 200:
            write_format(fout, "SAINT", 0)
            format = "SAINT"
        else:
            write_format(fout, "", -1)

# print("numbers", n1, n2, n3, n4, n5, n6, n7, n8, n9, nn7, kk7)
def conversion_start(inpfile, outfile, format_inp, format_out, nfile, label, label_items, PDBID, sf_type, pdbfile, VERB, diagfile, iscif, start, end):
    # ============================= converting start  ================================
    if len(outfile) <= 0:
        outfile = f"{inpfile}.{format_out}"
    outfile_tmp = f"{inpfile}_new"

    if nfile > 1 and format_out.lower() == "mmcif":  # multifile conversion
        # convert multiple files to mmcif format (combine)
        multiple_file_conversion(inpfile_all, outfile)
        if len(pdbfile) > 0:
            make_complete_SF(pdbfile, outfile)

    elif label > 0:
        # convert CNS/MTZ to mmCIF for irregular labels or multiple data sets.
        print(f"Manual conversion from {format_inp} to mmCIF format ...")
        if format_inp.lower() in ["cns", "xplor"]:
            cns_multi_sets(inpfile, outfile, label_items, PDBID)
        elif format_inp.lower() == "mtz":
            mtz_man_sets(inpfile, outfile, label_items, PDBID)

        reformat_sfhead(outfile, outfile_tmp)
        if len(pdbfile) > 0:
            make_complete_SF(pdbfile, outfile_tmp)
        cif2cif_sf_all(outfile_tmp, outfile, PDBID, 2)

    elif format_inp.lower() == "mmcif" and format_out.lower() == "mmcif":  # mmcif to mmcif conversion:
        reformat_sfhead(inpfile, outfile_tmp)
        if len(pdbfile) > 0:
            make_complete_SF(pdbfile, outfile_tmp)
        cif2cif_sf_all(outfile_tmp, outfile, PDBID, 2)
        if VERB == 0:
            delete_file(outfile_tmp)

    elif format_inp.lower() != "mmcif" and format_out.lower() == "mmcif":  # non-mmcif to mmcif conversion:
        various_2_cif(inpfile, outfile, format_inp, PDBID, sf_type)
        reformat_sfhead(outfile, outfile_tmp)
        if len(pdbfile) > 0:
            make_complete_SF(pdbfile, outfile_tmp)
        cif2cif_sf_all(outfile_tmp, outfile, PDBID, 2)
        add_audit(outfile)
        if VERB == 0:
            delete_file(outfile_tmp)

    elif format_inp.lower() == "mmcif" and format_out.lower() != "mmcif":  # mmcif to non-mmcif conversion:
        cif_2_various(inpfile, pdbfile, outfile, format_out)

    else:  # non-mmcif to non-mmcif conversion: (bridged by mmcif)
        various_2_cif(inpfile, outfile_tmp, format_inp, PDBID, sf_type)
        cif_2_various(outfile_tmp, pdbfile, outfile, format_out)
        if VERB == 0:
            delete_file(outfile_tmp)

    if format_out.lower() == "mmcif":
        sf_stat(outfile)
    get_sf_info(diagfile)
    if iscif and VERB == 0:
        delete_file(pdbfile)

    print(f"\nOutput File Name = {outfile} : ({format_out} format)\n")
    end = time.time()
    print(f"cpu time {end - start}s\n")



guess_sf_format(f'/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop\ files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/cif_files/1o08.cif', None)



# def main():
#     # Define the input and output formats
#     input_formats = ['MTZ', 'mmCIF', 'CIF', 'CNS', 'Xplor', 'SHELX', 'HKL2000', 
#                      'Scalepack', 'Dtrek', 'TNT', 'SAINT', 'EPMR', 'XSCALE', 
#                      'XPREP', 'XTALVIEW', 'X-GEN', 'XENGEN', 'MULTAN', 'MAIN', 'OTHER']
#     output_formats = ['mmCIF', 'MTZ', 'CNS', 'TNT', 'SHELX', 'EPMR', 'XTALVIEW', 
#                       'HKL2000', 'Dtrek', 'XSCALE', 'MULTAN', 'MAIN', 'OTHER']

#     parser = argparse.ArgumentParser(description='Structure factor conversion')
#     parser.add_argument('-i', type=str, choices=input_formats, help='Input format')
#     parser.add_argument('-o', type=str, choices=output_formats, required=True, help='Output format')
#     parser.add_argument('-sf', type=str, required=True, help='Data file')
#     parser.add_argument('-out', type=str, help='Output file')
#     parser.add_argument('-label', type=str, help='Label name for CNS & MTZ')
#     parser.add_argument('-freer', type=int, help='A free test number in the reflection (SF) file')
#     parser.add_argument('-pdb', type=str, help='A PDB file (add items to the converted SF file if missing)')
#     parser.add_argument('-sf_type', type=str, choices=['I', 'F'], help='I (intensity) or F (amplitude). Only for shelx or TNT')
#     parser.add_argument('-detail', type=str, help='A note to the data set')
#     parser.add_argument('-wave', type=float, help='Wavelength. It overwrites the existing one')
#     parser.add_argument('-diags', type=str, help='Log file containing warning/error message')
#     parser.add_argument('-man', type=str, help='Cells & symmetry (a,b,c,alpha,beta,gamma,p21)')
#     parser.add_argument('-flag', type=int, help='A number for re-setting the Rfree random test set')
#     parser.add_argument('-format', action='store_true', help='Guess the format of the SF file')
#     parser.add_argument('-audit', type=str, help='Update the audit record')
#     parser.add_argument('-valid', type=str, help='Check various SF errors, and correct')
#     parser.add_argument('-rescut', type=float, help='High resolution cutoff for SF_4_validate.cif')
#     parser.add_argument('-sigcut', type=float, help='I/SigI cutoff for SF_4_validate.cif')
#     parser.add_argument('-cif_check', action='store_true', help='Check pdbx dictionary. (local use only)')
#     parser.add_argument('-ext_data', type=str, help='Extract data from SF file')

#     args = parser.parse_args()

#     # Check the input format
#     # if args.i is None:
#     #     if args.format:
#     #         args.i = 'OTHER'
#     #     else:
#     #         parser.error('Input format is not specified')

#     # Check the output format
#     if args.o is None:
#         parser.error('Output format is not specified')
#     else:



# if __name__ == "__main__":
#     main()

# def main():
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('--sffile', type=str, required=True, help='Path to the SF file')
    # parser.add_argument('--pinfo_value', type=int, default=0, help='Value for pinfo')
    # parser.add_argument('--fout_path', type=str, default=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))), 'output'), help='Optional path to the output file for write_sf_4_validation')
    # parser.add_argument('--nblock', type=int, default=0, help='Optional nblock value for write_sf_4_validation')
    # parser.add_argument('--check_all', action='store_true', help='Check all SF blocks if this flag is set')
    # parser.add_argument('--write_validation', action='store_true', help='Write SF for validation if this flag is set')

    # args = parser.parse_args()

    # sffile = SFFile()
    # sffile.readFile(args.sffile)
    # n = sffile.getBlocksCount()


    # pinfo("", 2)
    # pinfo(f"Total number of data blocks = {n} \n\n", args.pinfo_value)

    # calculator = CheckSfFile(sffile, args.fout_path, args.pinfo_value)

    # if args.write_validation:
    #     calculator.write_sf_4_validation(args.nblock)

    # if args.check_all:
    #     check_sf_all_blocks(calculator, n)