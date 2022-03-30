# -----------------------------------------------------------
#
# Orchestrator Unit test file - Login
#
# -----------------------------------------------------------

import time

import pytest
import sail.core
from assertpy.assertpy import assert_that
from config import RESEARCHER_EMAIL, SAIL_PASS
from utils.helpers import pretty_print


@pytest.mark.active
def test_successful_login(orchestrator_fresh_session_fixture, get_portal_port, get_portal_ip):
    """
    Test Logging in to the Orchestrator using an IP address

    :param get_portal_port: fixture
    :type get_portal_port: int
    :param get_portal_port: fixture
    :type get_portal_port: string
    """
    # Act
    test_response = sail.core.login(RESEARCHER_EMAIL, SAIL_PASS, get_portal_port, get_portal_ip)

    # Assert
    assert_that(test_response).is_equal_to(201)


# Marked current until we get hostnames setup in our test environment
@pytest.mark.current
def test_successful_login_hostname(orchestrator_fresh_session_fixture, get_portal_port, get_portal_hostname):
    """
    Test Logging in to the Orchestrator using a hostname

    :param get_portal_port: fixture
    :type get_portal_port: int
    :param get_portal_ip: fixture
    :type get_portal_ip: string
    """
    # Act
    test_response = sail.core.login(RESEARCHER_EMAIL, SAIL_PASS, get_portal_port, get_portal_hostname)

    # Assert
    assert_that(test_response).is_equal_to(201)


@pytest.mark.active
@pytest.mark.parametrize(
    "bad_login_information",
    [
        # Username that doesn't exist
        {"User": "FakeAccount", "Password": "SailPassword@123"},
        # Bad password
        {"User": "lbart@igr.com", "Password": "SailPassword@123_BAD"},
    ],
)
def test_bad_credential_login(
    orchestrator_fresh_session_fixture, bad_login_information, get_portal_port, get_portal_ip
):
    """
    Test Logging in to the Orchestrator using a bad credentials

    :param bad_login_information: string
    :type bad_login_information: string
    :param get_portal_port: fixture
    :type get_portal_port: int
    :param get_portal_ip: fixture
    :type get_portal_ip: string
    """
    # Act
    test_response = sail.core.login(
        bad_login_information["User"], bad_login_information["Password"], get_portal_port, get_portal_ip
    )

    # Assert
    assert_that(test_response).is_equal_to(404)


@pytest.mark.active
@pytest.mark.parametrize(
    "bad_network_port",
    [
        -1,
        70000,
        0,
    ],
)
def test_bad_port_login(orchestrator_fresh_session_fixture, bad_network_port, get_portal_ip):
    """
    Test Logging in to the Orchestrator using a bad port

    :param bad_network_port: fixture
    :type bad_network_port: int
    :param get_portal_ip: fixture
    :type get_portal_ip: int
    """
    # Act
    test_response = sail.core.login("lbart@igr.com", "SailPassword@123", bad_network_port, get_portal_ip)

    # Assert
    assert_that(test_response).is_equal_to(401)


@pytest.mark.active
@pytest.mark.parametrize(
    "bad_ip",
    [" ", "127.0.0.a"],
)
def test_bad_ip_login(orchestrator_fresh_session_fixture, bad_ip, get_portal_port):
    """
    Test Logging in to the Orchestrator using a bad ip

    :param bad_ip: fixture
    :type bad_ip: string
    :param get_portal_port: fixture
    :type get_portal_prt: int
    """
    # Act
    test_response = sail.core.login("lbart@igr.com", "SailPassword@123", get_portal_port, bad_ip)

    # Assert
    assert_that(test_response).is_equal_to(401)


@pytest.mark.active
def test_eosb_on_login(orchestrator_login_fixture):
    """
    Test Logging in to the Orchestrator gets us an EOSB

    :param orchestrator_login_fixture: fixture
    :type orchestrator_login_fixture: A fixture which will log us with in valid credentials
    """

    # Act
    test_response = sail.core.get_current_eosb()

    # Assert
    assert_that(test_response).is_not_none()


@pytest.mark.active
def test_eosb_no_session(orchestrator_fresh_session_fixture):
    """
    Test not being logged in to the Orchestrator gets us no EOSB

    :param orchestrator_fresh_session_fixture: fixture
    :type orchestrator_fresh_session_fixture: A fixture which will ensure we don't have a session
    """
    # Act
    test_response = sail.core.get_current_eosb()

    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
def test_no_eosb_rotation(orchestrator_login_fixture):
    """
    Test that the EOSB does not rotate in a short time window

    :param orchestrator_login_fixture: fixture
    :type orchestrator_login_fixture: A fixture which will log us with in valid credentials
    """
    # Arrange
    initial_eosb = sail.core.get_current_eosb()

    # Our EOSB ortation time is 10 minutes, with a 10 minute grace period, slee for
    # less than that
    time.sleep(30)

    # Act
    test_response = sail.core.get_current_eosb()

    # Assert
    assert_that(test_response).is_equal_to(initial_eosb)


@pytest.mark.functional
def test_eosb_rotation(orchestrator_login_fixture):
    """
    Test that the EOSB rotates after it should expire (10 minutes)

    :param orchestrator_login_fixture: fixture
    :type orchestrator_login_fixture: A fixture which will log us with in valid credentials
    """
    # Arrange
    initial_eosb = sail.core.get_current_eosb()

    # Our EOSB ortation time is 10 minutes, with a 10 minute grace period
    time.sleep(60 * 11)

    # Act
    test_response = sail.core.get_current_eosb()

    # Assert
    assert_that(test_response).is_not_equal_to(initial_eosb)
