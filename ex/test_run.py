from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import data
import linsolv_model as lsm
from scipy.optimize import linprog

FILE = 'data.csv'

if __name__ == "__main__":
	kv_data = data.RandomKvData()
	data.Generation.file_generate_kv(FILE, kv_data)
	builder = lsm.Builder(data.Read.readf_iter(FILE))

	sol = linprog(
		c = builder.mat_max_equation,
		A_eq = builder.mat_a.matrix,
		b_eq = builder.mat_b.matrix,
		bounds = builder.bounds
	)

	print(sol)
	print(len(sol.x))
