import argparse
import re
import os
import sys
from pathlib import Path
from sf_convert.sffile.get_items_pdb import ProteinDataBank
from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.import_dir.mtz2cif import MtzToCifConverter
from sf_convert.export_dir.cns2cif import CNSToCifConverter
from sf_convert.export_dir.cif2cns import CifToCNSConverter
from sf_convert.export_dir.cif2mtz import CifToMTZConverter
from sf_convert.sffile.guess_sf_format import guess_sf_format
from sf_convert.utils.pinfo_file import pinfo
from sf_convert.utils.get_sf_info_file import get_sf_info




class CustomHelpParser(argparse.ArgumentParser):
    def print_help(self):
        custom_help_message = """
=======================================================================
              sf_convert (version: x.xxx : 2023-xx-xx )                      
=======================================================================

Usage: 'sf_convert  -i input_format -o output_format -sf data_file'
   or  'sf_convert  -o output_format -sf data_file'
=======================================================================
-i <input_format> :  optional,  support one of the format below.  
         (If '-i' is not given, sf_convert will guess the input format.) 

         MTZ, mmCIF, CNS. 

-o  <output_format> : support one of output format (below) 

         mmCIF, MTZ, CNS. 

-sf  <datafile> : Give  the  Input Structure Factor File Name. 

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

 _refln.F_meas_au         	      F           FP 
 _refln.F_meas_sigma_au               Q           SIGFP 
 _refln.intensity_meas    	      J           I     
 _refln.intensity_sigma   	      Q           SIGI   

 _refln.F_calc_au            	      F           FC     
 _refln.phase_calc        	      P           PHIC   
 _refln.phase_meas        	      P           PHIB   
 _refln.fom               	      W           FOM    
 
_refln.pdbx_FWT                       F           FWT    
_refln.pdbx_PHWT                      P           PHWT   
_refln.pdbx_DELFWT                    F           DELFWT  
_refln.pdbx_DELPHWT                   P           DELPHWT 
 
 _refln.pdbx_HL_A_iso                 A       	  HLA   
 _refln.pdbx_HL_B_iso                 A       	  HLB   
 _refln.pdbx_HL_C_iso                 A       	  HLC   
 _refln.pdbx_HL_D_iso                 A       	  HLD   
 
 _refln.pdbx_F_plus         	      G           F(+)   
 _refln.pdbx_F_plus_sigma   	      L           SIGF(+) 
 _refln.pdbx_F_minus        	      G           F(-)   
 _refln.pdbx_F_minus_sigma  	      L           SIGF(-)
 _refln.pdbx_anom_difference          D           DP   
 _refln.pdbx_anom_difference_sigma    Q           SIGDP
 _refln.pdbx_I_plus                   K           I(+)   
 _refln.pdbx_I_plus_sigma             M           SIGI(+)
 _refln.pdbx_I_minus                  K           I(-)   
 _refln.pdbx_I_minus_sigma            M           SIGI(-) 

_refln.status            	      I           FREE    
_refln.pdbx_r_free_flag               I           FLAG    
==============================================================================

Example_1: convert any supported format to any output format:   
    sf_convert  -o any_output_format -sf sf_file -out output_file 

Example_2: convert mtz to mmcif (automatic): 
    sf_convert  -o mmcif -sf mtzfile -out output_file 

Example_3: convert mtz to mmcif (give the free set): 
    sf_convert  -o mmcif -sf mtzfile -freer 1 -out output_file 

Example_4: convert mtz to mmcif (use labels in mtz, one data set): 
           (The labels on the left must be one of mmcif tokens) 
    sf_convert -o mmcif -sf mtzfile -label FP=?, SIGFP=?, FREE=?, \ 
               I=?, SIGI=?  -freer 1 -out output_file 

Example_5: convert MTZ to mmcif (one data set with anomalous)
           (If label has '(' or ')', the pair must be quoted by ' ')
    sf_convert  -o mmcif -sf mtz_file -freer 1 -label FP=? ,SIGFP=? , \ 
               FREE=? , 'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?'

Example_6: convert MTZ to mmcif (two or more data set using labels)
           (Each data set must be separated by ':' !)
    sf_convert  -o mmcif -sf mtz_file -freer 1 -label \ 
                FP=? ,SIGFP=? , FREE=? , I=?, SIGI=?, \ 
                'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?', \ 
                'I(+)=?' ,'SIGI(+)=?','I(-)=?' ,'SIGI(-)=?'  \ 
                :  \ 
                 FP=? ,SIGFP=? , FREE=? , I=?, SIGI=?, \ 
                'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?',  \ 
                'I(+)=?' ,'SIGI(+)=?','I(-)=?' ,'SIGI(-)=?' \ 
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
        #self.print_help()
        #raise ValueError(message)
        #print(f"Error: {message}")
        sys.stderr.write('Error: %s\n' % message)
        sys.exit(2)

def validate_file_exists(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")

def validate_format(file_format, valid_formats):
    if file_format not in valid_formats:
        raise ValueError(f"Invalid format: {file_format}. Please use one of the following formats: {valid_formats}")

def main():
    try:
        parser = CustomHelpParser(description="""This script allows various operations on files. Refer to the help document for more details.""")
        parser.add_argument('-i', type=str, help='Input format')
        parser.add_argument('-o', type=str, help='Output format. Accepted values are mmCIF, CNS, MTZ')
        parser.add_argument('-sf', type=str, help='Source file')
        parser.add_argument('-out', type=str, default='output', help='Output file name (if not given, default by program)')
        parser.add_argument('-label', type=str, help='Label name for CNS & MTZ')
        parser.add_argument('-pdb', type=str, help='PDB file (add items to the converted SF file if missing)')
        parser.add_argument('-freer', type=int, help='free test number in the reflection (SF) file')
        parser.add_argument('-wave', type=float, help='Wavelength setting. It overwrites the existing one')
        parser.add_argument('-diags', type=str, help='Log file containing warning/error message')
        parser.add_argument('-detail', type=str, help='Give a note to the data set')
        parser.add_argument('-valid', type=str, help='Check various SF errors, and correct!')
        parser.add_argument('-multidatablock', type=str, help='Update block name')

        args = parser.parse_args()

        # TODO: Implement the logic based on the arguments

        valid_formats = ["CNS", "MTZ", "mmCIF"]

        pdb = ProteinDataBank()

        # If -i argument is provided, validate it
        if args.i is not None:
            validate_format(args.i, valid_formats)

        # If -i argument is not provided, use guess_sf_format() to determine the input format
        else:
            if args.sf is None:
                raise ValueError("Source file (-sf) must be provided.")
            args.i = guess_sf_format(args.sf)
            validate_format(args.i, valid_formats)

        # Check if -o argument is provided
        if args.o is None:
            raise ValueError(f"Output format (-o) must be provided. Please use one of the following formats: {valid_formats}")
        
        if args.sf is None:
            raise ValueError("Source file (-sf) must be provided.")

        # Validate the output format
        validate_format(args.o, valid_formats)

        # Check the extension of the file specified by the -pdb argument
        if args.pdb:
            validate_file_exists(args.pdb)
            if args.pdb.endswith(".cif"):
                sffile = StructureFactorFile()
                sffile.readFile(str(Path(args.pdb)))
                data = pdb.extract_attributes_from_cif(sffile)
            elif args.pdb.endswith(".pdb"):
                pdb_id = pdb.extract_attributes_from_pdb(args.pdb)
            else:
                raise ValueError("Invalid file format for -pdb argument. Please use either a PDBx/mmCIF Format (.cif) or PDB Format (.pdb) file.")

        # Validate the -label argument
        if args.label:
            # Check if label is in the format "key=value, key=value, ..."
            pattern = re.compile(r'^([^=]+=[^=]+)(,\s*[^=]+=[^=]+)*$')
            if not pattern.match(args.label):
                raise ValueError("Invalid format for -label argument. Please use the format 'key1=value1, key2=value2, ...'")

        if args.freer:
            if args.freer <= 0:
                raise ValueError("-freer argument must be a positive integer.")
            pdb.update_FREERV(args.freer)
            pinfo(f"Note: {args.freer} is used for free data set.", 0)

        if args.wave:
            if args.wave <= 0.0:
                raise ValueError("-wave argument must be a positive float.")
            pdb.update_WAVE(args.wave)

        
        if args.diags:
            #validate_file_exists(args.diags)
            get_sf_info(args.diags)
            #pinfo(f"Note: {args.diags} is used for warning/error messages.", 0)

        
        # Handle the -i and -o arguments
        input_format = args.i
        output_format = args.o

        # Conversion logic
        if input_format == "CNS" and output_format == "mmCIF":
            processor = CNSToCifConverter(args.sf, pdb.pdb_id, pdb.FREERV)
            processor.process_file()
            processor.rename_keys()
            processor.create_data_categories()
            processor.write_to_file(args.out+".mmcif")

        elif input_format == "MTZ" and output_format == "mmCIF":
            converter = MtzToCifConverter(args.sf, args.out+".mmcif", pdb.pdb_id)
            if args.label:
                converter.process_labels(args.label)
            converter.convert_and_write()

        elif input_format == "mmCIF" and output_format == "MTZ":
            converter = CifToMTZConverter(args.sf)
            converter.load_cif()
            converter.determine_mappings()
            converter.convert_to_mtz(args.out+".mtz")

        elif input_format == "mmCIF" and output_format == "CNS":
            sffile = StructureFactorFile()
            sffile.read_file(args.sf)
            CNSexport = CifToCNSConverter(sffile, args.out+".CNS", pdb.pdb_id)
            CNSexport.convert()

        else:
            raise ValueError(f"Conversion from {input_format} to {output_format} is not supported.")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()