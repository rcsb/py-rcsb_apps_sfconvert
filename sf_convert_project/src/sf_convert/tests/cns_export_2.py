from src.sf_convert.sffile.sf_file import SFFile
from src.sf_convert.utils import CheckSfFile
from pathlib import Path
import random

def get_cns_man(inpfile: str, outfile: str, test: float = 0.001):
    # Read input CIF file
    sf_file = SFFile()
    sf_file.readFile(inpfile)
    calculator = CheckSfFile(sf_file, ".", 0)
    container = sf_file.getBlockByIndex(0)  # Assume the file contains one data block
    refln_obj = container.getObj("refln")

    hkl = refln_obj.getColumn(refln_obj.getIndex("index_h")), refln_obj.getColumn(refln_obj.getIndex("index_k")), refln_obj.getColumn(refln_obj.getIndex("index_l"))
    f_meas = refln_obj.getColumn(refln_obj.getIndex("F_meas_au"))
    sigma = refln_obj.getColumn(refln_obj.getIndex("F_meas_sigma_au"))
    refln_status = refln_obj.getColumn(refln_obj.getIndex("status"))

    # Write output file in CNS format
    with open(outfile, 'w') as output_file:
        output_file.write("NREFlection= {}\n".format(refln_obj.getRowCount()))
        output_file.write("ANOMalous=FALSe { equiv. to HERMitian=TRUE}\n")
        output_file.write("DECLare NAME=FOBS            DOMAin=RECIprocal   TYPE=REAL END\n")
        output_file.write("DECLare NAME=SIGMA           DOMAin=RECIprocal   TYPE=REAL END\n")
        output_file.write("DECLare NAME=TEST            DOMAin=RECIprocal   TYPE=INTE END\n")

        if sf.Io or sf.F2o:
            output_file.write("DECLare NAME=IOBS            DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=SIGI            DOMAin=RECIprocal   TYPE=REAL END\n")

        if sf.F_plus and sf.F_minus:
            output_file.write("DECLare NAME=F+           DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=SIGF+        DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=F-           DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=SIGF-        DOMAin=RECIprocal   TYPE=REAL END\n")
        elif sf.I_plus and sf.I_minus:
            output_file.write("DECLare NAME=I+           DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=SIGI+        DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=I-           DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=SIGI-        DOMAin=RECIprocal   TYPE=REAL END\n")

        if sf.fom:
            output_file.write("DECLare NAME=FOM   DOMAin=RECIprocal   TYPE=REAL END\n")

        if sf.hla:
            output_file.write("DECLare NAME=HLA   DOMAin=RECIprocal   TYPE=REAL END\n")   
            output_file.write("DECLare NAME=HLB   DOMAin=RECIprocal   TYPE=REAL END\n")   
            output_file.write("DECLare NAME=HLC   DOMAin=RECIprocal   TYPE=REAL END\n")   
            output_file.write("DECLare NAME=HLD   DOMAin=RECIprocal   TYPE=REAL END\n")  

        for h, k, l, f, sig, status in zip(*hkl, f_meas, sigma, refln_status):
            if sf.status and sf.status[0] == 'x':
                continue

            if test > 0.001:
                flag = 1 if random.randint(0, test) == 1 else 0
            else:
                if sf.status:
                    flag = 1 if (sf.status[0] == 'f' or sf.status[0] == '1') else 0
                else:
                    flag = 0

            output_file.write("INDE  {} {} {} FOBS= {:.2f} SIGMA= {:.2f} TEST= {}\n".format(h, k, l, f, sig, flag))

            if sf.Io or sf.F2o:
                output_file.write("IOBS= {:.2f} SIGI= {:.2f}\n".format(ii, sii))

            if sf.F_plus and sf.F_minus:
                output_file.write("F+= {:.2f} SIGF+= {:.2f}\n".format(float(sf.F_plus), float(sf.sF_plus)))
                output_file.write("F-= {:.2f} SIGF-= {:.2f}\n".format(float(sf.F_minus), float(sf.sF_minus)))
            elif sf.I_plus and sf.I_minus:
                output_file.write("I+= {:.2f} SIGI+= {:.2f}\n".format(float(sf.I_plus), float(sf.sI_plus)))
                output_file.write("I-= {:.2f} SIGI-= {:.2f}\n".format(float(sf.I_minus), float(sf.sI_minus)))

            if sf.fom:
                output_file.write("FOM= {:.2f}\n".format(float(sf.fom)))

            if sf.hla:
                output_file.write("HLA={} HLB={} HLC={} HLD={}\n".format(sf.hla, sf.hlb, sf.hlc, sf.hld))

# inpfile = Path("/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/cif_files/1o08-sf.cif")
# outfile = Path("your_output_file.txt")

inpfile = str(Path("/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/cif_files/1o08-sf.cif"))
outfile = str(Path("your_output_file.txt"))
get_cns_man(inpfile, outfile)
