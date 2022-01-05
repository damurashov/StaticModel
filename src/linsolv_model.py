# This module forms an input matrix for scipy linear solver based on the data it is provided with.
# The input data format is defined and described in `data.py`

class EqMatrix:
	"""
	Contains a set of useful shortcuts that interpret subject area equality-constraints pertaining to channel
	designation task into a system of equations for scipy linear solver represented in a format Ax = b.

	With considerations to structural stability spans, the matrix is formed in the following way:

	/-----------------------------------------|-----------------------------------------/
	|x_111   ...   x_ij1   y_j1   z_j1   g_j1 |                                         |  |  j = 1 (details omitted here)
	|                                         |                                         |  |  j = 2
	|                 ...over j               |                                         |  v  ... over j
	|-----------------------------------------|-----------------------------------------|
	|     memory remainder y_j1               | x_112   ...   x_ij2   y_j2   z_j2   g_j2|  |  j = 1 (details omitted here)
	|                                         |                                         |  |  j = 2
	|                                         |                    ... over j           |  v  ... over j
	/-----------------------------------------|-----------------------------------------/
	                  n=1                                         n = 2
	              --------------------------------------------------------->

	Roughly speaking, the matrix is divided into quadrants, each of which corresponds to a structural stability span. A
	certain number of methods in this class refers to offsets, which are used to calculate a position of a requested
	element (a channel, i.e. x_ij, an amount of memoized info y_jl, etc.).
	"""

	@staticmethod
	def get_row_offset_step(data):
		pass

	@staticmethod
	def get_col_offset_step(data):
		pass

	def get_n_x_ij(self):
		""" Returns number of channels (i.e. x_ij) """
		return self.m * (self.m - 1)  # Number of permulations for nodes i,j given that i != j, a.k.a number of channels possible, given that the node cannot have a channel leading into itself

	def get_xij_offset(self, i, j):
		"""
		Regardless of current structural stability span, it calculates a position of x_ij in a row consisting of
		permutations of i and j. For example, say we have 3 nodes. The sequence is, therefore, formed as follows:
		x12 x13 x21 x23 x31 x32. `i` and `j` are counted from 1.

		Returns an offset from position 1 for a given element. For example, for x12, the offset equals 0
		"""
		assert i >= 1 and j >= 1

		# Count from 0.
		i -= 1
		j -= 1

		n = self.get_n_x_ij()

		return i * n + j - int(j > i)

	def __init__(self, data: callable):
		# Ax = b
		mat_a = [[0]]
		mat_b = [0]
		m = None  # Number of nodes, a.k.a max(j)
		k = None  # Number of structural stability spans, a.k.a max(l)

	def set_val(row, col, val):
		pass

	def set_z_jl():
