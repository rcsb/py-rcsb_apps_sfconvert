import argparse
import os
import re
import sys
from pathlib import Path
from sf_convert.sffile.get_items_pdb import ProteinDataBank
from sf_convert.import_dir.mtz2cif import MtzToCifConverter
from sf_convert.import_dir.import_cif import ImportCif
from sf_convert.import_dir.cns2cif import CNSToCifConverter
from sf_convert.export_dir.cif2cns import CifToCNSConverter
from sf_convert.export_dir.cif2mtz import CifToMTZConverter
from sf_convert.export_dir.export_cif import ExportCif
from sf_convert.sffile.guess_sf_format import guess_sf_format
from sf_convert.utils.reformat_sfhead import reformat_sfhead, reorder_sf_file, update_exptl_crystal
from sf_convert.utils.sf_correct import SfCorrect
from sf_convert.utils.pinfo_file import PInfoLogger
from sf_convert.utils.get_sf_info_file import get_sf_info
from sf_convert.utils.CheckSfFile import CheckSfFile
from sf_convert.utils.version import get_version
from sf_convert.utils.TextUtils import is_cif

VALID_FORMATS = ["CNS", "MTZ", "MMCIF", "CIF"]


class SFConvertMain:
    """Main class to perform conversion steps."""
    def __init__(self, logger):
        self.__logger = logger
        self.__legacy = True  # old sf_convert behaviour

    def mmCIF_to_mmCIF(self, pdict, logger):
        """
        Converts from mmCIF format to mmCIF format.

        Args:
        pdict: request dictionary
        """
        sfin =  pdict["sfin"]
        output = pdict["output"]
        pdb_data = pdict.get("pdb_data", {})
        pdb_wave = pdb_data.get("WAVE", None)
        wave_arg = pdict.get("wave_cmdline", None)        

        ic = ImportCif(logger)
        ic.import_files(sfin)
        sffile = ic.get_sf()

        sfc = SfCorrect(self.__logger)
        
        # PDB id comes from
        #  sffile block name - unless coordinate file used - and then use that
        pdbid = pdb_data.get("pdb_id", None)

        if not pdbid:
            pdbid = sfc.get_pdbid(sffile)  # XXX should be a utility function somewhere else

        if pdbid:
            pdbid = pdbid.lower()
            
        # Logic:
        #  If command line - then use
        #  If SF file has and model file - use model file and warn
        #  If SF has - leave alone
        #  Else write empty

        setwlarg = None
        if wave_arg:
            setwlarg = wave_arg
        elif pdb_wave not in [".", "?", None]:
            setwlarg = pdb_wave

        sfc.annotate_wavelength(sffile, pdbid, setwlarg, logger)
        # cell

        # Cleanup exptl_crystal. Only leave id

        
        sfc.handle_standard(sffile, pdbid, logger)
        
        ec = ExportCif(self.__legacy)
        ec.set_sf(sffile)
        
        ec.write_file(output)


class CustomHelpParser(argparse.ArgumentParser):
    def print_help(self, file=None):  # pylint: disable=unused-argument
        """
        Prints the custom help message for the sf_convert script.
        """
        custom_help_message = """
    =======================================================================
                """ + get_version() + """
    =======================================================================

    Usage: 'sf_convert  -i input_format -o output_format -sf data_file'
    or  'sf_convert  -o output_format -sf data_file'
    =======================================================================
    -i <input_format> :  optional,  support one of the format below.
            (If '-i' is not given, sf_convert will guess the input format.)

            MTZ, mmCIF, CNS.

    -o  <output_format> : support one of output format (below)

            mmCIF, MTZ, CNS.

    -sf  <datafile> : Give the Input Structure Factor File Name.
    -sf  <datafile> <datafile>: Provide multiple input files. Types will be based on first

    -out <output_file> :  Give output file name (if not given, default by program).

        Other options (below) can be added to the argument:
    -label   followed by label name for CNS & MTZ (see examples below).
    -freer   followed by a free test number (-freer 1) in the reflection (SF) file.
    -pdb     followed by a PDB file (add items to the converted SF file if missing).
    -detail  followed by a text (-detail " text " ), give a note to the data set.
    -wave    followed by a wavelength (-wave 0.998). It overwrites the existing one.
    -diags   followed by a log file (-diags file) containing warning/error message.

        Other not often used options (below) can be added to the argument:
    -valid   check various SF errors, and correct!(sf_convert -valid sffile)

    ==============================================================================
    Note:
    1. CIF is for small molecule. The mmCIF is for macro-molecule format.

        mmCIF token                    type     data label

    _refln.F_meas_au                  F           FP
    _refln.F_meas_sigma_au            Q           SIGFP
    _refln.intensity_meas             J           I
    _refln.intensity_sigma            Q           SIGI

    _refln.F_calc_au                  F           FC
    _refln.phase_calc                 P           PHIC
    _refln.phase_meas                 P           PHIB
    _refln.fom                        W           FOM

    _refln.pdbx_FWT                   F           FWT
    _refln.pdbx_PHWT                  P           PHWT
    _refln.pdbx_DELFWT                F           DELFWT
    _refln.pdbx_DELPHWT               P           DELPHWT

    _refln.pdbx_HL_A_iso              A           HLA
    _refln.pdbx_HL_B_iso              A           HLB
    _refln.pdbx_HL_C_iso              A           HLC
    _refln.pdbx_HL_D_iso              A           HLD

    _refln.pdbx_F_plus                G           F(+)
    _refln.pdbx_F_plus_sigma          L           SIGF(+)
    _refln.pdbx_F_minus               G           F(-)
    _refln.pdbx_F_minus_sigma         L           SIGF(-)
    _refln.pdbx_anom_difference       D           DP
    _refln.pdbx_anom_difference_sigma Q           SIGDP
    _refln.pdbx_I_plus                K           I(+)
    _refln.pdbx_I_plus_sigma          M           SIGI(+)
    _refln.pdbx_I_minus               K           I(-)
    _refln.pdbx_I_minus_sigma         M           SIGI(-)

    _refln.status                     I           FREE
    _refln.pdbx_r_free_flag           I           FLAG
    ==============================================================================

    Example_1: convert any supported format to any output format:
        sf_convert  -o any_output_format -sf sf_file -out output_file

    Example_2: convert mtz to mmcif (automatic):
        sf_convert  -o mmcif -sf mtzfile -out output_file

    Example_3: convert mtz to mmcif (give the free set):
        sf_convert  -o mmcif -sf mtzfile -freer 1 -out output_file

    Example_4: convert mtz to mmcif (use labels in mtz, one data set):
            (The labels on the left must be one of mmcif tokens)
        sf_convert -o mmcif -sf mtzfile -label FP=?, SIGFP=?, FREE=?, \\
                I=?, SIGI=?  -freer 1 -out output_file

    Example_5: convert MTZ to mmcif (one data set with anomalous)
            (If label has '(' or ')', the pair must be quoted by ' ')
        sf_convert  -o mmcif -sf mtz_file -freer 1 -label FP=? ,SIGFP=? , \\
                FREE=? , 'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?'

    Example_6: convert MTZ to mmcif (two or more data set using labels)
            (Each data set must be separated by ':' !)
        sf_convert  -o mmcif -sf mtz_file -freer 1 -label \\
                    FP=? ,SIGFP=? , FREE=? , I=?, SIGI=?, \\
                    'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?', \\
                    'I(+)=?' ,'SIGI(+)=?','I(-)=?' ,'SIGI(-)=?'  \\
                    :  \\
                    FP=? ,SIGFP=? , FREE=? , I=?, SIGI=?, \\
                    'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?',  \\
                    'I(+)=?' ,'SIGI(+)=?','I(-)=?' ,'SIGI(-)=?' \\
                    -out output_file

    Example_7: Multiple file auto-conversion. (files separated by ',' or space)
        sf_convert  -o mmcif -sf sffile1 sffile2 sffile3 -out outfile_name

    Example_8: Make the converted mmcif be complete (using coordinate).
        sf_convert  -o mmcif -sf sf_file -pdb xyzfile

    Example_9: Give a remark to the converted data set.
        sf_convert  -o mmcif -sf sf_file -detail "any text"

    Note: The question marks '?' correspond to the labels in the SF file.
    """
        print(custom_help_message)

    def error(self, message):
        """
        Prints an error message and exits the program.

        Args:
            message: The error message to be printed.
        """
        sys.stderr.write('Error: %s\n' % message)
        sys.exit(2)


def validate_file_exists(filepath: str):
    """
    Validates if a given file exists.

    Args:
        filepath: The path to the file to be validated.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")


def validate_format(file_format: str):
    """
    Validates if the given format is one of the VALID_FORMATS.

    Args:
        file_format: The format to be validated.

    Raises:
        ValueError: If the format is not valid.
    """
    if file_format.upper() not in VALID_FORMATS:
        raise ValueError(f"Invalid format: {file_format}. Please use one of the following formats: {VALID_FORMATS}")


def get_input_format(args: argparse.Namespace) -> str:
    """
    Determines the input format either from the provided argument or by guessing.

    Args:
        args: The command line arguments.

    Returns:
        The determined input format.

    Raises:
        ValueError: If the source file is not provided.
    """
    if args.i:
        validate_format(args.i)
        return args.i
    if args.sf is None:
        raise ValueError("Source file (-sf) must be provided.")
    return guess_sf_format(args.sf[0])


def handle_pdb_argument(args, pdb, logger):
    """
    Handles operations related to the -pdb argument.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.

    Returns:
        The extracted attributes from the PDB file.

    Raises:
        ValueError: If the file format for -pdb argument is invalid.
        FileNotFoundError: If the PDB file does not exist.
    """
    validate_file_exists(args.pdb)
    if is_cif(args.pdb, logger):
        return pdb.extract_attributes_from_cif(args.pdb)
    else:
        return pdb.extract_attributes_from_pdb(args.pdb)


def handle_label_argument(args):
    """
    Validates the -label argument format.

    Args:
        args: The command line arguments.

    Raises:
        ValueError: If the format for -label argument is invalid.
    """
    pattern = re.compile(r'^([^=]+=[^=]+)(,\s*[^=]+=[^=]+)*$')
    if not pattern.match(args.label):
        raise ValueError("Invalid format for -label argument. Please use the format 'key1=value1, key2=value2, ...'")


def handle_freer_argument(args, pdb, logger):
    """
    Handles operations related to the -freer argument.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.
        logger: The PInfoLogger object.

    Raises:
        ValueError: If the -freer argument is not a positive integer.
    """
    if args.freer <= 0:
        raise ValueError("-freer argument must be a positive integer.")
    pdb.update_FREERV(args.freer)
    logger.pinfo(f"Note: {args.freer} is used for free data set.", 0)


def handle_wave_argument(args, pdb):
    """
    Handles operations related to the -wave argument.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.

    Raises:
        ValueError: If the -wave argument is not a positive float.
    """
    if args.wave <= 0.0:
        raise ValueError("-wave argument must be a positive float.")

def handle_diags_argument(args):
    """
    Handles operations related to the -diags argument.

    Args:
        args: The command line arguments.
    """
    get_sf_info(args.diags)


def handle_valid_argument(args, logger):
    """
    Handles operations related to the -valid argument.

    Args:
        args: The command line arguments.
        logger: The PInfoLogger object.
    """
    sffile = StructureFactorFile()
    sffile.read_file(args.sf)
    n = sffile.get_number_of_blocks()
    sf_stat = CheckSfFile(sffile, logger, args.out + "_SF_4_validate.cif")
    sf_stat.check_sf_all_blocks(n)
    sf_stat.write_sf_4_validation()


def convert_from_CNS_to_mmCIF(args, pdb, logger):
    """
    Converts from CNS format to mmCIF format.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.
        logger: The PInfoLogger object.
    """
    processor = CNSToCifConverter(args.sf, pdb.pdb_id, logger, pdb.FREERV)
    processor.process_file()
    processor.rename_keys()
    processor.create_data_categories()
    processor.write_to_file(args.out)

    sffile = StructureFactorFile()
    sffile.read_file(args.out)

    reformat_sf_header(sffile, args, logger)

    if args.multidatablock:
        validate_block_name(args.multidatablock)
        sffile.correct_block_names(args.multidatablock)

    sffile.write_file(args.out + ".mmcif")
    os.remove(args.out)


def convert_from_MTZ_to_mmCIF(args, pdb, logger):
    """
    Converts from MTZ format to mmCIF format.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.
        logger: The PInfoLogger object.
    """
    converter = MtzToCifConverter(args.sf, args.out, pdb.pdb_id, logger)
    if args.label:
        converter.process_labels(args.label)
    if pdb.FREERV:
        converter.convert_for_nfree(pdb.FREERV)
    else:
        converter.convert_and_write()

    sffile = StructureFactorFile()
    sffile.read_file(args.out)

    reformat_sf_header(sffile, args, logger)

    if args.multidatablock:
        validate_block_name(args.multidatablock)
        sffile.correct_block_names(args.multidatablock)

    sffile.write_file(args.out + ".mmcif")
    os.remove(args.out)


def convert_from_mmCIF_to_MTZ(args):
    """
    Converts from mmCIF format to MTZ format.

    Args:
        args: The command line arguments.
    """
    converter = CifToMTZConverter(args.sf)
    converter.load_cif()
    converter.determine_mappings()
    converter.convert_to_mtz(args.out + ".mtz")


def convert_from_mmCIF_to_CNS(args, pdb):
    """
    Converts from mmCIF format to CNS format.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.
    """
    sffile = StructureFactorFile()
    sffile.read_file(args.sf)
    CNSexport = CifToCNSConverter(sffile, args.out + ".CNS", pdb.pdb_id)
    CNSexport.convert()


def convert_from_CNS_to_MTZ(args, pdb, logger):
    """
    Converts from CNS format to MTZ format through mmCIF.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.
        logger: The PInfoLogger object.
    """
    # Convert from CNS to mmCIF first
    original_out = args.out
    intermediate_mmcif = original_out + "_intermediate.mmcif"
    args.out = intermediate_mmcif[:-6]  # remove ".mmcif" from the end
    convert_from_CNS_to_mmCIF(args, pdb, logger)

    # Convert the generated mmCIF to MTZ
    args.sf = intermediate_mmcif
    args.out = original_out
    convert_from_mmCIF_to_MTZ(args)

    # Remove the intermediary mmCIF file
    os.remove(intermediate_mmcif)


def convert_from_MTZ_to_CNS(args, pdb, logger):
    """
    Converts from MTZ format to CNS format through mmCIF.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.
        logger: The PInfoLogger object.
    """
    # Save the original output name
    original_out = args.out

    # Convert from MTZ to mmCIF first
    intermediate_mmcif = original_out + "_intermediate.mmcif"
    args.out = intermediate_mmcif[:-6]  # remove ".mmcif" from the end
    convert_from_MTZ_to_mmCIF(args, pdb, logger)

    # Convert the generated mmCIF to CNS
    args.sf = intermediate_mmcif
    args.out = original_out
    convert_from_mmCIF_to_CNS(args, pdb)

    # Remove the intermediary mmCIF file
    os.remove(intermediate_mmcif)


def reformat_sf_header(sffile, pdbid, logger, detail=None):
    """
    Reformats the SF header.

    Args:
        sffile: The StructureFactorFile object.
        pdbid: the pdb id to set
        logger: The PInfoLogger object.
        detail: Any details
    """
    _ = reformat_sfhead(sffile, pdbid, logger, detail)


def validate_block_name(block_name):
    """
    Validates the block name length.

    Args:
        block_name: The block name to be validated.

    Raises:
        ValueError: If the block name is not 4 characters long.
    """
    if len(block_name) != 4:
        raise ValueError(f"Block name must be 4 characters long. {block_name} is not valid.")


def convert_files(args, input_format, pdb_data, logger):
    """
    Converts files based on input and output formats.

    Args:
        args: The command line arguments.
        input_format: The determined input format.
        pdb: The ProteinDataBank object.
        logger: The PInfoLogger object.

    Raises:
        ValueError: If the conversion from input to output format is not supported.
    """
    output_format = args.o
    input_format = input_format.upper()

    if output_format is None:
        raise ValueError(f"Conversion from {input_format} to {output_format} is not supported.")

    output_format = output_format.upper()

    # Setup dictionary of what we would like done
    pdict = {}
    pdict["sfin"] = args.sf

    if args.out is not None:
        output = args.out
    else:
        output = f"{args.sf[0]}.{args.o}"

    pdict["output"] = output
    pdict["pdb_data"] = pdb_data

    if args.wave is not None:
        pdict["wave_cmdline"] = float(args.wave)   #  Type checked in argument parser
        
    # Maybe come from SF if set originally?
    #pdbid = "xxxx"
    #validate_block_name(pdbid)

    #pdict["pdbid"] = pdbid

    sfc = SFConvertMain(logger)
    
    if input_format == "CNS" and output_format == "MMCIF":
        convert_from_CNS_to_mmCIF(args, pdb, logger)
    elif input_format == "MTZ" and output_format == "MMCIF":
        convert_from_MTZ_to_mmCIF(args, pdb, logger)
    elif input_format == "MMCIF" and output_format == "MTZ":
        convert_from_mmCIF_to_MTZ(args)
    elif input_format == "MMCIF" and output_format == "CNS":
        convert_from_mmCIF_to_CNS(args, pdb)
    # elif input_format == "mmCIF" and output_format == "mmCIF":
    elif (input_format in ["MMCIF", "CIF"]) and output_format == "MMCIF":
        sfc.mmCIF_to_mmCIF(pdict, logger)
    elif input_format == "CNS" and output_format == "MTZ":
        convert_from_CNS_to_MTZ(args, pdb, logger)
    elif input_format == "MTZ" and output_format == "CNS":
        convert_from_MTZ_to_CNS(args, pdb, logger)
    elif args.valid is False:
        raise ValueError(f"Conversion from {input_format} to {output_format} is not supported.")


def main():
    """
    The main function that handles the execution of the sf_convert script.
    """
    try:
        args = parse_arguments()
        pdb = ProteinDataBank()
        logger = PInfoLogger('path_to_log1.log', 'path_to_log2.log')
        # logger.clear_logs()

        input_format = get_input_format(args)

        if args.pdb:
            pdb_data = handle_pdb_argument(args, pdb, logger)
        else:
            pdb_data = {}

        # Wavelength, etc - not pdb_data - need to know where comes from
            
        if args.label:
            handle_label_argument(args)

        if args.freer:
            handle_freer_argument(args, pdb, logger)

        if args.wave:
            handle_wave_argument(args, pdb)

        if args.diags:
            handle_diags_argument(args)

        if args.valid:
            handle_valid_argument(args, logger)

        convert_files(args, input_format, pdb_data, logger)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(2)


def parse_arguments() -> argparse.Namespace:
    """
    Parses and returns the command line arguments.

    Returns:
        The parsed command line arguments.
    """
    parser = CustomHelpParser(description="This script allows various operations on files. Refer to the help document for more details.")

    parser.add_argument('-i', type=str, help='Input format')
    parser.add_argument('-o', type=str, help='Output format. Accepted values are mmCIF, CNS, MTZ')
    parser.add_argument('-sf', type=str, nargs="+", help='Source file')
    parser.add_argument('-out', type=str, default=None, help='Output file name (if not given, default by program)')
    parser.add_argument('-label', type=str, help='Label name for CNS & MTZ')
    parser.add_argument('-pdb', type=str, help='PDB file (add items to the converted SF file if missing)')
    parser.add_argument('-freer', type=int, help='Free test number in the reflection (SF) file')
    parser.add_argument('-wave', type=float, help='Wavelength setting. It overwrites the existing one')
    parser.add_argument('-diags', type=str, help='Log file containing warning/error message')
    parser.add_argument('-detail', type=str, help='Give a note to the data set')
    parser.add_argument('-valid', action='store_true', help='Check various SF errors, and correct!')
    parser.add_argument('-multidatablock', type=str, help='Update block name')

    return parser.parse_args()


if __name__ == "__main__":
    main()
