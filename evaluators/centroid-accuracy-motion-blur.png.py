#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys

blur_exposures = np.linspace(0, 1, num=8)

plt.plot(blur_exposures, np.random.default_rng().poisson(5, size=8))
plt.savefig(sys.argv[1])
