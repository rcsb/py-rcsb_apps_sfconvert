import os
import shutil

# Directory path
# dir_path = "/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/RCSB/PU/"
dir_path = "/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop\ files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/tests/data/PU"

# Create directories if they don't exist
cif_to_cif_dir = os.path.join(dir_path, "cif_to_cif")
mtz_to_cif_dir = os.path.join(dir_path, "mtz_to_cif")

if not os.path.exists(cif_to_cif_dir):
    os.makedirs(cif_to_cif_dir)

if not os.path.exists(mtz_to_cif_dir):
    os.makedirs(mtz_to_cif_dir)

# Loop through all files in the directory to find input files
for filename in os.listdir(dir_path):

    # CIF to CIF files
    if filename.endswith('sf-upload_P1.cif.V1') and 'convert' not in filename:
        expected_output = filename.replace('_P1.cif.V1', '_convert_P1.cif.V1')
        if expected_output in os.listdir(dir_path):
            shutil.move(os.path.join(dir_path, filename), cif_to_cif_dir)
            shutil.move(os.path.join(dir_path, expected_output), cif_to_cif_dir)
    
    # MTZ to CIF files
    elif filename.endswith('sf-upload_P1.mtz.V1'):
        expected_output = filename.replace('_P1.mtz.V1', '_convert_P1.cif.V1')
        if expected_output in os.listdir(dir_path):
            shutil.move(os.path.join(dir_path, filename), mtz_to_cif_dir)
            shutil.move(os.path.join(dir_path, expected_output), mtz_to_cif_dir)
