#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

exposures = np.linspace(params.centroid_exposure_min_exposure, params.centroid_exposure_max_exposure, num=params.centroid_exposure_num_pts)

def run_at_exposure(algo_params, exposure):
    saturation_photons = exposure * params.centroid_exposure_saturation_photoelectrons_at_exposure_1
    ran = runner.run_lost(['--generate', params.centroid_num_trials,
                           '--generate-random-attitudes', 'true',
                           '--generate-saturation-photons', saturation_photons,
                           '--generate-exposure', exposure,
                           '--compare-centroids=-']
                          + algo_params)
    return ran['centroids_mean_error']

for algo_name, algo_code in params.centroid_exposure_algos:
    ax.plot(exposures, [run_at_exposure(algo_code, exposure) for exposure in exposures],
            label=algo_name,
            marker='.')

ax.set_title('Centroid error vs Exposure (Controlling effective brightness)')
ax.set_xlabel('Exposure (see text)')
ax.set_ylabel('Centroid error (pixels)')
ax.legend()

plt.savefig(sys.argv[1])
