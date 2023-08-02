import subprocess
import pytest

cli_script = '/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/sffile/main2.py'

def test_input_format():
    result = subprocess.run(['python', cli_script, '-i', 'CNS'], capture_output=True, text=True)
    assert 'CNS' in result.stdout

def test_output_format():
    result = subprocess.run(['python', cli_script, '-o', 'mmCIF'], capture_output=True, text=True)
    assert 'mmCIF' in result.stdout

def test_both_input_output_format():
    result = subprocess.run(['python', cli_script, '-i', 'CNS', '-o', 'mmCIF'], capture_output=True, text=True)
    assert 'CNS' in result.stdout
    assert 'mmCIF' in result.stdout

def test_sf_file():
    result = subprocess.run(['python', cli_script, '-sf', 'source_file.cif'], capture_output=True, text=True)
    assert 'source_file.cif' in result.stdout

def test_out_file():
    result = subprocess.run(['python', cli_script, '-out', 'output_file.cif'], capture_output=True, text=True)
    assert 'output_file.cif' in result.stdout

def test_label():
    result = subprocess.run(['python', cli_script, '-label', 'FP=DELFWT, SIGFP=SIGF_XDSdataset'], capture_output=True, text=True)
    assert 'FP=DELFWT, SIGFP=SIGF_XDSdataset' in result.stdout

def test_pdb_file():
    result = subprocess.run(['python', cli_script, '-pdb', 'pdb_file.pdb'], capture_output=True, text=True)
    assert 'pdb_file.pdb' in result.stdout
