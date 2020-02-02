import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame

from datagen.datagen import ApiCallSheet
from datasource import datasource

import logging
import sys

from outputs import outputhelper

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(filename)s:%(lineno)d %(levelname)s - \n%(message)s')
log = logging.getLogger(__name__)

# _ticketcount = "ticketcount"
# _duration = "duration"
# _improved = "improved"

_ticketcount: str = ApiCallSheet.attr_names()[0]
_url: str = ApiCallSheet.attr_names()[1]
_duration: str = ApiCallSheet.attr_names()[2]

_difference: str = "difference"
_signum: str = "signum"


def draw_mean_graph(file1="raw-calls", file2="raw-calls-2"):
    raw_calls_base = load_api_result_csv(file1)
    raw_calls_2 = load_api_result_csv(file2)

    df = merge_data_(raw_calls_base, raw_calls_2)

    agg_col_duration = create_mean_dataframe(df, columns_to_use=[_ticketcount, _duration + "_1"])
    agg_col_improved = create_mean_dataframe(df, columns_to_use=[_ticketcount, _duration + "_2"])

    fig = create_figure(df, agg_col_duration, agg_col_improved)
    outputhelper.save_figure(fig, "profile-mean")


def merge_data_(raw_calls_base, raw_calls_2):
    merged_data = raw_calls_base.merge(raw_calls_2, how="inner", on=[_ticketcount, _url], suffixes=["_1", "_2"])
    log.debug("merged data")
    log.debug(merged_data)

    return merged_data


# def draw_mean_graph_internal():
#     csv_path = datasource.get_file_path("api-mean-changes.csv")
#     df = pd.read_csv(csv_path, header=0, names=["", _ticketcount, _duration, _improved],
#                      usecols=[_ticketcount, _duration, _improved])
#     log.debug("Loaded data")
#     log.debug(df)
#
#     agg_col_duration = create_mean_dataframe(df, columns_to_use=[_ticketcount, _duration])
#     agg_col_improved = create_mean_dataframe(df, columns_to_use=[_ticketcount, _improved])
#
#     fig = create_figure(df, agg_col_duration, agg_col_improved)
#     outputhelper.save_figure(fig, "profile-mean")


def load_api_result_csv(filename: str) -> DataFrame:
    csv_path = datasource.get_file_path(filename + ".csv")

    df = pd.read_csv(csv_path, header=0, names=[_ticketcount, _url, _duration],
                     usecols=[_ticketcount, _url, _duration])

    log.debug("Loaded data")
    log.debug(df)

    return df


def create_figure(df, mean_duration, mean_improved):
    fig = go.Figure()
    fig.update_layout(
        title="Sampled Calls Grouped By Ticket Count - Before After",
        xaxis_title="Ticket Count For Account Called",
        yaxis_title="Api Duration (ms)"
    )

    traces = []
    traces.append(go.Scatter(x=df[_ticketcount], y=df[_duration + "_1"], mode="markers",
                             name="Base"))

    traces.append(go.Scatter(x=mean_duration.index, y=mean_duration[_duration + "_1"], mode="lines+markers",
                             name="Base-Mean"))

    traces.append(go.Scatter(x=df[_ticketcount], y=df[_duration + "_2"], mode="markers",
                             name="Improved"))

    traces.append(go.Scatter(x=mean_improved.index, y=mean_improved[_duration + "_2"], mode="lines+markers",
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
    # draw_mean_graph()
    draw_mean_graph("results-timed-api", "results-timed-api2")
