class CNSConverter:
    def __init__(self, sffile, fout_path):
        self.__sf_file = sffile
        self.__fout_path = fout_path

        # Define attributes
        self.attributes = {
            "hla": "hla",
            "hlb": "hlb",
            "hlc": "hlc",
            "hld": "hld",
            "fom": "fom",
            "status": "status",
            "Io": "Io",
            "F2o": "F2o",
            "F_plus": "F_plus",
            "F_minus": "F_minus",
            "I_plus": "I_plus",
            "I_minus": "I_minus",
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

    def write_cns_file(self, hkl, f_meas, sigma, refln_status):
        """
        Method to write data to a CNS file
        """
        with open(self.__fout_path, 'w') as output_file:
            output_file.write("NREFlection= {}\n".format(self.__nref))
            output_file.write("ANOMalous=FALSe { equiv. to HERMitian=TRUE}\n")
            output_file.write("DECLare NAME=FOBS            DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=SIGMA           DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=TEST            DOMAin=RECIprocal   TYPE=INTE END\n")

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

            #for h, k, l, f, sig, status in zip(*hkl, f_meas, sigma, refln_status):
            for h, k, l, f, sig, status in zip(h, k, l, f_meas, sigma, refln_status):

                if status and status[0] == 'x':
                    continue

                if test > 0.001:
                    flag = 1 if random.randint(0, test) == 1 else 0
                else:
                    if status:
                        flag = 1 if (status[0] == 'f' or status[0] == '1') else 0
                    else:
                        flag = 0

                output_file.write("INDE  {} {} {} FOBS= {:.2f} SIGMA= {:.2f} TEST= {}\n".format(h, k, l, f, sig, flag))

                if self.__Io or self.__F2o:
                    output_file.write("IOBS= {:.2f} SIGI= {:.2f}\n".format(ii, sii))

                if self.__F_plus and self.__F_minus:
                    output_file.write("F+= {:.2f} SIGF+= {:.2f}\n".format(float(self.__F_plus), float(self.__sF_plus)))
                    output_file.write("F-= {:.2f} SIGF-= {:.2f}\n".format(float(self.__F_minus), float(self.__sF_minus)))
                elif self.__I_plus and self.__I_minus:
                    output_file.write("I+= {:.2f} SIGI+= {:.2f}\n".format(float(self.__I_plus), float(self.__sI_plus)))
                    output_file.write("I-= {:.2f} SIGI-= {:.2f}\n".format(float(self.__I_minus), float(self.__sI_minus)))

                if self.__fom:
                    output_file.write("FOM= {:.2f}\n".format(float(self.__fom)))

                if self.__hla:
                   output_file.write("HLA= {:.2f} HLB= {:.2f} HLC= {:.2f} HLD= {:.2f}\n".format(
                        float(self.__hla), float(self.__hlb), float(self.__hlc), float(self.__hld)))















    def convert(self):
        self.write_cns_file(self.H, self.K, self.L, self.Fo_au, self.sFo_au, self.__status)

