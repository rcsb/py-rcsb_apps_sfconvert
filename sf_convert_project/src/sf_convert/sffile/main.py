import argparse
from sf_convert_project.src.sf_convert.sffile.sf_file import SFFile
from sf_convert_project.src.sf_convert.utils.pinfo_file import pinfo
from sf_convert_project.src.sf_convert.utils.checksffile import CheckSfFile
import os
import sys
import re

def main():
    # Define the input and output formats
    input_formats = ['MTZ', 'mmCIF', 'CIF', 'CNS', 'Xplor', 'SHELX', 'HKL2000', 
                     'Scalepack', 'Dtrek', 'TNT', 'SAINT', 'EPMR', 'XSCALE', 
                     'XPREP', 'XTALVIEW', 'X-GEN', 'XENGEN', 'MULTAN', 'MAIN', 'OTHER']
    output_formats = ['mmCIF', 'MTZ', 'CNS', 'TNT', 'SHELX', 'EPMR', 'XTALVIEW', 
                      'HKL2000', 'Dtrek', 'XSCALE', 'MULTAN', 'MAIN', 'OTHER']

    parser = argparse.ArgumentParser(description='Structure factor conversion')
    parser.add_argument('-i', type=str, choices=input_formats, help='Input format')
    parser.add_argument('-o', type=str, choices=output_formats, required=True, help='Output format')
    parser.add_argument('-sf', type=str, required=True, help='Data file')
    parser.add_argument('-out', type=str, help='Output file')
    parser.add_argument('-label', type=str, help='Label name for CNS & MTZ')
    parser.add_argument('-freer', type=int, help='A free test number in the reflection (SF) file')
    parser.add_argument('-pdb', type=str, help='A PDB file (add items to the converted SF file if missing)')
    parser.add_argument('-sf_type', type=str, choices=['I', 'F'], help='I (intensity) or F (amplitude). Only for shelx or TNT')
    parser.add_argument('-detail', type=str, help='A note to the data set')
    parser.add_argument('-wave', type=float, help='Wavelength. It overwrites the existing one')
    parser.add_argument('-diags', type=str, help='Log file containing warning/error message')
    parser.add_argument('-man', type=str, help='Cells & symmetry (a,b,c,alpha,beta,gamma,p21)')
    parser.add_argument('-flag', type=int, help='A number for re-setting the Rfree random test set')
    parser.add_argument('-format', action='store_true', help='Guess the format of the SF file')
    parser.add_argument('-audit', type=str, help='Update the audit record')
    parser.add_argument('-valid', type=str, help='Check various SF errors, and correct')
    parser.add_argument('-rescut', type=float, help='High resolution cutoff for SF_4_validate.cif')
    parser.add_argument('-sigcut', type=float, help='I/SigI cutoff for SF_4_validate.cif')
    parser.add_argument('-cif_check', action='store_true', help='Check pdbx dictionary. (local use only)')
    parser.add_argument('-ext_data', type=str, help='Extract data from SF file')

    args = parser.parse_args()

    # Check the input format
    # if args.i is None:
    #     if args.format:
    #         args.i = 'OTHER'
    #     else:
    #         parser.error('Input format is not specified')

    # Check the output format
    # if args.o is None:
    #     parser.error('Output format is not specified')
    # else:
    #     pass

if __name__ == '__main__':
    main()

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