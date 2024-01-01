from sf_convert.import_dir.cns2cif import CNSToCifConverter
from sf_convert.utils.pinfo_file import PInfoLogger
import os


class TestCnsToCifConversion:
    def test_cns2cif(self, tmp_path, cns_5pny_data_path, cif_5pny_data_path):
        """
        Tests the conversion of a CNS file to CIF format.

        Args:
            tmp_path: The path to the temporary directory.
            cns_5pny_data_path: The path to the CNS file to be converted.
            cif_5pny_data_path: The path to the reference CIF file for comparison.

        Returns:
            None
        """
        print("Starting the test...")

        output_path = os.path.join(tmp_path, "output.mmcif")

        print("Loading and converting the file...")
        logger = PInfoLogger('path_to_log1.log', 'path_to_log2.log')
        processor = CNSToCifConverter(cns_5pny_data_path, "5pny", logger, 1)  # pdb.FREERV: FreeRValue
        processor.process_file()
        processor.rename_keys()
        processor.create_data_categories()
        processor.write_to_file(output_path)

        print("Comparing the outputs...")
        with open(cif_5pny_data_path, 'r') as f:
            expected_output = f.read()
        with open(output_path, 'r') as f:
            actual_output = f.read()

        assert actual_output == expected_output

        print("Test completed.")
