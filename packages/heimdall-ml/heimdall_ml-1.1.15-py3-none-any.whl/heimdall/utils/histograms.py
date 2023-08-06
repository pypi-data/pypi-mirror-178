import numpy as np
from heimdall.gulltoppr.drift_monitor.algorithms.helper_functions import vectorify


def df_bins(df):
    q25, q75 = np.percentile(df, [25, 75])

    if q25 == q75:
        q25 = q25 - 0.5
        q75 = q75 + 0.5

    iqr = q75 - q25
    n = len(df)

    h = 2 * iqr * n ** (-1 / 3)
    n_bins = max((df.max() - df.min()) / h, 1)

    return n_bins


def get_edges(df):
    first_edge = df.min()
    last_edge = df.max()

    if first_edge == last_edge:
        last_edge = last_edge + 0.5

    return first_edge, last_edge


def get_bin_edges(df, n_bins, first_edge, last_edge):
    bin_type = np.result_type(first_edge, last_edge, df)
    if np.issubdtype(bin_type, np.integer):
        bin_type = np.result_type(bin_type, float)

    bin_edges = np.linspace(
        first_edge, last_edge, n_bins + 1, endpoint=True, dtype=bin_type
    )

    return bin_edges


def get_hist_edges(df, max_bins):
    num_unique = len(np.unique(df))
    n_bins = int(np.ceil(min(max_bins, df_bins(df))))

    if num_unique < n_bins:
        n_bins = num_unique

    first_edge, last_edge = get_edges(df)
    bin_edges = get_bin_edges(df, n_bins, first_edge, last_edge)

    return bin_edges


def get_joint_hist(prod_data, valid_data, grams: tuple = (1, 1)):
    if valid_data.dtype in ["string", "object", "category"]:
        valid_data, prod_data = vectorify(valid_data, prod_data, grams)
        valid_data = valid_data.round(4)
        prod_data = prod_data.round(4)
        hist_dict = (
            valid_data.merge(prod_data)
            .set_index("vocab")
            .rename(columns={"validation_data": "valid", "prod_data": "prod"})
            .T.to_dict()
        )

    else:
        combined_data = np.concatenate((prod_data, valid_data))
        hist_bins = get_hist_edges(combined_data, 100)

        prod_heights, _ = np.histogram(prod_data, bins=hist_bins)
        valid_heights, _ = np.histogram(valid_data, bins=hist_bins)

        prod_heights = (prod_heights / len(prod_data)).round(4)
        valid_heights = (valid_heights / len(valid_data)).round(4)

        if len(hist_bins) == 3:
            hist_bins = np.delete(hist_bins, 1)

        hist_dict = {
            round(k, 3): {"valid": v1, "prod": v2}
            for k, v1, v2 in zip(hist_bins, valid_heights, prod_heights)
        }

    return hist_dict
