from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.export_dir.cif2cns import CifToCNSConverter
import os
import difflib


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

        # Read the files
        with open(cns_5pny_data_path, 'r') as file:
            file1_lines = file.read().splitlines()

        with open(output_path, 'r') as file:
            file2_lines = file.read().splitlines()

        # Normalize whitespace in each line
        file1_lines = [' '.join(line.split()) for line in file1_lines]
        file2_lines = [' '.join(line.split()) for line in file2_lines]

        # Compare the files
        differ = difflib.Differ()
        diffs = list(differ.compare(file1_lines, file2_lines))

        # Check if there are differences
        differences = [diff for diff in diffs if diff[0] in ('-', '+')]

        assert len(differences) == 0, "Files are not the same"

        print("Test completed.")
