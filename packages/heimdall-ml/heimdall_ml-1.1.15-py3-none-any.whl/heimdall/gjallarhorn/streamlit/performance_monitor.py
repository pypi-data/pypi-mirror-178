import json
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from heimdall.gjallarhorn.streamlit.utils.constants import HEIMDALL_LOGO, UW_LOGO
from heimdall.gjallarhorn.streamlit.utils.meta import get_meta, performance_statistics
from heimdall.gjallarhorn.streamlit.utils.graph import (
    create_graph,
    create_results_table,
)

COLUMNS = {
    "index": "Metric",
    "prod_metric": "Production dataset score",
    "eval_metric": "Validation dataset score",
    "threshold": "Production warning threshold",
    "drift_detected": "Drift detected",
}


def performance_monitor_page(
    selected_model,
    heimdall_results,
    redis_server=None,
):
    model_results = heimdall_results.get(selected_model)
    performance_tests = model_results.get("performance")

    (
        model_name,
        model_description,
        load_model_data,
        features,
        targets,
        predictions,
    ) = get_meta(heimdall_results, selected_model)

    ## Assumption right now is that having a performance monitor is equivalent
    ## to having only 1 target
    target_name = targets[0]
    prediction_name = predictions[0]

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
    st.subheader(f"Performance summary for {model_name}")

    (
        metrics_ran,
        metrics_used_for_testing,
        metrics_failed,
        percent_metrics_failed,
    ) = performance_statistics(performance_tests)

    col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8 = st.columns(8)

    col_3.metric(label="Metrics calculated", value=metrics_ran)
    col_4.metric(label="Metrics tested", value=metrics_used_for_testing)
    col_5.metric(label="Tests failed", value=metrics_failed)
    col_6.metric(label="Percentage failed", value=f"{percent_metrics_failed:.1%}")

    target_preposition = "" if metrics_failed > 0 else "not "
    st.write(
        f"""
        After running the specified performance tests for {model_name}, Heimdall has {target_preposition}detected performance drift in the model.
        Out of the {metrics_ran} tests ran, {metrics_failed} tests failed ({percent_metrics_failed:.1%}). 
        A breakdown of the test scores can be found below, as well as prediction distribution graphs.
        """
    )

    st.subheader("Test results")

    test_data = create_results_table(performance_tests, columns=COLUMNS)
    AgGrid(test_data, fit_columns_on_grid_load=True, height=150, theme="streamlit")

    st.subheader("Prediction distribution")

    if load_model_data:
        prediction_data = json.loads(
            redis_server.execute_command("JSON.GET", model_name, prediction_name)
        )
        keys = list(prediction_data.keys())
        contains_grams = all("gram" in key for key in keys)
        if contains_grams:
            if len(keys) > 0:
                ngram = st.selectbox("N-grams", keys)
            else:
                ngram = keys[0]

            graph_data = pd.DataFrame(prediction_data.get(ngram)).T.reset_index()
        else:
            graph_data = pd.DataFrame(prediction_data).T.reset_index()

        st.plotly_chart(
            create_graph(
                prediction_name,
                graph_data,
                height=600,
                width=1200,
            )
        )
