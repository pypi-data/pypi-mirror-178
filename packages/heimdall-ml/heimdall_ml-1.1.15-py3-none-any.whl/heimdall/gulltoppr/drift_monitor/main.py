import pandas as pd
from heimdall.utils.logging import get_logger
from heimdall.gulltoppr.drift_monitor.algorithms import algorithms as algs

logger = get_logger(__name__)


class DriftMonitor:
    def __init__(
        self,
        model: dict,
        prod_features: pd.DataFrame = None,
        valid_features: pd.DataFrame = None,
        prod_target: pd.DataFrame = None,
        valid_target: pd.DataFrame = None,
        prod_predictions: pd.DataFrame = None,
        valid_predictions: pd.DataFrame = None,
    ):
        self.model = model
        self.model_name = model.get("name")
        self.model_target_config = self.model.get("target")
        self.model_prediction_config = self.model.get("prediction")
        self.model_feature_config = self.model.get("features")

        self.columns_with_drift_detected = []
        self.tests_ran = 0

        logger.info(f"Initialising drift monitor for {self.model_name}")
        self.test_model(
            prod_features,
            valid_features,
            prod_target,
            valid_target,
            prod_predictions,
            valid_predictions,
        )

    @staticmethod
    def get_feature_name(feature: dict, validation_column: bool = False):
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

    @staticmethod
    def get_test(tests):
        if type(tests) == dict:
            stat_test = list(tests)[0]
            test_kwargs = tests.get(stat_test)

        elif type(tests) == str:
            stat_test = tests
            test_kwargs = {}

        test = algs.__getattribute__(stat_test)

        return test, stat_test, test_kwargs

    def perform_test(
        self, features: dict, prod_data: pd.DataFrame, valid_data: pd.DataFrame
    ):
        test_results = {}
        for feature in features:
            name = self.get_feature_name(feature)

            input_prod_data = prod_data[[name]]
            input_valid_data = valid_data[[name]]

            dtype = feature.get("dtype")
            description = feature.get("description")

            feature_results = {}
            for tests in feature.get("tests"):
                test_func, stat_test, test_kwargs = self.get_test(tests)

                if stat_test == "default_test":
                    score, p_value, threshold, pass_fail, stat_test = test_func(
                        input_prod_data, input_valid_data, **test_kwargs
                    )

                else:
                    score, p_value, threshold, pass_fail = test_func(
                        input_prod_data, input_valid_data, **test_kwargs
                    )

                self.tests_ran += 1

                feature_results.update(
                    {
                        stat_test: {
                            "score": round(score, 4),
                            "p_value": round(p_value, 4),
                            "threshold": round(threshold, 4),
                            "drift_detected": pass_fail,
                        }
                    }
                )

            any_drift_detected = max(
                [
                    feature_results.get(test).get("drift_detected")
                    for test in feature_results
                ]
            )

            if any_drift_detected:
                self.columns_with_drift_detected.append(name)

            test_results.update(
                {
                    name: {
                        "description": description,
                        "dtype": dtype,
                        "drift_detected": any_drift_detected,
                        "test_results": feature_results,
                    }
                }
            )

        return test_results

    def test_model(
        self,
        prod_features: pd.DataFrame = None,
        valid_features: pd.DataFrame = None,
        prod_target: pd.DataFrame = None,
        valid_target: pd.DataFrame = None,
        prod_predictions: pd.DataFrame = None,
        valid_predictions: pd.DataFrame = None,
    ):
        self.model_tests = {}

        if self.model_feature_config:
            feature_tests = self.perform_test(
                self.model_feature_config, prod_features, valid_features
            )
            self.model_tests.update({"features": feature_tests})

        if self.model_target_config:
            target_tests = self.perform_test(
                self.model_target_config, prod_target, valid_target
            )
            self.model_tests.update({"target": target_tests})

        if self.model_prediction_config:
            prediction_tests = self.perform_test(
                self.model_prediction_config, prod_predictions, valid_predictions
            )
            self.model_tests.update({"prediction": prediction_tests})
