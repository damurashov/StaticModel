# Encapsulates working with data.
# The format adopted for data is list of dictionaries with keys comprised of values stored in Generation.SCHEME.
# The indices, namely i, j, l are counted from 1. The appropriate adjustments must be taken by data consuming modules,
# such as linsolv_model

from random import randint, uniform, random
import csv


class Generation:

	# Data generation constraints. Mind the types - they are used to infer the type of a generated value

	PSI_JL_MAX = 3.0  # Max channel throughput
	V_J_MAX = 1.0  # Max memory for node J
	PHI_JL_MAX = 1.5  # Max node performance
	N_L = 2  # Number of structural stability regions
	N_J = 3  # Number of nodes
	CONNECTEDNESS = .6  # Probability that there is a link b/w 2 nodes
	X_JL_MAX = 2.0  # Data threshold, max constraint value. Fixed amount of data that should be processed on a given node during structural stability timespan `L`

	SCHEME = ["l", "j", "i", "psi_jil", "v_j", "phi_jl", "x_jl"]

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
	def iter_generate(f_gen_scheme=True):
		if f_gen_scheme:
			yield Generation.SCHEME

		for j in range(Generation.N_J):
			v_j = Generation._uniform(0, Generation.V_J_MAX)

			for l in range(Generation.N_L):
				phi_jl = Generation._uniform(0, Generation.PHI_JL_MAX)
				x_jl  = Generation._uniform(0, Generation.X_JL_MAX)

				for i in range(Generation.N_J):
					if i == j:
						continue

					psi_jil = Generation._is_connected() * Generation._uniform(0, Generation.PSI_JL_MAX)

					yield [l, j, i, psi_jil, v_j, phi_jl, x_jl]

	@staticmethod
	def generate():
		return list(Generation.iter_generate())

	@staticmethod
	def file_generate(filename='data.csv'):
		with open(filename, 'w') as f:
			writer = csv.writer(f)

			for row in Generation.iter_generate():
				writer.writerow(row)


class Read:
	@staticmethod
	def readf_iter(filename):
		with open(filename, 'r') as f:
			reader = csv.DictReader(f)

			for row in reader:
				yield(row)

	@staticmethod
	def search_iter(data_iterable, condition=lambda row: None):
		for d in data_iterable:
			if condition(d):
				yield(d)


if __name__ == "__main__":
	Generation.file_generate('data.csv')

	for r in Read.readf_iter("data.csv"):
		print(r)
