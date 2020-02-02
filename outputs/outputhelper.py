import os

from pandas import DataFrame
from plotly.offline import plot as saveplotoffline

dirname = os.path.dirname(os.path.abspath(__file__))


def save_figure(fig, filename: str = "temp"):
    full_filename = os.path.join(dirname, "graphs", filename + ".html")
    saveplotoffline(fig, filename=full_filename)


def dump_data(df: DataFrame, filename: str = "apirawtimes"):
    full_filename = os.path.join(dirname, "datadump", filename + ".csv")
    df.to_csv(full_filename)
    print(f"File saved to {full_filename}")
