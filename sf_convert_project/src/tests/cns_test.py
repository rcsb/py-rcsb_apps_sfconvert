from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.export_dir.cif2cns import CifToCNSConverter
#from pathlib import Path
import os

class TestCns:

    @staticmethod
    def test_cif2cns(tmp_path, cif_5pny_data_path):
        sffile = StructureFactorFile()
        infile = cif_5pny_data_path
        outfile = os.path.join(tmp_path, "cns_file.txt")
        # We should return a diagnostic on reading
        print("XXXXX", infile)
        sffile.read_file(infile)
        assert sffile.get_number_of_blocks() > 0
    
        CNSexport = CifToCNSConverter(sffile, outfile, "xxxx")
        # We should have a diagnostic
        CNSexport.write_cns_file(0)

        assert os.path.exists(outfile)
    
if __name__ == "__main__":
    main()
