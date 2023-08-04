from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.export_dir.cif2cns import CifToCNSConverter
import os
#degubbing
import filecmp
#import shutil

class TestCifToCnsConversion:
    def test_cif2cns(self, tmp_path, cif_5pny_data_path, cns_5pny_data_path):
        print("Starting the test...")
        
        output_path = os.path.join(tmp_path, "output.CNS")
        
        print("Reading the input file...")
        sffile = StructureFactorFile()
        sffile.read_file(cif_5pny_data_path)
        
        print("Converting the file...")
        converter = CifToCNSConverter(sffile, output_path, "5pny")
        converter.convert()

        # permanent_output_path = "/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/sffile/output.CNS"
        # shutil.copyfile(output_path, permanent_output_path)

        # print("Loading the expected output...")
        # with open(cns_5pny_data_path, 'r') as f:
        #     expected_output = f.read()

        # print("Loading the actual output...")
        # with open(output_path, 'r') as f:
        #     actual_output = f.read()

        # print("Comparing the outputs...")
        # assert actual_output == expected_output

        # print("Test completed.")

        assert filecmp.cmp(cns_5pny_data_path, output_path, shallow = False)

