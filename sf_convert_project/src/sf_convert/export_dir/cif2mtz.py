import gemmi

class CifToMTZConverter:
    def __init__(self, cif_path):
        self.cif_path = cif_path
        self.mappings = {
            'h_index_mapping' : [['index_h', 'H', 'H', 0]],
            'k_index_mapping' : [['index_k', 'K', 'H', 0]],
            'l_index_mapping' : [['index_l', 'L', 'H', 0]],
            'status_mapping' : [['status', 'FREE', 'I', 0, 'o=1,f=0'], ['pdbx_r_free_flag', 'FREE', 'I', 0]], # add more tags if needed
            'F_meas_mapping' : [['F_meas_au', 'FP', 'F', 1], ['F_meas', 'FP', 'F', 1]],
            'F_sigma_mapping' : [['F_meas_sigma_au', 'SIGFP', 'Q', 1], ['F_meas_sigma', 'SIGFP', 'Q', 1]],
            'F_calc_mapping' : [['F_calc_au', 'FC', 'F', 1], ['F_calc', 'FC', 'F', 1]],
            'phase_calc_mapping' : [['phase_calc', 'PHIC', 'P', 1]],
            'phase_meas_mapping' : [['phase_meas', 'PHIB', 'P', 1]],
            'fom_mapping' : [['fom', 'FOM', 'W', 1], ['weight', 'FOM', 'W', 1]],
            'intensity_meas_mapping' : [['intensity_meas', 'I', 'J', 1], ['F_squared_meas', 'I', 'J', 1]],
            'intensity_sigma_mapping' : [['intensity_sigma', 'SIGI', 'Q', 1], ['F_squared_sigma', 'SIGI', 'Q', 1]],
            'F_part_mapping' : [['F_part_au', 'FPART', 'F', 1]],
            'phase_part_mapping' : [['phase_part', 'PHIP', 'P', 1]],
            'pdbx_F_plus_mapping' : [['pdbx_F_plus', 'F(+)', 'G', 1]],
            'pdbx_F_plus_sigma_mapping' : [['pdbx_F_plus_sigma', 'SIGF(+)', 'L', 1]],
            'pdbx_F_minus_mapping' : [['pdbx_F_minus', 'F(-)', 'G', 1]],
            'pdbx_F_minus_sigma_mapping' : [['pdbx_F_minus_sigma', 'SIGF(-)', 'L', 1]],
            'pdbx_anom_difference_mapping' : [['pdbx_anom_difference', 'DP', 'D', 1]],
            'pdbx_anom_difference_sigma_mapping' : [['pdbx_anom_difference_sigma', 'SIGDP', 'Q', 1]],
            'pdbx_I_plus_mapping' : [['pdbx_I_plus', 'I(+)', 'K', 1]],
            'pdbx_I_plus_sigma_mapping' : [['pdbx_I_plus_sigma', 'SIGI(+)', 'M', 1]],
            'pdbx_I_minus_mapping' : [['pdbx_I_minus', 'I(-)', 'K', 1]],
            'pdbx_I_minus_sigma_mapping' : [['pdbx_I_minus_sigma', 'SIGI(-)', 'M', 1]],
            'pdbx_HL_A_iso_mapping' : [['pdbx_HL_A_iso', 'HLA', 'A', 1]],
            'pdbx_HL_B_iso_mapping' : [['pdbx_HL_B_iso', 'HLB', 'A', 1]],
            'pdbx_HL_C_iso_mapping' : [['pdbx_HL_C_iso', 'HLC', 'A', 1]],
            'pdbx_HL_D_iso_mapping' : [['pdbx_HL_D_iso', 'HLD', 'A', 1]],
            'pdbx_DELFWT_mapping' : [['pdbx_DELFWT', 'DELFWT', 'F', 1]],
            'pdbx_DELPHWT_mapping' : [['pdbx_DELPHWT', 'PHDELWT', 'P', 1]],
            'pdbx_FWT_mapping' : [['pdbx_FWT', 'FWT', 'F', 1]],
            'pdbx_PHWT_mapping' : [['pdbx_PHWT', 'PHWT', 'P', 1]],
        }
        self.rblock = None
        self.cv = gemmi.CifToMtz()

    def load_cif(self):
        cif_doc = gemmi.cif.read(self.cif_path)
        self.rblock = gemmi.as_refln_blocks(cif_doc)[0]
        return self.rblock.column_labels()

    def determine_mappings(self):
        spec_lines = []
        column_labels = self.rblock.column_labels()
        for key, alternatives in self.mappings.items():
            for alternative in alternatives:
                if alternative[0] in column_labels:
                    spec_line = ' '.join([alternative[0]] + list(map(str, alternative[1:])))
                    spec_lines.append(spec_line)
                    break
        self.cv.spec_lines = spec_lines
        return spec_lines

    def convert_to_mtz(self, output_path):
        mtz = self.cv.convert_block_to_mtz(self.rblock)
        mtz.write_to_file(output_path)
        return [col.label for col in mtz.columns]