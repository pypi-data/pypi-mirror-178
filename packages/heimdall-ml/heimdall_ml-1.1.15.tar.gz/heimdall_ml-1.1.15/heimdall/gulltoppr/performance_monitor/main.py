import pandas as pd
from heimdall.utils.logging import get_logger
from heimdall.gulltoppr.performance_monitor.metrics import metrics as mets

logger = get_logger(__name__)


class PerformanceMonitor:
    def __init__(
        self,
        model: dict,
        target: list,
        prediction: list,
        prod_target: pd.DataFrame,
        valid_target: pd.DataFrame,
    ):
        self.model = model
        self.model_name = model.get("name")
        self.metrics = model.get("metrics").get("performance")
        self.target = target
        self.prediction = prediction

        logger.info(f"Initialising performance monitor for {self.model_name}")
        self.calculate_metrics(self.metrics, prod_target, valid_target)

    @staticmethod
    def get_metric(metrics):
        if type(metrics) == dict:
            metric_name = list(metrics)[0]
            metric_kwargs = metrics.get(metric_name)

        elif type(metrics) == str:
            metric_name = metrics
            metric_kwargs = {}

        metric_func = mets.__getattribute__(metric_name)

        return metric_func, metric_name, metric_kwargs

    def calculate_metrics(self, metrics, prod_data, valid_data):
        metric_results = {}
        for metric in metrics:
            metric_func, metric_name, metric_kwargs = self.get_metric(metric)

            prod_target = prod_data[self.target]
            prod_prediction = prod_data[self.prediction]

            validation_target = valid_data[self.target]
            validation_prediction = valid_data[self.prediction]

            prod_metric, metric_threshold, below_threshold = metric_func(
                prod_target, prod_prediction, **metric_kwargs
            )

            eval_metric, _, _ = metric_func(
                validation_target, validation_prediction, **metric_kwargs
            )

            metric_results.update(
                {
                    metric_name: {
                        "prod_metric": round(prod_metric, 4),
                        "eval_metric": round(eval_metric, 4),
                        "threshold": metric_threshold,
                        "drift_detected": below_threshold,
                    }
                }
            )

        self.metric_results = metric_results
