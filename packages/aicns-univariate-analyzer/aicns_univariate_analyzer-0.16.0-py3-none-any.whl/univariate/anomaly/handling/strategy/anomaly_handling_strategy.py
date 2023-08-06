"""

"""

from abc import ABCMeta, abstractmethod
from enum import Enum
from pyspark.sql import DataFrame
from typing import Optional


class AnomalyHandlingStrategyType(Enum):
    exponential_moving_average = "ExponentialMovingAverage"
    seasonal_mean_replacing = "SeasonalMeanReplacing"


class AnomalyHandlingStrategy(metaclass=ABCMeta):
    """

    """
    @staticmethod
    @abstractmethod
    def handle(ts: DataFrame, time_col_name: str, data_col_name: str, handled_col_name: str, **kwargs) -> DataFrame:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :param handled_col_name:
        :param kwargs:
        :return:
        """
        pass
