import os
import pytest


@pytest.fixture(name="data_dir")
def fixture_data_dir():
    """
    Fixture for the data directory used in tests.

    Returns:
        str: The path to the data directory.
    """
    yield os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def cns_data_path(data_dir):
    """
    Fixture for the path to the CNS data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CNS data file.
    """
    yield os.path.join(data_dir, "cif_files", "cns-sf6.cv")


@pytest.fixture
def cif_5pny_data_path(data_dir):
    """
    Fixture for the path to the CIF data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "cif_files", "5pny-sf.cif")


@pytest.fixture
def cif_5pny_coordinate_path(data_dir):
    """
    Fixture for the path to the CIF data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "cif_files", "5pny.cif")


@pytest.fixture
def cif_5pny_nodb2_coordinate_path(data_dir):
    """
    Fixture for the path to the CIF data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "cif_files", "5pny_nodb2.cif")


@pytest.fixture
def cif_5pny_coordinate_pdb_path(data_dir):
    """
    Fixture for the path to the PDB data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "pdb_files", "5pny.pdb")


@pytest.fixture
def cns_5pny_data_path(data_dir):
    """
    Fixture for the path to the CNS data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CNS data file.
    """
    yield os.path.join(data_dir, "cif_files", "5pny-sf.CNS")


@pytest.fixture
def cns_cif_5pny_data_path(data_dir):
    """
    Fixture for the path to the CNS to cif conversion data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CNS data file.
    """
    yield os.path.join(data_dir, "cif_files", "5pny-sf-CNS.mmcif")


@pytest.fixture
def mtz_Ras_NAD_data_path(data_dir):
    """
    Fixture for the path to the MTZ data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the MTZ data file.
    """
    yield os.path.join(data_dir, "cif_files", "Ras_NAD.mtz")


@pytest.fixture
def cif_Ras_NAD_data_path(data_dir):
    """
    Fixture for the path to the CIF data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "cif_files", "Ras_NAD.mtz.mmcif")


@pytest.fixture
def cif_SF_4_validate_data_path(data_dir):
    """
    Fixture for the path to the CIF data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "cif_files", "SF_4_validate.cif")


@pytest.fixture
def cif_mmcif_5pny_data_path(data_dir):
    """
    Fixture for the path to the CIF data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "cif_files", "5pny-sf.cif.mmcif")


@pytest.fixture
def cif_mmcif_5pny_detail_data_path(data_dir):
    """
    Fixture for the path to the CIF data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "cif_files", "5pny-sf-detail.cif.mmcif")


@pytest.fixture
def cns_to_mmcif_data_path(data_dir):
    """
    Fixture for the path to the CIF data file.

    Args:
        data_dir (str): The path to the data directory.

    Returns:
        str: The path to the CIF data file.
    """
    yield os.path.join(data_dir, "cif_files", "cns-sf6.cv.mmcif")
