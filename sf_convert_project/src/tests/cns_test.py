from sf_convert.sffile.sf_file import SFFile
from sf_convert.export.cns_export import CNSConverter
#from pathlib import Path
import os

class TestCns:

    @staticmethod
    def test_cif2cns(tmp_path, cif_5pny_data_path):
        sffile = SFFile()
        infile = cif_5pny_data_path
        outfile = os.path.join(tmp_path, "cns_file.txt")
        # We should return a diagnostic on reading
        print("XXXXX", infile)
        sffile.readFile(infile)
        assert sffile.getBlocksCount() > 0
    
        CNSexport = CNSConverter(sffile, outfile)
        # We should have a diagnostic
        CNSexport.convert()

        assert os.path.exists(outfile)
    
if __name__ == "__main__":
    main()
