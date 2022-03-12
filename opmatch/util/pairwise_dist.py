import numpy as np
import random

import pyximport
pyximport.install()
from pairwise_dist_cython import pairwise_distance

r = np.array([random.randrange(1, 1000) for _ in range(0, 1000)], dtype=float)

pairwise_distance(r)