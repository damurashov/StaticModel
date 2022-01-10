# Scipy linprog test
# Min 2*x1 - 4*x2
# x1 + x2 = 6
# 0 <= x1 <= 9
# 0 <= x2 <= 60

from scipy.optimize import linprog


c = [2, -4]
a_ub = None
b_ub = None
a_eq = [[1, 1], [0, 0]]
b_eq = [[6],[0]]
x1_bound = (0, 9,)
x2_bound = (0, 60,)
bounds = [x1_bound, x2_bound]


if __name__ == "__main__":
	print(linprog(c=c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds))
