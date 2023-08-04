from sf_convert.export.mtz2cif import MtzToCifConverter


class TestMtzToCifConversion:
    def test_mtz2cif(self, tmp_path, mtz_Ras_NAD_data_path, cif_Ras_NAD_data_path):
        print("Starting the test...")
        
        output_path = tmp_path / "output.cif"
        
        print("Loading and converting the file...")
        converter = MtzToCifConverter(mtz_Ras_NAD_data_path, output_path, "5pny")
        converter.process_labels()  # if labels are required
        converter.convert_and_write()
        
        print("Comparing the outputs...")
        with open(cif_Ras_NAD_data_path, 'r') as f:
            expected_output = f.read()
        with open(output_path, 'r') as f:
            actual_output = f.read()

        assert actual_output == expected_output

        print("Test completed.")