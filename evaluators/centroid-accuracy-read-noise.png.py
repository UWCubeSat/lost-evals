#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

read_noise_levels = np.linspace(0, params.centroid_noise_max_noise, num=params.centroid_noise_num_pts)

def run_at_noise(algo, noise):
    ran = runner.run_lost(['--generate', params.centroid_num_trials,
                           '--generate-random-attitudes', 'true']
                          + params.centroid_noise_base_args
                          + ['--centroid-algo', algo, '--generate-read-noise', noise]
                          + ['--compare-centroids', '-'])
    return ran['centroids_mean_error']

for algo_name, algo_code in params.centroid_algos:
    ax.plot(read_noise_levels, [run_at_noise(algo_code, noise_level) for noise_level in read_noise_levels],
            label=algo_name,
            marker='.')

ax.set_title('Centroid error vs Read Noise')
ax.set_xlabel('Read noise stddev (fraction of full-scale)')
ax.set_ylabel('Mean centroid error (pixels)')
ax.legend()
        
plt.savefig(sys.argv[1])
