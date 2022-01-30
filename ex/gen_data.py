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
	# data.Generation.file_userinput(M, K, ALPHA_1, ALPHA_2, FILE)
	kv_data = data.UiKvData()
	data.Generation.file_generate_kv('data_ui.csv', kv_data, True)

	kv_data.save('data.pickle')
	kv_data.load('data.pickle')
	kv_data.set(32, 'echo', 1, 2, 3)
	print(kv_data)
	print(kv_data.get('v_j', 0))

	kv_data = data.RandomKvData()
	data.Generation.file_generate_kv('data_random.csv', kv_data, True)
