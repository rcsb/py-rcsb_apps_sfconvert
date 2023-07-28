import re
def get_items_pdb(filename):
    # Initiate the variables
    pdb_id = None
    wave = None
    nfree = None
    resoh = None
    resol = None
    freerv = None
    cell = [None]*6
    symm = None

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('HEADER'):
                pdb_id = line[61:66].strip().lower()

            elif 'REMARK 200  WAVELENGTH OR RANGE        (A) :' in line:
                wave = float(line.split(':')[1].strip())
                if wave > 3.0 or (wave < 0.6 and wave > 0.01):
                    print(f"Warning:  wavelength ({wave}) in coord. is abnormal (double check)!")

            elif 'FREE R VALUE TEST SET COUNT   (NO CUTOFF)' in line:
                nfree = int(re.search(r'\d+', line.split(':')[1]).group())

            elif 'RESOLUTION RANGE HIGH (ANGSTROMS)' in line:
                resoh = float(re.search(r'[-+]?\d*\.\d+|\d+', line.split(':')[1]).group())

            elif 'RESOLUTION RANGE LOW  (ANGSTROMS)' in line:
                resol = float(re.search(r'[-+]?\d*\.\d+|\d+', line.split(':')[1]).group())

            elif 'REMARK   test_flag_value:' in line and freerv is None:
                freerv = line.split(':')[1].strip()

            elif line.startswith('CRYST1'):
                cell_values = line[6:].split()[:6]
                cell = [float(val) for val in cell_values]
                symmetry_in = line[54:64].strip()
                symm = symmetry_in  # you need to define this function

                # after getting the cell and symmetry data, we can break from the loop
                break

    return {'pdb_id': pdb_id, 'RESOH': resoh, 'RESOL': resol, 'FREERV': freerv, 
            'WAVE': wave, 'NFREE': nfree, 'SYMM': symm, 'CELL': cell}

# Test the function with the provided PDB file

# Test the function with the provided PDB file
print(get_items_pdb('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/RCSB/1o08.pdb'))
