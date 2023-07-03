from sf_file import SFFile
from pathlib import Path

def get_cns_man(inpfile: str, outfile: str):
    # Read input CIF file
    sf_file = SFFile()
    sf_file.readFile(inpfile)

    #container = data[0]
    container = sf_file.getBlockByIndex(0)  # Assume the file contains one data block
    refln_obj = container.getObj("refln")

    # Fetch the reflection data we're interested in
    #hkl = refln_obj.getColumn("index_h"), refln_obj.getColumn("index_k"), refln_obj.getColumn("index_l")
    hkl = refln_obj.getColumn(refln_obj.getIndex("index_h")), refln_obj.getColumn(refln_obj.getIndex("index_k")), refln_obj.getColumn(refln_obj.getIndex("index_l"))
    #f_meas = refln_obj.getColumn("F_meas_au")
    f_meas = refln_obj.getColumn(refln_obj.getIndex("F_meas_au"))
    #sigma = refln_obj.getColumn("F_meas_sigma_au")
    sigma = refln_obj.getColumn(refln_obj.getIndex("F_meas_sigma_au"))

    #refln_status = refln_obj.getValueList("_refln.status")
    refln_status = refln_obj.getColumn(refln_obj.getIndex("status"))


    # Write output file in CNS format
    with open(outfile, 'w') as output_file:
        output_file.write("NREFlections= {}\n".format(refln_obj.getRowCount()))

        # Iterate over all reflection data
        # for h, k, l, f, sig in zip(*hkl, f_meas, sigma):
        #     output_file.write("INDE {h} {k} {l} FOBS= {f} SIGMA= {sig}\n".format(h=h, k=k, l=l, f=f, sig=sig))

        for h, k, l, f, sig, status in zip(*hkl, f_meas, sigma, refln_status):
            test_flag = 1 if status == 'f' else 0  # CNS might use a different convention, adjust as necessary
            output_file.write("INDE {h} {k} {l} FOBS= {f} SIGMA= {sig} TEST= {test}\n".format(h=h, k=k, l=l, f=f, sig=sig, test=test_flag))


# inpfile = Path("/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/cif_files/1o08-sf.cif")
# outfile = Path("your_output_file.txt")

inpfile = str(Path("/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/cif_files/1o08-sf.cif"))
outfile = str(Path("your_output_file.txt"))
get_cns_man(inpfile, outfile)

