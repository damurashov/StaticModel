from random import randint, uniform, random
import csv


class Generation:

	PSI_JL_MAX = 3.0
	V_J_MAX = 1.0
	PHI_JL_MAX = 1.5  # Max channel throughput
	N_L = 4  # Number of structural stability regions
	N_J = 10  # Number of nodes
	CONNECTEDNESS = .6  # Probability that there is a link b/w 2 nodes

	SCHEME = ["l", "j", "i", "psi_ijl", "psi_jil", "v_j", "phi_jl"]

	@staticmethod
	def _uniform(a, b):
		f_float = type(a) is float or type(b) is float

		if f_float:
			return uniform(a, b)
		else:
			return randint(a ,b)

	@staticmethod
	def _is_connected() -> int:
		return int(random() < Generation.CONNECTEDNESS)

	@staticmethod
	def _iter_generate():
		yield Generation.SCHEME

		for j in range(Generation.N_J):
			v_j = Generation._uniform(0, Generation.V_J_MAX)

			for l in range(Generation.N_L):
				phi_jl = Generation._uniform(0, Generation.PHI_JL_MAX)

				for i in range(Generation.N_J):
					if i == j:
						continue

					psi_ijl = Generation._is_connected() * Generation._uniform(0, Generation.PSI_JL_MAX)
					psi_jil = Generation._is_connected() * Generation._uniform(0, Generation.PSI_JL_MAX)

					yield [l, j, i, psi_ijl, psi_jil, v_j, phi_jl]

	@staticmethod
	def generate():
		return list(Generation._iter_generate())

	@staticmethod
	def file_generate(filename='data.csv'):
		with open(filename, 'w') as f:
			writer = csv.writer(f)

			for row in Generation._iter_generate():
				writer.writerow(row)


if __name__ == "__main__":
	Generation.file_generate('data.csv')
