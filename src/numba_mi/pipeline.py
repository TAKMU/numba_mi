from pathlib import Path
import pandas as pd
from numba_mi.mi_entropy import create_mi_matrix
from numba_mi.preprocess import discretize_infotheo, delete_zeroes
import polars as pl
from tempfile import TemporaryDirectory


def whole_process(file_path : str, axis : int = 1, sep : str = "\t", index_col : int = 0, num_threads : int = -1 ) -> pl.DataFrame:
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        df = delete_zeroes(file_path, axis, sep, index_col)
        df.to_csv(f"{tmpdir}/simplified.csv")
        discretize_infotheo(f"{tmpdir}/simplified.csv", f"{tmpdir}/discretized.csv")
        df = pd.read_csv(f"{tmpdir}/discretized.csv")
    return create_mi_matrix(df, num_threads = num_threads)

