
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import linsolv_model


if __name__ == "__main__":
    print(linsolv_model.wrap_solve_pickle(sys.argv[1]))
