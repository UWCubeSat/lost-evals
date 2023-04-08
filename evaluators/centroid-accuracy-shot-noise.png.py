#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

photoelectrons = np.linspace(params.centroid_shot_noise_min_photoelectrons, params.centroid_shot_noise_max_photoelectrons,
                             num=params.centroid_shot_noise_num_pts)

def run_at_photoelectrons(algo_params, pes):
    saturation_photons = pes / params.centroid_shot_noise_photoelectron_sensitivity_ratio
    ran = runner.run_lost(params.centroid_shot_noise_base_args +
                          ['--generate', params.centroid_num_trials,
                           '--generate-random-attitudes=true',
                           '--generate-zero-mag-photons', pes,
                           '--generate-saturation-photons', saturation_photons,
                           '--generate-exposure=1',
                           '--compare-centroids=-']
                          + algo_params)
    return ran['centroids_mean_error']

for algo_name, algo_code in params.centroid_shot_noise_algos:
    ax.plot(photoelectrons, [run_at_photoelectrons(algo_code, pes) for pes in photoelectrons],
            label=algo_name,
            marker='.')

ax.set_title('Centroid error vs Photoelectrons (Constant effective brightness)')
ax.set_xlabel('Photoelectrons for zero-magnitude star')
ax.set_ylabel('Centroid error (pixels)')
ax.legend()

plt.savefig(sys.argv[1])
