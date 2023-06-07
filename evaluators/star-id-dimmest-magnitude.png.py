#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
from common.starid_helpers import evaluate_starid

fig, ax = plt.subplots()

min_magnitudes = np.linspace(params.dimmest_brightest, params.dimmest_dimmest, num=params.dimmest_num_pts)
special_paramss = [['--generate-cutoff-mag', m] for m in min_magnitudes]

evaluate_starid(ax, special_paramss, min_magnitudes)

ax.set_title('Star-ID Availability & Error Rate vs Dimmest Visible Star')
ax.set_xlabel('Dimmest Centroided Star (magnitude)')

plt.savefig(sys.argv[1])
