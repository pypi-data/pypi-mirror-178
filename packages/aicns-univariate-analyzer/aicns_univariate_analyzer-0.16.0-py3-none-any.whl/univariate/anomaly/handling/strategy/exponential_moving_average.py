"""

"""


from univariate.anomaly.handling.strategy import AnomalyHandlingStrategy
from typing import Optional, List
from pyspark.sql import DataFrame
from functools import reduce
from pyspark.sql import functions as F
from pyspark.sql.types import FloatType
from pyspark.sql.window import Window


class ExponentialMovingAverage(AnomalyHandlingStrategy):
    """


    """
    @staticmethod
    def handle(ts: DataFrame, time_col_name: str, data_col_name: str, handled_col_name: str, alpha: Optional[float] = None, window_size: Optional[int] = 10, point_wise: Optional[bool] = False, anomaly_flag_col: Optional[str] = None) -> DataFrame:
        """
        
        :param ts: 
        :param time_col_name: 
        :param data_col_name: 
        :param handled_col_name: 
        :param alpha: 
        :param window_size: If alpha is None, then adjusted 2.0 / (windowSize + 1)
        :param point_wise: if point_wise is True (default False), EMA will be applied only in {anomaly_flag_col} is True.
        So if point_wise is True, than anomaly_flag_col must be passed.
        :param anomaly_flag_col: If point_wise is True, only {anomaly_flag_col} will be applied EMA, otherwise remain {data_col_name} value
        :return: 
        """
        window = Window.orderBy(time_col_name).rowsBetween(-window_size + 1, 0)
        window_df = ts.sort(time_col_name).withColumn("_window", F.collect_list(data_col_name).over(window))

        if not point_wise:
            anomaly_flag_col = "_dummy"
            window_df = window_df.withColumn(anomaly_flag_col, F.lit(True))

        if alpha is None:
            alpha = 2.0 / (window_size + 1)

        calc_exponential_moving_average_udf = F.udf(calc_exponential_moving_average, FloatType())
        handled_df = window_df.withColumn(handled_col_name, F.when(F.col(anomaly_flag_col), calc_exponential_moving_average_udf(F.col("_window"), F.lit(alpha))).otherwise(F.col(data_col_name))).drop("_window").sort(time_col_name)

        if not point_wise:
            handled_df = handled_df.drop(anomaly_flag_col)

        return handled_df


def calc_exponential_moving_average(window: List[float], alpha: float):
    """

    :param window:
    :param alpha:
    :return:
    """
    if len(window) == 0:
        raise ValueError("Window size must be greater than 0")

    return reduce(lambda s_t_1, y_t: alpha * y_t + (1 - alpha) * s_t_1, window[1:], window[0])