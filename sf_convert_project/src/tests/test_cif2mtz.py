import os
from sf_convert.export_dir.cif2mtz import CifToMTZConverter


class TestCifToMtzConversion:
    def test_cif2mtz(self, tmp_path, cif_5pny_data_path):
        """
        Tests the conversion of a CIF file to MTZ format.

        Args:
            tmp_path: The path to the temporary directory.
            cif_5pny_data_path: The path to the CIF file to be converted.

        Returns:
            None
        """
        print("Starting the test...")

        # output_path = tmp_path / "output.mtz"
        output_path = os.path.join(tmp_path, "output.mtz")

        print("Loading and converting the file...")
        converter = CifToMTZConverter(cif_5pny_data_path)
        converter.load_cif()
        converter.determine_mappings()
        converter.convert_to_mtz(output_path)

        print("Checking the output...")
        assert os.path.isfile(output_path)
        assert os.path.getsize(output_path) > 0

        print("Test completed.")
