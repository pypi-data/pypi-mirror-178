import json
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from heimdall.gjallarhorn.streamlit.utils.constants import HEIMDALL_LOGO, UW_LOGO
from heimdall.gjallarhorn.streamlit.utils.meta import (
    get_meta,
    performance_statistics,
    bias_statistics,
)
from heimdall.gjallarhorn.streamlit.utils.graph import (
    create_results_table,
)

COLUMNS = {
    "index": "Metric",
    "metric_score": "Production dataset score",
    "threshold": "Production warning threshold",
    "drift_detected": "Drift detected",
}


def systems_monitor_page(
    selected_model,
    heimdall_results,
    redis_server=None,
):
    model_results = heimdall_results.get(selected_model)
    systems_tests = model_results.get("systems")

    (
        model_name,
        model_description,
        load_model_data,
        features,
        targets,
        predictions,
    ) = get_meta(heimdall_results, selected_model)

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
    st.subheader(f"Concept summary for {model_name}")

    bias_results = systems_tests.get("bias")
    metric_results = systems_tests.get("metrics")

    if bias_results:
        st.header(f"Bias detection results for {model_name}")
        _, _, col_13, col_14, col_15, col_16, _, _ = st.columns(8)

        if "overprivileged_test" in bias_results:
            overprivileged_test = bias_results.get("overprivileged_test")

            overprivileged_features, overprivileged_groups = bias_statistics(
                bias_results.get("overprivileged_test")
            )

            overprivileged = list(overprivileged_test.keys())
            st.write(
                f"Overprivilege bias detection ran for {model_name}. Bias found for the following columns: "
                + ", ".join(overprivileged)
                + ". For specific groupings, see the logs"
            )
        else:
            overprivileged_features = None
            overprivileged_groups = None

        if "underprivileged_test" in bias_results:
            underprivileged_test = bias_results.get("underprivileged_test")

            underprivileged_features, underprivileged_groups = bias_statistics(
                underprivileged_test
            )

            underprivileged = list(underprivileged_test.keys())

            st.write(
                f"Underprivilege bias detection ran for {model_name}. Bias found for the following columns: "
                + ", ".join(underprivileged)
                + ". For specific groupings, see the logs"
            )
        else:
            underprivileged_features = None
            underprivileged_groups = None

        col_13.metric(label="Overprivileged features", value=overprivileged_features)
        col_14.metric(label="Overprivileged groups", value=overprivileged_groups)
        col_15.metric(label="Underprivileged features", value=underprivileged_features)
        col_16.metric(label="Underprivileged groups", value=underprivileged_groups)

    if metric_results:
        st.header(f"Metric results for {model_name}")

        (
            metrics_ran,
            metrics_used_for_testing,
            metrics_failed,
            percent_metrics_failed,
        ) = performance_statistics(metric_results)

        _, _, col_23, col_24, col_25, col_26, _, _ = st.columns(8)

        col_23.metric(label="Metrics calculated", value=metrics_ran)
        col_24.metric(label="Metrics tested", value=metrics_used_for_testing)
        col_25.metric(label="Tests failed", value=metrics_failed)
        col_26.metric(label="Percentage failed", value=f"{percent_metrics_failed:.1%}")

        target_preposition = "" if metrics_failed > 0 else "not "
        st.write(
            f"""
            After running the specified systems tests for {model_name}, Heimdall has {target_preposition}detected performance drift in the model.
            Out of the {metrics_ran} tests ran, {metrics_failed} tests failed ({percent_metrics_failed:.1%}). 
            A breakdown of the test scores can be found below:
            """
        )

        st.subheader("Test results")

        test_data = create_results_table(metric_results, columns=COLUMNS)
        AgGrid(test_data, fit_columns_on_grid_load=True, height=150, theme="streamlit")
