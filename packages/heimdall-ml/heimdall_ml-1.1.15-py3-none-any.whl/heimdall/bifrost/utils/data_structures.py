from google.cloud import bigquery
import pandas as pd
import time


def get_time():
    unix = int(time.time())
    now = pd.Timestamp(unix, unit="s", tz="GMT")
    return now


METRIC_CONFIG = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("model", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("performance_metric", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("production_score", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("validation_score", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("threshold", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("drift_detected", "BOOLEAN", mode="REQUIRED"),
    ]
)

metric_columns = {
    "level_0": "timestamp",
    "level_1": "model",
    "level_2": "performance_metric",
    "prod_metric": "production_score",
    "eval_metric": "validation_score",
}


def get_metric_table(heimdall_results):
    final_dict = {}
    now = get_time()

    for model in heimdall_results:
        model_results = heimdall_results.get(model)
        if "performance" in model_results:
            performance_results = model_results.get("performance")

            unnested_dict = {
                (now, model, metric): performance_results.get(metric)
                for metric in performance_results
            }

            final_dict.update(unnested_dict)

    metric_df = (
        pd.DataFrame.from_dict(final_dict, orient="index")
        .reset_index()
        .rename(columns=metric_columns)
    )

    return metric_df


TEST_CONFIG = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("model", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("feature_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("feature_description", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("feature_dtype", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("is_feature_drifted", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("test_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("score", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("p_value", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("threshold", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("drift_detected", "BOOLEAN", mode="REQUIRED"),
    ]
)


test_columns = {
    "level_0": "timestamp",
    "level_1": "model",
    "level_2": "feature_name",
    "level_3": "feature_description",
    "level_4": "feature_dtype",
    "level_5": "is_feature_drifted",
    "level_6": "test_name",
}


def get_test_table(heimdall_results):
    final_dict = {}
    now = get_time()

    for model in heimdall_results:
        model_results = heimdall_results.get(model)

        if "drift" in model_results:
            drift_results = model_results.get(
                "drift"
            )  ## this will have feature, target, and prediction in it

            for type in drift_results:
                type_results = drift_results.get(
                    type
                )  ## this now only has one of the three types of features

                unnested_dict = {
                    (
                        now,
                        model,
                        feature,
                        type_results.get(feature).get("description"),
                        type_results.get(feature).get("dtype"),
                        type_results.get(feature).get("drift_detected"),
                        test,
                    ): type_results.get(feature)
                    .get("test_results")
                    .get(test)
                    for feature in type_results
                    for test in type_results.get(feature).get("test_results")
                }

                final_dict.update(unnested_dict)

    test_df = (
        pd.DataFrame.from_dict(final_dict, orient="index")
        .reset_index()
        .rename(columns=test_columns)
    )

    return test_df
