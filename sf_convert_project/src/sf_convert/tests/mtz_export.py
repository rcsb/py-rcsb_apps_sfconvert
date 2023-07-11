import gemmi

SFCIF_PATH = '/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/tests/data/cif_files/1o08-sf.cif'
cif_doc = gemmi.cif.read(SFCIF_PATH)
rblock = gemmi.as_refln_blocks(cif_doc)[0]

print(rblock.column_labels())




mappings = {
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

spec_lines = []
column_labels = rblock.column_labels()

for key, alternatives in mappings.items():
    for alternative in alternatives:
        if alternative[0] in column_labels:
            spec_line = ' '.join([alternative[0]] + list(map(str, alternative[1:])))
            spec_lines.append(spec_line)
            break

cv = gemmi.CifToMtz()
cv.spec_lines = spec_lines

print("spec_lines: ", spec_lines)

mtz = cv.convert_block_to_mtz(rblock)

print("mtz: ", mtz)

mtz.write_to_file('output.mtz')

print([col.label for col in mtz.columns])


# cif2mtz = gemmi.CifToMtz()
# mtz = cif2mtz.convert_block_to_mtz(rblock)

# # Save the MTZ object to a file
# mtz.write_to_file('output.mtz')


# >>>d = gemmi.cif.read('2083844_biotin_NIS_file001.fcf')
# >>>rb = gemmi.hkl_cif_as_refln_block(d[0])
# >>> rb.column_labels()
# ['index_h', 'index_k', 'index_l', 'F_squared_calc', 'F_squared_meas', 'F_squared_sigma', 'observed_status']
# >>> cv = gemmi.CifToMtz()
# >>> cv.spec_lines = ['F_squared_meas IMEAN J 1', 'F_squared_sigma SIGIMEAN Q 1']
# >>> mtz = cv.convert_block_to_mtz(rb)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# RuntimeError: Miller index tag not found: index_h