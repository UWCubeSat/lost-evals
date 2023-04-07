#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

blur_exposures = np.linspace(0.1, 1, num=params.centroid_blur_num_pts)

def run_at_exposure(algo_params, exposure):
    ran = runner.run_lost(['--generate', params.centroid_num_trials,
                           '--generate-random-attitudes', 'true',
                           '--generate-blur-ra=.3', '--generate-blur-de=.15', '--generate-blur-roll=0',
                           '--generate-exposure', exposure]
                          + params.centroid_blur_base_args
                          + algo_params
                          + ['--compare-centroids', '-'])
    return ran['centroids_mean_error']

for algo_name, algo_params in params.centroid_blur_algos:
    ax.plot(blur_exposures, [run_at_exposure(algo_params, expo) for expo in blur_exposures],
            label=algo_name,
            marker='.')

ax.set_title('Centroid error vs Motion Blur')
ax.set_xlabel('Blur angle')
ax.set_ylabel('Mean centroid error (pixels)')
ax.legend()

plt.savefig(sys.argv[1])
