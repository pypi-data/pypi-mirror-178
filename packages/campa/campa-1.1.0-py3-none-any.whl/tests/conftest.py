import os

import pytest


@pytest.fixture(autouse=True)
def _set_config():
    """
    set EXPERIMENT_DIR and BASE_DATA_DIR in campa config
    """
    from campa.utils import init_logging
    from campa.constants import SCRIPTS_DIR, campa_config
    from campa.data._download_data import load_test_data

    init_logging()  # NOTE: this will silence some warnings of 3rd party packages
    # ensure that test data is downloaded
    load_test_data()

    campa_config.EXPERIMENT_DIR = os.path.join(SCRIPTS_DIR, "tests", "_experiments")
    campa_config.BASE_DATA_DIR = os.path.join(SCRIPTS_DIR, "tests/_data")
    campa_config.add_data_config("TestData", os.path.join(SCRIPTS_DIR, "tests/_data/TestData_constants.py"))
    campa_config.CO_OCC_CHUNK_SIZE = 1e7

    print("CAMPA CONFIG:")
    print(campa_config)
