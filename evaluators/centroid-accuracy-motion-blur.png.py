#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

blur_exposures = np.linspace(0, params.centroid_blur_max_exposure, num=params.centroid_blur_num_pts)

def run_at_exposure(algo, exposure):
    ran = runner.run_lost(['--generate', params.centroid_num_trials,
                           '--generate-random-attitudes', 'true']
                          + params.centroid_blur_base_args
                          + ['--centroid-algo', algo, '--generate-exposure', exposure]
                          + ['--compare-centroids', '-'])
    return ran['mean_error']

for algo_name, algo_code in params.centroid_algos:
    ax.plot(blur_exposures, [run_at_exposure(algo_code, expo) for expo in blur_exposures],
            label=algo_name,
            marker='.')

ax.set_title('Centroid error vs Motion Blur')
ax.set_xlabel('Exposure')
ax.set_ylabel('Mean centroid error (pixels)')
ax.legend()
        
plt.savefig(sys.argv[1])
