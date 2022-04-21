import numpy as np
import pandas as pd

# from sail_safe_funcions.orchestrator.series_federated import SeriesFederated


# class SeriesFederatedLocal(SeriesFederated):


class SeriesFederatedLocal:
    """
    Helper class for testing federated statics, it incorperates several series but pretends to be asingle one
    """

    def __init__(self, name: str = None) -> None:
        super().__init__()
        self.dict_series = {}
        self.name = None

    def add_series(self, key: str, series=pd.Series):
        if self.name is None:
            self.name = series.name
        else:
            if self.name != series.name:
                raise RuntimeError("Cannot add series with different name")
        self.dict_series[key] = series

    def add_array(self, key: str, array: np.ndarray, name: str = None):
        if name is None:
            self.add_series(key, pd.Series(data=array, name=self.name))
        else:
            self.add_series(key, pd.Series(data=array, name=name))

    def to_numpy(self) -> np.ndarray:
        list_array_numpy = []
        for series in self.dict_series.values():
            list_array_numpy.append(series.to_numpy())
        return np.concatenate(list_array_numpy)
