from sf_convert.import_dir.import_mtz import ImportMtz
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
        converter = ImportMtz(logger)
                
        # converter.process_labels()  # if labels are required
        converter.import_files([mtz_Ras_NAD_data_path])
        sffile = converter.get_sf()
        sffile.write_file(output_path)

        print("Comparing the outputs...")
        comp_sfcif(cif_Ras_NAD_data_path, output_path)

        print("Test completed.")
