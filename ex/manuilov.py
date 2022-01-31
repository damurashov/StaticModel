from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import data
import pickle
import linsolv_model as lsm
from scipy.optimize import linprog

userinput = {
	('v_j', 0) : 20,
	('phi_jl', 0, 0) : 50,
	('x_jl', 0, 0) : 100,
	('psi_jil', 0, 1, 0) : 100,
	('psi_jil', 0, 2, 0) : 100,
	('psi_jil', 0, 3, 0) : 0,
	('psi_jil', 0, 4, 0) : 0,
	('psi_jil', 0, 5, 0) : 0,
	('psi_jil', 0, 6, 0) : 0,
	('phi_jl', 0, 1) : 50,
	('x_jl', 0, 1) : 50,
	('psi_jil', 0, 1, 1) : 100,
	('psi_jil', 0, 2, 1) : 100,
	('psi_jil', 0, 3, 1) : 0,
	('psi_jil', 0, 4, 1) : 0,
	('psi_jil', 0, 5, 1) : 0,
	('psi_jil', 0, 6, 1) : 0,
	('phi_jl', 0, 2) : 50,
	('x_jl', 0, 2) : 0,
	('psi_jil', 0, 1, 2) : 0,
	('psi_jil', 0, 2, 2) : 0,
	('psi_jil', 0, 3, 2) : 0,
	('psi_jil', 0, 4, 2) : 0,
	('psi_jil', 0, 5, 2) : 0,
	('psi_jil', 0, 6, 2) : 0,
	('v_j', 1) : 20,
	('phi_jl', 1, 0) : 50,
	('x_jl', 1, 0) : 31.4,
	('psi_jil', 1, 0, 0) : 0,
	('psi_jil', 1, 2, 0) : 0,
	('psi_jil', 1, 3, 0) : 100,
	('psi_jil', 1, 4, 0) : 100,
	('psi_jil', 1, 5, 0) : 0,
	('psi_jil', 1, 6, 0) : 0,
	('phi_jl', 1, 1) : 50,
	('x_jl', 1, 1) : 31.6,
	('psi_jil', 1, 0, 1) : 0,
	('psi_jil', 1, 2, 1) : 0,
	('psi_jil', 1, 3, 1) : 100,
	('psi_jil', 1, 4, 1) : 100,
	('psi_jil', 1, 5, 1) : 0,
	('psi_jil', 1, 6, 1) : 0,
	('phi_jl', 1, 2) : 50,
	('x_jl', 1, 2) : 15,
	('psi_jil', 1, 0, 2) : 0,
	('psi_jil', 1, 2, 2) : 0,
	('psi_jil', 1, 3, 2) : 100,
	('psi_jil', 1, 4, 2) : 100,
	('psi_jil', 1, 5, 2) : 0,
	('psi_jil', 1, 6, 2) : 0,
	('v_j', 2) : 20,
	('phi_jl', 2, 0) : 50,
	('x_jl', 2, 0) : 20.5,
	('psi_jil', 2, 0, 0) : 0,
	('psi_jil', 2, 1, 0) : 0,
	('psi_jil', 2, 3, 0) : 100,
	('psi_jil', 2, 4, 0) : 0,
	('psi_jil', 2, 5, 0) : 0,
	('psi_jil', 2, 6, 0) : 0,
	('phi_jl', 2, 1) : 50,
	('x_jl', 2, 1) : 38.4,
	('psi_jil', 2, 0, 1) : 0,
	('psi_jil', 2, 1, 1) : 0,
	('psi_jil', 2, 3, 1) : 100,
	('psi_jil', 2, 4, 1) : 0,
	('psi_jil', 2, 5, 1) : 0,
	('psi_jil', 2, 6, 1) : 0,
	('phi_jl', 2, 2) : 50,
	('x_jl', 2, 2) : 15,
	('psi_jil', 2, 0, 2) : 0,
	('psi_jil', 2, 1, 2) : 0,
	('psi_jil', 2, 3, 2) : 100,
	('psi_jil', 2, 4, 2) : 0,
	('psi_jil', 2, 5, 2) : 0,
	('psi_jil', 2, 6, 2) : 0,
	('v_j', 3) : 50,
	('phi_jl', 3, 0) : 50,
	('x_jl', 3, 0) : 20.5,
	('psi_jil', 3, 0, 0) : 0,
	('psi_jil', 3, 1, 0) : 50,
	('psi_jil', 3, 2, 0) : 0,
	('psi_jil', 3, 4, 0) : 100,
	('psi_jil', 3, 5, 0) : 0,
	('psi_jil', 3, 6, 0) : 50,
	('phi_jl', 3, 1) : 50,
	('x_jl', 3, 1) : 18.4,
	('psi_jil', 3, 0, 1) : 0,
	('psi_jil', 3, 1, 1) : 50,
	('psi_jil', 3, 2, 1) : 0,
	('psi_jil', 3, 4, 1) : 100,
	('psi_jil', 3, 5, 1) : 0,
	('psi_jil', 3, 6, 1) : 0,
	('phi_jl', 3, 2) : 50,
	('x_jl', 3, 2) : 35,
	('psi_jil', 3, 0, 2) : 0,
	('psi_jil', 3, 1, 2) : 50,
	('psi_jil', 3, 2, 2) : 0,
	('psi_jil', 3, 4, 2) : 100,
	('psi_jil', 3, 5, 2) : 0,
	('psi_jil', 3, 6, 2) : 0,
	('v_j', 4) : 50,
	('phi_jl', 4, 0) : 50,
	('x_jl', 4, 0) : 20.3,
	('psi_jil', 4, 0, 0) : 0,
	('psi_jil', 4, 1, 0) : 0,
	('psi_jil', 4, 2, 0) : 0,
	('psi_jil', 4, 3, 0) : 0,
	('psi_jil', 4, 5, 0) : 0,
	('psi_jil', 4, 6, 0) : 0,
	('phi_jl', 4, 1) : 50,
	('x_jl', 4, 1) : 30,
	('psi_jil', 4, 0, 1) : 0,
	('psi_jil', 4, 1, 1) : 0,
	('psi_jil', 4, 2, 1) : 0,
	('psi_jil', 4, 3, 1) : 0,
	('psi_jil', 4, 5, 1) : 0,
	('psi_jil', 4, 6, 1) : 0,
	('phi_jl', 4, 2) : 50,
	('x_jl', 4, 2) : 85,
	('psi_jil', 4, 0, 2) : 0,
	('psi_jil', 4, 1, 2) : 0,
	('psi_jil', 4, 2, 2) : 0,
	('psi_jil', 4, 3, 2) : 0,
	('psi_jil', 4, 5, 2) : 0,
	('psi_jil', 4, 6, 2) : 0,
	('v_j', 5) : 10,
	('phi_jl', 5, 0) : 50,
	('x_jl', 5, 0) : 50,
	('psi_jil', 5, 0, 0) : 0,
	('psi_jil', 5, 1, 0) : 0,
	('psi_jil', 5, 2, 0) : 0,
	('psi_jil', 5, 3, 0) : 100,
	('psi_jil', 5, 4, 0) : 0,
	('psi_jil', 5, 6, 0) : 100,
	('phi_jl', 5, 1) : 50,
	('x_jl', 5, 1) : 60,
	('psi_jil', 5, 0, 1) : 0,
	('psi_jil', 5, 1, 1) : 0,
	('psi_jil', 5, 2, 1) : 0,
	('psi_jil', 5, 3, 1) : 100,
	('psi_jil', 5, 4, 1) : 0,
	('psi_jil', 5, 6, 1) : 0,
	('phi_jl', 5, 2) : 50,
	('x_jl', 5, 2) : 50,
	('psi_jil', 5, 0, 2) : 0,
	('psi_jil', 5, 1, 2) : 0,
	('psi_jil', 5, 2, 2) : 0,
	('psi_jil', 5, 3, 2) : 100,
	('psi_jil', 5, 4, 2) : 0,
	('psi_jil', 5, 6, 2) : 0,
	('v_j', 6) : 20,
	('phi_jl', 6, 0) : 50,
	('x_jl', 6, 0) : 0,
	('psi_jil', 6, 0, 0) : 0,
	('psi_jil', 6, 1, 0) : 0,
	('psi_jil', 6, 2, 0) : 0,
	('psi_jil', 6, 3, 0) : 50,
	('psi_jil', 6, 4, 0) : 100,
	('psi_jil', 6, 5, 0) : 0,
	('phi_jl', 6, 1) : 50,
	('x_jl', 6, 1) : 1,
	('psi_jil', 6, 0, 1) : 0,
	('psi_jil', 6, 1, 1) : 0,
	('psi_jil', 6, 2, 1) : 0,
	('psi_jil', 6, 3, 1) : 0,
	('psi_jil', 6, 4, 1) : 100,
	('psi_jil', 6, 5, 1) : 0,
	('phi_jl', 6, 2) : 50,
	('x_jl', 6, 2) : 1,
	('psi_jil', 6, 0, 2) : 0,
	('psi_jil', 6, 1, 2) : 0,
	('psi_jil', 6, 2, 2) : 0,
	('psi_jil', 6, 3, 2) : 0,
	('psi_jil', 6, 4, 2) : 0,
	('psi_jil', 6, 5, 2) : 0,
}

if __name__ == "__main__":
	FILE = 'manuilov.pickle'
	FILE_CSV = 'manuilov.csv'

	kv_data = data.UiKvData()
	kv_data.load(FILE)


	k = int(kv_data.get('k'))
	for l in range(k):

		total_input = kv_data.get('total_input_l', l)
		m = int(kv_data.get('m'))

		n_processing = 0
		for j in range(m):
			n_processing += kv_data.get('processing_fraction_jl', j, l)

		frac_processing = total_input / n_processing

		for j in range(m):
			x_jl = frac_processing * kv_data.get('processing_fraction_jl', j, l)
			kv_data.set(x_jl, 'x_jl', j, l)

			kv_data.save(FILE)

	for j in range(int(kv_data.get('m'))):
		for l in range(int(kv_data.get('k'))):
			key = ('x_jl', j, l,)
			val = kv_data.get(*key)

			print(f'{key} : {val}')

	data.Generation.file_generate_kv(FILE_CSV, kv_data)
	builder = lsm.Builder(data.Read.readf_iter(FILE_CSV))

	sol = linprog(
		c = builder.mat_max_equation,
		A_eq = builder.mat_a.matrix,
		b_eq = builder.mat_b.matrix,
		bounds = builder.bounds
	)

	print(sol)
	print(len(sol.x))
