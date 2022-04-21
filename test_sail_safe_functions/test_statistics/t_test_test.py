from typing import Tuple
import pytest
from scipy import stats

from sail_statstics.procedure.t_test.t_test_federate import TTestFederate
from helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


@pytest.mark.active
def test_t_test_unpaired_equal_varriance_big(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """Preform a unpaired t-test asuming equal varriance

    Args:
        two_sample_big (Tuple[SeriesFederatedLocal, SeriesFederatedLocal]): A tuple of two federated series
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]

    # Act
    t_statistic_sail, p_value_sail = TTestFederate.ttest_ind(
        sample_0, sample_1, equal_varriances=True, alternative="less"
    )

    t_statistic_scipy, p_value_scipy = stats.ttest_ind(
        sample_0.to_numpy(), sample_1.to_numpy(), equal_var=True, alternative="less"
    )

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)


@pytest.mark.active
def test_t_test_unpaired_unequal_varriance_small(two_sample_small: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """Preform a unpaired t-test asuming unequal varriance (welch t-test) using a smaller dataset

    Args:
        two_sample_big (Tuple[SeriesFederatedLocal, SeriesFederatedLocal]): A tuple of two federated series
    """
    # Arrange
    sample_0 = two_sample_small[0]
    sample_1 = two_sample_small[1]

    # Act
    t_statistic_sail, p_value_sail = TTestFederate.ttest_ind(
        sample_0, sample_1, equal_varriances=False, alternative="less"
    )

    t_statistic_scipy, p_value_scipy = stats.ttest_ind(
        sample_0.to_numpy(), sample_1.to_numpy(), equal_var=False, alternative="less"
    )

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)


@pytest.mark.active
def test_t_test_unpaired_unequal_varriance_big(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """Preform a unpaired t-test asuming unequal varriance (welch t-test) using a smaller dataset

    Args:
        two_sample_big (Tuple[SeriesFederatedLocal, SeriesFederatedLocal]): A tuple of two federated series
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]

    # Act
    t_statistic_sail, p_value_sail = TTestFederate.ttest_ind(
        sample_0, sample_1, equal_varriances=False, alternative="less"
    )

    t_statistic_scipy, p_value_scipy = stats.ttest_ind(
        sample_0.to_numpy(), sample_1.to_numpy(), equal_var=False, alternative="less"
    )

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)
