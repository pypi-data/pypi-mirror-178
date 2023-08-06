import numpy as np
import pandas as pd
import plotly.express as px


def create_graph(feature, dataset, height: int = 400, width: int = 1000):
    size = len(dataset)

    df = pd.DataFrame(
        dict(
            data_set=np.concatenate((["validation"] * size, ["prod"] * size)),
            index=np.concatenate((dataset["index"], dataset["index"])),
            value=np.concatenate((dataset["valid"], dataset["prod"])),
        )
    )

    graph = px.bar(
        df,
        x="index",
        y="value",
        color="data_set",
        color_discrete_map={"prod": "#46039f", "validation": "#fb9f3a"},
        barmode="overlay",
        title=f"Probability density for {feature}",
        width=width,
        height=height,
        labels={"value": "Probability density", "index": feature},
    )

    graph.update_layout(
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.01,
        )
    )

    return graph


def create_results_table(test_results, columns):
    results_table = pd.DataFrame(test_results).transpose().reset_index()
    results_table = results_table.rename(columns=columns)
    return results_table
