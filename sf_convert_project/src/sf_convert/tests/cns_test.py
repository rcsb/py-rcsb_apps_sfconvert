from sffile.sf_file import SFFile
from export.cns_export import CNSConverter
from pathlib import Path

def main():
    sffile = SFFile()
    infile = str(Path("/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/cif_files/5pny-sf.cif"))
    outfile = str(Path("/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/export/cns_file.txt"))
    sffile.readFile(infile)
    CNSexport = CNSConverter(sffile, outfile)
    CNSexport.convert()

if __name__ == "__main__":
    main()
