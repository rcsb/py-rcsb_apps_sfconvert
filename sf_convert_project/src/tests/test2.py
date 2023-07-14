import gemmi
from pathlib import Path
import sys
path_to_append = Path('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/sffile')
sys.path.append(str(path_to_append))

from sf_file import SFFile

import os


class MtzToCifConverter:
    def __init__(self):
        self.sffile = SFFile()

    def convert_mtz_to_mmcif(self, mtz_file, mmcif_file):
        # Create an MtzToCif object
        mtz2cif = gemmi.MtzToCif()

        # Read the MTZ file
        mtz = gemmi.read_mtz_file(mtz_file)

        # Convert the MTZ data to CIF format
        cif_string = mtz2cif.write_cif_to_string(mtz)

        # Write the CIF data to a file
        with open(mmcif_file, 'w') as f:
            f.write(cif_string)

    def read_cif_file(self, cif_file):
        self.sffile.readFile(cif_file)

    def add_data(self, category_name, data_dict):
        self.sffile.addData(category_name, data_dict)

    def add_data_to_block(self, block_name, category_name, data_dict):
        self.sffile.addDataToBlock(block_name, category_name, data_dict)

    def write_cif_file(self, cif_file):
        self.sffile.writeFile(cif_file)

    def convert_and_write(self, mtz_file, output_cif_file, category_name, data_dict):
        temp_file = "temp_file.cif"
        self.convert_mtz_to_mmcif(mtz_file, temp_file)
        self.read_cif_file(temp_file)
        self.add_data(category_name, data_dict)
        #print(self.sffile.getCategories())
        #self.sffile.reorderCategories()
        #print(self.sffile.getCategories())
        self.write_cif_file(output_cif_file)
        os.remove(temp_file)

    def convert_and_write_to_block(self, mtz_file, output_cif_file, block_name, category_name, data_dict):
        temp_file = "temp_file.cif"
        self.convert_mtz_to_mmcif(mtz_file, temp_file)
        self.read_cif_file(temp_file)
        #print(self.sffile.getCategories())
        self.add_data_to_block(block_name, category_name, data_dict)
        #print(self.sffile.getCategories())
        self.write_cif_file(output_cif_file)
        os.remove(temp_file)


converter = MtzToCifConverter()

data_dict = {
    "revision_id": "1_0",
    "creation_date": "?",
    "update_record": "Initial release"
}

#converter.convert_and_write_to_block("1N9F.mtz", "output_cif_file.cif", "mtz", "audit", data_dict)
converter.convert_and_write("1N9F.mtz", "output_cif_file.cif", "audit", data_dict)
