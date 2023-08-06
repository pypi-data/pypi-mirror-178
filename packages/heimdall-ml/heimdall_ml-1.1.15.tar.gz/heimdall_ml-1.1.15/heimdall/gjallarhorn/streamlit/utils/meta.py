def get_meta(heimdall_results, model):
    meta = heimdall_results.get(model).get("meta")
    model_name = meta.get("model_name")
    model_description = meta.get("model_description")
    load_model_data = meta.get("output_data_logs")

    drift_results = heimdall_results.get(model).get("drift")

    if "features" in drift_results:
        model_features = list(drift_results.get("features").keys())
    else:
        model_features = None

    if "target" in drift_results:
        model_target = list(drift_results.get("target").keys())
    else:
        model_target = None

    if "prediction" in drift_results:
        model_prediction = list(drift_results.get("prediction").keys())
    else:
        model_prediction = None

    return (
        model_name,
        model_description,
        load_model_data,
        model_features,
        model_target,
        model_prediction,
    )


def performance_statistics(tests):
    tests_failed = sum(
        [
            tests.get(metric).get("drift_detected")
            for metric in tests
            if tests.get(metric).get("threshold") > 0
        ]
    )
    tests_used_for_testing = sum(
        [1 for metric in tests if tests.get(metric).get("threshold") > 0]
    )
    tests_ran = len(tests)
    percent_tests_failed = tests_failed / max(tests_used_for_testing, 1)

    return tests_ran, tests_used_for_testing, tests_failed, percent_tests_failed


def bias_statistics(tests):
    features_with_priviledge = len(tests)
    priviledged_groups = sum([len(tests.get(metric)) for metric in tests])

    return features_with_priviledge, priviledged_groups


def drift_statistics(results):
    tests_ran = 0
    drift_detected = 0

    for result in results:
        single_result = results.get(result)

        tests = len(single_result.get("test_results"))
        tests_ran += tests

        if single_result.get("drift_detected"):
            drift_detected += 1

    return tests_ran, drift_detected
