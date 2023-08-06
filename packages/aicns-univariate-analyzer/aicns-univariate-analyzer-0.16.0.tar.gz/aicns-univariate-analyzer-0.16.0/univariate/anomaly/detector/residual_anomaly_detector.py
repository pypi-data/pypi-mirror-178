"""

"""

from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport
from univariate.anomaly.detector import AnomalyDetector
from typing import Optional
import pyspark.sql.functions as F
import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd


class ResidualAnomalyDetector(AnomalyDetector):
    """

    """
    @staticmethod
    def detect(ts: DataFrame, time_col_name: str, resid_col_name: str, ad_hoc: Optional[bool] = True, upper_limit: Optional[float] = None, lower_limit: Optional[float] = None) -> AnalysisReport:
        """
        Anomaly detection by residual distribution. It use 6-sigma rule now.
        :param ts:
        :param time_col_name:
        :param resid_col_name:
        :param ad_hoc:
        :param upper_limit:
        :param lower_limit:
        :return:
        """
        # todo: parameterize confidence interval
        # validate parameters #1: if ad_hoc is false, then lower_limit, upper_limit must be passed
        if not ad_hoc and (lower_limit is None or upper_limit is None):
            raise TypeError("If ad_hoc is false, then lower_limit, upper_limit must be passed")

        # ad-hoc distribution analysis, for obtaining mean, stddev, lower_limit(mean - 3*stddev), upper_limit(mean + 3*stddev)
        if ad_hoc:
            stat_dict = ts.agg(
                F.mean(resid_col_name).alias(
                    "mean"
                ),
                F.stddev(resid_col_name).alias(
                    "stddev"
                )
            ).first().asDict()

            # shadow parameters
            mean = stat_dict["mean"]
            stddev = stat_dict['stddev']

            lower_limit = mean - 3 * stddev
            upper_limit = mean + 3 * stddev

        # detect outliers (classify)
        condition = (F.col(resid_col_name) <= lower_limit) | (F.col(resid_col_name) >= upper_limit)
        anomaly_detected_df = ts.withColumn("is_anomaly_by_residual", F.when(condition, True).otherwise(False))  # checked null -> false, # todo: testcase..

        # figure plot
        plot = ResidualAnomalyDetector.__build_plot(ts, time_col_name, resid_col_name, lower_limit, upper_limit)

        # build report
        report = AnalysisReport()
        report.parameters["lower_limit"] = lower_limit
        report.parameters["upper_limit"] = upper_limit
        report.parameters["anomaly_detected_df"] = anomaly_detected_df
        report.plots['resid_plot'] = plot
        return report

    @staticmethod
    def __build_plot(ts: DataFrame, time_col_name: str, resid_col_name: str, lower_limit: float, upper_limit: float) -> Figure:
        ts_pd = ts.sort(time_col_name).select(time_col_name, resid_col_name).toPandas()
        ts_pd[time_col_name] = pd.to_datetime(ts_pd[time_col_name], unit='ms')
        fig = px.line(ts_pd, x=time_col_name, y=resid_col_name)
        fig.add_hline(y=upper_limit, line_dash="dot",
                      annotation_text="mean(resid) + stddev(resid) * 3",
                      annotation_position="top left")
        fig.add_hline(y=lower_limit, line_dash="dot",
                      annotation_text="mean(resid) - stddev(resid) * 3",
                      annotation_position="bottom left")
        return fig
