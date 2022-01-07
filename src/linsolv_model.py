# This module forms an input matrix for scipy linear solver based on the data it is provided with.
# The input data format is defined and described in `data.py`


class EqMatrixA:
	"""
	Matrix builder for the equality constraint
	$ x_j = F(x_ij, x_ji, y_j, z_j, g_j) $

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

	def get_offset_x_ij(self, i, j):
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

		return i * self.n_x_ij + j - int(j > i)

	def get_offset_quadrant(self, qrow, qcolumn) -> int and int:
		assert qrow >= 0 and qcolumn >= 0

		return self.quadrant_height * qrow, self.quadrant_width * qcolumn

	def __init__(self, m, k):
		"""
		m: number of nodes
		k: number of structual stability spans
		"""
		self.m = m
		self.k = k

		self.n_x_ij = self.m * (self.m - 1)  # Number of channels ij excluding (a, a)

		self.offset_y = self.n_x_ij
		self.offset_z = self.n_x_ij + 1
		self.offset_g = self.n_x_ij + 2

		self.quadrant_width = self.offset_g + 1
		self.quadrant_height = self.m

		self.matrix = [[0] * self.quadrant_width * k] * k * self.quadrant_height

	def set_x_ijl(self, i, j, l, val):
		"""
		For the equality constraint written in the form
		`x_j = F(x_ij, x_ji, y_j, z_j, g_j)`:

		x_(index_i, index_j)l = val. For x_jil, use set_x_jil
		"""

		assert i >= 1 and j >= 1 and l >= 1

		off_x_ij = self.get_offset_x_ij(i, j)
		self.set_val(j - 1, off_x_ij, val, (l-1, l-1,))

	def set_x_jil(self, j, i, l, val):
		"""
		Complementary method to EqMatrixA.set_x_ijl
		"""

		assert i >= 1 and j >= 1 and l >= 1

		off_x_ji = self.get_offset_x_ij(j, i)
		self.set_val(j - 1, off_x_ji, val, (l-1, l-1,))

	def set_y_jl(self, j, l, value):
		"""
		y_jl = value
		"""

		assert j >= 1 and l >= 1

		self.set_val(j - 1, self.offset_y, value, (l - 1, l - 1,))

	def set_y_jlm1(self, j, l, value):
		"""
		y_j(l-1) = value
		"""

		assert j >= 1 and l >= 2

		self.set_val(j - 1, self.offset_y, value, (l - 1, l - 2,))

	def set_g_jl(self, j, l, value):
		"""
		g_jl = value
		"""

		assert j >= 1 and l >= 1

		self.set_val(j - 1, self.offset_g, value, (l - 1, l - 1,))

	def set_z_jl(self, j, l, value):
		"""
		z_jl = value
		"""

		assert j >= 1 and l >= 1

		self.set_val(j - 1, self.offset_z, value, (l - 1, l - 1,))

	def set_val(self, row, col, val, quadrant:tuple = None):
		assert row >= 0 and col >= 0 and quadrant[0] >= 0 and quadrant[1] >= 0

		if quadrant is not None:
			off_row, off_col = self.get_offset_quadrant(*quadrant)
		else:
			off_row, off_col = 0, 0

		self.matrix[row + off_row][col + off_col] = val
