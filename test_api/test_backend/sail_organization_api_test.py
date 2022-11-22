# -----------------------------------------------------------
#
# SAIL Organization API test file
#
# -----------------------------------------------------------
import threading

import pytest
from api_portal.sail_portal_api import SailPortalApi
from assertpy.assertpy import assert_that
from cerberus import Validator
from config import DATAOWNER_EMAIL, RESEARCHER_EMAIL, SAIL_PASS, TEMP_PASS
from config import TEST_ORGANIZATION_EMAIL, TEST_ORGANIZATION_PASS, TEST_ORGANIZATION_ID
from config import SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS
from utils.helpers import random_name

temp_email = " "
temp_pass = " "

def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")

def print_response_values(function_name, response, response_json, access_token):
    print(f"\n\n=========={function_name}==========")
    print(f"Test Response: {response}\n")
    print(f"Test Response JSON: {response_json}\n")
    print(f"Access Token: {access_token}\n")


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id",
    [
        "20a8b905-06ca-4237-a072-8a7a7285f603",
        "3a2a2c16-8a7b-4375-8940-1c1461573c26",
        "624d3db0-3a01-4b16-bf25-9d42147506bd",
    ],
)
def test_get_valid_organization(get_base_url: str, org_id: str):
    """
    Testing valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=RESEARCHER_EMAIL, password=SAIL_PASS)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "avatar": {"type": "string", "default": "AVATAR"},  # avatar variable currently NaN/Null/None. keeping for future iterations.
        "id": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.get_organization_by_id(org_id)

    print_response_values(test_get_valid_organization.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id",
    [
        random_name(32),
        random_name(32),
        random_name(32),
        random_name(32),
        random_name(32),
        random_name(32),
        random_name(32),
        random_name(32),
        random_name(32),
        random_name(32),
    ],
)
def test_get_invalid_organization(get_base_url: str, org_id: str):
    """
    Testing valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=RESEARCHER_EMAIL, password=SAIL_PASS)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.get_organization_by_id(org_id)

    #print_response_values(test_get_invalid_organization.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.active
@pytest.mark.parametrize(
    "email, password",
    [
        (RESEARCHER_EMAIL, SAIL_PASS),
        #(DATAOWNER_EMAIL, SAIL_PASS),
    ],
)
def test_get_all_organizations(get_base_url: str, email: str, password: str):
    """
    Testing valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param email: email
    :type email: string
    :param password: password
    :type password: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=email, password=password)
    schema = {"access_token": {"type": "string"}, "refresh_token": {"type": "string"}, "token_type": {"type": "string"}}
    validator = Validator(schema)
    # Act
    test_response, test_response_json, access_token = sail_portal.get_all_organizations()

    print_response_values(test_get_all_organizations.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.active
@pytest.mark.parametrize(
    "name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar",
    [
        (
            "Nates Testing Organization",
            "Description of Nates Testing Organization",
            "temp_nates_avatar_string",
            "Nate Administrator",
            "Software Developer in Test",
            "nathan@secureailabs.com",
            "nathanpassword",
            "temp_admin_avatar_string"
        ),
    ],
)
def test_register_new_valid_organization(get_base_url: str, name: str, description: str, avatar: str, admin_name: str, admin_job_title: str, admin_email: str, admin_password: str, admin_avatar: str):
    """
    Testing registering a new organization using valid parameters.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param name: name
    :type name: string
    :param description: description
    :type description: string
    :param avatar: avatar
    :type avatar: string
    :param admin_name: admin name
    :type admin_name: string
    :param admin_job_title: admin job title
    :type admin_job_title: string
    :param admin_email: admin email
    :type admin_email: string
    :param admin_password: admin password
    :type admin_password: string
    :param admin_avatar: admin avatar
    :type admin_avatar: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=RESEARCHER_EMAIL, password=SAIL_PASS)

    schema = {
        "id": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.register_new_organization(name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar)

    print_response_values(test_register_new_valid_organization.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.active
@pytest.mark.parametrize(
    "name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar",
    [
        (
            "Nates Testing Organization",
            "Description of Nates Testing Organization",
            "temp_nates_avatar_string",
            "Nate Administrator",
            "Software Developer in Test",
            "nathan@secureailabs.com",
            "nathanpassword",
            "temp_admin_avatar_string"
        ),
    ],
)
def test_register_new_invalid_organization(get_base_url: str, name: str, description: str, avatar: str, admin_name: str, admin_job_title: str, admin_email: str, admin_password: str, admin_avatar: str):
    """
    Testing registering a new organization using invalid parameters.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param name: name
    :type name: string
    :param description: description
    :type description: string
    :param avatar: avatar
    :type avatar: string
    :param admin_name: admin name
    :type admin_name: string
    :param admin_job_title: admin job title
    :type admin_job_title: string
    :param admin_email: admin email
    :type admin_email: string
    :param admin_password: admin password
    :type admin_password: string
    :param admin_avatar: admin avatar
    :type admin_avatar: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=RESEARCHER_EMAIL, password=SAIL_PASS)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.register_new_organization(name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar)

    print_response_values(test_register_new_invalid_organization.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.active
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_name, new_description, new_avatar",
    [
        (
            TEST_ORGANIZATION_ID, TEST_ORGANIZATION_EMAIL, TEST_ORGANIZATION_PASS, "Valid Credentials Name", "This org has been updated using valid credentials", random_name(32),
        ),
    ],
)
def test_update_valid_organization_valid_credentials(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_name: str, new_description: str, new_avatar: str):
    """
    Testing updating a valid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "avatar": {"type": "string", "default": "AVATAR"},  # avatar variable currently NaN/Null/None. keeping for future iterations.
        "id": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.update_organization_info(org_id, new_name, new_description, new_avatar)

    print_response_values(test_update_valid_organization_valid_credentials.__name__, test_response, test_response_json, access_token)

    # Assert
    # TODO: add checks to verify the given organization ID had its values change
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.active
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_name, new_description, new_avatar",
    [
        (
            TEST_ORGANIZATION_ID, RESEARCHER_EMAIL, SAIL_PASS, "Valid Credentials Name", "This org has been updated using valid credentials", random_name(32),
        ),
    ],
)
def test_update_valid_organization_invalid_credentials(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_name: str, new_description: str, new_avatar: str):
    """
    Testing updating a valid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "detail": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.update_organization_info(org_id, new_name, new_description, new_avatar)

    print_response_values(test_update_valid_organization_invalid_credentials.__name__, test_response, test_response_json, access_token)

    # Assert
    # TODO: add checks to verify the given organization ID had its values change
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(403)


@pytest.mark.active
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_name, new_description, new_avatar",
    [
        (
            random_name(32), TEST_ORGANIZATION_EMAIL, TEST_ORGANIZATION_PASS, "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32),
        ),
    ],
)
def test_update_invalid_organization_valid_credentials(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_name: str, new_description: str, new_avatar: str):
    """
    Testing updating a valid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.update_organization_info(org_id, new_name, new_description, new_avatar)

    print_response_values(test_update_invalid_organization_valid_credentials.__name__, test_response, test_response_json, access_token)

    # Assert
    # TODO: add checks to verify the given organization ID had its values change
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.active
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_name, new_description, new_avatar",
    [
        (
            random_name(32), random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32),
        ),
    ],
)
def test_update_invalid_organization_invalid_credentials(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_name: str, new_description: str, new_avatar: str):
    """
    Testing updating a valid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "detail": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.update_organization_info(org_id, new_name, new_description, new_avatar)

    print_response_values(test_update_invalid_organization_invalid_credentials.__name__, test_response, test_response_json, access_token)

    # Assert
    # TODO: add checks to verify the given organization ID had its values change
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(401)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass",
    [
        (TEST_ORGANIZATION_ID, TEST_ORGANIZATION_EMAIL, TEST_ORGANIZATION_PASS),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS),
    ],
)
def test_get_valid_organization_users(get_base_url: str, org_id: str, admin_email: str, admin_pass: str):
    """
    Testing updating a valid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "users": {"type": "list"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.get_organization_users(org_id)

    print_response_values(test_get_valid_organization_users.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass",
    [
        (random_name(32), TEST_ORGANIZATION_EMAIL, TEST_ORGANIZATION_PASS),
        (random_name(32), SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS),
    ],
)
def test_get_invalid_organization_users(get_base_url: str, org_id: str, admin_email: str, admin_pass: str):
    """
    Testing updating a valid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    test_response, test_response_json, access_token = sail_portal.get_organization_users(org_id)

    print_response_values(test_get_invalid_organization_users.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)







