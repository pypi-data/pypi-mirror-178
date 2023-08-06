import json
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from heimdall.gjallarhorn.streamlit.utils.graph import (
    create_graph,
    create_results_table,
)
from heimdall.gjallarhorn.streamlit.utils.meta import get_meta
from heimdall.gjallarhorn.streamlit.utils.constants import HEIMDALL_LOGO, UW_LOGO

COLUMNS = {
    "index": "Statistical test",
    "score": "Test score",
    "p_value": "p-value",
    "threshold": "Confidence level",
    "drift_detected": "Drift detected",
}


def drift_monitor_page(
    selected_model,
    heimdall_results,
    redis_server=None,
):
    model_results = heimdall_results.get(selected_model)
    drift_tests = model_results.get("drift")

    (
        model_name,
        model_description,
        load_model_data,
        features,
        targets,
        predictions,
    ) = get_meta(heimdall_results, selected_model)

    feature_tests = drift_tests.get("features")
    target_tests = drift_tests.get("target")
    prediction_tests = drift_tests.get("prediction")

    if feature_tests:
        feature_logos, feature_tests_ran, feature_drift = get_logos(feature_tests)

        if len(features) > 1:
            with st.sidebar:
                st.sidebar.markdown("""---""")
                selected_feature = st.selectbox(
                    label="Feature to display", options=features
                )

        else:
            selected_feature = features[0]
    else:
        features = [0]
        feature_tests_ran = 0
        feature_drift = 0

    if target_tests:
        target_logos, target_tests_ran, target_drift = get_logos(target_tests)

        if len(targets) > 1:
            with st.sidebar:
                st.sidebar.markdown("""---""")
                selected_target = st.selectbox(
                    label="Target to display", options=targets
                )

        else:
            selected_target = targets[0]
    else:
        targets = [0]
        target_tests_ran = 0
        target_drift = 0

    if prediction_tests:
        prediction_logos, prediction_tests_ran, prediction_drift = get_logos(
            prediction_tests
        )

        if len(predictions) > 1:
            with st.sidebar:
                st.sidebar.markdown("""---""")
                selected_prediction = st.selectbox(
                    label="Prediction to display", options=predictions
                )

        else:
            selected_prediction = predictions[0]
    else:
        predictions = [0]
        prediction_tests_ran = 0
        prediction_drift = 0

    percent_targets_drifted = target_drift / len(targets)
    percent_predictions_drifted = prediction_drift / len(predictions)
    percent_feature_drifted = feature_drift / len(features)

    title_block_1, title_block_2, title_block_3 = st.columns([1, 7, 1])
    title_block_1.image(
        image=HEIMDALL_LOGO,
        width=80,
    )
    title_block_2.markdown(
        f'<h1 style="color:#4c138a;font-size:48px;">{model_name}</h1>',
        unsafe_allow_html=True,
    )
    title_block_3.image(
        image=UW_LOGO,
        width=120,
    )
    st.text(model_description)
    st.subheader(f"Drift summary for {model_name}")

    col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8 = st.columns(8)

    col_1.metric(label="Total features", value=len(features))
    col_2.metric(
        label="Total tests performed",
        value=feature_tests_ran + target_tests_ran + prediction_tests_ran,
    )
    col_3.metric(label="Target drifted", value=target_drift)
    col_4.metric(label="% Target drifted", value=f"{percent_targets_drifted:.0%}")
    col_5.metric(label="Predictions drifted", value=prediction_drift)
    col_6.metric(
        label="% Predictions drifted", value=f"{percent_predictions_drifted:.0%}"
    )
    col_7.metric(label="Features drifted", value=feature_drift)
    col_8.metric(label="% Features drifted", value=f"{percent_feature_drifted:.0%}")

    # st.write(f"Heimdall has ran the specified tests for {model_name}, the findings of which are:")

    # if target_tests:
    #     st.write(f"Heimdall has detected drift for {target_drift:.0f} features out of a total {len(targets)} ({percent_targets_drifted:.1%}). ")

    # if prediction_tests:
    #     st.write(f"Heimdall has detected drift for {prediction_drift:.0f} features out of a total {len(predictions)} ({percent_predictions_drifted:.1%}). ")

    # if feature_tests:
    #     st.write(f"Heimdall has detected drift for {feature_drift:.0f} features out of a total {len(features)} ({percent_feature_drifted:.1%}). ")

    # st.write("A breakdown of the findings can be found below, and using the sidebar to the left.")

    if target_tests:
        if load_model_data:
            target_data = json.loads(
                redis_server.execute_command("JSON.GET", model_name, selected_target)
            )
        else:
            target_data = None

        target_test = target_tests.get(selected_target)
        create_streamlit_section(target_test, selected_target, target_data)

    if prediction_tests:
        if load_model_data:
            prediction_data = json.loads(
                redis_server.execute_command(
                    "JSON.GET", model_name, selected_prediction
                )
            )
        else:
            prediction_data = None

        prediction_test = prediction_tests.get(selected_prediction)
        create_streamlit_section(prediction_test, selected_prediction, prediction_data)

    if feature_tests:
        if load_model_data:
            feature_data = json.loads(
                redis_server.execute_command("JSON.GET", model_name, selected_feature)
            )
        else:
            feature_data = None

        feature_test = feature_tests.get(selected_feature)
        create_streamlit_section(feature_test, selected_feature, feature_data)


def get_logos(results):
    logos = []
    tests_ran = 0
    drift_detected = 0

    for result in results:
        single_result = results.get(result)

        tests = len(single_result.get("test_results"))
        tests_ran += tests

        if single_result.get("drift_detected"):
            logos.append("exclamation-circle")
            drift_detected += 1
        else:
            logos.append("check-circle")

    return logos, tests_ran, drift_detected


def get_drift_emoji(drift):
    # return "❌" if drift else "✅"
    if drift:
        return "❌", "drift detected"
    else:
        return "✅", "no drift detected"


def create_streamlit_section(
    selected_test, selected_name, selected_data=None, graph_height=600, graph_width=1200
):
    description = selected_test.get("description")
    data_type = selected_test.get("dtype")
    any_drift_detected = selected_test.get("drift_detected")
    results = selected_test.get("test_results")
    drift_emoji, drift_text = get_drift_emoji(any_drift_detected)

    st.subheader(f"{drift_emoji} {selected_name}")
    st.markdown(
        f"""
                **Description:** _{description}_  
                **Status:** _{drift_text}_  
                **Data type:** _{data_type}_
        """
    )

    test_data = create_results_table(results, COLUMNS)
    AgGrid(test_data, fit_columns_on_grid_load=True, height=150, theme="streamlit")

    if selected_data is not None:
        keys = list(selected_data.keys())
        contains_grams = all("gram" in key for key in keys)
        if contains_grams:
            if len(keys) > 0:
                ngram = st.selectbox("N-grams", keys)
            else:
                ngram = keys[0]

            graph_data = pd.DataFrame(selected_data.get(ngram)).T.reset_index()
        else:
            graph_data = pd.DataFrame(selected_data).T.reset_index()

        st.plotly_chart(
            create_graph(
                selected_name,
                graph_data,
                height=graph_height,
                width=graph_width,
            )
        )
