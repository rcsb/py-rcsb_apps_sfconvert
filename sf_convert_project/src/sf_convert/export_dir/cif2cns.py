import random
#from sffile.sf_convert import sf_convert
#from sf_convert.sffile.sf_file import SFFile
from pathlib import Path

import sys
sys.path.append("/Users/vivek/OneDrive - Rutgers University/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src")
from sf_convert.sffile.sf_file import StructureFactorFile as sf_convert


class CifToCNSConverter:
    def __init__(self, sffile, fout_path, pdb_id='xxxx'):
        self.__pdb_id = pdb_id
        self.__sf_file = sffile
        self.__fout_path = fout_path
        self.__attr_existence = {}

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
            "pdbx_HL_A_iso": "hla",
            "pdbx_HL_B_iso": "hlb",
            "pdbx_HL_C_iso": "hlc",
            "pdbx_HL_D_iso": "hld"
        }

        self.__initialize_data()

    def __initialize_data(self):
        self.__initialize_refln_data()
        self.__initialize_counts()
        self.__check_attributes_exist()

    def __initialize_refln_data(self):
        self.__sf_block = self.__sf_file.get_block_by_index(0)
        self.__refln_data = self.__sf_block.getObj("refln")
        #print(self.__refln_data)

    def __initialize_counts(self):
        if self.__refln_data:
            self.__nref = self.__refln_data.getRowCount()

    def __check_attributes_exist(self):
        
        for attr, value in self.attributes.items():
            self.__attr_existence[value] = self.__refln_data.hasAttribute(attr)

        # Check existence of specific attributes
        check_attributes = {
            "Io": ["intensity_meas", "intensity_meas_au", "intensity"],
            "sIo": ["intensity_sigma", "intensity_sigma_au", "intensity_sigm", "intensity_meas_sigma", "intensity_meas_sigma_au"],
            "status": ["status", "R_free_flag", "statu", "status_au"]
        }

        for attribute, alternatives in check_attributes.items():
            self.__attr_existence[attribute] = any(self.__refln_data.hasAttribute(alternative) for alternative in alternatives)

    def __initialize_columns_at_index(self, i):
        attL = self.__refln_data.getAttributeList()

        # First row - set attribute for columns that do not exist
        if i == 0:
            for attr, var in self.attributes.items():
                if attr not in attL:
                    setattr(self, "_CifToCNSConverter__"+var, None)
                
        for attr, var in self.attributes.items():
            if attr in attL:
                value = self.__refln_data.getValue(attr, i)
                # setattr(self, var, value)
                setattr(self, "_CifToCNSConverter__"+var, value)
                #print(f'Attribute: {attr}, Variable: {var}, Value at index {i}: {value}')  # Print the value

        self.__initialize_Io_at_index(i)
        self.__initialize_sIo_at_index(i)
        self.__initialize_status_at_index(i)

    def __initialize_Io_at_index(self, i):
        self.__Io = self.__get_first_refln_value(["intensity_meas", "intensity_meas_au", "intensity"],
                                                 i)

    def __initialize_sIo_at_index(self, i):
        self.__sIo = self.__get_first_refln_value(["intensity_sigma", "intensity_sigma_au",
                                                   "intensity_sigm", "intensity_meas_sigma",
                                                   "intensity_meas_sigma_au"],
                                                  i)

    def __initialize_status_at_index(self, i):
        self.__status = self.__get_first_refln_value(["status", "R_free_flag", "statu", "status_au"], i)

    def __get_first_refln_value(self, attrList, row):
        attL = self.__refln_data.getAttributeList()

        ret = None
        for att in attrList:
            if att in attL:
                ret = self.__refln_data.getValue(att, row)
                break

        return ret

        
    def get_F_I(self, j):
        """
        Method to get H, K, L, F o& I from SF
        """
        self.__initialize_columns_at_index(j)
        # These are handled by __inialize_columns_at_index()
        # self.__initialize_Io_at_index(j)
        # self.__initialize_sIo_at_index(j)
        # self.__initialize_status_at_index(j)

        # Parse values to integers
        h = int(self.__H)
        k = int(self.__K)
        l = int(self.__L)

        # Initialize variables
        f, ssf, i, si, f1, sf1, f2, sf2 = 0, 0, 0, 0, 0, 0, 0, 0

        #sigma
        si = self.float_or_zero(self.__sIo) if self.__sIo else 0.0
        ssf = self.float_or_zero(self.__sFo_au) if self.__sFo_au else self.float_or_zero(self.__sFo) if self.__sFo else 0.0

        # for F
        f = self.float_or_zero(self.__Fo_au) if self.__Fo_au else self.float_or_zero(self.__Fo) if self.__Fo else \
            self.float_or_zero(self.__Fc_au) if self.__Fc_au else self.float_or_zero(self.__Fc) if self.__Fc else 0.0

        if not self.__Io:
            i = f * f
            si = 2 * f * ssf

        # for I
        i = self.float_or_zero(self.__Io) if self.__Io else self.float_or_zero(self.__F2o) if self.__F2o else \
            self.float_or_zero(self.__Ic) if self.__Ic else self.float_or_zero(self.__F2c) if self.__F2c else 0.0

        if not self.__Fo_au and i >= 0:
            f = i ** 0.5
            ssf = si / (2. * f)

        # F_plus exist
        if self.__F_plus and not (self.__Fo_au or self.__Io):
            f1 = self.float_or_zero(self.__F_plus)
            sf1 = self.float_or_zero(self.__sF_plus)

            f2 = self.float_or_zero(self.__F_minus)
            sf2 = self.float_or_zero(self.__sF_minus)

            if f1 > 0 and f2 < 0.0001:
                f = f1
                ssf = sf1
            elif f2 > 0 and f1 < 0.0001:
                f = f2
                ssf = sf2
            else:
                f = 0.5 * (f1 + f2)
                ssf = 0.5 * (sf1 + sf2)

            if not self.__I_plus:
                i = f * f
                si = 2.0 * f * ssf

        # I_plus exist
        if self.__I_plus and not (self.__Fo_au or self.__Io):
            f1 = self.float_or_zero(self.__I_plus)
            sf1 = self.float_or_zero(self.__sI_plus)

            f2 = self.float_or_zero(self.__I_minus)
            sf2 = self.float_or_zero(self.__sI_minus)

            if f1 > 0 and f2 < 0.0001:
                i = f1
                si = sf1
            elif f2 > 0 and f1 < 0.0001:
                i = f2
                si = sf2
            else:
                i = 0.5 * (f1 + f2)
                si = 0.5 * (sf1 + sf2)

            if not self.__F_plus:
                if i >= 0:
                    f = i ** 0.5
                    ssf = si / (2 * f) if f > 0.0001 else 0

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

    def write_cns_file(self):
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
            if self.__attr_existence['Io'] or self.__attr_existence['F2o']:
                output_file.write("DECLare NAME=IOBS            DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI            DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__attr_existence['F_plus'] and self.__attr_existence['F_minus']:
                output_file.write("DECLare NAME=F+           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGF+        DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=F-           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGF-        DOMAin=RECIprocal   TYPE=REAL END\n")

            elif self.__attr_existence['I_plus'] and self.__attr_existence['I_minus']:
                output_file.write("DECLare NAME=I+           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI+        DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=I-           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI-        DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__attr_existence['fom']:
                output_file.write("DECLare NAME=FOM   DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__attr_existence['hla']:
                output_file.write("DECLare NAME=HLA   DOMAin=RECIprocal   TYPE=REAL END\n")   
                output_file.write("DECLare NAME=HLB   DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=HLC   DOMAin=RECIprocal   TYPE=REAL END\n")   
                output_file.write("DECLare NAME=HLD   DOMAin=RECIprocal   TYPE=REAL END\n")

            # Loop over all the data points
            for i in range(self.__nref):

                self.__initialize_columns_at_index(i)

                h, k, l, ff, sff, ii, sii = self.get_F_I(i)

                if self.__attr_existence['status'] and self.__status == 'x':
                    continue

                if self.__status:
                    flag = 1 if (self.__status == 'f' or self.__status == '1') else 0
                else:
                    flag = 0

                output_file.write("INDE  {} {} {} FOBS= {:.2f} SIGMA= {:.2f} TEST= {}\n".format(h, k, l, ff, sff, flag))

                if self.__attr_existence['Io'] or self.__attr_existence['F2o']:
                    output_file.write("IOBS= {:.2f} SIGI= {:.2f}\n".format(ii, sii))

                if self.__attr_existence['F_plus'] and self.__attr_existence['F_minus']:
                    output_file.write("F+= {:.2f} SIGF+= {:.2f}\n".format(self.float_or_zero(self.__F_plus), self.float_or_zero(self.__sF_plus)))
                    output_file.write("F-= {:.2f} SIGF-= {:.2f}\n".format(self.float_or_zero(self.__F_minus), self.float_or_zero(self.__sF_minus)))

                elif self.__attr_existence['I_plus'] and self.__attr_existence['I_minus']:
                    output_file.write("I+= {:.2f} SIGI+= {:.2f}\n".format(self.float_or_zero(self.__I_plus), self.float_or_zero(self.__sI_plus)))
                    output_file.write("I-= {:.2f} SIGI-= {:.2f}\n".format(self.float_or_zero(self.__I_minus), self.float_or_zero(self.__sI_minus)))

                if self.__attr_existence['fom']:
                    output_file.write("FOM= {:.2f}\n".format(self.float_or_zero(self.__fom)))

                if self.__attr_existence['hla']:
                    output_file.write("HLA= {:.2f} HLB= {:.2f} HLC= {:.2f} HLD= {:.2f}\n".format(
                        self.float_or_zero(self.__hla), self.float_or_zero(self.__hlb), self.float_or_zero(self.__hlc), self.float_or_zero(self.__hld)))

    def convert(self):
        self.write_cns_file()

# def main():
#     sffile = sf_convert()
#     sffile.read_file(str(Path("/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/sffile/5pny-sf.cif")))
#     CNSexport = CifToCNSConverter(sffile, str(Path("your_output_file.txt")), 'xxxx')
#     CNSexport.convert()

# if __name__ == "__main__":
#     main()
