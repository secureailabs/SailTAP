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
@pytest.mark.usefixtures("orchestrator_fresh_session_fixture")
def test_list_no_loaded():
    """
    Test listing datasets with no one logged in
    """
    # Act
    test_response = sail.core.get_datasets()
    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_list_cleared_exit_session():
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
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_list_datasets():
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
                                "TableIdentifier": {"type": "string"},
                                "ColumnName": {"type": "string"},
                                "Description": {"type": "string"},
                                "Tags": {"type": "string"},
                                "Hashtags": {"type": "string", "required": False},
                                "Name": {"type": "string", "required": False},
                                "NumberColumns": {"type": "number", "required": False},
                                "NumberRows": {"type": "number", "required": False},
                                "Title": {"type": "string"},
                                "NumberOfColumns": {"type": "number"},
                                "NumberOfRows": {"type": "number"},
                                "CompressedDataSizeInBytes": {"type": "number"},
                                "DataSizeInBytes": {"type": "number"},
                                "AllColumnProperties": {
                                    "type": "dict",
                                    "valueschema": {
                                        "type": "dict",
                                        "schema": {
                                            "ColumnIdentifier": {"type": "string"},
                                            "Description": {"type": "string"},
                                            "Tags": {"type": "string"},
                                            "Title": {"type": "string"},
                                            "Type": {"type": "string"},
                                            "Units": {"type": "string"},
                                        },
                                    },
                                },
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
