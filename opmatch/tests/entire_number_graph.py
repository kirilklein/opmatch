import matplotlib.pyplot as plt
import numpy as np

ps = np.linspace(0.1, 1, 100)
matching_ratio = ((1-ps)/ps).astype(int)
plt.scatter(ps, matching_ratio)
plt.xlabel('ps')
plt.ylabel('matching ratio')
plt.show()