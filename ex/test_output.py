from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import data
import linsolv_model as lsm

FILE = 'data.csv'

if __name__ == "__main__":
    data.Generation.file_generate(FILE)
    builder = lsm.Builder(data.Read.readf_iter(FILE))

    print(builder.mat_a)
    lsm.Output.print_matrix(builder.mat_b.matrix)
    print(builder.bounds)
