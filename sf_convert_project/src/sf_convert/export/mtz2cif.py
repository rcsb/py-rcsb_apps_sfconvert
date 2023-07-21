import gemmi
import os
from pathlib import Path
import sys
from mmcif.api.DataCategory import DataCategory
path_to_append = Path('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/sffile')
sys.path.append(str(path_to_append))

from sf_file import SFFile

class MtzToCifConverter:
    def __init__(self, mtz_file_path, output_file_path):
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

    def set_spec(self):
        spec_lines = ['\t'.join(line) for line in self.spec_file_content]
        self.mtz2cif.spec_lines = spec_lines

    def convert_mtz_to_cif(self):
        mtz = gemmi.read_mtz_file(self.mtz_file_path)
        return self.mtz2cif.write_cif_to_string(mtz)

    def read_cif_file(self, cif_file):
        self.sffile.readFile(cif_file)

    def add_category(self, categories):
        for category_name, data_dict in categories.items():
            category = DataCategory(category_name)
            for key in data_dict.keys():
                category.appendAttribute(key)
            category.append(tuple(data_dict.values()))
            self.sffile.add_category(category)

    def convert_and_write(self):
        temp_file = "temp_file.cif"
        self.set_spec()
        cif_doc = self.convert_mtz_to_cif()
        with open(temp_file, 'w') as f:
            f.write(cif_doc)
        self.read_cif_file(temp_file)
        self.add_category(self.categories)
        #self.sffile.reorder_objects(['entry', 'cell', 'symmetry', 'audit', 'refln'])
        self.sffile.reorder_objects(['audit', 'cell', 'diffrn_radiation_wavelength', 'entry', 'exptl_crystal', 'reflns_scale', 'symmetry', 'refln'])
        self.sffile.writeFile(self.output_file_path)
        os.remove(temp_file)


# Use the class to convert MTZ to CIF
converter = MtzToCifConverter('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/tests/data/cif_files/Ras_NAD.mtz', 'output.cif')
converter.convert_and_write()
