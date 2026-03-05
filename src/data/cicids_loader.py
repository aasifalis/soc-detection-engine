import pandas as pd
import numpy as np


def load_cicids_dataset(path, sample_size=100000):

    df = pd.read_csv(path, nrows=sample_size)

    # clean column names
    df.columns = df.columns.str.strip()

    # remove problematic values
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    return df