from typing import Tuple
import numpy as np
import pandas as pd
from heimdall.gulltoppr.drift_monitor.algorithms.helper_functions import (
    normalising_factor,
    array_like,
    mean_difference,
    get_contingency_table,
)
from scipy.stats import (
    anderson_ksamp,
    ttest_ind,
    ks_2samp,
    mannwhitneyu,
    wasserstein_distance,
    chi2_contingency,
    cramervonmises_2samp,
    binomtest,
    fisher_exact,
    boschloo_exact,
    barnard_exact,
    wilcoxon,
)

TestResult = Tuple[float, float, float, bool]


def default_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
    grams: tuple = (1, 1),
) -> TestResult:
    is_text = validation_data.dtypes[0] in ["string", "object", "category"]
    validation_data_size = len(validation_data)
    validation_unique_values = validation_data.nunique()[0]

    prod_data_size = len(prod_data)
    prod_data_unique_values = prod_data.nunique()[0]

    is_binary = (prod_data_unique_values <= 2) & (validation_unique_values <= 2)
    low_cardinality = (prod_data_unique_values <= 10) & (validation_unique_values <= 10)
    low_volume = (prod_data_size < 1000) & (validation_data_size < 1000)
    different_sample_sizes = 0.025 < prod_data_size / validation_data_size < 25

    if is_binary:
        return binomial_test(validation_data, prod_data, threshold, grams) + (
            "binomial_test",
        )

    elif is_text:
        return chi_sq_test(validation_data, prod_data, threshold, grams) + (
            "chi_sq_test",
        )

    elif low_cardinality:
        return chi_sq_test(validation_data, prod_data, threshold, grams) + (
            "chi_sq_test",
        )

    elif different_sample_sizes:
        return welch_ttest(validation_data, prod_data, threshold) + ("welch_ttest",)

    elif low_volume:
        return ks_test(validation_data, prod_data, threshold) + ("ks_test",)

    else:
        return wasserstein_distance_test(validation_data, prod_data, threshold) + (
            "wasserstein_distance_test",
        )


def binomial_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
    grams: tuple = (1, 1),
) -> TestResult:
    trans_continguency_table = get_contingency_table(
        validation_data, prod_data, grams
    ).T

    if (trans_continguency_table[0][0] != 0) & (trans_continguency_table[0][1] != 0):
        ks = trans_continguency_table[0]
    else:
        ks = trans_continguency_table[1]

    prod_k = ks[0].astype(int)
    validation_k = ks[1].astype(int)

    validation_n = len(validation_data)
    prod_n = len(prod_data)
    p = validation_k / validation_n

    p_value = round(binomtest(prod_k, prod_n, p).pvalue, 4)

    return p, p_value, threshold, p_value < 1 - threshold


def accepted_values_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    values: list = [],
) -> TestResult:
    validation_data, prod_data = array_like(validation_data, prod_data)

    accepted_set = list(set(values))
    reference_set = list(set(validation_data.squeeze()))
    current_set = list(set(prod_data.squeeze()))

    accepted_set = len(accepted_set)
    reference_set = len(reference_set)
    current_set = len(reference_set)

    equal_sets = (accepted_set == current_set) & (reference_set == current_set)
    test_score = 0 if not equal_sets else 1

    return (current_set + reference_set) / (2 * accepted_set), test_score, 1, equal_sets


def unique_values_test(
    validation_data: pd.DataFrame, prod_data: pd.DataFrame
) -> TestResult:
    validation_data, prod_data = array_like(validation_data, prod_data)

    reference_unique = validation_data.nunique()
    reference_count = validation_data.count()

    current_unique = prod_data.nunique()
    current_count = prod_data.count()

    unique_data = (reference_count == reference_unique) & (
        current_unique == current_count
    )
    test_score = 0 if not unique_data else 1

    return (
        (reference_unique + current_unique) / (reference_count + current_count),
        test_score,
        1,
        unique_data,
    )


def mann_whitney_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
) -> TestResult:
    validation_data, prod_data = array_like(validation_data, prod_data)

    test_result = mannwhitneyu(validation_data, prod_data)
    test_score = round(test_result.statistic, 4)
    p_value = round(test_result.pvalue, 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def wilcoxon_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
) -> TestResult:
    validation_data, prod_data = array_like(validation_data, prod_data)

    test_result = wilcoxon(validation_data, prod_data)
    test_score = round(test_result.statistic, 4)
    p_value = round(test_result.pvalue, 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def anderson_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
) -> TestResult:
    validation_data, prod_data = array_like(validation_data, prod_data)

    test_result = anderson_ksamp(np.array([validation_data, prod_data]))
    test_score = round(test_result.statistic, 4)
    p_value = round(test_result.significance_level, 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def cramer_von_mises_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
) -> TestResult:
    validation_data, prod_data = array_like(validation_data, prod_data)

    test_result = cramervonmises_2samp(validation_data, prod_data)
    test_score = round(test_result.statistic, 4)
    p_value = round(test_result.pvalue, 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def welch_ttest(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
) -> TestResult:
    """
    Welch's t-test for independence.

    Args:
        validation_data (pd.DataFrame): Data used when training the model.
        prod_data (pd.DataFrame): Data currently being input to the model.
        threshold (float, optional): Threshold to determine whether or not to reject the null
            hypothesis that the reference data and current data come for the same distribution.
            Defaults to 0.95.

    Returns:
        TestResult: Tuple of the score generated by test, the p value of the test,
            the threshold used, and whether or not to reject the null hypothesis.
    """
    validation_data, prod_data = array_like(validation_data, prod_data)

    test_result = ttest_ind(validation_data, prod_data)
    test_score = round(test_result.statistic, 4)
    p_value = round(test_result.pvalue, 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def ks_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
) -> TestResult:
    validation_data, prod_data = array_like(validation_data, prod_data)

    test_result = ks_2samp(validation_data, prod_data)
    test_score = round(test_result.statistic, 4)
    p_value = round(test_result.pvalue, 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def wasserstein_distance_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.1,
) -> TestResult:
    """
    Wasserstein distance test used to determine whether two sets of data come from the same distribution,
    by calculating the work required to turn one into the other.

    Wasserstein distance is an integral over |x-y|, so we normalise with standard deviation.

    Args:
        validation_data (pd.DataFrame): Data used when training the model.
        prod_data (pd.DataFrame): Data currently being input to the model.
        threshold (float, optional): Threshold to determine whether or not to reject the null
            hypothesis that the reference data and current data come for the same distribution.
            Defaults to 0.1.

    Returns:
        TestResult: Tuple of the score generated by test, the p value of the test,
            the threshold used, and whether or not to reject the null hypothesis.
    """
    validation_data, prod_data = array_like(validation_data, prod_data)

    norm = normalising_factor(validation_data)
    test_result = wasserstein_distance(validation_data, prod_data)
    test_score = round(test_result, 4)
    p_value = round(test_result / norm, 4)

    return test_score, p_value, threshold, p_value >= threshold


def chi_sq_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
    grams: tuple = (1, 1),
) -> TestResult:
    contingency_table = get_contingency_table(validation_data, prod_data, grams)

    test_result = chi2_contingency(contingency_table)
    test_score = round(test_result[0], 4)
    p_value = round(test_result[1], 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def fisher_exact_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
    grams: tuple = (1, 1),
) -> TestResult:
    contingency_table = get_contingency_table(validation_data, prod_data)

    test_result = fisher_exact(contingency_table)
    test_score = round(test_result[0], 4)
    p_value = round(test_result[1], 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def boschloo_exact_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
    grams: tuple = (1, 1),
) -> TestResult:
    contingency_table = get_contingency_table(validation_data, prod_data, grams)

    test_result = boschloo_exact(contingency_table)
    test_score = round(test_result.statistic, 4)
    p_value = round(test_result.pvalue, 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def barnard_exact_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.95,
    grams: tuple = (1, 1),
) -> TestResult:
    contingency_table = get_contingency_table(validation_data, prod_data)

    test_result = barnard_exact(contingency_table)
    test_score = round(test_result.statistic, 4)
    p_value = round(test_result.pvalue, 4)

    return test_score, p_value, threshold, p_value < 1 - threshold


def distribution_mean_test(
    validation_data: pd.DataFrame,
    prod_data: pd.DataFrame,
    threshold: float = 0.1,
) -> TestResult:
    validation_data, prod_data = array_like(validation_data, prod_data)

    norm = normalising_factor(validation_data)
    test_result = mean_difference(validation_data, prod_data)
    test_score = round(test_result, 4)
    p_value = round(abs(test_result) / norm, 4)

    return test_score, p_value, threshold, p_value >= threshold
