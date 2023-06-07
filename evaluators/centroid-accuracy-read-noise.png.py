#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params

from common.centroid_helpers import evaluate_centroid

fig, ax = plt.subplots()

read_noise_levels = np.linspace(0.01, params.centroid_noise_max_noise, num=params.centroid_noise_num_pts)
special_paramss = [['--generate-read-noise', noise] for noise in read_noise_levels]

evaluate_centroid(ax, special_paramss, read_noise_levels)

ax.set_title('Centroid Error vs Read Noise')
ax.set_xlabel('Read Noise Stddev (fraction of full-scale)')
        
plt.savefig(sys.argv[1])
