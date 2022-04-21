"""
Pytest fixtures
"""
import os
from typing import Tuple
import pytest

import numpy as np

from config import DATA_PATH

from helper_sail_safe_functions.dataframe_federated_local import DataframeFederatedLocal
from helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


@pytest.fixture
def one_sample_big() -> SeriesFederatedLocal:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset

    :return: DataframeFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"

    dataframe = DataframeFederatedLocal()
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        dataframe.add_csv(path_file_csv)

    return dataframe[id_column_0]


@pytest.fixture
def two_sample_big() -> SeriesFederatedLocal:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset

    :return: DataframeFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"
    id_column_1 = "PD-L1 level after treatment"

    dataframe = DataframeFederatedLocal()
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        dataframe.add_csv(path_file_csv)

    return (dataframe[id_column_0], dataframe[id_column_1])


@pytest.fixture
def two_sample_small() -> Tuple[SeriesFederatedLocal, SeriesFederatedLocal]:
    """
    A two sample tuple with data from

    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    sample_0_numpy = np.array([17.2, 20.9, 22.6, 18.1, 21.7, 21.4, 23.5, 24.2, 14.7, 21.8])
    sample_1_numpy = np.array(
        [
            21.5,
            22.8,
            21.0,
            23.0,
            21.6,
            23.6,
            22.5,
            20.7,
            23.4,
            21.8,
            20.7,
            21.7,
            21.5,
            22.5,
            23.6,
            21.5,
            22.5,
            23.5,
            21.5,
            21.8,
        ]
    )

    sample_0 = SeriesFederatedLocal("sample_0")
    sample_0.add_array("array_test", sample_0_numpy)
    sample_1 = SeriesFederatedLocal("sample_1")
    sample_1.add_array("array_test", sample_1_numpy)
    return (sample_0, sample_1)
