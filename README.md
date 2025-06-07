# sfconvert structure factor conversion

This software allows for the conversion of MX structure factor formatted files.

## Installation

You need Python 3.6 or later to run this script. The `py-mmcif` library can be installed via pip:

```bash
pip install sf_convert
```

## Usage

Run the command `sf_convert` with the `-h` or `--help` option to view the help message:

```bash
sf_convert -h
```

Here are the available command line arguments:

- `-sf`: specify the input structure factor file.
- `-pdb`: Coordinate file to copy over cell, wavelnegth, etc if not specified.
- `-o`: Output format.
