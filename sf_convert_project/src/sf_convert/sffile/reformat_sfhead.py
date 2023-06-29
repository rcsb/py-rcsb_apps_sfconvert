from mmcif.io.PdbxWriter import PdbxWriter
from mmcif.io.PdbxReader import PdbxReader

def reformat_sfhead(ifile, ofile):
    # CIF keys mapping
    ciflist = {
        "_refln.A_calc_au": "_refln.A_calc",
        "_refln.B_calc_au": "_refln.B_calc",
        "_refln.A_cal": "_refln.A_calc",
        "_refln.B_cal": "_refln.B_calc",
        "_refln.resolution": "_refln.d_spacing",
        "_refln.Fc_au": "_refln.F_calc_au",
        "_refln.F_sigma": "_refln.F_meas_sigma_au",
        "_refln.F_meas_au_sigma": "_refln.F_meas_sigma_au",
        "_refln.F_squared_meas_sigma": "_refln.F_squared_sigma",
        "_refln.I_meas_au": "_refln.intensity_meas",
        "_refln.intensity": "_refln.intensity_meas",
        "_refln.intensity_meas_au": "_refln.intensity_meas",
        "_refln.intensity_sigm": "_refln.intensity_sigma",
        "_refln.I_meas_sigma_au": "_refln.intensity_sigma",
        "_refln.intensity_sigma_au": "_refln.intensity_sigma",
        "_refln.intensity_meas_sigma": "_refln.intensity_sigma",
        "_refln.intensity_meas_sigma_au": "_refln.intensity_sigma",
        "_refln.dfano": "_refln.pdbx_anom_difference",
        "_refln.DF_anomalous": "_refln.pdbx_anom_difference",
        "_refln.ccp4_phase_anom": "_refln.pdbx_anom_difference",
        "_refln.pdbx_phase_anom": "_refln.pdbx_anom_difference",
        "_refln.ccp4_anomalous_diff": "_refln.pdbx_anom_difference",
        "_refln.ccp4_SAD_phase_anom": "_refln.pdbx_anom_difference",
        "_refln.pdbx_anomalous_diff": "_refln.pdbx_anom_difference",
        "_refln.pdbx_SAD_phase_anom": "_refln.pdbx_anom_difference",
        "_refln.pdbx_anomalous_meas_au": "_refln.pdbx_anom_difference",
        "_refln.I_ano_meas": "_refln.pdbx_anom_difference",
        "_refln.I_ano_sigma": "_refln.pdbx_anom_difference_sigma",
        "_refln.DF_anomalous_sigma": "_refln.pdbx_anom_difference_sigma",
        "_refln.ccp4_phase_anom_sigma": "_refln.pdbx_anom_difference_sigma",
        "_refln.pdbx_phase_anom_sigma": "_refln.pdbx_anom_difference_sigma",
        "_refln.ccp4_anomalous_diff_sigma": "_refln.pdbx_anom_difference_sigma",
        "_refln.ccp4_SAD_phase_anom_sigma": "_refln.pdbx_anom_difference_sigma",
        "_refln.pdbx_SAD_phase_anom_sigma": "_refln.pdbx_anom_difference_sigma",
        "_refln.pdbx_anomalous_meas_sigma_au": "_refln.pdbx_anom_difference_sigma",
        "_refln.F-_meas_au": "_refln.pdbx_F_minus",
        "_refln.pdbx_F_meas_minus": "_refln.pdbx_F_minus",
        "_refln.ccp4_F_meas_minus_au": "_refln.pdbx_F_minus",
        "_refln.pdbx_F_meas_minus_au": "_refln.pdbx_F_minus",
        "_refln.ccp4_SAD_F_meas_minus_au": "_refln.pdbx_F_minus",
        "_refln.F-_meas_sigma_au": "_refln.pdbx_F_minus_sigma",
        "_refln.pdbx_F_meas_minus_sigma": "_refln.pdbx_F_minus_sigma",
        "_refln.ccp4_F_meas_minus_sigma_au": "_refln.pdbx_F_minus_sigma",
        "_refln.pdbx_F_meas_minus_sigma_au": "_refln.pdbx_F_minus_sigma",
        "_refln.ccp4_SAD_F_meas_minus_sigma_au": "_refln.pdbx_F_minus_sigma",
        "_refln.F+_meas_au": "_refln.pdbx_F_plus",
        "_refln.pdbx_F_meas_plus": "_refln.pdbx_F_plus",
        "_refln.ccp4_F_meas_plus_au": "_refln.pdbx_F_plus",
        "_refln.pdbx_F_meas_plus_au": "_refln.pdbx_F_plus",
        "_refln.ccp4_SAD_F_meas_plus_au": "_refln.pdbx_F_plus",
        "_refln.F+_meas_sigma_au": "_refln.pdbx_F_plus_sigma",
        "_refln.pdbx_F_meas_plus_sigma": "_refln.pdbx_F_plus_sigma",
        "_refln.ccp4_F_meas_plus_sigma_au": "_refln.pdbx_F_plus_sigma",
        "_refln.pdbx_F_meas_plus_sigma_au": "_refln.pdbx_F_plus_sigma",
        "_refln.ccp4_SAD_F_meas_plus_sigma_au": "_refln.pdbx_F_plus_sigma",
        "_refln.pdbx_HLA": "_refln.pdbx_HL_A_iso",
        "_refln.ccp4_HL_A_iso": "_refln.pdbx_HL_A_iso",
        "_refln.ccp4_SAD_HL_A_iso": "_refln.pdbx_HL_A_iso",
        "_refln.pdbx_SAD_HL_A_iso": "_refln.pdbx_HL_A_iso",
        "_refln.pdbx_HLB": "_refln.pdbx_HL_B_iso",
        "_refln.ccp4_HL_B_iso": "_refln.pdbx_HL_B_iso",
        "_refln.ccp4_SAD_HL_B_iso": "_refln.pdbx_HL_B_iso",
        "_refln.pdbx_SAD_HL_B_iso": "_refln.pdbx_HL_B_iso",
        "_refln.pdbx_HLC": "_refln.pdbx_HL_C_iso",
        "_refln.ccp4_HL_C_iso": "_refln.pdbx_HL_C_iso",
        "_refln.ccp4_SAD_HL_C_iso": "_refln.pdbx_HL_C_iso",
        "_refln.pdbx_SAD_HL_C_iso": "_refln.pdbx_HL_C_iso",
        "_refln.pdbx_HLD": "_refln.pdbx_HL_D_iso",
        "_refln.ccp4_HL_D_iso": "_refln.pdbx_HL_D_iso",
        "_refln.ccp4_SAD_HL_D_iso": "_refln.pdbx_HL_D_iso",
        "_refln.pdbx_SAD_HL_D_iso": "_refln.pdbx_HL_D_iso",
        "_refln.ccp4_I_minus": "_refln.pdbx_I_minus",
        "_refln.ccp4_I_minus_sigma": "_refln.pdbx_I_minus_sigma",
        "_refln.ccp4_I_plus": "_refln.pdbx_I_plus",
        "_refln.ccp4_I_plus_sigma": "_refln.pdbx_I_plus_sigma",
        "_refln.pahse_calc": "_refln.phase_calc",
        "_refln.F.phase_calc": "_refln.phase_calc",
        "_refln.phase_au": "_refln.phase_meas",
        "_refln.sgx_fmap": "_refln.pdbx_FWT",
        "_refln.pdbx_fom_weighted_fmap": "_refln.pdbx_FWT",
        "_refln.statu": "_refln.status",
        "_refln.F_status": "_refln.status",
        "_refln.status_au": "_refln.status",
        "_refln.R_free_flag": "_refln.status",
        "_refln.phenix_R_free_flags": "_refln.pdbx_r_free_flag",
        "_refln.observed_status": "_refln.status",
        "_refln.waveLEngth_id": "_refln.wavelength_id",
        "_refln.wavelength_di": "_refln.wavelength_id",
        "_refln.index_l>": "_refln.index_l",
        "_refln.fiber_coordinate": "_refln.pdbx_fiber_coordinate",
        "_refln.fiber_F_meas_au": "_refln.pdbx_fiber_F_meas_au",
        "_refln.fiber_layer": "_refln.pdbx_fiber_layer",
        "_audit.update_recor": "_audit.update_record",
        "_cell.enrty_id": "_cell.entry_id",
        "_cell.enry_id": "_cell.entry_id",
        "_cell.entry": "_cell.entry_id",
        "_cell_entry.id": "_cell.entry_id",
        "_cell.entry.id": "_cell.entry_id",
        "_cell.ndb_unique_axis": "_cell.pdbx_unique_axis",
        "_diffrn.detail": "_diffrn.details",
        "_diffrn_radiation.id": "_diffrn_radiation.diffrn_id",
        "_pdbx_powder_refln.d_spacing": "_refln.d_spacing",
        "_pdbx_powder_refln.F_squared_calc": "_refln.F_squared_calc",
        "_pdbx_powder_refln.F_squared_meas": "_refln.F_squared_meas",
        "_pdbx_powder_refln.gsas_i100_meas": "_refln.pdbx_gsas_i100_meas",
        "_pdbx_powder_refln.index_h": "_refln.index_h",
        "_pdbx_powder_refln.index_k": "_refln.index_k",
        "_pdbx_powder_refln.index_l": "_refln.index_l",
        "_pdbx_powder_refln.observed_status": "_refln.status",
        "_pdbx_powder_refln.phase_calc": "_refln.phase_calc",
        "_radiation.id": "_diffrn_radiation.diffrn_id",
        "__symmetry.entry_id": "_symmetry.entry_id",
        "_symmetry.int_tables_number": "_symmetry.Int_Tables_number",
        "_symmetry.ndb_full_space_group_name_H-M": "_symmetry.space_group_name_H-M",
        "_symmetry.space_group_name_h-m": "_symmetry.space_group_name_H-M",
        "_refln_index_h": "_refln.index_h",
        "_refln_index_k": "_refln.index_k",
        "_refln_index_l": "_refln.index_l",
        "_refln.F_squared_meas": "_refln.intensity_meas",
        "_refln.F_squared_sigma": "_refln.intensity_sigma",
        "_refln_F_squared_meas": "_refln.F_squared_meas",
        "_refln_F_squared_sigma": "_refln.F_squared_sigma",
        "_refln_F_calc": "_refln.F_calc",
        "_refln_observed_status": "_refln.status",
        "_refln_F_squared_calc": "_refln.F_squared_calc",
        "_refln_phase_calc": "_refln.phase_calc",
        "_refln_d_spacing": "_refln.d_spacing",
        "_gsas_i100_meas": "_refln.pdbx_gsas_i100_meas",
        "_refln.gsas_i100_meas": "_refln.pdbx_gsas_i100_meas",
        "_pd_meas_intensity_total": "_pdbx_powder_data.pd_meas_intensity_total",
        "_pd_proc_intensity_total": "_pdbx_powder_data.pd_proc_intensity_total",
        "_pd_proc_ls_weight": "_pdbx_powder_data.pd_proc_ls_weight",
        "_pd_proc_intensity_bkg_calc": "_pdbx_powder_data.pd_proc_intensity_bkg_calc",
        "_pd_calc_intensity_total": "_pdbx_powder_data.pd_calc_intensity_total"
    }

    # Initialize a container list
    myContainerList = []

    # Initialize a flag to track if changes have been made
    changes_made = False

    # Attempt to read data from the input file
    try:
        # Open the input file in read mode
        with open(ifile, "r") as ifh:
            # Create a new PdbxReader object with the input file handle
            pRd = PdbxReader(ifh)
            # Read the data from the input file into the container list
            pRd.read(myContainerList)
            
    # If an error occurs, print an error message
    except Exception as e:
        print("An error occurred:", str(e))

    # Loop through each container in the container list
    for container in myContainerList:

        # Get the 'reflns' object from the container
        cobj = container.getObj("reflns")

        # If the 'reflns' object exists
        if cobj:

            # Get the attribute list from the 'reflns' object
            attributeList = cobj.getAttributeList()

            # Initialize an empty dictionary to store the renamed attributes
            renameDict = {}

            # Loop through each attribute in the attribute list
            for attr in attributeList:
                # If the attribute is in the ciflist
                if attr in ciflist:
                    # Add the attribute and its corresponding value from ciflist to the rename dictionary
                    renameDict[attr] = ciflist[attr]
            
            # If the rename dictionary is not empty, changes have been made
            if renameDict:
                changes_made = True

            # Rename the attributes in the 'reflns' object using the rename dictionary
            cobj.renameAttributes(renameDict)

        # Attempt to remove the 'citation' category from the container
        citation_removed = container.remove("citation")

        # If the 'citation' category was removed, changes have been made
        if citation_removed:
            changes_made = True

    # If changes were made
    if changes_made:

        # Open the output file in write mode
        with open(ofile, "w") as ofh:

            # Create a new PdbxWriter object with the output file handle
            pWd = PdbxWriter(ofh)

            # Write the data from the container list to the output file
            pWd.write(myContainerList)


reformat_sfhead("7xvx-sf.cif.mmcif", "7xvx-sf_test.cif.mmcif")