import os

use_gpu = bool(os.environ.get('USE_GPU'))

if use_gpu:
    import cupy as np
else:
    import numpy as np
