import os
import pytest

pythonpath = ["helpers"]

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

