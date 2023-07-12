# import gemmi

# # Load the MTZ file
# mtz_object = gemmi.read_mtz_file('1N9F.mtz')

# # Get the column information
# column_list = mtz_object.columns
# labels = mtz_object.column_labels()

# # Get the dataset information
# dataset_list = mtz_object.datasets

# # Open the output file
# with open('output.txt', 'w') as f:
#     # Print the column list
#     f.write("Columns:\n")
#     for column in column_list:
#         f.write(f"{column.label}\n")

#     # Print the column labels
#     f.write("\nColumn Labels:\n")
#     for label in labels:
#         f.write(f"{label}\n")

#     # Print the columns with their types
#     f.write("\nColumns with types:\n")
#     for column in column_list:
#         f.write(f"{column.label}, {column.type}\n")

#     # Print the datasets
#     f.write("\nDatasets:\n")
#     for dataset in dataset_list:
#         f.write(f"{dataset.id}\n")


# import gemmi

# def list_mtz_data(mtz_file):
#     # Read MTZ file
#     mtz = gemmi.read_mtz_file(mtz_file)

#     # Print general information
#     print(f"Title: {mtz.title}")
#     print(f"Spacegroup: {mtz.spacegroup_name}")

#     # Print information about each dataset
#     for i, dataset in enumerate(mtz.datasets):
#         #print(f"Dataset {i + 1}: {dataset.name}")
#         print(f"  Cell: {mtz.get_cell(dataset.id)}")

#     # Print information about each column
#     for column in mtz.columns:
#         print(f"Column: {column.label}")
#         print(f"  Type: {column.type}")
#         #print(f"  Dataset: {mtz.dataset(column.dataset_id).name}")
#         print(f"  Values: {column.array}")

# # Usage:
# list_mtz_data("1N9F.mtz")

# import gemmi

# def list_mtz_data(mtz_file):
#     # Read MTZ file
#     mtz = gemmi.read_mtz_file(mtz_file)

#     # Print labels, types, and datasets for all columns
#     for column in mtz.columns:
#         print(f"Column: {column.label}")
#         print(f"  Type: {column.type}")
#         print(f"  Dataset: {mtz.dataset(column.dataset_id).name}")
#         print("")

#     # Find minimum and maximum dataset IDs
#     min_id = min(dataset.id for dataset in mtz.datasets)
#     max_id = max(dataset.id for dataset in mtz.datasets)
#     print(f"Minimum dataset ID: {min_id}")
#     print(f"Maximum dataset ID: {max_id}")

#     # Check for presence of certain labels
#     labels_to_check = ["PH2FOFCWT", "PHWT", "PHIF"]
#     for label in labels_to_check:
#         print(f"Presence of {label}: {'Yes' if mtz.column_with_label(label) else 'No'}")

#     # Print the native dataset
#     print(f"Native dataset: {mtz.dataset(0).name}")

#     # Print items for each dataset
#     for dataset in mtz.datasets:
#         print(f"Dataset {dataset.name} items:")
#         for column in dataset.columns:
#             print(f"  {column.label}")
#         print("")

# # Usage:
# list_mtz_data("1N9F.mtz")


# import gemmi

# def convert_mtz_to_mmcif(mtz_file, mmcif_file):
#     # Create an MtzToCif object
#     mtz2cif = gemmi.MtzToCif()

#     # Specify the structure of the MTZ data
#     mtz2cif.spec_lines = [
#         '_refln.index_h H H',
#         '_refln.index_k K H',
#         '_refln.index_l L H',
#         '_refln.F_meas_au FP F',
#         '_refln.F_meas_sigma_au SIGFP Q',
#         '_refln.pdbx_r_free_flag FREE I'
#     ]

#     # Read the MTZ file
#     mtz = gemmi.read_mtz_file(mtz_file)

#     # Convert the MTZ data to CIF format
#     cif_string = mtz2cif.write_cif_to_string(mtz)

#     # Write the CIF data to a file
#     with open(mmcif_file, 'w') as f:
#         f.write(cif_string)

# # Usage:
# # convert_mtz_to_mmcif("input.mtz", "output.cif")


# # Usage:
# convert_mtz_to_mmcif("1N9F.mtz", "output2.cif")

import gemmi

def print_first_columns(mtz_file, num_columns=3):
    # Read MTZ file
    mtz = gemmi.read_mtz_file(mtz_file)

    # Print labels of the first few columns
    for column in mtz.columns[:num_columns]:
        print(f"Column: {column.label}")

# Usage:
print_first_columns("1N9F.mtz")
