import gemmi

SFCIF_PATH = '/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/tests/data/cif_files/1o08-sf.cif'
cif_doc = gemmi.cif.read(SFCIF_PATH)
rblock = gemmi.as_refln_blocks(cif_doc)[0]

cif2mtz = gemmi.CifToMtz()
mtz = cif2mtz.convert_block_to_mtz(rblock)

# Save the MTZ object to a file
mtz.write_to_file('output.mtz')