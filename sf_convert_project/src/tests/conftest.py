import os
import pytest

@pytest.fixture
def data_dir():
    """Datadir for tests"""
    yield os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def cns_data_path(data_dir):
    yield os.path.join(data_dir, "cif_files", "cns-sf6.cv")

@pytest.fixture
def cif_5pny_data_path(data_dir):
    yield os.path.join(data_dir, "cif_files", "5pny-sf.cif")
    

