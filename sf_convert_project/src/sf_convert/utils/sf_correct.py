# Utilities to correct imported CIF files

from mmcif.api.DataCategory import DataCategory

from sf_convert.utils.reformat_sfhead import reformat_sfhead, reorder_sf_file


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
                logger("Error: trying to set wavelength to non float", 0)

            if curwave:
                if curwave not in ["?", "."]:
                    try:
                        wave = float(curwave)
                        if wave > 2.0 or wave < 0.6:
                            logger.pinfo(f"Warning: ({pdb_id} nblock={idx} wavelength value (curwave) is abnormal (double check)!", 0)
                    except ValueError:
                        logger.pinfo(f"Wavelength not a float {curwave}", 0)

                    if setwl != ".":
                        if setwlf > 0.8 and setwlf < 1.8 and setwlf != 1.0:
                            if abs(setwlf - wave) > 0.0001 and idx == 0:
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
                wl = setwlarg if setwlarg else "."

                if cObj and "wavelength_id" in cObj.getAttributeList():
                    values = cObj.getAttributeUniqueValueList("wavelength_id")
                    data = []
                    for val in values:
                        data.append([val, wl])
                else:
                    data = [["1", wl]]

                newObj = DataCategory(cat, ["id", "wavelength"], data)
                blk.append(newObj)
                logger.pinfo(f"Creating {cat} in nblock={idx}", 0)

    def __instantiate_diffrn_rad_wavelength(self, sffile, logger):
        """Instantiate diffrn_radiation_wavelength if needed.  In case wavelength is not set, but needed for dictionary purposes"""

        cat = "diffrn_radiation_wavelength"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj(cat)
            if cObj:
                continue

            # Instantiate if needed
            cObj = blk.getObj("refln")
            if not cObj:
                continue
            if "wavelength_id" not in cObj.getAttributeList():
                continue

            values = cObj.getAttributeUniqueValueList("wavelength_id")

            data = []
            for val in values:
                data.append([val, "."])

            newObj = DataCategory(cat, ["id", "wavelength"], data)
            blk.append(newObj)
            logger.pinfo(f"Creating {cat} in nblock={idx}", 0)

    def handle_standard(self, sffile, pdbid, logger):
        """Handles standard operations"""

        detail = None
        self.__update_exptl_crystal(sffile, logger)

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

        if self.__legacy:
            self.__cleanup_symmetry(sffile)

        self.__ensure_catkeys(sffile, pdbid)

        self.__instantiate_exptl_crystal(sffile)

        self.__instantiate_entry(sffile, pdbid)

        self._cleanup_audit(sffile, logger)

        # This reorders categories as well
        reformat_sfhead(sffile, pdbid, logger, detail)

        # Reflns names might have been modified
        self.__handle_reflns(sffile, logger)

        self.__handle_diffrn(sffile, pdbid, logger, details=detail)

        self.__instantiate_diffrn_rad_wavelength(sffile, logger)

        sffile.correct_block_names(pdbid)

        # In case some blocks need updating
        self.__reorder_refln_all(sffile)

        self.__reorder_symmetry(sffile)

        self.__reorder_sf_file(sffile)

    def __handle_legacy_attributes(self, sffile):
        """ Adds in _refln.crystal_id, refln.wavelength_id and refln.scale_group_code if need be"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            # For new data coming from staraniso, these attributes are not added
            if "pdbx_audit_conform" in blk.getObjNameList():
                continue

            cObj = blk.getObj("refln")
            if not cObj:
                continue

            for attr in ["crystal_id", "wavelength_id", "scale_group_code"]:
                if attr not in cObj.getAttributeList():
                    cObj.appendAttributeExtendRows(attr, "1")

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

    def ensure_catkeys(self, sffile, pdbid):
        """Fix entry_id in categories - public"""
        self.__ensure_catkeys(sffile, pdbid)

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

    def __cleanup_symmetry(self, sffile):
        """If symmetry is present, we only allow entry_id and space_group_name_H-M"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "symmetry" not in blk.getObjNameList():
                continue

            cObj = blk.getObj("symmetry")

            attrlist = list(cObj.getAttributeList())  # ensure not an iterator that might get changed

            for attr in attrlist:
                if attr not in ["entry_id", "space_group_name_H-M", "Int_Tables_number"]:
                    cObj.removeAttribute(attr)

            # Remove "empty" category
            attrlist = cObj.getAttributeList()
            if len(attrlist) == 0 or attrlist == ["entry_id"]:
                blk.remove("symmetry")

    def __handle_diffrn(self, sffile, pdbid, logger, details=None):  # pylint: disable=unused-argument
        """Instantiate diffrn category if needed, see diffrn.id if needed."""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            # Assemble list of possible diffrn_ids needed

            # Get diffrn ids if present...
            difids = set()

            needdiffrn = False
            for cat in ["diffrn_refln", "diffrn_radiation", "diffrn_reflns"]:
                if cat in blk.getObjNameList():
                    cObj2 = blk.getObj(cat)
                    if "diffrn_id" in cObj2.getAttributeList():
                        values = cObj2.getAttributeUniqueValueList("diffrn_id")
                        difids.update(values)
                        needdiffrn = True

            if len(difids) == 0:
                difids.add("1")
            diffidsl = sorted([int(x) for x in list(difids)])

            # Crystal id
            if "refln" in blk.getObjNameList():
                cObj2 = blk.getObj("refln")
                if "crystal_id" not in cObj2.getAttributeList():
                    crystids = ["1"]
                else:
                    crystids = cObj2.getAttributeUniqueValueList("crystal_id")

            # If we need to instantiate do it
            if "diffrn" not in blk.getObjNameList() and needdiffrn is False and details is None:
                continue

            cObj = blk.getObj("diffrn")
            if cObj is None:
                # Instantiate category
                rows = []
                if details is None:
                    details = "?"
                for d in diffidsl:
                    for c in crystids:
                        rows.append([d, c, details])
                newObj = DataCategory("diffrn", ["id", "crystal_id", "details"], rows)
                blk.append(newObj)
                continue

            # Update existing copy
            # XXX Someday - instantiate all values
            if "id" not in cObj.getAttributeList():
                cObj.appendAttributeExtendRows("id", diffidsl[0])
            if "crystal_id" not in cObj.getAttributeList():
                cObj.appendAttributeExtendRows("crystal_id", crystids[0])
            if details and "details" not in cObj.getAttributeList():
                cObj.appendAttributeExtendRows("details", details)

            sffile.reorder_category_attributes("diffrn", ["id", "crystal_id", "ambient_temp", "crystal_treatment", "details"], blk.getName())

    def _cleanup_audit(self, sffile, logger):
        """Cleanup audit records that should not be present

        Args:
            sffile (StructureFactorFile): The structure factor file object.
            logger: The logger object for logging messages.

        Returns:
            None: True if the value was modified, False otherwise.
        """

        blk = sffile.get_block_by_index(0)

        cat = "audit"
        cObj = blk.getObj(cat)
        if cObj is None:
            return False

        curlist = cObj.getAttributeList()

        allowed = ["revision_id", "creation_date", "update_record"]

        upd = False
        for attr in curlist:
            if attr not in allowed:
                cObj.removeAttribute(attr)
                logger.pinfo(f"Warning: block has unwanted CIF item _{cat}.{attr} and is removed", 0)
                upd = True

        return upd

    def __handle_reflns(self, sffile, logger):  # pylint: disable=unused-argument
        """Handles reflns and diffrn_reflns data

        Assumption: diffrn_id is 1 if not provided

        diffrn_reflns and reflns are merged to diffrn_reflns
        """
        def get_val(attr_ref, attr_dif):
            val = None
            if cObjref and attr_ref in cObjref.getAttributeList():
                val = cObjref.getValue(attr_ref, 0)
            if val is None and cObjdif and attr_dif in cObjdif.getAttributeList():
                val = cObjdif.getValue(attr_dif, 0)

            return val

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObjdif = blk.getObj("diffrn_reflns")
            cObjref = blk.getObj("reflns")

            if cObjdif is None and cObjref is None:
                continue

            props = [["resh", "d_resolution_high", "pdbx_d_res_high"],
                     ["resl", "d_resolution_low", "pdbx_d_res_low"],
                     ["hmax", "limit_h_max", "limit_h_max"],
                     ["hmin", "limit_h_min", "limit_h_min"],
                     ["kmax", "limit_k_max", "limit_k_max"],
                     ["kmin", "limit_k_min", "limit_k_min"],
                     ["lmax", "limit_l_max", "limit_l_max"],
                     ["lmin", "limit_l_min", "limit_l_min"],
                     ["nall", "number_all", "number"],
                     ["nobs", "number_obs", "pdbx_number_obs"],
                     ]

            data = {}
            for p in props:
                k = p[0]
                rk = p[1]
                rd = p[2]
                val = get_val(rk, rd)
                if val:
                    data[k] = val

            if not data.get("resh", None) and not data.get("nall", None) and not data.get("nobs", None):
                continue

            if cObjref:
                blk.remove("reflns")

            create = False
            if cObjdif is None:
                cObjdif = DataCategory("diffrn_reflns")
                create = True

            if "diffrn_id" not in cObjdif.getAttributeList():
                # appendAttributeExtendRows must have data to use or will not set - until some data present
                cObjdif.appendAttributeExtendRows("diffrn_id")
                cObjdif.setValue("1", "diffrn_id", 0)

            for p in props:
                k = p[0]
                rd = p[2]
                if k in data:
                    val = data[k]
                    if rd in cObjdif.getAttributeList():
                        cObjdif.setValue(val, rd, 0)
                    else:
                        cObjdif.appendAttributeExtendRows(rd, val)

            if create:
                blk.append(cObjdif)

    def __reorder_sf_file(self, sffile):
        """Reorders sf_file"""
        reorder_sf_file(sffile)

    def reorder_sf_file(self, sffile):
        """Reorders sf_file"""
        self.__reorder_sf_file(sffile)

    def __update_exptl_crystal(self, sf_file, logger):  # pylint: disable=unused-argument
        """If exptl_crystal present, remove everything but id

           Args:
              sf_file (StructureFactorFile): The structure factor file object.
              logger: The logger object for logging messages.

           Returns:
              bool: True if the value was modified, False otherwise.
        """
        modified = False
        for idx in range(sf_file.get_number_of_blocks()):
            blk = sf_file.get_block_by_index(idx)

            cObj = blk.getObj("exptl_crystal")
            if not cObj:
                continue

            attrNames = cObj.getAttributeList()
            # We do not want to to be updating while removing
            for attr in attrNames:
                if attr not in ["id"]:
                    modified = True
                    cObj.removeAttribute(attr)

            if len(cObj.getAttributeList()) == 0:
                blk.remove("exptl_crystal")
                modified = True

        return modified

    def __reorder_refln_all(self, sffile):
        """Reorders refln category for all blocks"""
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("refln")
            if not cObj:
                continue

            sffile.reorder_category_attributes("refln", self.__stdorder, blk.getName())

    def __reorder_symmetry(self, sffile):
        """Reorders symmetry category for all blocks"""
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("symmetry")
            if not cObj:
                continue

            sffile.reorder_category_attributes("symmetry", ["entry_id", "space_group_name_H-M", "Int_Tables_number"], blk.getName())

    def correct_cell_precision(self, sffile):
        """We limit cell to 3 significant digits

           Used with non cif2cif
        """

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("cell")
            if not cObj:
                continue

            alist = ["length_a", "length_b", "length_c",
                     "angle_alpha", "angle_beta", "angle_gamma"]

            attrlist = cObj.getAttributeList()

            for attr in alist:
                if attr in attrlist:
                    try:
                        val = float(cObj.getValue(attr, 0))
                        val = f"{val:.3f}"
                        cObj.setValue(str(val), attr, 0)
                    except ValueError:
                        # Ignore
                        pass

    def set_cell(self, sffile, cell):
        """Sets the unit cell -- assumption all blocks"""

        assert len(cell) == 6

        alist = ["length_a", "length_b", "length_c",
                 "angle_alpha", "angle_beta", "angle_gamma"]

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("cell")

            create = False
            if not cObj:
                cObj = DataCategory("cell", alist)
                create = True

            # Delete unknown
            attrlist = cObj.getAttributeList()

            for attr in alist:
                if attr not in attrlist:
                    cObj.removeAttribute(attr)

            # Now set
            attrlist = cObj.getAttributeList()
            for idx, attr in enumerate(alist):
                if attr not in attrlist:
                    cObj.appendAttributeExtendRows(attr, cell[idx])
                else:
                    cObj.setValue(cell[idx], attr, 0)

            if create:
                blk.append(cObj)

    def cleanup_extra_audit(self, sffile, logger):
        """Removes extra audit records from second and more blocks"""

        cat = "audit"
        for block_index in range(1, sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            if cat in blk.getObjNameList():
                blk.remove(cat)
                logger.pinfo(f"Removing {cat} category from block {blk.getName()}", 0)
