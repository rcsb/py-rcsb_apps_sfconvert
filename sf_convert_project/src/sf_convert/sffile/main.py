import argparse
import sys
from pathlib import Path
# import cProfile
# import re


# Append necessary paths to sys path for module imports
project_paths = [
    '/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/sffile',
    '/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/export'
]
for path in project_paths:
    sys.path.append(str(Path(path)))

# Local module imports
from sf_file import SFFile
from cns_export import CNSConverter
from mtz_export import MTZConverter
from get_items_pdb import ProteinDataBank
from mtz2cif import MtzToCifConverter

def main():
    parser = argparse.ArgumentParser(description='This script allows various operations on files.')
    parser.add_argument('-o', type=str, help='Output format')
    parser.add_argument('-sf', type=str, help='Source file')
    parser.add_argument('-pdb', type=str, default='xxxx', help='PDBx/mmcif file name or mmcif file name')
    parser.add_argument('-freer', type=int, help='free test number in the reflection (SF) file')

    args = parser.parse_args()

    protein_data = ProteinDataBank()
    if args.pdb.endswith(".cif"):
        sffile = SFFile()
        sffile.readFile(str(Path(args.pdb)))
        data = protein_data.extract_attributes_from_cif(sffile)
        print(data)
    elif args.pdb.endswith(".pdb"):
        #pdb_id = protein_data.extract_pdb_id_from_pdb(args.pdb)
        pdb_id = protein_data.extract_attributes_from_pdb(args.pdb)
        print(pdb_id)
    else:
        pdb_id = args.pdb
        print(pdb_id)

    if args.freer:
        protein_data.update_FREERV(args.freer)

    if args.o == 'CNS':
        sffile = SFFile()
        sffile.readFile(str(Path(args.sf)))
        CNSexport = CNSConverter(sffile, str(Path("your_output_file.txt")), pdb_id)
        CNSexport.convert()

    elif args.o == 'MTZ':
        converter = MTZConverter(str(Path(args.sf)))
        converter.load_cif()
        converter.determine_mappings()
        converter.convert_to_mtz('output.mtz')

    elif args.o == 'mmcif':
        converter = MtzToCifConverter(str(Path(args.sf)), 'output.mmcif')
        converter.convert_and_write()

if __name__ == "__main__":
    #main()
    #cProfile.run('main()')
    #cProfile.run('re.compile("foo|bar")')
    main()
