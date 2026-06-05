import subprocess
import pandas as pd
from pathlib import Path 

def delete_zeroes(file_path : str, axis : int = 1, sep : str = "\t", index_col : int = 0) -> pd.DataFrame:
    """
    Delete rows or columns of zeroes to reduce computation time. Accepts TSV/CSV and returns a pandas DataFrame.
    """
    df = pd.read_csv(file_path, sep=sep, index_col=index_col)
    try:
        if axis not in [0, 1]:
            raise ValueError("Invalid axis value. Use 1 for columns or 0 for rows.")
        if axis == 0:
            df = df.transpose()
    except ValueError as e:
        print(e)
        return None
    df["sum"] = df.sum(axis = 1)
    df = df.query("sum != 0.0")
    df = df.drop(columns=["sum"])
    df = df.transpose()
    return df


def discretize_infotheo(input_file: str, output_file: str) -> None:
    """Discretize the data using the R package infotheo. The input and output files should be in CSV format."""
    
    project_root = Path(__file__).resolve().parents[2]

    subprocess.run(['Rscript', './R/discretize_infotheo.R', 
                     '-i', input_file, 
                     '-o', output_file]
                     , cwd=project_root,
                      check=True,)
    return None