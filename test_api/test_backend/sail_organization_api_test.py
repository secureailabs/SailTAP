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


temp_org_id = ""

def get_temp_org_id():
    global temp_org_id
    print(f"Getting temp_org_id: {temp_org_id}")
    return temp_org_id

def set_temp_org_id(new_org_id):
    global temp_org_id
    temp_org_id = new_org_id
    print(f"Setting temp_org_id to: {temp_org_id}")

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
        SAIL_ORGANIZATION_ID,
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
    sail_portal = SailPortalApi(base_url=get_base_url, email=SAIL_ORGANIZATION_EMAIL, password=SAIL_ORGANIZATION_PASS)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "avatar": {"type": "string", "default": "AVATAR"},  # avatar variable currently NaN/Null/None. keeping for future iterations.
        "id": {"type": "string"},
    }
    
    validator = Validator(schema)

    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.get_organization_by_id(access_token, org_id)

    #print_response_values(test_get_valid_organization.__name__, test_response, test_response_json, access_token)

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
    sail_portal = SailPortalApi(base_url=get_base_url, email=SAIL_ORGANIZATION_EMAIL, password=SAIL_ORGANIZATION_PASS)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    _, _, access_token = sail_portal.login()
    test_response, test_response_json, access_token = sail_portal.get_organization_by_id(access_token, org_id)

    #print_response_values(test_get_invalid_organization.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(422)


# TODO: Retest/rewrite when permissioned user is available for testing
@pytest.mark.broken
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
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.get_all_organizations(access_token)

    print_response_values(test_get_all_organizations.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.updated
@pytest.mark.parametrize(
    "name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar",
    [
        (
            "Valid Testing Organization",
            "Description of Valid Testing Organization",
            "temp_nates_avatar_string",
            "Nate Administrator",
            "Software Developer in Test",
            TEST_ORGANIZATION_EMAIL,
            TEST_ORGANIZATION_PASS,
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

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.register_new_organization(access_token, name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar)

    print_response_values(test_register_new_valid_organization.__name__, test_response, test_response_json, access_token)
    set_temp_org_id(test_response_json["id"])

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.updated
@pytest.mark.parametrize(
    "name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar",
    [
        (
            None,"temp_description","temp_avatar_string","temp_admin","temp_title","temp@email.com","temp_pass","temp_admin_avatar"
        ),
        (
            "temp_name",None,"temp_avatar_string","temp_admin","temp_title","temp@email.com","temp_pass","temp_admin_avatar"
        ),
        (
            "temp_name","temp_description","temp_avatar_string",None,"temp_title","temp@email.com","temp_pass","temp_admin_avatar"
        ),
        (
            "temp_name","temp_description","temp_avatar_string","temp_admin",None,"temp@email.com","temp_pass","temp_admin_avatar"
        ),
        (
            "temp_name","temp_description","temp_avatar_string","temp_admin","temp_title",None,"temp_pass","temp_admin_avatar"
        ),
        (
            "temp_name","temp_description","temp_avatar_string","temp_admin","temp_title","temp@email.com",None,"temp_admin_avatar"
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

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.register_new_organization(access_token, name, description, avatar, admin_name, admin_job_title, admin_email, admin_password, admin_avatar)

    #print_response_values(test_register_new_invalid_organization.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(access_token)
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_name, new_description, new_avatar",
    [
        (
            SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "Updated SAIL Organization", "This org (SAIL) has been updated using valid credentials", random_name(32),
        ),
    ],
)
def test_update_valid_organization_valid_credentials(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_name: str, new_description: str, new_avatar: str):
    """
    Testing updating a valid organization with valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    :param new_name: new organization name
    :type new_name: string
    :param new_description: new organization description
    :type new_description: string
    :param new_avatar: new organization avatar
    :type new_avatar: string
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

    # Act
    _, _, access_token = sail_portal.login()
    update_response, update_response_json, _ = sail_portal.update_organization_info(access_token, org_id, new_name, new_description, new_avatar)
    test_response, test_response_json, _ = sail_portal.get_organization_by_id(access_token, org_id)

    #print_response_values(test_update_valid_organization_valid_credentials.__name__, update_response, update_response_json, access_token)
    #print_response_values(test_update_valid_organization_valid_credentials.__name__, test_response, test_response_json, access_token)

    # Assert
    assert_that(update_response.status_code).is_equal_to(204)
    assert_that(test_response_json["name"]).is_equal_to(new_name)
    assert_that(test_response_json["description"]).is_equal_to(new_description)
    assert_that(test_response_json["avatar"]).is_equal_to(new_avatar)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_name, new_description, new_avatar",
    [
        (SAIL_ORGANIZATION_ID, random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (SAIL_ORGANIZATION_ID, random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (SAIL_ORGANIZATION_ID, random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (SAIL_ORGANIZATION_ID, random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (SAIL_ORGANIZATION_ID, random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
    ],
)
def test_update_valid_organization_invalid_credentials(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_name: str, new_description: str, new_avatar: str):
    """
    Testing updating a valid organization with invalid credentials.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    :param new_name: new organization name
    :type new_name: string
    :param new_description: new organization description
    :type new_description: string
    :param new_avatar: new organization avatar
    :type new_avatar: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "detail": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.update_organization_info(access_token, org_id, new_name, new_description, new_avatar)

    #print_response_values(test_update_valid_organization_invalid_credentials.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(401)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_name, new_description, new_avatar",
    [
        (random_name(32), SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (random_name(32), SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (random_name(32), SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (random_name(32), SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (random_name(32), SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
    ],
)
def test_update_invalid_organization_valid_credentials(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_name: str, new_description: str, new_avatar: str):
    """
    Testing updating an invalid organization with valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    :param new_name: new organization name
    :type new_name: string
    :param new_description: new organization description
    :type new_description: string
    :param new_avatar: new organization avatar
    :type new_avatar: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.update_organization_info(access_token, org_id, new_name, new_description, new_avatar)

    #print_response_values(test_update_invalid_organization_valid_credentials.__name__, test_response, test_response_json, access_token)

    # Assert
    # TODO: add checks to verify the given organization ID had its values change
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_name, new_description, new_avatar",
    [
        (random_name(32), random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (random_name(32), random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (random_name(32), random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (random_name(32), random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
        (random_name(32), random_name(16), random_name(16), "Invalid Credentials Name", "This org has been updated using invalid credentials", random_name(32)),
    ],
)
def test_update_invalid_organization_invalid_credentials(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_name: str, new_description: str, new_avatar: str):
    """
    Testing updating an invalid organization with invalid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    :param new_name: new organization name
    :type new_name: string
    :param new_description: new organization description
    :type new_description: string
    :param new_avatar: new organization avatar
    :type new_avatar: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "detail": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.update_organization_info(access_token, org_id, new_name, new_description, new_avatar)

    #print_response_values(test_update_invalid_organization_invalid_credentials.__name__, test_response, test_response_json, access_token)

    # Assert
    # TODO: add checks to verify the given organization ID had its values change
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(401)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS),
    ],
)
def test_get_valid_organization_users(get_base_url: str, org_id: str, admin_email: str, admin_pass: str):
    """
    Testing getting all users of a valid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "users": {"type": "list"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.get_organization_users(access_token, org_id)

    print_response_values(test_get_valid_organization_users.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass",
    [
        (random_name(32), SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS),
        (random_name(32), SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS),
    ],
)
def test_get_invalid_organization_users(get_base_url: str, org_id: str, admin_email: str, admin_pass: str):
    """
    Testing getting all users of an invalid organization

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, access_token = sail_portal.get_organization_users(access_token, org_id)

    #print_response_values(test_get_invalid_organization_users.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, user_email, user_pass",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS),
    ],
)
def test_get_organization_valid_user(get_base_url: str, org_id: str, user_email: str, user_pass: str):
    """
    Testing getting a valid user from an organization.  Currently gets the first user in the users list, then tries to get that user data. Can be updated to loop through the user list.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=user_email, password=user_pass)

    schema = {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "job_title": {"type": "string"},
        "role": {"type": "string"},
        "avatar": {"type": "string", "default": "AVATAR"},  # avatar variable currently NaN/Null/None. keeping for future iterations.
        "id": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.get_organization_users(access_token, org_id)
    user = test_response_json['users'][0]
    test_response, test_response_json, _ = sail_portal.get_organization_user_by_id(access_token, org_id, user['id'])

    #print_response_values(test_get_valid_organization_users.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, user_email, user_pass, user_id",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
    ],
)
def test_get_organization_invalid_user(get_base_url: str, org_id: str, user_email: str, user_pass: str, user_id: str):
    """
    Testing getting a valid user from an organization.  Currently gets the first user in the users list, then tries to get that user data. Can be updated to loop through the user list.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=user_email, password=user_pass)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.get_organization_users(access_token, org_id)
    test_response, test_response_json, _ = sail_portal.get_organization_user_by_id(access_token, org_id, user_id)

    #print_response_values(test_get_valid_organization_users.__name__, test_response, test_response_json, access_token)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, user_name, user_email, user_job_title, user_role, user_avatar, user_password",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "new_user", "new@user.com", "new_user_title", "ADMIN", "new_user_avatar", "newuserpassword"),
    ],
)
def test_register_valid_user_to_organization(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, user_name: str, user_email: str, user_job_title: str, user_role: str, user_avatar: str, user_password: str):
    """
    Testing registering a new organization using valid parameters.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    :param user_name: new user name
    :type user_name: string
    :param user_email: new user email
    :type user_email: string
    :param user_job_title: new user job title
    :type user_job_title: string
    :param user_role: new user role
    :type user_role: string
    :param user_avatar: new user avatar
    :type user_avatar: string
    :param user_password: new user password
    :type user_password: string
    """

    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "id": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.register_new_user_to_organization(access_token, org_id, user_name, user_email, user_job_title, user_role, user_avatar, user_password)

    print_response_values(test_register_new_valid_user_to_organization.__name__, test_response, test_response_json, access_token)
    

    temp_response, temp_response_json, _ = sail_portal.get_organization_users(access_token, org_id)
    users = temp_response_json['users']

    is_found = False
    for x in users:
        print(f"\n{x}\n")
        if x['id'] == test_response_json["id"]:
            is_found = True

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(is_found).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, user_name, user_email, user_job_title, user_role, user_avatar, user_password",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, None, "new@user.com", "new_user_title", "ADMIN", "new_user_avatar", "newuserpassword"),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "new_user", None, "new_user_title", "ADMIN", "new_user_avatar", "newuserpassword"),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "new_user", "new@user.com", None, "ADMIN", "new_user_avatar", "newuserpassword"),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "new_user", "new@user.com", "new_user_title", None, "new_user_avatar", "newuserpassword"),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "new_user", "new@user.com", "new_user_title", "ADMIN", "new_user_avatar", None),
    ],
)
def test_register_invalid_user_to_organization(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, user_name: str, user_email: str, user_job_title: str, user_role: str, user_avatar: str, user_password: str):
    """
    Testing registering a new organization using invalid parameters.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    :param user_name: new user name
    :type user_name: string
    :param user_email: new user email
    :type user_email: string
    :param user_job_title: new user job title
    :type user_job_title: string
    :param user_role: new user role
    :type user_role: string
    :param user_avatar: new user avatar
    :type user_avatar: string
    :param user_password: new user password
    :type user_password: string
    """

    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()
    test_response, test_response_json, _ = sail_portal.register_new_user_to_organization(access_token, org_id, user_name, user_email, user_job_title, user_role, user_avatar, user_password)

    print_response_values(test_register_new_valid_user_to_organization.__name__, test_response, test_response_json, access_token)
    

    #temp_response, temp_response_json, _ = sail_portal.get_organization_users(access_token, org_id)
    #users = temp_response_json['users']

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, new_job_title, new_role, new_acc_state, new_avatar",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, "test_new_title", "ADMIN", "ACTIVE", "test_new_avatar"),
    ],
)
def test_update_valid_user_valid_data(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, new_job_title: str, new_role: str, new_acc_state: str, new_avatar: str):
    """
    Testing updating a valid organization with valid credentials by registering a new user to the SAIL organization, then attempting to update that users info.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    :param new_name: new organization name
    :type new_name: string
    :param new_description: new organization description
    :type new_description: string
    :param new_avatar: new organization avatar
    :type new_avatar: string
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

    # Act
    _, _, access_token = sail_portal.login()

    temp_response, temp_response_json, _ = sail_portal.register_new_user_to_organization(access_token, org_id, "TestName", "test@email.com", "test_title", "ADMIN", "test_avatar", "testpass")
    user_id = temp_response_json["id"]
    print(f"\nUser ID: {user_id}\n")

    update_response, update_response_json, _ = sail_portal.update_organization_user(access_token, org_id, user_id, new_job_title, new_role, new_acc_state, new_avatar)
    print_response_values("Update User Response", update_response, update_response_json, access_token)
    
    test_response, test_response_json, _ = sail_portal.get_organization_user_by_id(access_token, org_id, user_id)
    print_response_values("Verify User Data Changed", test_response, test_response_json, access_token)

    # Assert
    assert_that(update_response.status_code).is_equal_to(204)
    assert_that(test_response_json["role"]).is_equal_to(new_role)
    assert_that(test_response_json["job_title"]).is_equal_to(new_job_title)
    assert_that(test_response_json["avatar"]).is_equal_to(new_avatar)


@pytest.mark.updated
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, user_id",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
    ],
)
def test_update_invalid_user_valid_data(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, user_id: str):
    """
    Testing updating an invalid organization user.

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    :param admin_email: administrator email
    :type admin_email: string
    :param admin_pass: administrator password
    :type admin_pass: string
    :param user_id: user id 
    :type user_id: string
    """
    # Arrange
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "error": {"type": "string"}
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()

    update_response, update_response_json, _ = sail_portal.update_organization_user(access_token, org_id, user_id, None, None, None, None)

    # Assert
    is_valid = validator.validate(update_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(422)



# TODO: Rework after discussion about deletion.
@pytest.mark.broken
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS),
    ],
)
def test_delete_valid_user_from_organization(get_base_url: str, org_id: str, admin_email: str, admin_pass: str):
    """
    Testing deleting a valid organization with valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    global temp_org_id
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()

    temp_response, temp_response_json, _ = sail_portal.register_new_user_to_organization(access_token, org_id, "DeleteName", "delete@email.com", "delete_title", "ADMIN", "delete_avatar", "deletepass")
    user_id = temp_response_json["id"]

    delete_response, delete_response_json, _ = sail_portal.delete_organization_user_by_id(access_token, org_id, user_id)

    verify_response, verify_response_json, _ = sail_portal.get_organization_user_by_id(access_token, org_id, user_id)

    # Assert
    assert_that(verify_response.status_code).is_equal_to(422)
    assert_that(delete_response.status_code).is_equal_to(204)


# TODO: Rework after discussion about deletion.
@pytest.mark.current
@pytest.mark.parametrize(
    "org_id, admin_email, admin_pass, user_id",
    [
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
        (SAIL_ORGANIZATION_ID, SAIL_ORGANIZATION_EMAIL, SAIL_ORGANIZATION_PASS, random_name(32)),
    ],
)
def test_delete_invalid_user_from_organization(get_base_url: str, org_id: str, admin_email: str, admin_pass: str, user_id: str):
    """
    Testing deleting a valid organization with valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    global temp_org_id
    sail_portal = SailPortalApi(base_url=get_base_url, email=admin_email, password=admin_pass)

    schema = {
        "error": {"type": "string"},
    }
    
    validator = Validator(schema)

    # Act
    _, _, access_token = sail_portal.login()

    delete_response, delete_response_json, _ = sail_portal.delete_organization_user_by_id(access_token, org_id, user_id)

    verify_response, verify_response_json, _ = sail_portal.get_organization_user_by_id(access_token, org_id, user_id)

    # Assert
    is_valid = validator.validate(delete_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    is_valid = validator.validate(verify_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(verify_response.status_code).is_equal_to(422)
    assert_that(delete_response.status_code).is_equal_to(422)


# TODO: Rewrite when the 500 Error issue is resolved.
@pytest.mark.broken
@pytest.mark.parametrize(
    "org_id, user_email, user_pass",
    [
        (get_temp_org_id(), TEST_ORGANIZATION_EMAIL, TEST_ORGANIZATION_PASS),
    ],
)
def test_delete_valid_organization_valid_credentials(get_base_url: str, org_id: str, user_email: str, user_pass: str):
    """
    Testing deleting a valid organization with valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    global temp_org_id
    sail_portal = SailPortalApi(base_url=get_base_url, email=user_email, password=user_pass)

    schema = {
        "error": {"type": "string"},
    }

    verify_schema = {
        'avatar': {"type": "string"}, 
        'description': {"type": "string"}, 
        'id': {"type": "string"}, 
        'name': {"type": "string"}
    }
    
    validator = Validator(schema)
    verify_validator = Validator(verify_schema)

    # Act
    _, _, access_token = sail_portal.login()
    print(f"TempOrgID: {temp_org_id}")
    delete_response, delete_response_json, _ = sail_portal.delete_organization(access_token, temp_org_id)
    verify_response, verify_response_json, _ = sail_portal.get_organization_by_id(access_token, temp_org_id)

    print_response_values(test_get_valid_organization_users.__name__, delete_response, delete_response_json, access_token)
    
    print_response_values(test_get_valid_organization_users.__name__, verify_response, verify_response_json, access_token)

    # Assert
    #is_valid = verify_validator.validate(verify_response_json)
    #assert_that(is_valid, description=validator.errors).is_true()
    #assert_that(verify_response.status_code).is_equal_to(422)
    assert_that(delete_response.status_code).is_equal_to(500)

