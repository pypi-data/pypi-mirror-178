from heimdall.gulltoppr.systems_monitor.metrics.helper_functions import (
    privilege_test,
    sample_datasets,
)
from aif360.sklearn.metrics import (
    class_imbalance,
    consistency_score,
    average_odds_difference,
    average_odds_error,
    conditional_demographic_disparity,
    generalized_entropy_error,
    df_bias_amplification,
    kl_divergence,
    coefficient_of_variation,
    theil_index,
)
from typing import Tuple, Union
import pandas as pd

## Bias scan allows us to decide if we aim to identify bias as higher than expected probabilities or lower than expected probabilities.
def overprivileged_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.Series,
    positive_group: Union[str, int],
    protected_df: list = None,
    threshold: float = 0.1,
) -> Tuple[dict, str]:
    subset = privilege_test(X_bucketed, y_true, y_pred, True)

    return subset


def underprivileged_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.Series,
    positive_group: Union[str, int],
    protected_df: list = None,
    threshold: float = 0.1,
) -> Tuple[dict, str]:
    subset = privilege_test(X_bucketed, y_true, y_pred, False)

    return subset


def imbalance_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.Series,
    positive_group: Union[str, int],
    protected_df: list = None,
    threshold: float = 0.1,
):
    imbalance = class_imbalance(
        y_true=y_true,
        y_pred=y_pred,
        prot_attr=protected_df,
        priv_group=positive_group,
    )

    return imbalance, threshold, imbalance > threshold


def odds_difference_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.Series,
    positive_group: Union[str, int],
    protected_df: list = None,
    threshold: float = 0.1,
):
    odds_difference = average_odds_difference(
        y_true=y_true,
        y_pred=y_label,
        prot_attr=protected_df,
        priv_group=positive_group,
    )

    return odds_difference, threshold, odds_difference > threshold


def odds_error_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.DataFrame,
    positive_group: Union[str, int],
    protected_df: list = 0.1,
    threshold: float = 0.95,
):
    odds_error = average_odds_error(
        y_true=y_true,
        y_pred=y_label,
        prot_attr=protected_df,
        priv_group=positive_group,
    )

    return odds_error, threshold, odds_error > threshold


def demographic_disparity_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.DataFrame,
    positive_group: Union[str, int],
    protected_df: list = 0.1,
    threshold: float = 0.95,
):
    y_true, y_label, protected_df = sample_datasets(y_true, y_label, protected_df)
    disparity = conditional_demographic_disparity(
        y_true=y_true, y_pred=y_label, prot_attr=protected_df
    )

    return disparity, threshold, disparity > threshold


def entropy_error_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.DataFrame,
    positive_group: Union[str, int],
    protected_df: list = None,
    threshold: float = 0.1,
):
    entropy_error = generalized_entropy_error(y_true=y_true, y_pred=y_label)

    return entropy_error, threshold, entropy_error > threshold


def bias_amplification_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.DataFrame,
    positive_group: Union[str, int],
    protected_df: list = None,
    threshold: float = 0.1,
):
    bias_amp = df_bias_amplification(
        y_true=y_true,
        y_pred=y_pred,
        prot_attr=protected_df,
        pos_label=positive_group,
    )

    return bias_amp, threshold, bias_amp > threshold


def consistency_score(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.DataFrame,
    positive_group: Union[str, int],
    protected_df: list = None,
    threshold: float = 0.1,
):
    cons_score = consistency_score(X=X, y=y_true)

    return cons_score, threshold, cons_score > threshold


def divergence_test(
    X: pd.DataFrame,
    X_bucketed: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    y_label: pd.DataFrame,
    positive_group: Union[str, int],
    protected_df: list = None,
    threshold: float = 0.1,
):
    divergence = kl_divergence(
        y_true=y_true,
        y_pred=y_pred,
        prot_attr=protected_df,
        priv_group=positive_group,
    )

    return divergence, threshold, divergence > threshold


def cov_test(X: pd.DataFrame):
    cov = coefficient_of_variation(X)

    return cov


def theil_test(X: pd.DataFrame):
    theil_test = theil_index(X)

    return theil_test
