# Defining the function again

labels = [
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


def match_and_replace_labels_v4(labels, input_string):
    """
    Matches the labels from a list of tuples based on a provided string of keys and values,
    and replaces the matched labels with the corresponding values.

    Args:
        labels (list of tuples): The labels to be matched and replaced.
        input_string (str): The string of keys and values for matching and replacing in the format "key1=value1, key2=value2, ...".

    Returns:
        list of tuples: The matched and replaced labels.
    """
    # Split the input_string by comma and space to get the key-value pairs
    key_value_pairs = input_string.split(', ')
    # Create the dictionary from the key-value pairs
    key_value_dict = {pair.split('=')[0]: pair.split('=')[1] for pair in key_value_pairs}

    replaced_labels = []

    for label in labels:
        if label[0] in ["?", "&"] and label[1] in key_value_dict.keys():
            replaced_labels.append((label[0], label[1], label[2], key_value_dict[label[1]]))
        elif label[0] in key_value_dict.keys():
            replaced_labels.append((label[0], label[1], key_value_dict[label[0]], *label[3:]))

    return replaced_labels

# Testing the function with the new input_string
#input_string = "FP=FP_XDS, SIGFP=SIGFP_XDS, HL=HL_XDS, FOM=FOM_XDS, FreeR_flag=FreeR_flag_XDS"

input_string = "FP=FP_XDS, SIGFP=SIGFP_XDS, H=H_XDS"

replaced_labels = match_and_replace_labels_v4(labels, input_string)

def format_labels(replaced_labels):
    """
    Formats the replaced labels by combining the first two elements of the tuples that start with '?' or '&'.

    Args:
        replaced_labels (list of tuples): The replaced labels to be formatted.

    Returns:
        list of tuples: The formatted labels.
    """
    formatted_labels = []

    for label in replaced_labels:
        if label[0] in ["?", "&"]:
            formatted_labels.append((f"{label[0]} {label[1]}", *label[2:]))
        else:
            formatted_labels.append(label)

    return formatted_labels

# Let's use the function with the replaced_labels we have.
formatted_labels = format_labels(replaced_labels)


# print(replaced_labels)

# print(formatted_labels)

def match_replace_and_format_labels(labels, input_string):
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

    for label in labels:
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

    return replaced_and_formatted_labels

# Testing the function with the new input_string
input_string = "FP=FP_XDS, SIGFP=SIGFP_XDS, H=H_XDS"
replaced_and_formatted_labels = match_replace_and_format_labels(labels, input_string)
print(replaced_and_formatted_labels)
