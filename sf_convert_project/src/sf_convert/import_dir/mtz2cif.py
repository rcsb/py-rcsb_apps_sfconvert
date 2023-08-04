import gemmi
import os
from pathlib import Path
import sys
from mmcif.api.DataCategory import DataCategory
from sf_convert.utils.pinfo_file import pinfo
# path_to_append = Path('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/sffile')
# sys.path.append(str(path_to_append))

from sf_convert.sffile.sf_file import StructureFactorFile as SFFile
from sf_convert.utils.CifUtils import reorderCategoryAttr

class MtzToCifConverter:
    def __init__(self, mtz_file_path, output_file_path, pdb_id):
        self.pdb_id = pdb_id
        self.__pinfo_value = 0
        self.mtz_file_path = mtz_file_path
        self.output_file_path = output_file_path
        self.mtz2cif = gemmi.MtzToCif()
        self.sffile = SFFile()
        self.categories = {
            "audit": {
                "revision_id": "1_0",
                "creation_date": "?",
                "update_record": "Initial release"
            },
            "exptl_crystal": {
                "id": "1"
            },
            "reflns_scale": {
                "group_code": "1"
            }
        }
        pinfo(f'Note: file {self.__file_path} has no _audit. (auto added)',self.__pinfo_value)
        self.spec_file_content = [
            ('H', 'H', 'index_h'),
            ('K', 'H', 'index_k'),
            ('L', 'H', 'index_l'),
            ('? FREE|RFREE|FREER|FreeR_flag|R-free-flags|FreeRflag', 'I', 'status', 'S'),
            ('FreeR_flag', 'I', 'pdbx_r_free_flag'),
            ('F_XDSdataset', 'F', 'F_meas_au'),
            ('SIGF_XDSdataset', 'Q', 'F_meas_sigma_au'),
            ('? FC', 'F', 'F_calc_au'),
            ('? PHIC', 'P', 'phase_calc'),
            ('? PHIB', 'P', 'phase_meas'),
            ('? FWT|2FOFCWT', 'F', 'pdbx_FWT'),
            ('& PHWT|PH2FOFCWT', 'P', 'pdbx_PHWT', '.3f'),
            ('? DELFWT|FOFCWT', 'F', 'pdbx_DELFWT'),
            ('& DELPHWT|PHDELWT|PHFOFCWT', 'P', 'pdbx_DELPHWT', '.3f'),
            ('? IMEAN|I|IOBS|I-obs', 'J', 'intensity_meas'),
            ('& SIG{prev}', 'Q', 'intensity_sigma'),
            ('? I(+)|IOBS(+)|I-obs(+)', 'K', 'pdbx_I_plus'),
            ('& SIG{prev}', 'M', 'pdbx_I_plus_sigma'),
            ('? I(-)|IOBS(-)|I-obs(-)', 'K', 'pdbx_I_minus'),
            ('& SIG{prev}', 'M', 'pdbx_I_minus_sigma'),
            ('? F|FP|FOBS|F-obs', 'F', 'F_meas_au'),
            ('& SIG{prev}', 'Q', 'F_meas_sigma_au'),
            ('? F(+)|FOBS(+)|F-obs(+)', 'G', 'pdbx_F_plus'),
            ('& SIG{prev}', 'L', 'pdbx_F_plus_sigma'),
            ('? F(-)|FOBS(-)|F-obs(-)', 'G', 'pdbx_F_minus'),
            ('& SIG{prev}', 'L', 'pdbx_F_minus_sigma'),
            ('? DP', 'D', 'pdbx_anom_difference'),
            ('& SIGDP', 'Q', 'pdbx_anom_difference_sigma'),
            ('? FOM', 'W', 'fom'),
            ('? HLA', 'A', 'pdbx_HL_A_iso'),
            ('& HLB', 'A', 'pdbx_HL_B_iso'),
            ('& HLC', 'A', 'pdbx_HL_C_iso'),
            ('& HLD', 'A', 'pdbx_HL_D_iso')
        ]
        self.labels = [
            ('H', 'H', 'index_h'),
            ('K', 'H', 'index_k'),
            ('L', 'H', 'index_l'),
            ('?', 'FREE', 'I', 'status', 'S'),
            ('?', 'RFREE', 'I', 'status', 'S'),
            ('?', 'FREER', 'I', 'status', 'S'),
            ('?', 'FreeR_flag', 'I', 'status', 'S'),
            ('?', 'R-free-flags', 'I', 'status', 'S'),
            ('?', 'FreeRflag', 'I', 'status', 'S'),
            ('FreeR_flag', 'I', 'pdbx_r_free_flag'),
            ('F_XDSdataset', 'F', 'F_meas_au'),
            ('SIGF_XDSdataset', 'Q', 'F_meas_sigma_au'),
            ('?', 'FC', 'F', 'F_calc_au'),
            ('?', 'PHIC', 'P', 'phase_calc'),
            ('?', 'PHIB', 'P', 'phase_meas'),
            ('?', 'FWT', 'F', 'pdbx_FWT'),
            ('?', '2FOFCWT', 'F', 'pdbx_FWT'),
            ('&', 'PHWT', 'P', 'pdbx_PHWT', '.3f'),
            ('&', 'PH2FOFCWT', 'P', 'pdbx_PHWT', '.3f'),
            ('?', 'DELFWT', 'F', 'pdbx_DELFWT'),
            ('?', 'FOFCWT', 'F', 'pdbx_DELFWT'),
            ('&', 'DELPHWT', 'P', 'pdbx_DELPHWT', '.3f'),
            ('&', 'PHDELWT', 'P', 'pdbx_DELPHWT', '.3f'),
            ('&', 'PHFOFCWT', 'P', 'pdbx_DELPHWT', '.3f'),
            ('?', 'IMEAN', 'J', 'intensity_meas'),
            ('?', 'I', 'J', 'intensity_meas'),
            ('?', 'IOBS', 'J', 'intensity_meas'),
            ('?', 'I-obs', 'J', 'intensity_meas'),
            ('&', 'SIGIMEAN', 'Q', 'intensity_sigma'),
            ('&', 'SIGI', 'Q', 'intensity_sigma'),
            ('&', 'SIGIOBS', 'Q', 'intensity_sigma'),
            ('&', 'SIGI-obs', 'Q', 'intensity_sigma'),
            ('?', 'I(+)', 'K', 'pdbx_I_plus'),
            ('?', 'IOBS(+)', 'K', 'pdbx_I_plus'),
            ('?', 'I-obs(+)', 'K', 'pdbx_I_plus'),
            ('&', 'SIGI(+)', 'M', 'pdbx_I_plus_sigma'),
            ('&', 'SIGIOBS(+)', 'M', 'pdbx_I_plus_sigma'),
            ('&', 'SIGI-obs(+)', 'M', 'pdbx_I_plus_sigma'),
            ('?', 'I(-)', 'K', 'pdbx_I_minus'),
            ('?', 'IOBS(-)', 'K', 'pdbx_I_minus'),
            ('?', 'I-obs(-)', 'K', 'pdbx_I_minus'),
            ('&', 'SIGI(-)', 'M', 'pdbx_I_minus_sigma'),
            ('&', 'SIGIOBS(-)', 'M', 'pdbx_I_minus_sigma'),
            ('&', 'SIGI-obs(-)', 'M', 'pdbx_I_minus_sigma'),
            ('?', 'F', 'F', 'F_meas_au'),
            ('?', 'FP', 'F', 'F_meas_au'),
            ('?', 'FOBS', 'F', 'F_meas_au'),
            ('?', 'F-obs', 'F', 'F_meas_au'),
            ('&', 'SIGF', 'Q', 'F_meas_sigma_au'),
            ('&', 'SIGFP', 'Q', 'F_meas_sigma_au'),
            ('&', 'SIGFOBS', 'Q', 'F_meas_sigma_au'),
            ('&', 'SIGF-obs', 'Q', 'F_meas_sigma_au'),
            ('?', 'F(+)', 'G', 'pdbx_F_plus'),
            ('?', 'FOBS(+)', 'G', 'pdbx_F_plus'),
            ('?', 'F-obs(+)', 'G', 'pdbx_F_plus'),
            ('&', 'SIGF(+)', 'L', 'pdbx_F_plus_sigma'),
            ('&', 'SIGFOBS(+)', 'L', 'pdbx_F_plus_sigma'),
            ('&', 'SIGF-obs(+)', 'L', 'pdbx_F_plus_sigma'),
            ('?', 'F(-)', 'G', 'pdbx_F_minus'),
            ('?', 'FOBS(-)', 'G', 'pdbx_F_minus'),
            ('?', 'F-obs(-)', 'G', 'pdbx_F_minus'),
            ('&', 'SIGF(-)', 'L', 'pdbx_F_minus_sigma'),
            ('&', 'SIGFOBS(-)', 'L', 'pdbx_F_minus_sigma'),
            ('&', 'SIGF-obs(-)', 'L', 'pdbx_F_minus_sigma'),
            ('?', 'DP', 'D', 'pdbx_anom_difference'),
            ('&', 'SIGDP', 'Q', 'pdbx_anom_difference_sigma'),
            ('?', 'FOM', 'W', 'fom'),
            ('?', 'HLA', 'A', 'pdbx_HL_A_iso'),
            ('&', 'HLB', 'A', 'pdbx_HL_B_iso'),
            ('&', 'HLC', 'A', 'pdbx_HL_C_iso'),
            ('&', 'HLD', 'A', 'pdbx_HL_D_iso')
        ]

    def set_spec(self):
        spec_lines = ['\t'.join(line) for line in self.spec_file_content]
        self.mtz2cif.spec_lines = spec_lines

    # def convert_mtz_to_cif(self):
    #     mtz = gemmi.read_mtz_file(self.mtz_file_path)
    #     cif_doc_string = self.mtz2cif.write_cif_to_string(mtz)
    #     # Parse the CIF document string into a gemmi.Document object
    #     cif_doc = gemmi.cif.read_string(cif_doc_string)
    #     # Change the name of the first data block
    #     cif_doc[0].name = self.pdb_id
    #     # Convert the modified Document back into a string
    #     return str(cif_doc)
    
    def convert_mtz_to_cif(self):
        mtz = gemmi.read_mtz_file(self.mtz_file_path)
        return self.mtz2cif.write_cif_to_string(mtz)

    def read_cif_file(self, cif_file):
        self.sffile.read_file(cif_file)

    def add_category(self, categories):
        for category_name, data_dict in categories.items():
            category = DataCategory(category_name)
            for key in data_dict.keys():
                category.appendAttribute(key)
            category.append(tuple(data_dict.values()))
            self.sffile.append_category_to_block(category)

    def match_replace_and_format_labels(self, input_string):
        """
        Matches the labels from a list of tuples based on a provided string of keys and values,
        replaces the matched labels with the corresponding values, and formats the replaced labels.

        Args:
            labels (list of tuples): The labels to be matched and replaced.
            input_string (str): The string of keys and values for matching and replacing in the format "key1=value1, key2=value2, ...".

        Returns:
            list of tuples: The matched, replaced and formatted labels.
        """
        # Split the input_string by comma and space to get the key-value pairs
        key_value_pairs = input_string.split(', ')
        # Create the dictionary from the key-value pairs
        key_value_dict = {pair.split('=')[0]: pair.split('=')[1] for pair in key_value_pairs}

        replaced_and_formatted_labels = []

        for label in self.labels:
            if label[0] in ["?", "&"] and label[1] in key_value_dict.keys():
                replaced_label = (label[0], label[1], label[2], key_value_dict[label[1]])
                if replaced_label[0] in ["?", "&"]:
                    replaced_and_formatted_labels.append((f"{replaced_label[0]} {replaced_label[1]}", *replaced_label[2:]))
                else:
                    replaced_and_formatted_labels.append(replaced_label)
            elif label[0] in key_value_dict.keys():
                replaced_label = (label[0], label[1], key_value_dict[label[0]], *label[3:])
                if replaced_label[0] in ["?", "&"]:
                    replaced_and_formatted_labels.append((f"{replaced_label[0]} {replaced_label[1]}", *replaced_label[2:]))
                else:
                    replaced_and_formatted_labels.append(replaced_label)

        self.spec_file_content = replaced_and_formatted_labels
        print(self.spec_file_content)
        self.convert_and_write()
        #return replaced_and_formatted_labels

    def process_labels(self, input_string):
        key_value_pairs = input_string.split(', ')
        key_value_dict = {pair.split('=')[0]: pair.split('=')[1] for pair in key_value_pairs}

        processed_labels = []

        for label in self.labels:
            if label[0] in ["?", "&"] and label[1] in key_value_dict.keys():
                replaced_label = (label[0], key_value_dict[label[1]], label[2], label[3])
                processed_label = (f"{replaced_label[0]} {replaced_label[1]}", *replaced_label[2:]) if replaced_label[0] in ["?", "&"] else replaced_label
                processed_labels.append(processed_label)
            elif label[0] in key_value_dict.keys():
                replaced_label = (key_value_dict[label[0]], label[1], *label[2:])
                processed_label = replaced_label
                processed_labels.append(processed_label)

        #return processed_labels
        #print(processed_labels)
        self.spec_file_content = processed_labels
        # print(processed_labels)
        # print("-------------------")
        # print(self.spec_file_content)
        # print("-------------------")
        #self.convert_and_write()

    def convert_and_write(self):
        temp_file = "temp_file.mmcif"
        self.set_spec()
        cif_doc = self.convert_mtz_to_cif()
        with open(temp_file, 'w') as f:
            f.write(cif_doc)
        self.read_cif_file(temp_file)
        self.add_category(self.categories)
        #self.sffile.reorder_objects(['entry', 'cell', 'symmetry', 'audit', 'refln'])
        #self.sffile.reorder_objects(['audit', 'cell', 'diffrn_radiation_wavelength', 'entry', 'exptl_crystal', 'reflns_scale', 'symmetry', 'refln'])
        #reorderCategoryAttr()
        new_order = ['audit', 'cell', 'diffrn_radiation_wavelength', 'entry', 'exptl_crystal', 'reflns_scale', 'symmetry', 'refln']
        self.sffile.reorder_categories_in_block(new_order)


        self.sffile.write_file(self.output_file_path)
        os.remove(temp_file)


# Use the class to convert MTZ to CIF
#converter = MtzToCifConverter('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/tests/data/cif_files/Ras_NAD.mtz', 'output.cif')
# converter = MtzToCifConverter(str(Path('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/RCSB/complex.mtz')), 'output_comp.cif')
# converter.convert_and_write()
#converter.process_labels("FP=DELFWT, SIGFP=SIGF_XDSdataset")
