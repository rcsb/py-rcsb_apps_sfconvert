from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.export_dir.cif2cns import CifToCNSConverter
import os

class TestCns:

    @staticmethod
    def test_cif2cns(tmp_path, cif_5pny_data_path):
        """
        Tests the conversion of a CIF file to CNS format.

        Args:
            tmp_path: The path to the temporary directory.
            cif_5pny_data_path: The path to the CIF file to be converted.

        Returns:
            None
        """
        sffile = StructureFactorFile()
        infile = cif_5pny_data_path
        outfile = os.path.join(tmp_path, "cns_file.txt")
        # We should return a diagnostic on reading
        print("XXXXX", infile)
        sffile.read_file(infile)
        assert sffile.get_number_of_blocks() > 0
    
        CNSexport = CifToCNSConverter(sffile, outfile, "xxxx")
        # We should have a diagnostic
        CNSexport.write_cns_file()

        assert os.path.exists(outfile)
    
if __name__ == "__main__":
    main()