from sf_file import StructureFactorFile

sf = StructureFactorFile()

sf.read_file('5pny-sf.cif')

print(sf.get_all_block_names())
print()
print(sf.get_category_names('r5pnysf'))
print()
print(sf.get_category_object('diffrn_radiation_wavelength'))
print()
#num_replaced = sf.replace_value_in_category('diffrn_radiation_wavelength', '1.5406', 'wavelength')



from get_items_pdb import ProteinDataBank

pdb_mmcif = ProteinDataBank()

sf_pdb_mmcif = StructureFactorFile()

sf_pdb_mmcif.read_file('5pny.cif')

print('-' * 150)

print(pdb_mmcif.extract_attributes_from_cif(sf_pdb_mmcif))
print('-' * 150)
print(pdb_mmcif.pdb_id)
print()


num_replaced = sf.replace_value_in_category('diffrn_radiation_wavelength', 'wavelength', pdb_mmcif.WAVE)


print(sf.get_category_object('diffrn_radiation_wavelength'))
print()