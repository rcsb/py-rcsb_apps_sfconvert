import re

class ProteinDataBank:
    def __init__(self):
        self.pdb_id = 'xxxx'
        self.RESOH = 0.1
        self.RESOL = 200
        self.FREERV = None
        self.WAVE = None
        self.NFREE = None
        self.CELL = None
        self.SYMM = None

    def _update_attributes(self, attributes):
        for key, value in attributes.items():
            if value is not None:
                self.__dict__[key] = value

    def extract_attributes_from_cif(self, sffile):
        container = sffile.get_block_by_index(0)
        attributes = self._get_cif_attributes(container)

        # Group cell parameters together
        attributes['CELL'] = [attributes.pop(key) for key in ['CELL_a', 'CELL_b', 'CELL_c', 'CELL_alpha', 'CELL_beta', 'CELL_gamma'] if key in attributes]

        self._update_attributes(attributes)
        return attributes

    def _get_cif_attributes(self, container):
        cif_attributes = {
            'entry': [('id', 'pdb_id')],
            'reflns': [('d_resolution_high', 'RESOH'), ('d_resolution_low', 'RESOL'), ('free_R_factor', 'FREERV')],
            'diffrn_radiation_wavelength': [('wavelength', 'WAVE')],
            'pdbx_refine': [('free_R_val_test_set_ct_no_cutoff', 'NFREE')],
            'cell': [('length_a', 'CELL_a'), ('length_b', 'CELL_b'), ('length_c', 'CELL_c'), ('angle_alpha', 'CELL_alpha'), ('angle_beta', 'CELL_beta'), ('angle_gamma', 'CELL_gamma')],
            'symmetry': [('space_group_name_H-M', 'SYMM')],
        }

        attributes = {}

        for obj_name, attrs in cif_attributes.items():
            obj = container.getObj(obj_name)
            if obj is not None:
                for attr, output_name in attrs:
                    if obj.hasAttribute(attr):
                        val = obj.getValue(attr)
                        attributes[output_name] = float(val) if val.replace('.', '', 1).isdigit() else val
                    else:
                        attributes[output_name] = None
            else:
                for attr, output_name in attrs:
                    attributes[output_name] = None

        return attributes

    def extract_attributes_from_pdb(self, filename):
        attributes = self._get_pdb_attributes(filename)
        self._update_attributes(attributes)
        return attributes

    def _get_pdb_attributes(self, filename):
        # Initiate the variables
        pdb_id = wave = nfree = resoh = resol = freerv = symm = None
        cell = [None]*6

        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('HEADER'):
                    pdb_id = line[61:66].strip()

                elif 'REMARK 200  WAVELENGTH OR RANGE        (A) :' in line:
                    wave = self._extract_float(line)

                elif 'FREE R VALUE TEST SET COUNT   (NO CUTOFF)' in line:
                    nfree = self._extract_int(line)

                elif 'RESOLUTION RANGE HIGH (ANGSTROMS)' in line:
                    resoh = self._extract_float(line)

                elif 'RESOLUTION RANGE LOW  (ANGSTROMS)' in line:
                    resol = self._extract_float(line)

                elif 'REMARK   test_flag_value:' in line and freerv is None:
                    freerv = line.split(':')[1].strip()

                elif line.startswith('CRYST1'):
                    cell = self._extract_cell_parameters(line)
                    symm = line[55:66].strip()

        return {'pdb_id': pdb_id, 'RESOH': resoh, 'RESOL': resol, 'FREERV': freerv, 'WAVE': wave, 'NFREE': nfree, 'SYMM': symm, 'CELL': cell}

    def _extract_float(self, line):
        return float(re.search(r'[-+]?\d*\.\d+|\d+', line.split(':')[1]).group())

    def _extract_int(self, line):
        return int(re.search(r'\d+', line.split(':')[1]).group())

    def _extract_cell_parameters(self, line):
        cell_values = line[6:].split()[:6]
        return [float(val) for val in cell_values]

    def update_FREERV(self, new_freerv):
        self.FREERV = new_freerv

    def update_WAVE(self, new_wave):
        self.WAVE = new_wave

# testing
# pdb = ProteinDataBank()
# from sf_file import SFFile
# sffile = SFFile()
# sffile.readFile('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/RCSB/1o08.cif')
# print(pdb.extract_attributes_from_cif(sffile))

        # self.pdb_id = 'xxxx' # used in MTZ and CNS(IG)
        # self.RESOH = 0.1 # used in check_sf needed this or else default values are used
        # self.RESOL = 200 # same as above
        # self.FREERV = None # Have to verfiy this with prof
        # self.WAVE = None # wavelength DONE
        # self.NFREE = None #
        # self.CELL = None # cell parameters to be implemented in MTZ file when there is no CELL found or this is not empty ig and also in sf-4-validatin we need to change and use this
        # self.SYMM = None # same as above
