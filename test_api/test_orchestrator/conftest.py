"""
Pytest fixtures
"""
import json

import pytest
import sail.core
from config import API_PORTAL_HOSTNAME, RESEARCHER_EMAIL, SAFE_FUNCTION_DIRECTORY, SAIL_PASS, TEST_SAFE_FUNCTION_GUID


def pytest_addoption(parser):
    """
    Pytest addoption cmdline arguments

    :param parser:
    :type parser:
    """
    parser.addoption("--hostname", action="store", default=API_PORTAL_HOSTNAME)
    parser.addoption("--safefndir", action="store", default=SAFE_FUNCTION_DIRECTORY)
    parser.addoption("--safefnguid", action="store", default=TEST_SAFE_FUNCTION_GUID)


@pytest.fixture(autouse=True)
def get_portal_ip(pytestconfig):
    """
    Fixture to get the IP address of our platform service server

    :param pytestconfig:
    :type pytestconfig:
    :return: ip
    :rtype: string
    """
    return pytestconfig.getoption("ip")


@pytest.fixture(autouse=True)
def get_portal_port(pytestconfig):
    """
    Fixture to get the port of our platform service server

    :param pytestconfig:
    :type pytestconfig:
    :return: port
    :rtype: string
    """
    return int(pytestconfig.getoption("port"))


@pytest.fixture(autouse=True)
def get_portal_hostname(pytestconfig):
    """
    Fixture to get the hostname (if available) of our platform service server

    :param pytestconfig:
    :type pytestconfig:
    :return: hostname
    :rtype: string
    """
    return pytestconfig.getoption("hostname")


@pytest.fixture(autouse=True)
def get_safe_function_dir(pytestconfig):
    """
    Fixture to get the location on disk of safe functions to load

    :param pytestconfig:
    :type pytestconfig:
    :return: safefndir
    :rtype: string
    """
    return pytestconfig.getoption("safefndir")


@pytest.fixture(autouse=True)
def get_safe_function_guid(pytestconfig):
    """
    Fixture to get the guid of a test safe function

    :param pytestconfig:
    :type pytestconfig:
    :return: safefnguid
    :rtype: string
    """
    return pytestconfig.getoption("safefnguid")


@pytest.fixture
def orchestrator_load_safe_functions_fixture(get_safe_function_dir):
    # Setup
    sail.core.load_safe_objects(get_safe_function_dir)
    yield

    # Teardown
    sail.core.exit_current_session()


@pytest.fixture
def orchestrator_login_fixture(get_portal_ip, get_portal_port):
    # Setup
    sail.core.login(RESEARCHER_EMAIL, SAIL_PASS, get_portal_port, get_portal_ip)

    yield

    # Teardown
    sail.core.exit_current_session()


@pytest.fixture
def orchestrator_fresh_session_fixture():
    sail.core.exit_current_session()


@pytest.fixture
def orchestrator_cleanup_provisions_fixture(orchestrator_get_digital_contract_guid_fixture):
    yield

    sail.core.deprovision_digital_contract(orchestrator_get_digital_contract_guid_fixture)


@pytest.fixture(autouse=True)
def orchestrator_get_dataset_guid_fixture(orchestrator_login_fixture):
    all_datasets = sail.core.get_datasets()

    provision_ds = ""

    if all_datasets is not None:
        json_datasets = json.loads(all_datasets)
        provision_ds = list(json_datasets.keys())[0]

    return provision_ds


@pytest.fixture(autouse=True)
def orchestrator_get_digital_contract_guid_fixture(orchestrator_login_fixture):
    all_digital_contracts = sail.core.get_digital_contracts()

    provision_dc = ""

    if all_digital_contracts is not None:
        json_datasets = json.loads(all_digital_contracts)
        provision_dc = list(json_datasets.keys())[0]

    return provision_dc
