from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from ast import literal_eval


def normalising_factor(validation_data: pd.Series) -> float:
    return max(validation_data.std(), 0.001)


def array_like(
    validation_data: pd.DataFrame, prod_data: pd.DataFrame
) -> Tuple[pd.Series, pd.Series]:
    return validation_data.squeeze(), prod_data.squeeze()


def mean_difference(validation_data: pd.DataFrame, prod_data: pd.DataFrame) -> float:
    difference_score = prod_data.mean() - validation_data.mean()
    return difference_score


def get_contingency_table(
    validation_data: pd.DataFrame, prod_data: pd.DataFrame, grams: tuple
) -> np.array:
    validation_data, prod_data = get_count_tables(validation_data, prod_data, grams)

    combined_data = pd.merge(validation_data, prod_data, how="outer").fillna(0)
    contingency_table = np.array(
        [combined_data["prod_data"], combined_data["validation_data"]]
    )

    return contingency_table


def get_count_tables(
    validation_data: pd.DataFrame, prod_data: pd.DataFrame, grams: tuple
):
    if validation_data.dtypes[0] in ["string", "object", "category"]:
        validation_data, prod_data = vectorify(validation_data, prod_data, grams)
    else:
        validation_data = get_count_table(validation_data, "validation_data")
        prod_data = get_count_table(prod_data, "prod_data")

    return validation_data, prod_data


def get_count_table(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df = pd.DataFrame(df.value_counts()).reset_index().rename({0: column_name}, axis=1)
    return df


def vectorify(validation_data: pd.DataFrame, prod_data: pd.DataFrame, grams: tuple):
    if type(grams) == int:
        grams = (grams, grams)

    if type(grams) == str:
        grams = literal_eval(grams)

    vectoriser = TfidfVectorizer(
        max_features=50,
        analyzer="word",
        strip_accents="ascii",
        stop_words="english",
        norm="l2",
        ngram_range=grams,
    )

    validation_data, prod_data = array_like(validation_data, prod_data)
    validation_size = len(validation_data)

    validation_representation = (
        vectoriser.fit_transform(validation_data).toarray().sum(axis=0)
    )
    prod_representation = (
        vectoriser.transform(prod_data).toarray().mean(axis=0) * validation_size
    )

    vectoriser_words = vectoriser.get_feature_names_out()

    validation_frequency = pd.DataFrame(
        (zip(vectoriser_words, validation_representation)),
        columns=["vocab", "validation_data"],
    )
    prod_frequency = pd.DataFrame(
        (zip(vectoriser_words, prod_representation)), columns=["vocab", "prod_data"]
    )

    return validation_frequency, prod_frequency
