from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import data
import linsolv_model as lsm

FILE = 'data.csv'

if __name__ == "__main__":
	kv_data = data.RandomKvData()
	data.Generation.file_generate_kv(FILE, kv_data)
	builder = lsm.Builder(data.Read.readf_iter(FILE))

	print(builder.mat_a)
	lsm.Output.print_matrix(builder.mat_b.matrix)
	print(builder.bounds)
	lsm.Output.print_matrix(builder.mat_max_equation)
