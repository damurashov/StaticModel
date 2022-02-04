from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import data
import linsolv_model as lsm


FILE = 'ushakov.pickle'


def prepare():
	k = 3
	m = 7
	kv_data = data.KvData()

	kv_data.set(.8, 'alpha_1')
	kv_data.set(.2, 'alpha_2')
	kv_data.set(3, 'k')
	kv_data.set(7, 'm')

	v_matrix = [500, 500, 200, 200, 50, 50, 50]
	phi_matrix = [30, 30, 10, 10, 3, 3, 3]
	x_jl_matrix = [[0, 0, 0], [0, 3, 0], [0, 0, 0], [0, 0, 0], [5, 0, 0], [0, 0, 15], [10, 0, 20]]
	psi_ji_matrix = [[0, 1, 4, 3, 1, 1, 3], [0, 0, 3, 1, 1, 5, 1], [5, 3, 0, 1, 1, 5, 3], [4, 4, 5, 0, 2, 2, 4], [2, 4, 5, 1, 0, 0, 1], [2, 3, 3, 5, 5, 0, 0], [2, 2, 3, 1, 2, 2, 0]]

	for j in range(m):
		for l in range(k):
			kv_data.set(v_matrix[j], 'v_jl', j, l)
			kv_data.set(phi_matrix[j], 'phi_jl', j, l)
			kv_data.set(x_jl_matrix[j][l], 'x_jl', j, l)

			for i in range(m):
				if i == j:
					continue

				kv_data.set(psi_ji_matrix[j][i], 'psi_jil', j, i, l)

	kv_data.save(FILE)


if __name__ == "__main__":
	lsm.wrap_solve_pickle(FILE)
