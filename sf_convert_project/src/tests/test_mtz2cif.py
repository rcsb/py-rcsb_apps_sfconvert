from sf_convert.import_dir.mtz2cif import MtzToCifConverter
from sf_convert.utils.pinfo_file import PInfoLogger
from TestHelper import comp_sfcif
import os


class TestMtzToCifConversion:
    def test_mtz2cif(self, tmp_path, mtz_Ras_NAD_data_path, cif_Ras_NAD_data_path):
        """
        Tests the conversion of an MTZ file to CIF format.

        Args:
            tmp_path: The path to the temporary directory.
            mtz_Ras_NAD_data_path: The path to the MTZ file to be converted.
            cif_Ras_NAD_data_path: The path to the reference CIF file for comparison.
2
        Returns:
            None
        """
        print("Starting the test...")

        output_path = os.path.join(tmp_path, "output.mmcif")

        print("Loading and converting the file...")
        logger = PInfoLogger('path_to_log1.log', 'path_to_log2.log')
        converter = MtzToCifConverter(mtz_Ras_NAD_data_path, output_path, "5pny", logger)
        # converter.process_labels()  # if labels are required
        converter.convert_and_write()

        print("Comparing the outputs...")
        # with open(cif_Ras_NAD_data_path, 'r') as f:
        #     expected_output = f.read()
        # with open(output_path, 'r') as f:
        #     actual_output = f.read()

        # assert cif_Ras_NAD_data_path == output_path
        comp_sfcif(cif_Ras_NAD_data_path, output_path)

        print("Test completed.")
