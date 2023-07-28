import re

class ProteinDataBank:
    def __init__(self):
        self.pdb_id = None
        self.RESOH = None
        self.RESOL = None
        self.FREERV = None
        self.WAVE = None
        self.NFREE = None
        self.CELL = None
        self.SYMM = None

    def extract_attributes_from_cif(self, sffile):
        container = sffile.getBlockByIndex(0)
        attributes = {
            'entry': [('id', 'pdb_id')],
            'reflns': [('d_resolution_high', 'RESOH'), ('d_resolution_low', 'RESOL'), ('free_R_factor', 'FREERV')],
            'diffrn_radiation_wavelength': [('wavelength', 'WAVE')],
            'pdbx_refine': [('free_R_val_test_set_ct_no_cutoff', 'NFREE')],
            'cell': [('length_a', 'CELL_a'), ('length_b', 'CELL_b'), ('length_c', 'CELL_c'), ('angle_alpha', 'CELL_alpha'), ('angle_beta', 'CELL_beta'), ('angle_gamma', 'CELL_gamma')],
            'symmetry': [('space_group_name_H-M', 'SYMM')],
        }

        result = {}

        for obj_name, attrs in attributes.items():
            obj = container.getObj(obj_name)
            if obj is not None:
                for attr, output_name in attrs:
                    if obj.hasAttribute(attr):
                        val = obj.getValue(attr)
                        result[output_name] = float(val) if val.replace('.', '', 1).isdigit() else val
                    else:
                        result[output_name] = None
            else:
                for attr, output_name in attrs:
                    result[output_name] = None

        # Group cell parameters together
        result['CELL'] = [result.pop(key) for key in ['CELL_a', 'CELL_b', 'CELL_c', 'CELL_alpha', 'CELL_beta', 'CELL_gamma'] if key in result]

        self.__dict__.update(result)
        return result

    def extract_attributes_from_pdb(self, filename):
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

        result = {'pdb_id': pdb_id, 'RESOH': resoh, 'RESOL': resol, 'FREERV': freerv, 'WAVE': wave, 'NFREE': nfree, 'SYMM': symm, 'CELL': cell}
        self.__dict__.update(result)
        return result

    def update_FREERV(self, new_freerv):
        self.FREERV = new_freerv


# testing
pdb = ProteinDataBank()
from sf_file import SFFile
sffile = SFFile()
sffile.readFile('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/RCSB/1o08.cif')
print(pdb.extract_attributes_from_cif(sffile))
