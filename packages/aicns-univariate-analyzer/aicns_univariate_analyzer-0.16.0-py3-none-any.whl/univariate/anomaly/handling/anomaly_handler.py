"""

"""

from abc import ABCMeta
from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport
from typing import Optional
from univariate.anomaly.handling.strategy import AnomalyHandlingStrategyType, AnomalyHandlingStrategy
import importlib
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


class AnomalyHandler(metaclass=ABCMeta):
    """

    """
    @staticmethod
    def handle(ts: DataFrame, time_col_name: str, data_col_name: str, handled_col_name: Optional[str] = None, handling_strategy_type: Optional[AnomalyHandlingStrategyType] = AnomalyHandlingStrategyType.exponential_moving_average, **kwargs) -> AnalysisReport:
        """

        :param ts:
        :param kwargs:
        :return:
        """
        concrete_cls = getattr(
            importlib.import_module("univariate.anomaly.handling.strategy"),
            handling_strategy_type.value,
        )
        handling_strategy: AnomalyHandlingStrategy = concrete_cls()

        if handled_col_name is None:
            handled_col_name = "anomaly_handled_data"

        handled_df = handling_strategy.handle(ts, time_col_name, data_col_name, handled_col_name, **kwargs)

        report = AnomalyHandler.__build_report(handled_df, handling_strategy_type, time_col_name, data_col_name, handled_col_name)
        return report

    @staticmethod
    def __build_report(handled_df: DataFrame, handling_strategy_type: AnomalyHandlingStrategyType, time_col_name: str, data_col_name: str, handled_col_name: str):
        """

        :param handled_df:
        :return:
        """
        report = AnalysisReport()
        report.parameters["handled_df"] = handled_df
        report.parameters["handling_strategy"] = handling_strategy_type.value

        report.plots["comparison_plot"] = AnomalyHandler.__build_plot(handled_df, time_col_name, data_col_name, handled_col_name)

        return report

    @staticmethod
    def __build_plot(handled_df: DataFrame, time_col_name: str, data_col_name: str, handled_col_name: str) -> Figure:
        """

        :param handled_df:
        :param time_col_name:
        :param data_col_name:
        :param handled_col_name:
        :return:
        """
        ts_pd = handled_df.select(time_col_name, data_col_name, handled_col_name).sort(time_col_name).toPandas()
        ts_pd[time_col_name] = pd.to_datetime(ts_pd[time_col_name], unit='ms')
        fig = px.line(ts_pd, x=time_col_name, y=[data_col_name, handled_col_name])
        return fig
