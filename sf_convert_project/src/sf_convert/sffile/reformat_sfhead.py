def reformat_sfhead():
    myContainerList = []
    changes_made = False

    remove_list = ["citation"]

    refln = {
        "A_calc_au": "A_calc",
        "B_calc_au": "B_calc",
        "A_cal": "A_calc",
        "B_cal": "B_calc",
        "resolution": "d_spacing",
        "Fc_au": "F_calc_au",
        "F_sigma": "F_meas_sigma_au",
        "F_meas_au_sigma": "F_meas_sigma_au",
        "F_squared_meas_sigma": "F_squared_sigma",
        "I_meas_au": "intensity_meas",
        "intensity": "intensity_meas",
        "intensity_meas_au": "intensity_meas",
        "intensity_sigm": "intensity_sigma",
        "I_meas_sigma_au": "intensity_sigma",
        "intensity_sigma_au": "intensity_sigma",
        "intensity_meas_sigma": "intensity_sigma",
        "intensity_meas_sigma_au": "intensity_sigma",
        "dfano": "pdbx_anom_difference",
        "DF_anomalous": "pdbx_anom_difference",
        "ccp4_phase_anom": "pdbx_anom_difference",
        "pdbx_phase_anom": "pdbx_anom_difference",
        "ccp4_anomalous_diff": "pdbx_anom_difference",
        "ccp4_SAD_phase_anom": "pdbx_anom_difference",
        "pdbx_anomalous_diff": "pdbx_anom_difference",
        "pdbx_SAD_phase_anom": "pdbx_anom_difference",
        "pdbx_anomalous_meas_au": "pdbx_anom_difference",
        "I_ano_meas": "pdbx_anom_difference",
        "I_ano_sigma": "pdbx_anom_difference_sigma",
        "DF_anomalous_sigma": "pdbx_anom_difference_sigma",
        "ccp4_phase_anom_sigma": "pdbx_anom_difference_sigma",
        "pdbx_phase_anom_sigma": "pdbx_anom_difference_sigma",
        "ccp4_anomalous_diff_sigma": "pdbx_anom_difference_sigma",
        "ccp4_SAD_phase_anom_sigma": "pdbx_anom_difference_sigma",
        "pdbx_SAD_phase_anom_sigma": "pdbx_anom_difference_sigma",
        "pdbx_anomalous_meas_sigma_au": "pdbx_anom_difference_sigma",
        "F-_meas_au": "pdbx_F_minus",
        "pdbx_F_meas_minus": "pdbx_F_minus",
        "ccp4_F_meas_minus_au": "pdbx_F_minus",
        "pdbx_F_meas_minus_au": "pdbx_F_minus",
        "ccp4_SAD_F_meas_minus_au": "pdbx_F_minus",
        "F-_meas_sigma_au": "pdbx_F_minus_sigma",
        "pdbx_F_meas_minus_sigma": "pdbx_F_minus_sigma",
        "ccp4_F_meas_minus_sigma_au": "pdbx_F_minus_sigma",
        "pdbx_F_meas_minus_sigma_au": "pdbx_F_minus_sigma",
        "ccp4_SAD_F_meas_minus_sigma_au": "pdbx_F_minus_sigma",
        "F+_meas_au": "pdbx_F_plus",
        "pdbx_F_meas_plus": "pdbx_F_plus",
        "ccp4_F_meas_plus_au": "pdbx_F_plus",
        "pdbx_F_meas_plus_au": "pdbx_F_plus",
        "ccp4_SAD_F_meas_plus_au": "pdbx_F_plus",
        "F+_meas_sigma_au": "pdbx_F_plus_sigma",
        "pdbx_F_meas_plus_sigma": "pdbx_F_plus_sigma",
        "ccp4_F_meas_plus_sigma_au": "pdbx_F_plus_sigma",
        "pdbx_F_meas_plus_sigma_au": "pdbx_F_plus_sigma",
        "ccp4_SAD_F_meas_plus_sigma_au": "pdbx_F_plus_sigma",
        "pdbx_HLA": "pdbx_HL_A_iso",
        "ccp4_HL_A_iso": "pdbx_HL_A_iso",
        "ccp4_SAD_HL_A_iso": "pdbx_HL_A_iso",
        "pdbx_SAD_HL_A_iso": "pdbx_HL_A_iso",
        "pdbx_HLB": "pdbx_HL_B_iso",
        "ccp4_HL_B_iso": "pdbx_HL_B_iso",
        "ccp4_SAD_HL_B_iso": "pdbx_HL_B_iso",
        "pdbx_SAD_HL_B_iso": "pdbx_HL_B_iso",
        "pdbx_HLC": "pdbx_HL_C_iso",
        "ccp4_HL_C_iso": "pdbx_HL_C_iso",
        "ccp4_SAD_HL_C_iso": "pdbx_HL_C_iso",
        "pdbx_SAD_HL_C_iso": "pdbx_HL_C_iso",
        "pdbx_HLD": "pdbx_HL_D_iso",
        "ccp4_HL_D_iso": "pdbx_HL_D_iso",
        "ccp4_SAD_HL_D_iso": "pdbx_HL_D_iso",
        "pdbx_SAD_HL_D_iso": "pdbx_HL_D_iso",
        "ccp4_I_minus": "pdbx_I_minus",
        "ccp4_I_minus_sigma": "pdbx_I_minus_sigma",
        "ccp4_I_plus": "pdbx_I_plus",
        "ccp4_I_plus_sigma": "pdbx_I_plus_sigma",
        "pahse_calc": "phase_calc",
        "F.phase_calc": "phase_calc",
        "phase_au": "phase_meas",
        "sgx_fmap": "pdbx_FWT",
        "pdbx_fom_weighted_fmap": "pdbx_FWT",
        "statu": "status",
        "F_status": "status",
        "status_au": "status",
        "R_free_flag": "status",
        "phenix_R_free_flags": "pdbx_r_free_flag",
        "observed_status": "status",
        "waveLEngth_id": "wavelength_id",
        "wavelength_di": "wavelength_id",
        "index_l>": "index_l",
        "fiber_coordinate": "pdbx_fiber_coordinate",
        "fiber_F_meas_au": "pdbx_fiber_F_meas_au",
        "fiber_layer": "pdbx_fiber_layer",
        "F_squared_meas": "intersity_meas",
        "F_squared_sigma": "intersity_sigma",
        "gsas_i100_meas": "pdbx_gsas_i100_meas"
        }

    audit = {
        "update_recor": "update_record"
    }

    cell = {
        "enrty_id": "entry_id",
        "enry_id": "entry_id",
        "entry": "entry_id",
        "ndb_unique_axis": "pdbx_unique_axis"
    }

    diffrn = {
        "detail": "details"
    }

    symmetry = {
        "int_tables_number": "Int_Tables_number",
        "ndb_full_space_group_name_H-M": "space_group_name_H-M",
        "space_group_name_h-m": "space_group_name_H-M"
    }

    mapping_dicts = {
        "refln": refln,
        "audit": audit,
        "cell": cell,
        "diffrn": diffrn,
        "symmetry": symmetry
    }

    myContainerList, changes_made = rename_sfhead(myContainerList, mapping_dicts)

    myContainerList, changes_made = remove_sfhead(myContainerList, remove_list)

    return myContainerList, changes_made




def rename_sfhead(myContainerList, mapping_dicts):


    # Initialize a container list
    #myContainerList = []

    # Initialize a flag to track if changes have been made
    changes_made = False

    # Loop through each dictionary in the mapping_dicts
    for dict_name, mapping_dict in mapping_dicts.items():

        # Loop through each container in the container list
        for container in myContainerList:

            # Get the object from the container based on current dict_name
            cobj = container.getObj(dict_name)

            # If the object exists
            if cobj:

                # Get the attribute list from the object
                attributeList = cobj.getAttributeList()

                # Initialize an empty dictionary to store the renamed attributes
                renameDict = {}

                # Loop through each attribute in the attribute list
                for attr in attributeList:
                    # If the attribute is in the mapping_dict
                    if attr in mapping_dict:
                        # Add the attribute and its corresponding value from mapping_dict to the rename dictionary
                        renameDict[attr] = mapping_dict[attr]

                # If the rename dictionary is not empty, changes have been made
                if renameDict:
                    changes_made = True

                # Rename the attributes in the object using the rename dictionary
                cobj.renameAttributes(renameDict)

            # Attempt to remove the 'citation' category from the container
            citation_removed = container.remove("citation")

            # If the 'citation' category was removed, changes have been made
            if citation_removed:
                changes_made = True

    return myContainerList, changes_made


def remove_sfhead(myContainerList, remove_list):
    changes_made = False
    for i in remove_list:
        removed_flag = myContainerList.remove(i)
        if removed_flag:
            changes_made = True

    return myContainerList, changes_made