import pandas as pd
from typing import Union
from heimdall.utils.logging import get_logger
from heimdall.gulltoppr.systems_monitor.metrics import metrics as mets
from heimdall.gulltoppr.systems_monitor.metrics.helper_functions import (
    bucket_features,
    get_continuous_list,
)

logger = get_logger(__name__)


class SystemsMonitor:
    def __init__(
        self,
        model: dict,
        dataset: pd.DataFrame,
        features: Union[list, str],
        target_column: str,
        prediction_column: str,
        predicted_label_column: str,
    ):
        self.model = model
        self.model_name = model.get("name")
        self.metrics = model.get("metrics").get("fairness")
        self.target_column = target_column
        self.prediction_column = prediction_column
        self.predicted_label_column = predicted_label_column

        self.protected_features = self.get_protected_features(self.model)
        self.positive_label = self.get_positive_label(self.model)

        X = dataset[features]
        X_bucketed = bucket_features(X.copy())
        X_protected = (
            None
            if len(self.protected_features) == 0
            else X_bucketed[self.protected_features]
        )

        y_true = dataset[target_column].squeeze()
        y_pred = dataset[prediction_column].squeeze()
        y_label = dataset[predicted_label_column].squeeze()

        logger.info(f"Initialising concept monitor for {self.model_name}")
        self.calculate_metrics(
            self.metrics,
            X,
            X_bucketed,
            X_protected,
            y_true,
            y_pred,
            y_label,
            self.positive_label,
        )

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

    @staticmethod
    def get_protected_features(model):
        protected_features = []

        if "features" in model:
            model_features = model.get("features")
            for feature in model_features:
                if feature.get("protected"):
                    protected_features.append(feature.get("name"))

        return protected_features

    @staticmethod
    def get_positive_label(model):
        model_target = model.get("target")
        positive_label = model_target[0].get("positive_label")

        return positive_label

    def calculate_metrics(
        self,
        metrics,
        X,
        X_bucketed,
        X_protected,
        y_true,
        y_pred,
        y_label,
        positive_group,
    ):
        metric_results = {}
        bias_results = {}

        for metric in metrics:
            metric_func, metric_name, metric_kwargs = self.get_metric(metric)

            metric_score = metric_func(
                X, X_bucketed, y_true, y_pred, y_label, positive_group, X_protected
            )

            if metric in ["overprivileged_test", "underprivileged_test"]:
                metric_score = metric_score[0]

                for i in metric_score:
                    bias_range = metric_score.get(i)
                    bias_range = get_continuous_list(bias_range)

                    metric_score.update({i: bias_range})

                bias_results.update({metric_name: metric_score})

            else:
                metric_value = round(metric_score[0], 4)
                metric_threshold = metric_score[1]
                below_threshold = metric_score[2]

                metric_results.update(
                    {
                        metric_name: {
                            "metric_score": metric_value,
                            "threshold": metric_threshold,
                            "drift_detected": below_threshold,
                        }
                    }
                )

        self.metric_results = metric_results
        self.bias_results = bias_results

        results = {}

        if len(metric_results) > 0:
            results.update({"metrics": metric_results})

        if len(bias_results) > 0:
            results.update({"bias": bias_results})

        self.results = results
