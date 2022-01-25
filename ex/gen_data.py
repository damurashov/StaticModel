from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import data

M = 7
K = 3
ALPHA_1 = .5
ALPHA_2 = .5
FILE = 'data.csv'

if __name__ == "__main__":
	data.Generation.file_userinput(M, K, ALPHA_1, ALPHA_2, FILE)
