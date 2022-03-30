# -----------------------------------------------------------
#
# Orchestrator Unit test file - Datasets
#
# -----------------------------------------------------------

import json

import pytest
import sail.core
from assertpy.assertpy import assert_that
from cerberus import Validator


@pytest.mark.active
def test_list_no_loaded(orchestrator_fresh_session_fixture):
    """
    Test listing datasets with no one logged in
    """
    # Act
    test_response = sail.core.get_datasets()
    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
def test_list_cleared_exit_session(orchestrator_login_fixture):
    """
    Test getting a dataset list after we've exited a session
    """

    # Arrange
    logged_in_response = sail.core.get_datasets()
    sail.core.exit_current_session()

    # Act
    test_response = sail.core.get_datasets()

    # Assert
    assert_that(test_response).is_none()
    assert_that(test_response).is_not_equal_to(logged_in_response)


@pytest.mark.active
def test_list_datasets(orchestrator_login_fixture):
    """
    Test getting a dataset list once we're logged in
    """
    # Arrange
    schema = {
        "return_value": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "DataOwnerGuid": {"type": "string"},
                    "DatasetGuid": {"type": "string"},
                    "DatasetName": {"type": "string"},
                    "Description": {"type": "string"},
                    "JurisdictionalLimitations": {"type": "string"},
                    "Keywords": {"type": "string"},
                    "OrganizationName": {"type": "string"},
                    "PrivacyLevel": {"type": "number"},
                    "PublishDate": {"type": "number"},
                    "Tables": {
                        "type": "dict",
                        "valueschema": {
                            "type": "dict",
                            "schema": {
                                "ColumnName": {"type": "string"},
                                "Description": {"type": "string"},
                                "Hashtags": {"type": "string"},
                                "Name": {"type": "string"},
                                "NumberColumns": {"type": "number"},
                                "NumberRows": {"type": "number"},
                            },
                        },
                    },
                    "VersionNumber": {"type": "string"},
                },
            },
        },
    }
    validator = Validator(schema)

    # Act
    test_response = sail.core.get_datasets()

    # Assert
    assert_that(test_response).is_not_none()
    json_response = {}
    json_response["return_value"] = json.loads(test_response)
    is_valid = validator.validate(json_response)
    assert_that(is_valid, description=validator.errors).is_true()
