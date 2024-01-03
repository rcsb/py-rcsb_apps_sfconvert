import gemmi
import os
from mmcif.api.DataCategory import DataCategory
import subprocess
import tempfile
from sf_convert.sffile.sf_file import StructureFactorFile as SFFile


class MtzToCifConverter:
    def __init__(self, mtz_file_path, output_file_path, pdb_id, logger):
        """
        Initializes the MtzToCifConverter object.

        Args:
            mtz_file_path (str): The path to the input MTZ file.
            output_file_path (str): The path to the output CIF file.
            pdb_id (str): The PDB ID.
            logger (Logger): The logger object for logging messages.
        """
        self.pdb_id = pdb_id
        self.__pinfo_value = 0
        self.mtz_file_path = mtz_file_path
        self.output_file_path = output_file_path
        self.mtz2cif = gemmi.MtzToCif()
        self.sffile = SFFile()
        self.__logger = logger
        self.assigned_labels = set()
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
        self.__logger.pinfo(f'Note: file {self.mtz_file_path} has no _audit. (auto added)', self.__pinfo_value)
        self.spec_file_content = [
            ('H', 'H', 'index_h'),
            ('K', 'H', 'index_k'),
            ('L', 'H', 'index_l'),
            ('? FREE|RFREE|FREER|FreeR_flag|R-free-flags|FreeRflag', 'I', 'status', 'S'),
            ('? FREE|RFREE|FREER|R-free-flags|FreeRflag', 'I', 'pdbx_r_free_flag'),
            ('? FreeR_flag', 'I', 'pdbx_r_free_flag'),
            ('? F_XDSdataset', 'F', 'F_meas_au'),
            ('? SIGF_XDSdataset', 'Q', 'F_meas_sigma_au'),
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

        self.REVERSE_LABEL_PREDICTIONS = {
            'F': {
                'FP': 'F_meas_au',
                'FC': 'F_calc_au',
                'FWT': 'pdbx_FWT',
                'DELFWT': 'pdbx_DELFWT',
            },
            'Q': {
                'SIGFP': 'F_meas_sigma_au',
                'SIGI': 'intensity_sigma',
                'SIGDP': 'pdbx_anom_difference_sigma',
            },
            'J': {
                'I': 'intensity_meas'
            },
            'P': {
                'PHIC': 'phase_calc',
                'PHIB': 'phase_meas',
                'PHWT': 'pdbx_PHWT',
                'DELPHWT': 'pdbx_DELPHWT',
            },
            'W': {
                'FOM': 'fom'
            },
            'A': {
                'HLA': 'pdbx_HL_A_iso',
                'HLB': 'pdbx_HL_B_iso',
                'HLC': 'pdbx_HL_C_iso',
                'HLD': 'pdbx_HL_D_iso',
            },
            'G': {
                'F(+)': 'pdbx_F_plus',
                'F(-)': 'pdbx_F_minus',
            },
            'L': {
                'SIGF(+)': 'pdbx_F_plus_sigma',
                'SIGF(-)': 'pdbx_F_minus_sigma',
            },
            'D': {
                'DP': 'pdbx_anom_difference'
            },
            'K': {
                'I(+)': 'pdbx_I_plus',
                'I(-)': 'pdbx_I_minus'
            },
            'M': {
                'SIGI(+)': 'pdbx_I_plus_sigma',
                'SIGI(-)': 'pdbx_I_minus_sigma'
            },
            'I': {
                'FREE': 'status',
                'FLAG': 'pdbx_r_free_flag'
            }
        }

        self.CUSTOM_START = [
            ('H', 'H', 'index_h'),
            ('K', 'H', 'index_k'),
            ('L', 'H', 'index_l')
        ]

        self.CUSTOM_END = [
            ('? FREE|RFREE|FREER|FreeR_flag|R-free-flags|FreeRflag', 'I', 'status', 'S')
        ]

    def set_spec(self):
        """
        Sets the spec lines for the MtzToCif object.
        """
        spec_lines = ['\t'.join(line) for line in self.spec_file_content]
        self.mtz2cif.spec_lines = spec_lines

    def convert_mtz_to_cif(self):
        """
        Converts the MTZ file to CIF format.

        Returns:
            str: The CIF document.
        """
        mtz = gemmi.read_mtz_file(self.mtz_file_path)
        return self.mtz2cif.write_cif_to_string(mtz)

    def read_cif_file(self, cif_file):
        """
        Reads the CIF file.

        Args:
            cif_file (str): The path to the CIF file.
        """
        self.sffile.read_file(cif_file)

    def add_category(self, categories):
        """
        Adds the specified categories to the CIF file.

        Args:
            categories (dict): A dictionary containing the category names and their attributes.
        """
        for category_name, data_dict in categories.items():
            category = DataCategory(category_name)
            for key in data_dict.keys():
                category.appendAttribute(key)
            category.append(tuple(data_dict.values()))
            self.sffile.append_category_to_block(category)

    def match_replace_and_format_labels(self, input_string):
        """
        Matches, replaces, and formats the labels based on the input string.

        Args:
            input_string (str): The input string containing the key-value pairs.

        Returns:
            None
        """
        key_value_pairs = input_string.split(', ')
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

    def process_labels(self, input_string):
        """
        Processes the labels based on the input string.

        Args:
            input_string (str): The input string containing the key-value pairs.

        Returns:
            None
        """
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

        self.spec_file_content = processed_labels

    def assign_label(self, desired_label):
        """
        Assigns a label to a desired label.

        Args:
            desired_label (str): The desired label.

        Returns:
            str: The assigned label.
        """
        if desired_label not in self.assigned_labels:
            self.assigned_labels.add(desired_label)
            return desired_label
        return "Unknown Label"

    def generate_full_label(self, i, labels_list):
        """
        Generates the full label based on the label type and content.

        Args:
            i (int): The index of the label in the labels list.
            labels_list (list): The list of labels.

        Returns:
            str: The generated full label.
        """
        label_type, label_content = labels_list[i]

        # Direct mappings
        if label_type == 'H' and label_content in ['H', 'K', 'L']:
            return self.assign_label(f"index_{label_content.lower()}")
        elif label_type == 'F' and label_content in ['2FOFCWT', 'FWT', 'F_ampl']:
            return self.assign_label('pdbx_FWT')
        elif label_type == 'P' and label_content in ['PH2FOFCWT', 'PHWT', 'PHIF']:
            return self.assign_label('pdbx_PHWT')
        elif label_content in ['FOFCWT', 'DELFWT']:
            return self.assign_label('pdbx_DELFWT')
        elif label_type == 'P' and label_content in ['PHFOFCWT', 'PHDELWT']:
            return self.assign_label('pdbx_DELPHWT')
        elif label_type == 'I' and any(term in label_content for term in ["free", "R-free-flag", "flag",
                                                                          "TEST", "FREE", "RFREE", "FREER",
                                                                          "FreeR_flag", "FreeRflag"]):  # FREE|RFREE|FREER|FreeR_flag|R-free-flags|FreeRflag
            return self.assign_label('pdbx_r_free_flag')
        elif label_type == 'D':
            return self.assign_label('pdbx_anom_difference')
        elif label_type == 'A':
            if 'HLA' in label_content:
                return self.assign_label('pdbx_HL_A_iso')
            elif 'HLB' in label_content:
                return self.assign_label('pdbx_HL_B_iso')
            elif 'HLC' in label_content:
                return self.assign_label('pdbx_HL_C_iso')
            elif 'HLD' in label_content:
                return self.assign_label('pdbx_HL_D_iso')
        elif label_type == 'W' and 'FOM' in label_content:
            return self.assign_label('fom')

        # Conditional checks based on label content and type of the previous or next label
        if label_type == 'F':
            if label_content in ['FP', 'F-obs-filtered', 'F-obs'] or (i < len(labels_list) - 1 and labels_list[i + 1][0] == 'Q'):
                return self.assign_label('F_meas_au')
            elif label_content in ['FC', 'Fcal']:
                return self.assign_label('F_calc_au')
        elif label_type == 'Q':
            if i > 0:
                prev_label_type = labels_list[i - 1][0]
                if prev_label_type == 'F':
                    return self.assign_label('F_meas_sigma_au')
                elif prev_label_type == 'J':
                    return self.assign_label('intensity_sigma')
                elif prev_label_type == 'D':
                    return self.assign_label('pdbx_anom_difference_sigma')

        # Conditional checks for labels that depend on label content alone
        if label_type == 'J':
            return self.assign_label('intensity_meas')
        elif label_type == 'G':
            if '(+)' in label_content:
                return self.assign_label('pdbx_F_plus')
            elif '(-)' in label_content:
                return self.assign_label('pdbx_F_minus')
        elif label_type == 'L':
            if '(+)' in label_content:
                return self.assign_label('pdbx_F_plus_sigma')
            elif '(-)' in label_content:
                return self.assign_label('pdbx_F_minus_sigma')
        elif label_type == 'K':
            if '(+)' in label_content:
                return self.assign_label('pdbx_I_plus')
            elif '(-)' in label_content:
                return self.assign_label('pdbx_I_minus')
        elif label_type == 'M':
            if '(+)' in label_content:
                return self.assign_label('pdbx_I_plus_sigma')
            elif '(-)' in label_content:
                return self.assign_label('pdbx_I_minus_sigma')
        elif label_type == 'P':
            if 'PHIC' in label_content or 'PHIC_ALL' in label_content or 'AC' in label_content:
                return self.assign_label('phase_calc')
            elif 'PHIB' in label_content or 'PHIM' in label_content:
                return self.assign_label('phase_meas')

        return "Unknown Label"

    def generate_full_labels_for_list(self, labels_list):
        """
        Generates the full labels for a list of labels.

        Args:
            labels_list (list): The list of labels.

        Returns:
            list: The list of generated full labels.
        """
        results = []
        for i in range(len(labels_list)):
            generated_label = self.generate_full_label(i, labels_list)
            results.append((labels_list[i][0], labels_list[i][1], generated_label))
            if generated_label == "pdbx_r_free_flag":
                self.CUSTOM_END = []
                self.CUSTOM_END.append((labels_list[i][1], labels_list[i][0], 'status', 'S'))
        return results

    def get_mtz_columns_with_custom_entries(self, mtz_file):
        """
        Gets the MTZ columns with custom entries.

        Args:
            mtz_file (str): The path to the MTZ file.

        Returns:
            list: The list of MTZ columns with custom entries.
        """
        mtz = gemmi.read_mtz_file(mtz_file)
        labels_list = [(column.type, column.label) for column in mtz.columns]
        results = self.generate_full_labels_for_list(labels_list)
        filtered_results = [(type_, label, full_label) for label, type_, full_label in results if full_label != "Unknown Label"]
        return filtered_results + self.CUSTOM_END

    def convert_and_write(self):
        """
        Converts the MTZ file to CIF format and writes it to the output file.
        """
        temp_file = "temp_file.mmcif"

        spec_lines_result = self.get_mtz_columns_with_custom_entries(self.mtz_file_path)
        self.spec_file_content = spec_lines_result

        self.set_spec()
        cif_doc = self.convert_mtz_to_cif()
        with open(temp_file, 'w') as f:
            f.write(cif_doc)
        self.read_cif_file(temp_file)
        self.add_category(self.categories)

        new_order = ['audit', 'cell', 'diffrn_radiation_wavelength', 'entry', 'exptl_crystal', 'reflns_scale', 'symmetry', 'refln']
        self.sffile.reorder_categories_in_block(new_order)
        self.sffile.correct_block_names("xxxx")  # XXXX assumes entry.id = xxxx - need to be able to specify pdb id
        self.sffile.write_file(self.output_file_path)
        os.remove(temp_file)

    def convert_for_nfree(self, nfree_value: int = None):
        """
        Converts the MTZ file to CIF format with the specified nfree value.

        Args:
            nfree_value (int): The nfree value.

        Returns:
            None
        """
        cmd = ["gemmi", "mtz2cif", self.mtz_file_path, self.output_file_path]

        # Create a temporary spec file from self.spec_file_content
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.spec') as temp_spec:
            for line in self.spec_file_content:
                temp_spec.write(' '.join(line) + '\n')
            spec_file_path = temp_spec.name

        # Add spec file to command
        cmd.insert(2, "--spec=" + spec_file_path)

        # Add nfree value if provided
        if nfree_value is not None:
            cmd.insert(2, "--nfree=" + str(nfree_value))

        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        # Delete the temporary spec file
        try:
            os.remove(spec_file_path)
        except Exception as e:
            self.__logger.pinfo(f"Error deleting temp spec file: {e}", 2)

        if result.returncode != 0:
            self.__logger.pinfo(f"Error occurred: {result.stderr}", 2)
        else:
            self.__logger.pinfo("Conversion successful!", 2)
