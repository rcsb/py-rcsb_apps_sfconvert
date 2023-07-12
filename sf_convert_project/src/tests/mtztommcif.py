import gemmi

def convert_mtz_to_mmcif(mtz_file, mmcif_file):
    # Read MTZ file
    mtz = gemmi.read_mtz_file(mtz_file)

    
    print(type(mtz))

    # Convert MTZ to mmCIF
    cif_string = gemmi.MtzToCif().write_cif_to_string(mtz)

    # Write the mmCIF data to a file
    with open(mmcif_file, "w") as f:
        f.write(cif_string)

# Usage:
# convert_mtz_to_mmcif("input.mtz", "output.cif")

convert_mtz_to_mmcif("1N9F.mtz", "mmcif_File.mmcif")