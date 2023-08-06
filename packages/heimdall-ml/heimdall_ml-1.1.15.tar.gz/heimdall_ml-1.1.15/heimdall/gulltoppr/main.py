import json
import numpy as np
from slack_sdk import WebClient
from heimdall.bifrost.feature_data import get_model_data
from heimdall.gulltoppr.drift_monitor.main import DriftMonitor
from heimdall.gulltoppr.performance_monitor.main import PerformanceMonitor
from heimdall.gulltoppr.systems_monitor.main import SystemsMonitor
from heimdall.utils.logging import get_logger
from heimdall.utils.coalesce import coalesce
from heimdall.utils.yaml_helper import load_yaml_file
from heimdall.utils.histograms import get_joint_hist
from heimdall.gjallarhorn.streamlit.utils.meta import (
    drift_statistics,
    performance_statistics,
)

logger = get_logger(__name__)


class Gulltoppr:
    def __init__(
        self,
        model_path: str,
        connector,
        metric_store=None,
        test_store=None,
        redis=None,
        slack_channel: str = None,
        slack_token: str = None,
    ):
        self.model = self.get_model(model_path)
        self.model_name = self.model.get("name")
        self.model_description = self.model.get("description")
        self.monitor_host_url = self.model.get("host_url")

        self.model_config = self.model.get("config")
        self.model_type = self.model_config.get("model")
        self.prediction_type = self.model_config.get("prediction_type")

        self.metric_store = metric_store
        self.test_store = test_store

        ## Here we check which services Heimdall should perform
        metrics = self.model.get("metrics")

        if metrics:
            self.run_performance_monitor = "performance" in metrics
            self.run_systems_monitor = "fairness" in metrics
        else:
            self.run_performance_monitor = False
            self.run_systems_monitor = False

        self.run_drift_monitor = "features" in self.model

        self.clean_data = self.safe_get(self.model_config, "clean_data")
        self.output_data_logs = self.safe_get(self.model_config, "output_data_logs")

        if self.output_data_logs:
            self.data_logs = {}
            self.r = redis

        ## Here we check the type of tables were using
        ## Double refers to a specific validation dataset vs a production dataset
        ## Single refers to one dataset with timeframes in there for both validation and prod.
        self.feature_table_type = self.get_table_type(self.model, "feature")
        self.target_table_type = self.get_table_type(self.model, "target")

        if slack_token:
            self.send_slack_alert = True
            self.slack_channel = slack_channel
            self.slack_client = WebClient(token=slack_token)

        else:
            self.send_slack_alert = False

        self.conn = connector

    @staticmethod
    def get_table_type(model, feature):
        type = (
            "single" if "table_name" in model.get(f"{feature}_store")[0] else "double"
        )
        return type

    @staticmethod
    def get_model(model_path: str):
        model = load_yaml_file(model_path)
        model = model.get("model")[0]
        return model

    @staticmethod
    def get_feature_name(feature, validation_column: bool = False):
        feature_prod_name = feature.get("name")
        if validation_column:
            name = (
                feature.get("validation_name")
                if feature.get("validation_name")
                else feature_prod_name
            )
        else:
            name = feature_prod_name

        return name

    def get_feature_list(self, features, is_validation=False):
        feature_list = [
            self.get_feature_name(feature, is_validation) for feature in features
        ]

        return feature_list

    def get_feature(self, column_name):
        feature_config = self.model.get(column_name)
        feature_list = self.get_feature_list(feature_config)
        validation_feature_list = self.get_feature_list(
            feature_config, is_validation=True
        )

        column_mapping = {
            self.get_feature_name(feature, True): self.get_feature_name(feature)
            for feature in feature_config
        }

        type_mapping = {
            self.get_feature_name(feature): feature.get("dtype")
            for feature in feature_config
        }

        return (
            feature_config,
            feature_list,
            validation_feature_list,
            column_mapping,
            type_mapping,
        )

    def get_core_features(self):
        if self.run_drift_monitor:
            (
                self.feature_config,
                self.model_features,
                self.validation_model_features,
                self.feature_column_mapping,
                self.feature_type_mapping,
            ) = self.get_feature("features")

        if self.run_drift_monitor or self.run_performance_monitor:
            (
                self.target_config,
                self.model_target,
                self.validation_model_target,
                self.target_column_mapping,
                self.target_type_mapping,
            ) = self.get_feature("target")

        if self.run_performance_monitor:
            (
                self.prediction_config,
                self.model_prediction,
                self.validation_model_prediction,
                self.prediction_column_mapping,
                self.prediction_type_mapping,
            ) = self.get_feature("prediction")
        else:
            self.model_prediction = None
            self.validation_model_prediction = None

    @staticmethod
    def format_date(date: str = None):
        date = f"date('{date}')" if date else "current_date"
        return date

    @staticmethod
    def format_data_store(data_store: list, data_store_type: str):
        if data_store_type == "single":
            return data_store[0]
        elif data_store_type == "double":
            return {k: v[0] for list_item in data_store for (k, v) in list_item.items()}

    def get_where_clause(
        self,
        date_column: str = None,
        prod_date: str = None,
        prod_date_range: int = None,
        valid_date: str = None,
        valid_date_range: int = None,
    ):
        if (not prod_date) & (not prod_date_range):
            where_clause = ""

        elif (not valid_date) | (not valid_date_range):
            prod_date = self.format_date(prod_date)
            where_clause = f" and date({date_column}) between date_sub({prod_date}, interval {prod_date_range} day) and {prod_date}"

        else:
            prod_date = self.format_date(prod_date)
            valid_date = self.format_date(valid_date)
            where_clause = f" and (date({date_column}) between date_sub({prod_date}, interval {prod_date_range} day) and {prod_date} or date({date_column}) between date_sub({valid_date}, interval {valid_date_range} day) and {valid_date})"

        return where_clause

    @staticmethod
    def get_store_date_config(dev_data_store: dict):
        date_column = dev_data_store.get("date_column")
        date_range = dev_data_store.get("date_range")
        date = dev_data_store.get("date")

        return date_column, date_range, date

    def get_data(
        self,
        data_store: dict,
        table_type: str,
        prod_features: list,
        valid_features: list,
    ):
        prod_features = prod_features.copy()
        valid_features = valid_features.copy()

        data_store = self.format_data_store(data_store, table_type)
        prod_store = data_store.get("prod")
        valid_store = data_store.get("validation")

        prod_date_column, prod_date_range, prod_date = self.get_store_date_config(
            prod_store
        )

        valid_date_column, valid_date_range, valid_date = self.get_store_date_config(
            valid_store
        )

        if table_type == "single":
            feature_table = data_store.get("table_name")
            id_column = data_store.get("id_column")
            date_column = data_store.get("date_column")

            where_clause = self.get_where_clause(
                date_column, prod_date, prod_date_range, valid_date, valid_date_range
            )

            prod_where_clause = self.get_where_clause(
                date_column, prod_date, prod_date_range
            )

            valid_where_clause = self.get_where_clause(
                date_column, valid_date, valid_date_range
            )

            table_clause = f"""
            case
              when 1=1 {prod_where_clause} then 'prod'
              when 1=1 {valid_where_clause} then 'valid'
            end as dataset
            """

            if id_column:
                prod_features.append(id_column)

            data = get_model_data(
                self.conn, feature_table, [table_clause] + prod_features, where_clause
            )

            prod_id_column = id_column
            valid_id_column = id_column
            prod_data = data[data["dataset"] == "prod"].drop(columns=["dataset"])
            valid_data = data[data["dataset"] == "valid"].drop(columns=["dataset"])

        elif table_type == "double":
            prod_feature_table = prod_store.get("table_name")
            prod_id_column = prod_store.get("id_column")
            prod_where_clause = self.get_where_clause(
                prod_date_column, prod_date, prod_date_range
            )

            if prod_id_column:
                prod_features.append(prod_id_column)

            prod_data = get_model_data(
                self.conn, prod_feature_table, prod_features, prod_where_clause
            )

            valid_feature_table = valid_store.get("table_name")
            valid_id_column = valid_store.get("id_column")
            valid_where_clause = self.get_where_clause(
                valid_date_column, valid_date, valid_date_range
            )

            if valid_id_column:
                valid_features.append(valid_id_column)

            valid_data = get_model_data(
                self.conn, valid_feature_table, valid_features, valid_where_clause
            )

        return prod_data, valid_data, prod_id_column

    def get_core_data(self):
        if self.run_performance_monitor:
            target_cols = self.model_target + self.model_prediction
            validation_target_cols = (
                self.validation_model_target + self.validation_model_prediction
            )
        else:
            target_cols = self.model_target
            validation_target_cols = self.validation_model_target

        prod_features, valid_features, self.prod_feature_id_column = self.get_data(
            self.model.get("feature_store"),
            self.feature_table_type,
            self.model_features,
            self.validation_model_features,
        )

        prod_target, valid_target, self.prod_target_id_column = self.get_data(
            self.model.get("target_store"),
            self.target_table_type,
            target_cols,
            validation_target_cols,
        )

        return prod_features, valid_features, prod_target, valid_target

    @staticmethod
    def map_data(df, data_type_map: dict = {}, column_name_map: dict = {}):
        if column_name_map:
            df = df.rename(columns=column_name_map)

        if data_type_map:
            for key in data_type_map:
                type = data_type_map.get(key)
                if (
                    type not in ["string", "category"]
                    and (df[[key]].dtypes == "object")[0]
                ):
                    df = df.explode(key)
                df[key] = df[key].astype(type)

        return df

    def map_core_data(self, prod_features, valid_features, prod_target, valid_target):
        prod_features = self.map_data(prod_features, self.feature_type_mapping)
        valid_features = self.map_data(
            valid_features, self.feature_type_mapping, self.feature_column_mapping
        )

        prod_target = self.map_data(prod_target, self.target_type_mapping)
        valid_target = self.map_data(
            valid_target, self.target_type_mapping, self.target_column_mapping
        )

        if self.run_performance_monitor:
            prod_target = self.map_data(prod_target, self.prediction_type_mapping)
            valid_target = self.map_data(
                valid_target,
                self.prediction_type_mapping,
                self.prediction_column_mapping,
            )

        if self.clean_data:
            prod_features = prod_features.dropna()
            valid_features = valid_features.dropna()
            prod_target = prod_target.dropna()
            valid_target = valid_target.dropna()

        return prod_features, valid_features, prod_target, valid_target

    @staticmethod
    def _classify_predictions(df, thresholds):
        labels = []
        for prediction in thresholds:
            label = prediction + "_predicted_label"
            labels.append(label)
            threshold = thresholds.get(prediction)

            df[label] = df[prediction].apply(lambda x: 1 if x > threshold else 0)

        return df, labels

    def run(self):
        self.heimdall_results = {}
        model_meta_info = {
            "model_name": self.model_name,
            "model_description": self.model_description,
            "output_data_logs": self.output_data_logs,
        }
        self.heimdall_results.update({"meta": model_meta_info})

        self.get_core_features()

        prod_features, valid_features, prod_target, valid_target = self.get_core_data()

        prod_features, valid_features, prod_target, valid_target = self.map_core_data(
            prod_features, valid_features, prod_target, valid_target
        )

        if self.run_performance_monitor or self.run_systems_monitor:
            logger.info("Finding target and predictions")

            prod_prediction = prod_target[self.model_prediction]
            valid_prediction = valid_target[self.model_prediction]

            if self.prediction_type in "classification":
                prediction_columns = self.model.get("prediction")

                model_prediction_thresholds = {
                    prediction.get("name"): coalesce(prediction.get("threshold"), 0.5)
                    for prediction in prediction_columns
                }

                logger.info("Assigning labels")

                prod_labels, self.model_predicted_labels = self._classify_predictions(
                    prod_target, model_prediction_thresholds
                )

                valid_labels, _ = self._classify_predictions(
                    valid_target, model_prediction_thresholds
                )

                predictive_columns = (
                    self.model_target
                    + self.model_prediction
                    + self.model_predicted_labels
                )
                prediction_column = self.model_predicted_labels

            else:
                prod_labels = prod_target.copy()
                valid_labels = valid_target.copy()
                predictive_columns = self.model_target + self.model_prediction
                prediction_column = self.model_prediction

        else:
            prod_prediction = None
            valid_prediction = None

        if self.run_performance_monitor:
            performance_monitor = PerformanceMonitor(
                self.model,
                self.model_target,
                prediction_column,
                prod_labels[predictive_columns],
                valid_labels[predictive_columns],
            )

            self.heimdall_results.update(
                {"performance": performance_monitor.metric_results}
            )

        if self.run_drift_monitor:
            drift_monitor = DriftMonitor(
                self.model,
                prod_features[self.model_features],
                valid_features[self.model_features],
                prod_target[self.model_target],
                valid_target[self.model_target],
                prod_prediction,
                valid_prediction,
            )

            self.heimdall_results.update({"drift": drift_monitor.model_tests})

        if self.run_systems_monitor:
            joint_dataset = prod_features.merge(
                prod_target,
                how="inner",
                left_on=self.prod_feature_id_column,
                right_on=self.prod_target_id_column,
            )

            systems_monitor = SystemsMonitor(
                model=self.model,
                dataset=joint_dataset,
                features=self.model_features,
                target_column=self.model_target,
                prediction_column=self.model_prediction,
                predicted_label_column=self.model_predicted_labels,
            )

            self.heimdall_results.update({"systems": systems_monitor.results})

        if self.send_slack_alert:
            if "performance" in self.heimdall_results:
                slack_block = self.get_slack_message(
                    "performance", self.heimdall_results, self.model_name
                )

                self.slack_client.chat_postMessage(
                    channel=self.slack_channel, text="", blocks=slack_block
                )

            if "drift" in self.heimdall_results:
                slack_block = self.get_slack_message(
                    "drift", self.heimdall_results, self.model_name
                )

                self.slack_client.chat_postMessage(
                    channel=self.slack_channel, text="", blocks=slack_block
                )

            final_link = f"*[{self.model_name}]* Full results available at the following link {self.monitor_host_url}."

            self.slack_client.chat_postMessage(
                channel=self.slack_channel,
                text="",
                blocks=[
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": final_link},
                    }
                ],
            )

        if self.output_data_logs:
            if self.model_features:
                for feature in self.model_features:
                    features_result = self.get_data_log(
                        feature, "features", prod_features, valid_features
                    )
                    self.data_logs.update(features_result)

            if self.model_target:
                for target in self.model_target:
                    target_result = self.get_data_log(
                        target, "target", prod_target, valid_target
                    )
                    self.data_logs.update(target_result)

            if self.model_prediction:
                for prediction in self.model_prediction:
                    prediction_result = self.get_data_log(
                        prediction, "prediction", prod_prediction, valid_prediction
                    )
                    self.data_logs.update(prediction_result)

            data_log_json = json.dumps(self.data_logs)
            self.r.execute_command("JSON.SET", self.model_name, ".", data_log_json)

    def get_data_log(self, feature, feature_type, prod_features, valid_features):
        model_features = self.model.get(feature_type)
        grams = self.get_ngrams(feature, model_features)
        anonymise = self.get_anonymise(feature, model_features)

        feature_result = self.dim_redu(
            feature, prod_features, valid_features, grams, anonymise
        )

        return feature_result

    @staticmethod
    def get_ngrams(feature, model_features):
        grams = []
        for model_feature in model_features:
            model_tests = model_feature.get("tests")
            if model_feature.get("name") == feature:
                for model_test in model_tests:
                    if type(model_test) == dict:
                        model_test_name = list(model_test.keys())[0]
                        gram = model_test.get(model_test_name).get("grams")

                        if gram:
                            grams.append(gram)

        return grams

    @staticmethod
    def get_anonymise(feature, model_features):
        anonymise = all(
            [
                model_feature.get("anonymise")
                for model_feature in model_features
                if model_feature.get("name") == feature
            ]
        )

        return anonymise

    @staticmethod
    def anonymise_dict(dataset):
        dataset_copy = {}
        for idx, key in enumerate(dataset):
            dataset_copy.update({idx: dataset.get(key)})

        return dataset_copy

    @staticmethod
    def get_slack_message(test_type, test_results, model_name):
        if test_type == "performance":
            performance_results = test_results.get(test_type)

            initial_performance_metric = list(test_results.get(test_type).keys())[0]
            prod_performance = round(
                performance_results.get(initial_performance_metric).get("prod_metric"),
                2,
            )
            valid_performance = round(
                performance_results.get(initial_performance_metric).get("eval_metric"),
                2,
            )
            performance_difference = round(
                100
                * ((prod_performance - valid_performance) / (valid_performance + 1e-8)),
                1,
            )
            sign = "+" if performance_difference > 0 else ""

            (
                tests_ran,
                tests_used_for_testing,
                tests_failed,
                percent_tests_failed,
            ) = performance_statistics(performance_results)

            message = f"*[{model_name}]* Performance monitor run for {model_name}, {initial_performance_metric} scored {prod_performance} vs validation score of {valid_performance} ({sign}{performance_difference}%). {tests_used_for_testing} tests ran - performance drift found for {tests_failed} out of {tests_used_for_testing} metrics ({percent_tests_failed:.1%})."

            slack_block = [
                {"type": "section", "text": {"type": "mrkdwn", "text": message}},
            ]

        elif test_type == "drift":
            slack_block = []
            drift_results = test_results.get("drift")

            for column in drift_results:
                column_drift = drift_results.get(column)
                tests_ran, drift_detected = drift_statistics(column_drift)
                features = len(column_drift)
                percent_drifted = drift_detected / features

                message = f"""*[{model_name}]* Drift monitor run for {column}. {tests_ran} tests ran - drift found for {drift_detected} out of {features} {column} ({percent_drifted:.1%})."""

                slack_message = {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": message},
                }

                slack_block.append(slack_message)

        return slack_block

    def dim_redu(self, feature, prod_data, valid_data, grams, anonymise: bool = False):
        prod_data = prod_data[[feature]].squeeze()
        valid_data = valid_data[[feature]].squeeze()

        if grams:
            hist_dict = {}
            for gram in grams:
                gram_dict = get_joint_hist(prod_data, valid_data, gram)

                if anonymise:
                    gram_dict = self.anonymise_dict(gram_dict)
                gram_dict = {f"{gram}" + "_gram": gram_dict}

                hist_dict.update(gram_dict)

            dict_output = {feature: hist_dict}

        else:
            hist_dict = get_joint_hist(prod_data, valid_data)

            dict_output = {feature: hist_dict}

            if anonymise:
                dict_output = self.anonymise_dict(dict_output)

        return dict_output

    @staticmethod
    def safe_get(dict, item, escape=False):
        return dict.get(item) if dict.get(item) else escape
