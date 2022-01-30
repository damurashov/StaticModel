# Encapsulates working with data.
# The format adopted for data is list of dictionaries with keys comprised of values stored in Generation.SCHEME.
# The indices, namely i, j, l are counted from 1. The appropriate adjustments must be taken by data consuming modules,
# such as linsolv_model

from random import Random, randint, uniform, random
import csv
import re


class KvData(dict):
	"""
	Stores key-value data pairs in format {(str(VAR), int(INDEX1), int(INDEX2), ...) : float(VALUE)}
	"""
	def get(self, var, *indices):
		key = KvData._as_key(var, *indices)

		if key in self.keys():
			return self[key]
		else:
			self._generate(var, *indices)
			return self[key]

	@staticmethod
	def _as_key(var, *indices):
		assert len(indices) > 0
		var = str(var)
		indices = (int(i) for i in indices)
		return (var, *indices,)

	def _generate(self, key):
		"""
		Either generates a key guaranteeing its presence in the dictionary, or throws an assertion
		"""
		raise NotImplemented

	def set(self, val, var, *indices):
		val = float(val)
		key = KvData._as_key(var, *indices)
		self[key] = val


class RandomKvData(KvData):

	PSI_JL_MAX = 3.0  # Max channel throughput
	V_J_MAX = 1.0  # Max memory for node J
	PHI_JL_MAX = 1.5  # Max node performance
	N_L = 2  # Number of structural stability intervals
	N_J = 3  # Number of nodes
	CONNECTEDNESS = .6  # Probability that there is a link b/w 2 nodes
	X_JL_MAX = 2.0  # Data threshold, max constraint value. Fixed amount of data that should be processed on a given node during structural stability timespan `L`

	@staticmethod
	def _uniform(a, b):
		f_float = type(a) is float or type(b) is float

		if f_float:
			return uniform(a, b)
		else:
			return randint(a ,b)

	@staticmethod
	def _is_connected() -> int:
		return int(random() < RandomKvData.CONNECTEDNESS)

	def _generate(self, key):

		var = key[0]

		gen_map = {
			'v_j': lambda: RandomKvData._uniform(0, RandomKvData.V_J_MAX),
			'phi_jl': lambda: RandomKvData._uniform(0, RandomKvData.PHI_JL_MAX),
			'x_jl': lambda: RandomKvData._uniform(0, RandomKvData.X_JL_MAX),
			'psi_jil': lambda: RandomKvData._is_connected() * RandomKvData._uniform(0, RandomKvData.PSI_JL_MAX),
			'm': lambda: RandomKvData.N_J,  # Number of nodes
			'k': lambda: RandomKvData.N_L,  # Number of structural stability intervals
			'alpha': lambda: .5,
		}
		assert var in gen_map.keys()
		assert key not in self.keys()
		generated = gen_map[var]()
		self.set(generated, *key)


class UiKvData(KvData):

	def _generate(self, key):
		"""
		Forms dictionary of values according to the following format:
		{(str(VAR), int(INDEX1), int(INDEX2), ...) : float(VALUE)}
		"""
		while True:
			if key in self.keys():
				return

			inp = input(str(key))
			inp = inp.strip()
			inp = re.split(r'\s+', inp)
			cmd = inp[0] if len(inp) else ''

			try:
				if cmd == '?':
					print('\n'.join([
						"?  -  help",
						"edit VAR INDEX1 INDEX2 ...  -  change entry",
						"show  -  show all"
					]))

				elif cmd == 'show':
					for k in self.keys():
						print(f"{k}  -  {self[k]}")

				elif cmd == 'edit':
					k = KvData._as_key(*inp[1:])

					res = self.pop(k, None)
					print(f"Removed: {res}")

					while k not in self.keys():
						self._generate(k)

				else:
					cmd = float(cmd)
					self.set(cmd, *key)

					return

			except Exception as e:
				print(str(e))


class Generation:

	# Data generation constraints. Mind the types - they are used to infer the type of a generated value

	PSI_JL_MAX = 3.0  # Max channel throughput
	V_J_MAX = 1.0  # Max memory for node J
	PHI_JL_MAX = 1.5  # Max node performance
	N_L = 2  # Number of structural stability regions
	N_J = 3  # Number of nodes
	CONNECTEDNESS = .6  # Probability that there is a link b/w 2 nodes
	X_JL_MAX = 2.0  # Data threshold, max constraint value. Fixed amount of data that should be processed on a given node during structural stability timespan `L`

	SCHEME = ["l", "j", "i", "psi_jil", "v_j", "phi_jl", "x_jl", "alpha_1", "alpha_2"]

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

		alpha_1 = Generation._uniform(0.0, 1.0)
		alpha_2 = 1 - alpha_1

		for j in range(Generation.N_J):
			v_j = Generation._uniform(0, Generation.V_J_MAX)

			for l in range(Generation.N_L):
				phi_jl = Generation._uniform(0, Generation.PHI_JL_MAX)
				x_jl  = Generation._uniform(0, Generation.X_JL_MAX)

				for i in range(Generation.N_J):
					if i == j:
						continue

					psi_jil = Generation._is_connected() * Generation._uniform(0, Generation.PSI_JL_MAX)

					yield [l, j, i, psi_jil, v_j, phi_jl, x_jl, alpha_1, alpha_2]

	@staticmethod
	def iter_generate_kv(kv_data, f_gen_scheme = True):
		pass

	@staticmethod
	def _ui_format_key(*args):
		var = args[0:1]
		inp = args[1:]
		print(var)
		inp = [int(v) for v in inp]
		print(inp)
		return tuple(list(var) + inp)

	@staticmethod
	def _ui_update_uimap(uimap, *args):
		"""
		Forms dictionary of values according to the following format:
		{(str(VAR), int(INDEX1), int(INDEX2), ...) : float(VALUE)}
		"""
		while True:
			if args in uimap.keys():
				return uimap

			inp = input(str(args))
			inp = inp.strip()
			inp = re.split(r'\s+', inp)

			try:
				if inp[0] == '?':
					print('\n'.join([
						"?  -  help",
						"edit VAR INDEX1 INDEX2 ...  -  rmv. entry",
						"show  -  show all"
					]))
					return Generation._ui_update_uimap(uimap, *args)
				elif inp[0] == 'show':
					for k in uimap.keys():
						print(f"{k}  -  {uimap[k]}")
				elif inp[0] == 'edit':
					key = Generation._ui_format_key(*inp[1:])

					res = uimap.pop(key, None)
					print(f"Removed: {res}")

					while key not in uimap.keys():
						uimap = Generation._ui_update_uimap(uimap, *key)
				else:
					try:
						inp = float(inp[0])
						uimap[args] = inp

						print(uimap)
						return uimap
					except Exception as e:
						print(str(e))

			except Exception as e:
				print(str(e))

	@staticmethod
	def iter_userinput(m, k, alpha_1, alpha_2, f_gen_scheme=True):
		"""
		m - number of nodes
		k - number of structural stability intervals
		"""

		if f_gen_scheme:
			yield Generation.SCHEME

		uimap = dict()

		for j in range(m):
			uimap = Generation._ui_update_uimap(uimap, 'v_j', j)

			for l in range(k):
				uimap = Generation._ui_update_uimap(uimap, 'phi_jl', j, l)
				uimap  = Generation._ui_update_uimap(uimap, 'x_jl', j, l)

				for i in range(m):
					if i == j:
						continue

					uimap = Generation._ui_update_uimap(uimap, 'psi_jil', j, i, l)

		for j in range(m):
			v_j = uimap.pop(('v_j', j))

			for l in range(k):
				phi_jl = uimap.pop(('phj_jl', j, l))
				x_jl  = uimap.pop(('x_jl', j, l))

				for i in range(m):
					if i == j:
						continue

					psi_jil = uimap.pop(('psi_ijl', i, j, l))

					yield [l, j, i, psi_jil, v_j, phi_jl, x_jl, alpha_1, alpha_2]

	@staticmethod
	def generate():
		return list(Generation.iter_generate())

	@staticmethod
	def file_generate(filename='data.csv'):
		with open(filename, 'w') as f:
			writer = csv.writer(f)

			for row in Generation.iter_generate():
				writer.writerow(row)

	@staticmethod
	def file_userinput(m, k, alpha_1, alpha_2, filename='data.csv'):
		with open(filename, 'w') as f:
			writer = csv.writer(f)

			for row in Generation.iter_userinput(m, k, alpha_1, alpha_2, True):
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
