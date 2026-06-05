import numpy as np
import pandas as pd
from numba import njit, prange, set_num_threads
import polars as pl

@njit
def entropy_from_labels(x: np.ndarray) -> float:
    """
        Calculate the entropy of discretized ndarray.
    """
    max_label = x.max()
    counts = np.zeros(max_label + 1, dtype=np.int64)

    for v in x:
        counts[v] += 1

    n = x.size
    h = 0.0

    for c in counts:
        if c > 0:
            p = c / n
            h -= p * np.log(p)

    return h


@njit
def joint_entropy_from_labels(x: np.ndarray, y: np.ndarray, n_bins_y: int) -> float:
    """
        Hashes and obtains the joint entropy of two sets
    """
    joint = x * n_bins_y + y
    return entropy_from_labels(joint)


@njit(parallel=True)
def mi_matrix_numba(X: np.ndarray) -> np.ndarray:
    """
        Calculate the mutual information matrix for a discretized 2D array.
    """
    n_samples, n_features = X.shape
    mi = np.zeros((n_features, n_features), dtype=np.float32)
    entropies = np.zeros(n_features, dtype=np.float64)

    max_label = X.max()
    n_bins = max_label + 1

    for i in prange(n_features):
        entropies[i] = entropy_from_labels(X[:, i])
        mi[i, i] = 1.0

    for i in prange(n_features):
        x = X[:, i]
        for j in range(i + 1, n_features):
            y = X[:, j]
            hxy = joint_entropy_from_labels(x, y, n_bins)
            score = entropies[i] + entropies[j] - hxy
            if score < 0:
                score = 0.0
            mi[i, j] = score
            mi[j, i] = score

    return mi


def create_mi_matrix(df : pd.DataFrame, num_threads : int = -1 ) -> pl.DataFrame:
    """
        Create a mutual information matrix from a discretized pandas DataFrame (col are genes, rows are samples). The number of threads can be set for parallel processing.
    """
    if num_threads != -1:
        set_num_threads(num_threads)
    genes = df.columns.tolist()
    for col in df.columns:
        df[col] = pd.factorize(df[col], sort=True)[0].astype("int32")
    X = df.to_numpy(dtype=np.int32)
    mi = mi_matrix_numba(X)
    
    df_mi = pl.from_numpy(mi, schema=genes)
    df_mi = df_mi.insert_column(0, pl.Series("", genes))
    return df_mi