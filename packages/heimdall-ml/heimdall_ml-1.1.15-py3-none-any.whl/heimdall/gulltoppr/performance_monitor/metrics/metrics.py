import sklearn.metrics as mets
import pandas as pd
from typing import Tuple

MetricResult = Tuple[float, float, bool]

## Classification


def log_loss(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.log_loss(y_true, y_pred)
    return metric, threshold, metric < threshold


def accuracy(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.accuracy_score(y_true, y_pred)
    return metric, threshold, metric < threshold


def balanced_accuracy(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.balanced_accuracy_score(y_true, y_pred)
    return metric, threshold, metric < threshold


def auc(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.roc_auc_score(y_true, y_pred)
    return metric, threshold, metric < threshold


def f1_score(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.f1_score(y_true, y_pred)
    return metric, threshold, metric < threshold


def precision(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.precision_score(y_true, y_pred)
    return metric, threshold, metric < threshold


def recall(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.recall_score(y_true, y_pred)
    return metric, threshold, metric < threshold


## Regression


def mae(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.mean_absolute_percentage_error(y_true, y_pred)
    return metric, threshold, metric < threshold


def mse(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.mean_absolute_error(y_true, y_pred)
    return metric, threshold, metric < threshold


def rmse(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.mean_absolute_error(y_true, y_pred, squared=False)
    return metric, threshold, metric < threshold


def r2(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.recall_score(y_true, y_pred)
    return metric, threshold, metric < threshold


def pinball(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.d2_pinball_score(y_true, y_pred)
    return metric, threshold, metric < threshold


def absolute_error(
    y_true: pd.DataFrame, y_pred: pd.DataFrame, threshold: float = 0
) -> MetricResult:
    metric = mets.d2_absolute_error_score(y_true, y_pred)
    return metric, threshold, metric < threshold
