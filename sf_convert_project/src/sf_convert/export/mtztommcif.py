import gemmi
from pathlib import Path
import sys
from mmcif.api.DataCategory import DataCategory

path_to_append = Path('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/sffile')
sys.path.append(str(path_to_append))

from sf_file import SFFile

import os


class MtzToCifConverter:
    def __init__(self):
        self.sffile = SFFile()
        self.categories = {
            "audit": {
                "revision_id": "1_0",
                "creation_date": "?",
                "update_record": "Initial release"
            }
        }

    def convert_mtz_to_mmcif(self, mtz_file, mmcif_file):
        mtz2cif = gemmi.MtzToCif()
        mtz = gemmi.read_mtz_file(mtz_file)
        cif_string = mtz2cif.write_cif_to_string(mtz)
        with open(mmcif_file, 'w') as f:
            f.write(cif_string)

    def read_cif_file(self, cif_file):
        self.sffile.readFile(cif_file)

    def write_cif_file(self, cif_file):
        self.sffile.writeFile(cif_file)

    def add_category(self, categories):
        for category_name, data_dict in categories.items():
            category = DataCategory(category_name)
            for key in data_dict.keys():
                category.appendAttribute(key)
            category.append(tuple(data_dict.values()))
            #self.sffile.containerList.append(category)
            self.sffile.add_category(category)

    def convert_and_write(self, mtz_file, output_cif_file):
        temp_file = "temp_file.cif"
        self.convert_mtz_to_mmcif(mtz_file, temp_file)
        self.read_cif_file(temp_file)
        self.add_category(self.categories)
        self.sffile.reorder_objects(['entry', 'cell', 'symmetry', 'audit', 'refln'])
        self.write_cif_file(output_cif_file)
        os.remove(temp_file)

# Create an instance of the MtzToCifConverter class
converter = MtzToCifConverter()

# Use the converter to convert an MTZ file to an mmCIF file and add the categories
converter.convert_and_write("1N9F.mtz", "output_cif_file.cif")
