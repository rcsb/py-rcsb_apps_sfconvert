# Redefining the write_labels_to_file and read_labels_from_file functions

def write_labels_to_file(labels, filename):
    """
    Write the labels to a file. Each label is written on a separate line.

    Args:
        labels (list of tuples): The labels to write to the file.
        filename (str): The name of the file to write to.
    """
    with open(filename, "w") as file:
        for label in labels:
            file.write(','.join(map(str, label)) + "\n")


def read_labels_from_file(filename):
    """
    Read the labels from a file. Each label is expected to be on a separate line.

    Args:
        filename (str): The name of the file to read from.

    Returns:
        list of tuples: The labels read from the file.
    """
    labels = []
    with open(filename, "r") as file:
        for line in file:
            labels.append(tuple(line.strip().split(',')))
    return labels

# Now let's write the spec_file_content to a file and then read it back
spec_file_content = [
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
# Write these labels to a file
# write_labels_to_file(spec_file_content, "spec_file_content.txt")

# # Now we'll read the labels back from the file
# read_labels = read_labels_from_file("spec_file_content.txt")

# print(read_labels)



spec_file_content_test = [
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



write_labels_to_file(spec_file_content_test, "spec_file_content.txt")

# Now we'll read the labels back from the file
read_labels = read_labels_from_file("spec_file_content.txt")

print(read_labels)


mapping_dic = {
    'FP': 'F_meas_au',
    'SIGFP': 'F_meas_sigma_au',
    'I': 'intensity_meas',
    'SIGI': 'intensity_sigma',
    'FC': 'F_calc_au',
    'PHIC': 'phase_calc',
    'PHIB': 'phase_meas',
    'FOM': 'fom',
    'FWT': 'pdbx_FWT',
    'PHWT': 'pdbx_PHWT',
    'DELFWT': 'pdbx_DELFWT',
    'DELPHWT': 'pdbx_DELPHWT',
    'HLA': 'pdbx_HL_A_iso',
    'HLB': 'pdbx_HL_B_iso',
    'HLC': 'pdbx_HL_C_iso',
    'HLD': 'pdbx_HL_D_iso',
    'F(+)': 'pdbx_F_plus',
    'SIGF(+)': 'pdbx_F_plus_sigma',
    'F(-)': 'pdbx_F_minus',
    'SIGF(-)': 'pdbx_F_minus_sigma',
    'DP': 'pdbx_anom_difference',
    'SIGDP': 'pdbx_anom_difference_sigma',
    'I(+)': 'pdbx_I_plus',
    'SIGI(+)': 'pdbx_I_plus_sigma',
    'I(-)': 'pdbx_I_minus',
    'SIGI(-)': 'pdbx_I_minus_sigma',
    'FREE': 'status',
    'FLAG': 'pdbx_r_free_flag'
}