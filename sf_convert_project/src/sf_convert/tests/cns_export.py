import random
from sffile.sf_file import SFFile
#from sf_convert.sffile.sf_file import SFFile
from pathlib import Path

class CNSConverter:
    def __init__(self, sffile, fout_path):
        self.__sf_file = sffile
        self.__fout_path = fout_path

        # Define attributes
        self.attributes = {
            "index_h": "H",
            "index_k": "K",
            "index_l": "L",
            "F_calc": "Fc",
            "F_calc_au": "Fc_au",
            "intensity_calc": "Ic",
            "F_squared_calc": "F2c",
            "F_meas_au": "Fo_au",
            "F_meas_sigma_au": "sFo_au",
            "F_meas_sigma": "sFo",
            "F_squared_sigma": "sF2o",
            "pdbx_I_plus_sigma": "sI_plus",
            "pdbx_I_minus_sigma": "sI_minus",
            "pdbx_F_plus_sigma": "sF_plus",
            "pdbx_F_minus_sigma": "sF_minus",
            "F_meas": "Fo",
            "F_squared_meas": "F2o",
            "pdbx_I_plus": "I_plus",
            "pdbx_I_minus": "I_minus",
            "pdbx_F_plus": "F_plus",
            "pdbx_F_minus": "F_minus",
            "fom": "fom",
            "phase_calc": "phase_c",
            "phase_meas": "phase_o",
            "pdbx_HL_A_iso": "hla",
            "pdbx_HL_B_iso": "hlb",
            "pdbx_HL_C_iso": "hlc",
            "pdbx_HL_D_iso": "hld"
        }

        self.initialize_data()

    def initialize_data(self):
        self.initialize_refln_data()
        self.initialize_counts()
        self.initialize_columns()

    def initialize_refln_data(self):
        self.__sf_block = self.__sf_file.getBlockByIndex(0)
        self.__refln_data = self.__sf_block.getObj("refln")

    def initialize_counts(self):
        if self.__refln_data:
            self.__nref = self.__refln_data.getRowCount()

    def initialize_columns(self):
        for attr, var in self.attributes.items():
            if self.__refln_data.hasAttribute(attr):
                setattr(self, var, self.__refln_data.getColumn(self.__refln_data.getIndex(attr)))
                setattr(self, "_CNSConverter__"+var, self.__refln_data.getColumn(self.__refln_data.getIndex(attr)))
            else:
                setattr(self, "_CNSConverter__"+var, None)

        self.initialize_Io()
        self.initialize_sIo()
        self.initialize_status()

    def initialize_Io(self):
        # Check if attribute "intensity_meas" is present
        if self.__refln_data.hasAttribute("intensity_meas"):
            self.__Io = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_meas"))
        else:
            self.__Io = None

        # If self.__Io is still None, check for attribute "intensity_meas_au"
        if not self.__Io:
            if self.__refln_data.hasAttribute("intensity_meas_au"):
                self.__Io = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_meas_au"))

        # If self.__Io is still None, check for attribute "intensity"
        if not self.__Io:
            if self.__refln_data.hasAttribute("intensity"):
                self.__Io = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity"))

    def initialize_sIo(self):
        # Check if attribute "intensity_sigma" is present
        if self.__refln_data.hasAttribute("intensity_sigma"):
            self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_sigma"))
        else:
            self.__sIo = None

        # If self.__sIo is still None, check for attribute "intensity_sigma_au"
        if not self.__sIo:
            if self.__refln_data.hasAttribute("intensity_sigma_au"):
                self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_sigma_au"))

        # If self.__sIo is still None, check for attribute "intensity_sigm"
        if not self.__sIo:
            if self.__refln_data.hasAttribute("intensity_sigm"):
                self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_sigm"))

        # If self.__sIo is still None, check for attribute "intensity_meas_sigma"
        if not self.__sIo:
            if self.__refln_data.hasAttribute("intensity_meas_sigma"):
                self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_meas_sigma"))

        # If self.__sIo is still None, check for attribute "intensity_meas_sigma_au"
        if not self.__sIo:
            if self.__refln_data.hasAttribute("intensity_meas_sigma_au"):
                self.__sIo = self.__refln_data.getColumn(self.__refln_data.getIndex("intensity_meas_sigma_au"))

    def initialize_status(self):
        self.__status = self.__refln_data.getColumn(self.__refln_data.getIndex("status"))
        if not self.__status:
            self.__status = self.__refln_data.getColumn(self.__refln_data.getIndex("R_free_flag"))

            if not self.__status:
                self.__status = self.__refln_data.getColumn(self.__refln_data.getIndex("statu"))

                if not self.__status:
                    self.__status = self.__refln_data.getColumn(self.__refln_data.getIndex("status_au"))

    def get_F_I(self, j):
        """
        Method to get H, K, L, F o& I from SF
        """

        # Parse values to integers
        h = int(self.__H[j])
        k = int(self.__K[j])
        l = int(self.__L[j])

        # Initialize variables
        f, ssf, i, si, f1, sf1, f2, sf2 = 0, 0, 0, 0, 0, 0, 0, 0

        #sigma
        if self.__sIo:
            si = self.float_or_zero(self.__sIo[j])
        elif self.__sF2o:
            si = self.float_or_zero(self.__sF2o[j])
        else:
            si=0.0

        if self.__sFo_au:
            ssf = self.float_or_zero(self.__sFo_au[j])
        elif self.__sFo:
            ssf = self.float_or_zero(self.__sFo[j])
        else:
            ssf = 0.0

        # for F
        if self.__Fo_au:
            f = self.float_or_zero(self.__Fo_au[j])
        elif self.__Fo:
            f = self.float_or_zero(self.__Fo[j])
        elif self.__Fc_au:
            f = self.float_or_zero(self.__Fc_au[j])
        elif self.__Fc:
            f = self.float_or_zero(self.__Fc[j])

        if not self.__Io:
            i=f*f
            si=2*f*ssf

        # for I
        if self.__Io:
            i = self.float_or_zero(self.__Io[j])
        elif self.__F2o:
            i = self.float_or_zero(self.__F2o[j])
        elif self.__Ic:
            i = self.float_or_zero(self.__Ic[j])
        elif self.__F2c:
            i = self.float_or_zero(self.__F2c[j])

        if not self.__Fo_au:
            if i>=0:
                f = i**0.5
                ssf = si/(2.*f)
            else:
                ssf=0

        # F_plus exist
        if self.__F_plus and not (self.__Fo_au or self.__Io):
            f1=self.float_or_zero(self.__F_plus[j])
            sf1=self.float_or_zero(self.__sF_plus[j])

            f2=self.float_or_zero(self.__F_minus[j])
            sf2=self.float_or_zero(self.__sF_minus[j])

            if f1>0 and f2<0.0001:
                f=f1
                ssf=sf1
            elif f2>0 and f1<0.0001:
                f=f2
                ssf=sf2
            else:
                f=0.5*(f1+f2)
                ssf=0.5*(sf1 + sf2)

            if not self.__I_plus:
                i=f*f
                si=2.0*f*ssf

        # I_plus exist
        if self.__I_plus and not (self.__Fo_au or self.__Io):
            f1=self.float_or_zero(self.__I_plus[j])
            sf1=self.float_or_zero(self.__sI_plus[j])

            f2=self.float_or_zero(self.__I_minus[j])
            sf2=self.float_or_zero(self.__sI_minus[j])

            if f1>0 and f2<0.0001:
                i=f1
                si=sf1
            elif f2>0 and f1<0.0001:
                i=f2
                si=sf2
            else:
                i=0.5*(f1+f2)
                si=0.5*(sf1 + sf2)

            if not self.__F_plus:
                if i>=0:
                    f=i**0.5
                    ssf=si/(2*f) if f>0.0001 else 0
        
        ff = f
        ii = i
        sii = si
        sff = ssf
        return h, k, l, ff, sff, ii, sii

    def float_or_zero(self, value):
        try:
            float(value)
            return float(value)
        except ValueError:
            return 0

    def write_cns_file(self, test):
        """
        Method to write data to a CNS file
        """
        with open(self.__fout_path, 'w') as output_file:
            output_file.write("NREFlection= {}\n".format(self.__nref))
            output_file.write("ANOMalous=FALSe { equiv. to HERMitian=TRUE}\n")
            output_file.write("DECLare NAME=FOBS            DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=SIGMA           DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=TEST            DOMAin=RECIprocal   TYPE=INTE END\n")

            # Assuming that all the variables here are boolean values
            if self.__Io or self.__F2o:
                output_file.write("DECLare NAME=IOBS            DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI            DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__F_plus and self.__F_minus:
                output_file.write("DECLare NAME=F+           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGF+        DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=F-           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGF-        DOMAin=RECIprocal   TYPE=REAL END\n")
            elif self.__I_plus and self.__I_minus:
                output_file.write("DECLare NAME=I+           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI+        DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=I-           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI-        DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__fom:
                output_file.write("DECLare NAME=FOM   DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__hla:
                output_file.write("DECLare NAME=HLA   DOMAin=RECIprocal   TYPE=REAL END\n")   
                output_file.write("DECLare NAME=HLB   DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=HLC   DOMAin=RECIprocal   TYPE=REAL END\n")   
                output_file.write("DECLare NAME=HLD   DOMAin=RECIprocal   TYPE=REAL END\n")  

            # Introducing an index i for iterating over rows
            #for i, (h, k, l, f, sig, status) in enumerate(zip(hkl[0], hkl[1], hkl[2], f_meas, sigma, refln_status)):
            for i in range(self.__nref):

                h, k, l, ff, sff, ii, sii = self.get_F_I(i)

                if self.__status and self.__status[i] == 'x':
                    continue

                if test > 0.001:
                    flag = 1 if random.randint(0, int(test)) == 1 else 0
                else:
                    if self.__status:
                        flag = 1 if (self.__status[i] == 'f' or self.__status[i] == '1') else 0
                    else:
                        flag = 0

                output_file.write("INDE  {} {} {} FOBS= {:.2f} SIGMA= {:.2f} TEST= {}\n".format(h, k, l, ff, sff, flag))

                if self.__Io or self.__F2o:
                    # Assuming that __ii and __sii are lists, use the correct index i
                    output_file.write("IOBS= {:.2f} SIGI= {:.2f}\n".format(ii, sii))

                if self.__F_plus and self.__F_minus:
                    output_file.write("F+= {:.2f} SIGF+= {:.2f}\n".format(self.float_or_zero(self.__F_plus[i]), self.float_or_zero(self.__sF_plus[i])))
                    output_file.write("F-= {:.2f} SIGF-= {:.2f}\n".format(self.float_or_zero(self.__F_minus[i]), self.float_or_zero(self.__sF_minus[i])))
                elif self.__I_plus and self.__I_minus:
                    output_file.write("I+= {:.2f} SIGI+= {:.2f}\n".format(self.float_or_zero(self.__I_plus[i]), self.float_or_zero(self.__sI_plus[i])))
                    output_file.write("I-= {:.2f} SIGI-= {:.2f}\n".format(self.float_or_zero(self.__I_minus[i]), self.float_or_zero(self.__sI_minus[i])))

                if self.__fom:
                    output_file.write("FOM= {:.2f}\n".format(self.float_or_zero(self.__fom[i])))

                if self.__hla:
                    output_file.write("HLA= {:.2f} HLB= {:.2f} HLC= {:.2f} HLD= {:.2f}\n".format(
                        self.float_or_zero(self.__hla[i]), self.float_or_zero(self.__hlb[i]), self.float_or_zero(self.__hlc[i]), self.float_or_zero(self.__hld[i])))

    def convert(self):
        self.write_cns_file(test=0)


def main():
    sffile = SFFile()
    sffile.readFile(str(Path("/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/cif_files/5pny-sf.cif")))
    CNSexport = CNSConverter(sffile, str(Path("your_output_file.txt")))
    CNSexport.convert()


if __name__ == "__main__":
    main()