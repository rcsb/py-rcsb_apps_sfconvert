a = [
'index_h', H, H, 0
'index_k', K, H, 0
'index_l', L, H, 0
'status','pdbx_r_free_flag', FREE, I, 0
'F_meas_au','F_meas', FP, F
'F_meas_sigma_au','F_meas_sigma', SIGFP, Q
'F_calc_au','F_calc', FC, F
'phase_calc', PHIC, P
'phase_meas', PHIB, P
'fom', 'weight', FOM, W
'intensity_meas','F_squared_meas', I, J, 1
'intensity_sigma','F_squared_sigma', SIGI, Q, 1
'F_part_au', FPART, F, 1
'phase_part', PHIP, P, 1
'pdbx_F_plus', F(+), G, 1
'pdbx_F_plus_sigma', SIGF(+), L, 1
'pdbx_F_minus', F(-), G, 1
'pdbx_F_minus_sigma', SIGF(-), L, 1
'pdbx_anom_difference', DP, D, 1
'pdbx_anom_difference_sigma', SIGDP, Q, 1
'pdbx_I_plus', I(+), K, 1
'pdbx_I_plus_sigma', SIGI(+), M, 1
'pdbx_I_minus', I(-), K, 1
'pdbx_I_minus_sigma', SIGI(-), M, 1
'pdbx_HL_A_iso', HLA, A, 1
'pdbx_HL_B_iso', HLB, A, 1
'pdbx_HL_C_iso', HLC, A, 1
'pdbx_HL_D_iso', HLD, A, 1
'pdbx_DELFWT', DELFWT, F, 1
'pdbx_DELPHWT', PHDELWT, P, 1
'pdbx_FWT', FWT, F, 1
'pdbx_PHWT' PHWT, P, 1
]

mappings = {
    'h_index_mapping' : [['index_h', 'H', 'H', 0]],
    'k_index_mapping' : [['index_k', 'K', 'H', 0]],
    'l_index_mapping' : [['index_l', 'L', 'H', 0]],
    'status_mapping' : [['status', 'FREE', 'I', 0], ['pdbx_r_free_flag', 'FREE', 'I', 0]], # add more tags if needed
    'F_meas_mapping' : [['F_meas_au', 'FP', 'F'], ['F_meas', 'FP', 'F']],
    'F_sigma_mapping' : [['F_meas_sigma_au', 'SIGFP', 'Q'], ['F_meas_sigma', 'SIGFP', 'Q']],
    'F_calc_mapping' : [['F_calc_au', 'FC', 'F'], ['F_calc', 'FC', 'F']],
    'phase_calc_mapping' : [['phase_calc', 'PHIC', 'P']],
    'phase_meas_mapping' : [['phase_meas', 'PHIB', 'P']],
    'fom_mapping' : [['fom', 'FOM', 'W'], ['weight', 'FOM', 'W']],
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
    
    
}
