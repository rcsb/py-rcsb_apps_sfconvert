# Utilities to correct imported CIF files

from mmcif.api.DataCategory import DataCategory

from sf_convert.utils.reformat_sfhead import reformat_sfhead, reorder_sf_file, update_exptl_crystal


class SfCorrect:
    def __init__(self, legacy=True):
        self.__legacy = legacy
        self.__stdorder = ["crystal_id", "wavelength_id", "scale_group_code",
                           "index_h", "index_k", "index_l", "status", "pdbx_r_free_flag",
                           "F_meas_au", "F_meas_sigma_au",
                           "intensity_calc", "intensity_meas", "intensity_sigma",
                           "F_calc", "F_calc_au",
                           "F_squared_meas", "F_squared_calc", "F_squared_sigma",
                           "phase_calc", "phase_meas",
                           "pdbx_I_plus", "pdbx_I_plus_sigma", "pdbx_I_minus", "pdbx_I_minus_sigma",
                           "pdbx_F_plus", "pdbx_F_plus_sigma", "pdbx_F_minus", "pdbx_F_minus_sigma",
                           "pdbx_HL_A_iso", "pdbx_HL_B_iso", "pdbx_HL_C_iso", "pdbx_HL_D_iso",
                           "pdbx_anom_difference", "pdbx_anom_difference_sigma",
                           "d_spacing", "A_calc", "B_calc",
                           "F_meas_sigma_uncorrected", "F_meas_uncorrected"
                           "pdbx_gsas_i100_meas",
                           "intensity_meas_unknown", "intensity_sigma_unknown",
                           "pdbx_phase_calc_part_solvent", "pdbx_F_calc_part_solvent", "pdbx_F_calc_with_solvent",
                           "pdbx_phase_calc_with_solvent",
                           "pdbx_FWT", "pdbx_PHWT", "pdbx_DELFWT", "pdbx_DELPHWT", "fom",                           
                           "pdbx_fiber_coordinate", "pdbx_fiber_F_meas_au", "pdbx_fiber_layer",
                           "weight",
                           ]
        
    def get_pdbid(self, sffile):
        """Returns the PDB id from datablock name of sf
        """
        return sffile.extract_pdbid_from_block()

    
    def annotate_wavelength(self, sffile, pdb_id, setwlarg, logger):
        """
        Handles addition of wavelength to the SF file if needed

        Args:
        sffile: SFFile object
        setlwarg: Wavelength to set
        logger: pfile object
        """

        cat = "diffrn_radiation_wavelength"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj(cat)
            if cObj:
                # Have wavelength
                curwave = cObj.getValue("wavelength", 0)
            else:
                curwave = None

            setwl = "."

            try:
                if setwlarg:
                    setwl = setwlarg
                    setwlf = float(setwlarg)
            except ValueError:
                logger(f"Error: trying to set wavelength to non integer", 0)
                
            if curwave:
                if curwave not in ["?", "."]:
                    try:
                        wave = float(curwave)
                        if wave > 2.0 or wave < 0.6:
                            logger.pinfo(f"Warning: ({pdb_id} nblock={idx} wavelength value (curwave) is abnormal (double check)!", 0);
                    except ValueError:
                        logger.pinfo(f"Wavelength not a float {curwave}", 0)

                    if setwl != ".":
                        if setwlf > 0.8 and setwlf < 1.8 and setwlf != 1.0:
                            if abs(setwlf - curwave) > 0.0001 and idx == 0:
                                logger.pinfo(f"Warning: ({pdb_id} nblock={idx}) wavelength mismatch (pdb= {setwlf} : sf= {curwave})!", 0)
                            elif setwlf > 0 and abs(setwlf - wave) > 0.0001 and idx == 0:
                                logger.pinfo("Warning: ({pdb_id} nblock={idx}) wavelength mismatch (pdb= {setwlf} : sf= {curwave}). (double check!)", 0)

                        # Set the values....
                        for row in range(cObj.getRowCount()):
                            cObj.setValue(setwl, "wavelength", row)

            else:
                # Create category - for dictionary compliance purposes. Might not be needed depending on data.
                # Decision to instantiate always for backwards compatibility - for potential outsider use.

                # Ensure proper values produced if existing data present
                cObj = blk.getObj("refln")
                if cObj and "wavelength_id" in cObj.getAttributeList():
                    values = cObj.getAttributeUniqueValueList("wavelength_id")
                    data = []
                    for val in values:
                        data.append([val, "."])
                else:
                    data = [["1", "."]]
                
                newObj = DataCategory(cat, ["id", "wavelength"], data)
                blk.append(newObj)
                logger.pinfo(f"Creating {cat} in nblock={idx}", 0)

    def handle_standard(self, sffile, pdbid, logger):
        """Handles standard operations"""

        detail = None
        update_exptl_crystal(sffile, logger)

        if self.__legacy:
            self.__remove_similar_refln_attr(sffile)
        
        if self.__legacy:
            self.__handle_legacy_attributes(sffile)

        self.__update_reflns_scale(sffile)

        if self.__legacy:
            self.__update_pdbx_r_free_flag(sffile)

        self.__update_status(sffile)

        if self.__legacy:
            self.__remove_categories(sffile)

        self.__ensure_catkeys(sffile, pdbid)
            
        self.__instantiate_exptl_crystal(sffile)

        self.__instantiate_entry(sffile, pdbid)
        
        sffile.correct_block_names(pdbid)

        reformat_sfhead(sffile, pdbid, logger, detail)


    def __handle_legacy_attributes(self, sffile):
        """ Adds in _refln.crystal_id, refln.wavelength_id and refln.scale_group_code if need be"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            added = False

            # For new data coming from staraniso, these attributes are not added
            if "pdbx_audit_conform" in blk.getObjNameList():
                continue

            cObj = blk.getObj("refln")
            if not cObj:
                continue
            
            for attr in ["crystal_id", "wavelength_id", "scale_group_code"]:
                if attr not in cObj.getAttributeList():
                    added = True
                    cObj.appendAttributeExtendRows(attr, "1")
            if added:
                self.__reorder_refln(sffile, blk.getName())
            
    def __reorder_refln(self, sffile, blockname):
        """Reorders the refln block"""
        sffile.reorder_category_attributes("refln", self.__stdorder, blockname)
        

    def __remove_similar_refln_attr(self, sffile):
        """ Remove common "similar" columns"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("refln")
            if not cObj:
                continue

            pairs = [[["F_meas_au", "F_meas_sigma_au"], ["F_meas", "F_meas_sigma"]],
                     ]

            attrlist = cObj.getAttributeList()
            for p in pairs:
                r1 = p[0]
                r2 = p[1]

                if r1[0] in attrlist and r1[1] in attrlist and r2[0] in attrlist and r2[1] in attrlist:
                    cObj.removeAttribute(r2[0])
                    cObj.removeAttribute(r2[1])
                
    
    def __update_reflns_scale(self, sffile):
        """ If reflns_scale missing in datablock add if needed"""

        cat = "reflns_scale"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if cat in blk.getObjNameList():
                continue

            if "refln" not in blk.getObjNameList():
                continue
            
            # See if need to instantiate
            cObj = blk.getObj("refln")
            if cObj and "scale_group_code" in cObj.getAttributeList():
                    values = cObj.getAttributeUniqueValueList("scale_group_code")
                    data = []
                    for val in values:
                        data.append([val])
                    newObj = DataCategory(cat, ["group_code"], data)
                    blk.append(newObj)
    
    def __update_pdbx_r_free_flag(self, sffile):
        """Old sf_convert used to use atoi(value) -- for "?" this converts to 0.  Luckily appears only for map coefficients
        """
        
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "refln" not in blk.getObjNameList():
                continue

            cObj = blk.getObj("refln")
            if cObj is None:
                continue  # should never happen
                
            if "pdbx_r_free_flag" in cObj.getAttributeList():
                cObj.replaceValue("?", "0", "pdbx_r_free_flag")

    def __update_status(self, sffile):
        """Old sf_convert used to use assume empty data is x.
        """
        
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "refln" not in blk.getObjNameList():
                continue

            cObj = blk.getObj("refln")
            if cObj is None:
                continue  # should never happen
                
            if "status" in cObj.getAttributeList():
                cObj.replaceValue("?", "x", "status")
                cObj.replaceValue(".", "x", "status")                
                
                        

    def __remove_categories(self, sffile):
        """Backwards compatibility - remove some categories"""

        cats = ["space_group", "space_group_symop"]
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            for cat in cats:
                if cat in blk.getObjNameList():
                    blk.remove(cat)
                    

    def __ensure_catkeys(self, sffile, pdbid):
        """Sometimes categories come in without the entry_id.  Add"""

        cats = ["cell", "symmetry"]

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            for cat in cats:
                if cat in blk.getObjNameList():
                    cObj = blk.getObj(cat)
                    if "entry_id" not in cObj.getAttributeList():
                        cObj.appendAttributeExtendRows("entry_id", pdbid)
                        # entry_id first in category
                        sffile.reorder_category_attributes(cat, ["entry_id"], blk.getName())

    def __instantiate_exptl_crystal(self, sffile):
        """If refln.crystal_id is present, exptl_crystal must be present"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "refln" in blk.getObjNameList():
                cObj = blk.getObj("refln")
                if "crystal_id" not in cObj.getAttributeList():
                    continue

                if "exptl_crystal" not in blk.getObjNameList():
                    values = cObj.getAttributeUniqueValueList("crystal_id")
                    data = []
                    for val in values:
                        data.append([val])

                    newObj = DataCategory("exptl_crystal", ["id"], data)
                    blk.append(newObj)


    
    def __instantiate_entry(self, sffile, pdb_id):
        """If entry category is not present, create"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "entry" not in blk.getObjNameList():
                newObj = DataCategory("entry", ["id"], [[pdb_id]])
                blk.append(newObj)