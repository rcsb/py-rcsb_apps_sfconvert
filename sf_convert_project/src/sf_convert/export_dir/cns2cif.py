from collections import defaultdict
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.IoAdapterCore import IoAdapterCore
from sf_convert.utils.pinfo_file import pinfo

class CNSToCifConverter:

    def __init__(self, file_path, pdb_id, FREERV=None):
        self.__FREERV = FREERV
        self.__pdb_id = pdb_id
        self.__file_path = file_path
        self.__h_values = []
        self.__k_values = []
        self.__l_values = []
        self.__values = defaultdict(list)
        #self.__curContainer = DataContainer("cif2cif")
        self.__curContainer = DataContainer(self.__pdb_id)
        self.__pinfo_value = 0


    def __process_line(self, line):
        words = line.split()
        if len(words) < 4:
            return
        try:
            h = int(words[1])
            k = int(words[2])
            l = int(words[3])
        except ValueError:
            return
        self.__h_values.append(h)
        self.__k_values.append(k)
        self.__l_values.append(l)
        current_key = None
        for word in words[4:]:
            if current_key is None and word.endswith('='):
                current_key = word[:-1]
            elif current_key is not None:
                try:
                    self.__values[current_key].append(float(word))
                except ValueError:
                    self.__values[current_key].append(word)
                current_key = None

                    
    def __process_status_line(self, line):
        if 'INDE' in line:
            ffg = 0
            if 'TEST' in line or 'FREE' in line:
                if 'TEST=' in line:
                    ffg = int(line.split('TEST=')[1].split()[0])
                elif 'TEST' in line:
                    ffg = int(line.split('TEST')[1].split()[0])
                elif 'FREE=' in line:
                    ffg = int(line.split('FREE=')[1].split()[0])
                elif 'FREE ' in line:
                    ffg = int(line.split('FREE ')[1].split()[0])
                if self.__FREERV:
                    self.__values['status'].append('f' if ffg == self.__FREERV else 'o')
                else:
                    self.__values['status'].append('f' if ffg == 1 else 'o')
                

    def __rename_keys_complete(self):
        rename_dict = {
            "FOBS": "F_meas_au",
            "FP": "F_meas_au",
            "SIGMA": "F_meas_sigma_au",
            "SIGFP": "F_meas_sigma_au",
            "TEST": "status",
            "FREE": "status",
            "IOBS": "intensity_meas",
            "I": "intensity_meas",
            "SIGI": "intensity_sigma",
            "PHIB": "phase_meas",
            "PHIC": "phase_calc",
            "FOM": "fom",
            "FC": "F_calc_au",
            "HLA": "pdbx_HLA",
            "HLB": "pdbx_HLB",
            "HLC": "pdbx_HLC",
            "HLD": "pdbx_HLD",
        }
        new_values = defaultdict(list)
        for key in self.__values:
            new_key = rename_dict.get(key, key)
            new_values[new_key] = self.__values[key]
        return new_values

    def process_file(self):
        with open(self.__file_path, 'r') as file:
            for line in file:
                self.__process_line(line)
                self.__process_status_line(line)



    def process_file(self):
        with open(self.__file_path, 'r') as file:
            for line in file:
                self.__process_line(line)


    def rename_keys(self):
        self.__values = self.__rename_keys_complete()
        self.__values['status'] = ['o' if v == 0 else 'f' for v in self.__values['status']]

    def create_data_categories(self):
        aCat = DataCategory("audit")
        aCat.appendAttribute("revision_id")
        aCat.appendAttribute("creation_date")
        aCat.appendAttribute("update_record")
        aCat.append(["1_0", "?", "Initial release"])
        self.__curContainer.append(aCat)
        pinfo(f'Note: file {self.__file_path} has no _audit. (auto added)',self.__pinfo_value)


        bCat = DataCategory("diffrn_radiation_wavelength")
        bCat.appendAttribute("id")
        bCat.appendAttribute("wavelength")
        bCat.append(["1", "."])
        self.__curContainer.append(bCat)
        pinfo("Warning: No wavelength value was found in SF file", self.__pinfo_value)


        cCat = DataCategory("entry")
        cCat.appendAttribute("id")
        cCat.append(["xxxx"])
        self.__curContainer.append(cCat)

        dCat = DataCategory("exptl_crystal")
        dCat.appendAttribute("id")
        dCat.append(["1"])
        self.__curContainer.append(dCat)

        eCat = DataCategory("reflns_scale")
        eCat.appendAttribute("group_code")
        eCat.append(["1"])
        self.__curContainer.append(eCat)

        fCat = DataCategory("refln")

        # Append the attribute names
        fCat.appendAttribute('crystal_id')
        fCat.appendAttribute('wavelength_id')
        fCat.appendAttribute('scale_group_code')
        fCat.appendAttribute('index_h')
        fCat.appendAttribute('index_k')
        fCat.appendAttribute('index_l')
        for key in self.__values.keys():
            fCat.appendAttribute(key)

        # Append the values
        for i in range(len(self.__h_values)):
            values_to_append = (1, 1, 1, self.__h_values[i], self.__k_values[i], self.__l_values[i])
            for key in self.__values.keys():
                values_to_append += (self.__values[key][i],)
            fCat.append(values_to_append)

        self.__curContainer.append(fCat)

    def write_to_file(self, output_file_path):
        myIo = IoAdapterCore()
        myIo.writeFile(output_file_path, [self.__curContainer])

# processor = CNSToCifConverter('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/RCSB/5pny-sf.cif.CNS')
# processor.process_file()
# processor.rename_keys()
# processor.create_data_categories()
# processor.write_to_file("cns2cif_output.cif")