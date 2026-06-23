# Documentation

## Description
The objective of this package is to offer a fast and easy way to obtain a (n x n) mutual information (MI) matrix. The basic process is the following:
<ol>
<li>Read the count matrix and delete genes that only has 0 as values (to reduce computation time)</li>
<li>Discretize using infotheo (R)</li>
<li>Obtain MI matrix using Numba and entropies</li>
<li>Save the matrix using polars</li>
</ol>

## Installation
<p>This is the documentation for the library numba_mi. To be able to run this package is important to prepare an environment like conda or venv</p>
<ol>
<li>Clone the repository
<li>Move to the directory
<li>Create environment in conda</li>
<code>conda create -n numba_mi python=3.12 pip</code>
<li>Install package</li>
<code>python3 -m pip install -e .</code>
<li>Install packages of R</li>
<code>R()</br>
install.packages("renv")</br>
renv:restore()</br>
</code>
<li>Import the package in your code</li>
<code>from numba_mi.preprocess import delete_zeroes, discretize_infotheo </br>
from numba_mi.mi_entropy import create_mi_matrix
</code>
</ol>

## Functions
<p>There are mainly 3 functions that you access in this library, which are the following:</p>
<ul>
<li>mi_entropy.create_mi_matrix<i>(df : pd.DataFrame, num_threads : int = -1 ) -> pl.DataFrame:</i></br>
This function is used to create a matrix of n x n of Mutual Information (MI). The values need to be discretize, please use preprocess.discretize_infotheo() to dicretize the matrix. It is also allowed to use any other method, as long as the matrix is discretized and dtype.int32 The parameters are:
<ul>
<li>df: DataFrame from pandas of n genes x m samples (col: genes, rows: samples)
<li>num_threads: int of number of workers/threads that this process will use. The default is the maximum number of threads allowed by the cpu.
</ul>
<li>preprocess.delete_zeroes<i>(file_path : str, axis : int = 1, sep : str = "\t", index_col : int = 0) -> pd.DataFrame:</i>: 
<ul>
<li>filepath: str of filepath to the unprocessed csv / tsv 
<li>axis: int, indicating the position of the genes. 1 if genes in rows, 0 if columns. 
<li>sep: str, use the same strings as when using pandas for separators.
<li>index_col: Indicate the index column in the count matrix. It is the same as pandas.read_csv's index_col.
</ul>
<li>discretize_infotheo<i>(input_file: str, output_file: str) -> None:</i>
<ul>
<li>input_file: str, path to input file (CSV) to discretize the data. It doesn't consider index columns. It is important to use absolute paths (os.path.abspath()) or temporary directories, as the Rscript runs on numbi_mi directory instead of your actual directory,
<li>output_file: str, path to output file (CSV) It is important to use absolute paths (os.path.abspath()) or temporary directories, as the Rscript runs on numbi_mi directory instead of your actual directory.
</ul>
</ul>
There is another function that does all the process, making temporary files and deletes them at the end:
<ul>
<li>pipeline.whole_process(file_path : str, axis : int = 1, sep : str = "\t", index_col : int = 0, num_threads : int = -1 ) -> pl.DataFrame:  </br>
Does the deletion of zeroes to allow faster computation, discretization, and mutual information matrix.
<ul>
<li>filepath: str of filepath to the unprocessed csv / tsv 
<li>axis: int, indicating the position of the genes. 1 if genes in rows, 0 if columns. 
<li>sep: str, use the same strings as when using pandas for separators.
<li>index_col: Indicate the index column in the count matrix. It is the same as pandas.read_csv's index_col.
<li>num_threads: int of number of workers/threads that this process will use. The default is the maximum number of threads allowed by the cpu.
</ul>
</ul>
