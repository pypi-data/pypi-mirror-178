"""

"""

from abc import ABCMeta
from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport
from typing import Optional

class AnomalyDetector(metaclass=ABCMeta):
    """

    """
    @staticmethod
    def detect(ts: DataFrame, **kwargs) -> AnalysisReport:
        """

        :param ts:
        :param kwargs:
        :return:
        """
        pass
