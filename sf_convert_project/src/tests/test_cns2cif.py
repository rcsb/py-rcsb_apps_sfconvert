from sf_convert.export_dir.cns2cif import CNSToCifConverter
import os
class TestCnsToCifConversion:
    def test_cns2cif(self, tmp_path, cns_5pny_data_path, cif_5pny_data_path):
        print("Starting the test...")
        
        output_path = os.path.join(tmp_path, "output.mmcif")
        
        print("Loading and converting the file...")
        processor = CNSToCifConverter(cns_5pny_data_path, "5pny", 1)  # pdb.FREERV: FreeRValue
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