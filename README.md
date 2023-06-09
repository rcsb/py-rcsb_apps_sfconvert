# CifConverter Class README

The `CifConverter` class is a Python module designed to manipulate CIF (Crystallographic Information Framework) files. This module provides an object-oriented API to perform various operations such as checking file size, opening files, comparing strings, splitting strings, deleting files, freeing memory, sorting an array by column, and converting CIF files.

## Methods

Here's an overview of the main methods in this class:

### 1. `__init__`
The constructor of the `CifConverter` class, which initializes several instance variables.

### 2. `check_file(size, file)`
Checks if the given file has at least a certain number of lines. Returns 1 if it does and 0 otherwise or if the file is not found.

### 3. `open_file_error(inpfile, message)`
This method is called when a file can't be opened. It prints an error message and stops the execution of the program.

### 4. `strcmp_case(s1, s2)`
Compares two strings in a case-insensitive manner and returns a result indicating which one is greater or if they are equal.

### 5. `string_token(str, token)`
Splits a string by a given token and returns the split parts and their count.

### 6. `delete_file(file)`
Deletes a file if it exists.

### 7. `free_memory_2d(var)`
Frees up the memory used by a 2D variable.

### 8. `array_sort_by_column(line, column, order, nstr)`
This is a placeholder method designed to sort a 2D array by a specific column. The implementation needs to be provided according to the specific use case.

### 9. `pinfo(info, id)`
Writes information to a log and/or the console, depending on the value of 'id'. This method is useful for logging warnings, errors, and other important information.

### 10. `cif2cif_sf_all(iFile, sffile_new, pdb_id, key)`
Performs the main task of the class, which is the conversion of a CIF file to another format. This method takes as input the input file name, the output file name, a PDB ID, and a key, and writes to the output file after processing.

## Usage
To use the `CifConverter` class, import the module and create an instance of the class. Then call the required methods. Note that this class has dependencies on the Python `os` module, so ensure that it is installed and available in your Python environment.

## Caveats
This class is a work in progress and has placeholders where specific functions or classes are needed. It is necessary to fill in these placeholders according to your specific requirements and logic.
