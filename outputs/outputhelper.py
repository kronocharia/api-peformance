import os

from pandas import DataFrame
from plotly.offline import plot as saveplotoffline

from datasource import datasource

dirname = os.path.dirname(os.path.abspath(__file__))


def save_figure(fig, filename: str = "temp"):
    full_filename = os.path.join(dirname, "graphs", filename + ".html")
    saveplotoffline(fig, filename=full_filename)


def dump_data_as_csv(df: DataFrame, filename: str = "apirawtimes"):
    full_filename = os.path.join(dirname, "datadump", filename + ".csv")
    df.to_csv(full_filename)
    print(f"File saved to {full_filename}")


def save_to_input_directory(df: DataFrame, filename: str = "apirawtimes"):
    full_filename = os.path.join(datasource.dirname, filename + ".csv")
    df.to_csv(full_filename, index=False)
    print(f"File saved to {full_filename}")
