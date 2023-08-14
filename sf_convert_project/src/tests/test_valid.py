from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.utils.CheckSfFile import CheckSfFile
from sf_convert.utils.pinfo_file import PInfoLogger
import os
import difflib


class TestValid:
    def test_sf_file_validation(self, tmp_path, cif_5pny_data_path, cif_SF_4_validate_data_path):
        print("Starting the test...")

        # Define the path for the output file
        output_path = os.path.join(tmp_path, "output.cif")

        print("Reading and validating the structure factor file...")
        sffile = StructureFactorFile()
        sffile.read_file(cif_5pny_data_path)
        n = sffile.get_number_of_blocks()
        logger = PInfoLogger('path_to_log1.log', 'path_to_log2.log')
        sf_stat = CheckSfFile(sffile, logger, output_path)
        sf_stat.check_sf_all_blocks(n)
        sf_stat.write_sf_4_validation()

        # Read the reference output file
        with open(cif_SF_4_validate_data_path, 'r') as file:
            file1_lines = file.read().splitlines()

        # Read the generated output file
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
