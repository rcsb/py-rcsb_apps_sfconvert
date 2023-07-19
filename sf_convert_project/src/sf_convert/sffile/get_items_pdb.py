class ProteinDataBank:
    def __init__(self):
        pass

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

        return result

    def extract_pdb_id_from_pdb(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('HEADER'):
                    return line[62:66].strip()
