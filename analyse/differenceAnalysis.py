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

_ticketcount: str = ApiCallSheet.attr_names()[0]
_url: str = ApiCallSheet.attr_names()[1]
_duration: str = ApiCallSheet.attr_names()[2]

_difference: str = "difference"
_signum: str = "signum"


def draw_difference_graph(file1="raw-calls", file2="raw-calls-2"):
    raw_calls_base = load_api_result_csv(file1)
    raw_calls_2 = load_api_result_csv(file2)

    merged = merge_data_and_compute_difference(raw_calls_2, raw_calls_base)

    colour_mapping = {-1: 'red', 0: 'blue', 1: 'lightgreen'}
    bar_colours = dict(color=[colour_mapping.get(x) for x in merged[_signum]])

    data = go.Bar(x=merged[_url], y=merged[_difference], marker=bar_colours)
    fig = go.Figure(data=data)
    fig.update_layout(
        title="API SpeedUp - Before After",
        yaxis_title="Difference in API Duration (Positive is time saved)",
        xaxis_title="Api Duration (ms)"
    )

    outputhelper.save_figure(fig, "difference-graph")
    outputhelper.dump_data_as_csv(merged, "difference-data")

    tolerance_ms = 10

    slowdowns = merged[(merged[_signum] == -1) & (abs(merged[_difference]) > tolerance_ms)]

    if slowdowns is None:
        log.info("✅✅There were no API calls that took longer")
    else:
        log.warning("============== 🔻🔻🔻 Results 🔻🔻🔻 ================")
        log.warning(f"🔻🔻 [{len(slowdowns.index)}] out of [{len(merged.index)}] api calls were slower "
                    f" (tolerance {tolerance_ms}ms)")
        outputhelper.dump_data_as_csv(slowdowns, "difference-data-slowdowns", with_index=False)


def merge_data_and_compute_difference(raw_calls_2, raw_calls_base):
    merged_data = raw_calls_base.merge(raw_calls_2, how="inner", on=[_ticketcount, _url], suffixes=["_1", "_2"])
    log.debug("merged data")
    log.debug(merged_data)

    merged_data[_difference] = merged_data[_duration + "_1"] - merged_data[_duration + "_2"]
    log.debug("merged data with difference")
    log.debug(merged_data)

    merged_data[_signum] = np.sign(merged_data[_difference])
    log.debug(merged_data)

    return merged_data


def load_api_result_csv(filename: str) -> DataFrame:
    csv_path = datasource.get_file_path(filename + ".csv")

    df = pd.read_csv(csv_path, header=0, names=[_ticketcount, _url, _duration],
                     usecols=[_ticketcount, _url, _duration])

    log.debug("Loaded data")
    log.debug(df)

    return df


if __name__ == '__main__':
    # draw_difference_graph()
    draw_difference_graph("results-timed-api", "results-timed-api2")
