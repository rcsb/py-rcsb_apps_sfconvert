def get_items_pdb(sffile):    
    # define the container
    #container = myContainerList[0]
    container = sffile.getBlockByIndex(0)
    
    # get attributes
    header_obj = container.getObj("entry")
    reflns_obj = container.getObj("reflns")
    #diffrn_obj = container.getObj("diffrn_radiation_wavelength")
    diffrn_radiation_wavelength_obj = container.getObj("diffrn_radiation_wavelength")
    #pdbx_refine.free_R_val_test_set_ct_no_cutoff
    pdbx_refine_obj = container.getObj("pdbx_refine")
    cell_obj = container.getObj("cell")
    exptl_obj = container.getObj("exptl")
    #symmetry.space_group_name_H-M 
    symmetery_obj = container.getObj("symmetry")
    
    # extract necessary information
    pdb_id = header_obj.getValue("id")
    
    #WAVE = float(reflns_obj.getValue("wavelength")) if reflns_obj.hasAttribute("wavelength") else None
    #WAVE = float(diffrn_obj.getValue("radiation_wavelength")) if diffrn_obj.hasAttribute("radiation_wavelength") else None
    WAVE = float(diffrn_radiation_wavelength_obj.getValue("wavelength")) if diffrn_radiation_wavelength_obj.hasAttribute("wavelength") else None
    #NFREE = int(reflns_obj.getValue("test_set_count")) if reflns_obj.hasAttribute("test_set_count") else None
    NFREE = int(pdbx_refine_obj.getValue("free_R_val_test_set_ct_no_cutoff")) if pdbx_refine_obj.hasAttribute("free_R_val_test_set_ct_no_cutoff") else None
    RESOH = float(reflns_obj.getValue("d_resolution_high")) if reflns_obj.hasAttribute("d_resolution_high") else None
    RESOL = float(reflns_obj.getValue("d_resolution_low")) if reflns_obj.hasAttribute("d_resolution_low") else None
    FREERV = reflns_obj.getValue("free_R_factor") if reflns_obj.hasAttribute("free_R_factor") else None
    # Need to check FREERV

    CELL = [float(cell_obj.getValue(x)) for x in ['length_a', 'length_b', 'length_c', 'angle_alpha', 'angle_beta', 'angle_gamma']]
    #SYMM = exptl_obj.getValue("crystal_system") if exptl_obj.hasAttribute("crystal_system") else None
    SYMM = symmetery_obj.getValue("space_group_name_H-M") if symmetery_obj.hasAttribute("space_group_name_H-M") else None

    return pdb_id, WAVE, NFREE, RESOH, RESOL, FREERV, CELL, SYMM

#print(get_items_pdb("1o08.cif"))