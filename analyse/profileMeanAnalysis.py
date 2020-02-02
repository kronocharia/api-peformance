import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame

from datasource import datasource

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(filename)s:%(lineno)d %(levelname)s - \n%(message)s')

log = logging.getLogger(__name__)

_ticketcount = "ticketcount"
_duration = "duration"
_improved = "improved"


def draw_mean_graph():
    csv_path = datasource.get_file_path("api-mean-changes.csv")
    df = pd.read_csv(csv_path, header=0, names=["", _ticketcount, _duration, _improved],
                     usecols=[_ticketcount, _duration, _improved])
    log.debug("Loaded data")
    log.debug(df)

    agg_col_duration = create_mean_dataframe(df, columns_to_use=[_ticketcount, _duration])
    agg_col_improved = create_mean_dataframe(df, columns_to_use=[_ticketcount, _improved])

    fig = create_figure(df, agg_col_duration, agg_col_improved)
    fig.show()


def create_figure(df, mean_duration, mean_improved):
    fig = go.Figure()
    fig.update_layout(
        title="Sampled Calls Grouped By Ticket Count - Before After",
        xaxis_title="Ticket Count For Account Called",
        yaxis_title="Api Duration (ms)"
    )

    traces = []
    traces.append(go.Scatter(x=df[_ticketcount], y=df[_duration], mode="markers",
                             name="Base"))

    traces.append(go.Scatter(x=mean_duration.index, y=mean_duration[_duration], mode="lines+markers",
                             name="Base-Mean"))

    traces.append(go.Scatter(x=df[_ticketcount], y=df[_improved], mode="markers",
                             name="Improved"))

    traces.append(go.Scatter(x=mean_improved.index, y=mean_improved[_improved], mode="lines+markers",
                             name="Improved-Mean"))

    for entry in traces:
        fig.add_trace(entry)

    return fig


def create_mean_dataframe(all_results: DataFrame, columns_to_use: [str]) -> DataFrame:
    selected_columns = all_results[columns_to_use].copy()
    log.debug("Selected columns")
    log.debug(selected_columns)

    mean = selected_columns.groupby(columns_to_use[0]).mean()
    log.debug("Mean Dataframe")
    log.debug(mean)
    return mean


if __name__ == '__main__':
    draw_mean_graph()
