from mmcif.io.PdbxReader import PdbxReader

def get_items_pdb(pdbfile):
    myContainerList = []

    # read data from file
    with open(pdbfile, "r") as ifh:
        pRd = PdbxReader(ifh)
        pRd.read(myContainerList)

    # define the container
    container = myContainerList[0]
    
    # get attributes
    header_obj = container.getObj("entry")
    reflns_obj = container.getObj("reflns")
    cell_obj = container.getObj("cell")
    exptl_obj = container.getObj("exptl")
    
    # extract necessary information
    pdb_id = header_obj.getValue("id")
    
    WAVE = float(reflns_obj.getValue("wavelength")) if reflns_obj.hasAttribute("wavelength") else None
    NFREE = int(reflns_obj.getValue("test_set_count")) if reflns_obj.hasAttribute("test_set_count") else None
    RESOH = float(reflns_obj.getValue("d_resolution_high")) if reflns_obj.hasAttribute("d_resolution_high") else None
    RESOL = float(reflns_obj.getValue("d_resolution_low")) if reflns_obj.hasAttribute("d_resolution_low") else None
    FREERV = reflns_obj.getValue("free_R_factor") if reflns_obj.hasAttribute("free_R_factor") else None

    CELL = [float(cell_obj.getValue(x)) for x in ['length_a', 'length_b', 'length_c', 'angle_alpha', 'angle_beta', 'angle_gamma']]
    SYMM = exptl_obj.getValue("crystal_system") if exptl_obj.hasAttribute("crystal_system") else None

    return pdb_id, WAVE, NFREE, RESOH, RESOL

print(get_items_pdb("1o08.cif"))