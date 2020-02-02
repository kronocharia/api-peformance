import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame

from datasource import datasource
from datasource.datasource import ApiResult, ApiProfile
from outputs import outputhelper


def import_additional_results_from_csv(filename: str) -> DataFrame:
    return import_additional_results(filename, "csv")


def import_additional_results(filename: str, extension: str) -> DataFrame:
    full_filename = filename + "." + extension
    csv_path = datasource.get_file_path(full_filename)
    df = pd.read_csv(csv_path, header=0, names=["x", filename], usecols=[0, 1])
    return df


def foo():
    csv_path = datasource.get_input_file_path()

    df = pd.read_csv(csv_path, header=1, names=["x", "y"], usecols=["x", "y"])
    # print(df)

    # print(df.iloc[:, 0])
    # print(df.iloc[:, 1])

    df2 = pd.read_csv(datasource.get_file_path("additional.csv"),
                      header=1, names=["a", "b", "c"], usecols=["b", "c"])

    second_run = import_additional_results("input2", "csv")
    run_3 = import_additional_results_from_csv("input3")

    print(run_3)
    # print(df.join(df2))
    # print(df.join(df2.iloc[:,0]))

    # df['b'] = df2.b

    df = df.join(second_run.input2)
    df = df.join(run_3.input3)

    fig = px.scatter(df, x=df.x, y=df.y)

    # fig.show()

    df_melt = df.melt(id_vars="x", value_vars=["y", "input2"])
    print(df_melt)

    # fig = px.scatter(df, x=df_melt.x, y=df_melt.value, color=df_melt.variable)

    trace2 = go.Scatter(x=df.x, y=df.input2, mode="lines+markers")
    fig.add_trace(trace2)

    fig.show()


def api():
    df = import_additional_results_from_csv("api_input")

    mean = df.groupby("x").mean()
    print(mean)
    fig = px.scatter(df, x=df.x, y=df.api_input)
    trace2 = go.Scatter(x=mean.index, y=mean.api_input, mode="lines+markers", name="Mean")
    fig.add_trace(trace2)
    outputhelper.save_figure(fig, "test1")


def api_live():
    apicalls: [ApiProfile] = datasource.create_dummy_api_csv()
    df = DataFrame.from_records([dict(entry) for entry in apicalls])

    df.duration = pd.to_numeric(df.duration)
    df.ticketcount = pd.to_numeric(df.ticketcount)
    # print(df.shape)
    print(df.info())

    mean = df.groupby("ticketcount").mean()
    # print(mean)

    api_improved = datasource.create_dummy_api_improvement_csv()
    df2 = DataFrame.from_records([dict(entry2) for entry2 in api_improved])
    df2.duration = pd.to_numeric(df2.duration)
    df2.ticketcount = pd.to_numeric(df2.ticketcount)
    trace3 = go.Scatter(x=df2.ticketcount, y=df2.duration, mode="markers", name="Improved")

    mean2 = df2.groupby("ticketcount").mean()
    trace4 = go.Scatter(x=mean2.index, y=mean2.duration, mode="lines+markers", name="Improved-Mean")


    fig = go.Figure()
    trace1 = go.Scatter(x=df.ticketcount, y=df.duration, mode="markers", name="Base")
    fig.add_trace(trace1)
    # fig = px.scatter(df, x=df.ticketcount, y=df.duration)
    trace2 = go.Scatter(x=mean.index, y=mean.duration, mode="lines+markers", name="Base-Mean")
    fig.add_trace(trace2)
    fig.add_trace(trace3)
    fig.add_trace(trace4)

    results = df[['ticketcount', 'duration']].copy()
    results['improved'] = df2.duration
    print(results)




    outputhelper.save_figure(fig)
    outputhelper.dump_data(results, "api-mean-changes")


if __name__ == '__main__':
    # foo()
    # api()
    api_live()
