import pandas as pd
import re
from typing import Tuple
from aif360.detectors.mdss_detector import bias_scan


def extract_range_values(x):
    regex = re.search("(\d+.\d+) - (\d+.\d+)", x)
    temp_left = regex[1]
    temp_right = regex[2]
    return temp_left, temp_right


def get_continuous_list(x):
    new_list = []
    for idx, i in enumerate(x):
        if idx == 0:
            left, right = extract_range_values(i)

        else:
            temp_left, temp_right = extract_range_values(i)

            if right == temp_left:
                right = temp_right
                continue

            else:
                new_list.append(f"{left} - {right}")

                left = temp_left
                right = temp_right

    new_list.append(f"{left} - {right}")

    return new_list


def sample_datasets(
    y_true: pd.Series,
    y_pred: pd.Series = None,
    X: pd.DataFrame = None,
    sample_size: int = 50000,
):
    y_true = y_true.sample(sample_size)
    sample_indices = y_true.index

    if X is not None:
        X = X.iloc[sample_indices]

    if y_pred is not None:
        y_pred = y_pred[sample_indices]

    return y_true, y_pred, X


def privilege_test(
    X_bucketed: pd.DataFrame, y_true: pd.Series, y_pred: pd.Series, overpredicted: bool
) -> Tuple[dict, float]:
    mode, scoring = get_bias_params(y_true)

    if len(y_true) > 10000:
        X_bucketed = X_bucketed.sample(10000)
        y_true = y_true[X_bucketed.index]
        y_pred = y_pred[X_bucketed.index]

    subset = bias_scan(
        data=X_bucketed,
        observations=y_true,
        expectations=y_pred,
        overpredicted=overpredicted,
        scoring=scoring,
        mode=mode,
    )

    return subset


def bucket_features(X: pd.DataFrame) -> pd.DataFrame:
    dtypes = X.dtypes
    for col in X.columns:
        col_dtype = dtypes[col]
        accepted_column = col_dtype not in ["string", "category", "object"]

        high_card = X[col].nunique() > 10

        if accepted_column and high_card:
            X[col] = pd.qcut(X[col], 10, duplicates="drop")
            X[col] = X[col].apply(
                lambda x: str(round(x.left, 3)) + " - " + str(round(x.right, 3))
            )

    return X


def get_bias_params(y_true: pd.Series) -> Tuple[str, str]:
    target_dtype = y_true.dtype
    if target_dtype == "int":
        unique_values = y_true.nunique()

        if unique_values <= 2:
            mode = "binary"
            scoring = "Bernoulli"

        elif unique_values <= 10:
            mode = "nominal"
            scoring = "Bernoulli"

        else:
            mode = "continuous"
            scoring = "Gaussian"

    else:
        mode = "continuous"
        scoring = "Gaussian"

    return mode, scoring
