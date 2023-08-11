from sf_convert.utils.pinfo_file import pinfo
from mmcif.api.DataCategoryBase import DataCategoryBase


def reformat_sfhead(sf_file, DETAIL=None):
    # myContainerList = []
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

    attributes_to_append = {
        "_diffrn": {
            "ambient_temp": "?",
            "crystal_treatment": "?"
        }
    }

    # Perform the renaming of attributes
    changes_made |= rename_sfhead(sf_file, mapping_dicts)

    # Perform the removal of categories
    changes_made |= remove_sfhead(sf_file, remove_list)

    # Perform the removal of duplicate reflections
    changes_made |= remove_duplicate_reflections(sf_file)

    # changes_made |= append_attributes(sf_file, attributes_to_append)
    # changes_made = sf_file.add_attributes_to_category("diffrn", attributes_to_append)


    block_names = sf_file.get_all_block_names()
    for i in range(len(block_names)):
        old_order = sf_file.get_category_names(block_names[i])

        old_order_copy = old_order[:]

        attributes_to_append = ["ambient_temp", "crystal_treatment"]

        changes_made = append_attributes(sf_file, "diffrn", attributes_to_append, block_names[i])

        if(DETAIL):
            changes_made = modify_attribute_value(sf_file, "diffrn", "details", DETAIL, block_names[i])
            changes_made = modify_attribute_value(sf_file, "diffrn", "crystal_id", 1, block_names[i])

        sf_file.reorder_category_attributes("diffrn", ["id", "crystal_id", "ambient_temp", "crystal_treatment", "details"], block_names[i])

        sf_file.reorder_categories_in_block(old_order_copy, block_names[i])

    return changes_made

def rename_sfhead(sf_file, mapping_dicts):
    changes_made = False
    for dict_name, mapping_dict in mapping_dicts.items():
        for block_index in range(sf_file.get_number_of_blocks()):
            block = sf_file.get_block_by_index(block_index)
            category_object = sf_file.get_category_object(dict_name, block.getName())
            if category_object:
                attributeList = category_object.getAttributeList()
                renameDict = {}
                for attr in attributeList:
                    if attr in mapping_dict:
                        renameDict[attr] = mapping_dict[attr]
                if renameDict:
                    changes_made = True
                    for old_name, new_name in renameDict.items():
                        pinfo(f"Renaming {old_name} to {new_name} in {dict_name} category of block {block.getName()}", 0)
                category_object.renameAttributes(renameDict)
    return changes_made

def remove_sfhead(sf_file, remove_list):
    changes_made = False
    for item in remove_list:
        for block_index in range(sf_file.get_number_of_blocks()):
            block = sf_file.get_block_by_index(block_index)
            removed_flag = sf_file.remove_category_by_name(item, block.getName())
            if removed_flag:
                changes_made = True
                pinfo(f"Removing {item} category from block {block.getName()}", 0)
    return changes_made

def remove_duplicate_reflections(sf_file):
    changes_made = False
    total_blocks = sf_file.get_number_of_blocks()
    for block_index in range(total_blocks):
        block = sf_file.get_block_by_index(block_index)
        #print(f"Checking duplicates from block {block_index + 1}/{total_blocks}")
        changes_made |= sf_file.remove_duplicates_in_category('refln', block.getName())
    return changes_made

def append_attributes(sf_file, category_name, attributes, block_name=None):
    """
    Appends specified attributes to a category within a block using appendAttributeExtendRows.

    Parameters:
    - sf_file (StructureFactorFile): The structure factor file object.
    - category_name (str): Name of the category to which attributes should be appended.
    - attributes (list): List of attributes to append.
    - block_name (str, optional): Name of the block to which attributes should be appended.
                                If not provided, the default block is used.

    Returns:
    bool: True if any changes were made, False otherwise.
    """
    changes_made = False

    # Get the block (use default block if block_name is None)
    if block_name:
        _, block = sf_file.get_block_by_name(block_name)
    else:
        block = sf_file.get_block_by_index(sf_file.get_default_block_index())
    
    if not block:
        return changes_made

    category = block.getObj(category_name)
    # If category doesn't exist, create it
    if not category:
        category = DataCategoryBase(category_name)
        block.append(category)
        changes_made = True

    # Check each attribute and append if not present
    for attr_name in attributes:
        if not category.hasAttribute(attr_name):
            category.appendAttributeExtendRows(attr_name)
            changes_made = True

    return changes_made

def modify_attribute_value(sf_file, category_name, attribute_name, new_value, block_name=None):
    """
    Modifies the value of a specified attribute in a given category within a block using replaceValue. 
    Automatically fetches the old value from the file using getValueOrDefault.

    Parameters:
    - sf_file (StructureFactorFile): The structure factor file object.
    - category_name (str): Name of the category containing the attribute.
    - attribute_name (str): Name of the attribute to modify.
    - new_value (str): The new value to set for the attribute.
    - block_name (str, optional): Name of the block containing the category.
                                  If not provided, the default block is used.

    Returns:
    bool: True if the value was modified, False otherwise (e.g., if the attribute or category doesn't exist).
    """
    # Get the block (use default block if block_name is None)
    if block_name:
        _, block = sf_file.get_block_by_name(block_name)
    else:
        block = sf_file.get_block_by_index(sf_file.get_default_block_index())
    
    if not block:
        return False

    category = block.getObj(category_name)
    # If category doesn't exist, return False
    if not category:
        return False

    # Fetch the old value using getValueOrDefault
    old_value = category.getValueOrDefault(attribute_name, rowIndex=0, defaultValue=".")
    # print(f"Old value: {old_value}")
    if old_value is not None:
        # Replace the old value with the new value
        num_replaced = category.replaceValue(old_value, new_value, attribute_name)
        return num_replaced > 0

    return False


# from sf_file import StructureFactorFile

# # Initialize a StructureFactorFile object and read data from a file
# sf_file = StructureFactorFile()
# sf_file.read_file('5pny-sf.cif')

# # Perform the reformatting
# changes_made = reformat_sfhead(sf_file)

# # Check if any changes were made
# if changes_made:
#     # Write the modified data back to a file
#     sf_file.write_file('example_modified.cif')
# else:
#     print("No changes were made to the structure factor file.")
