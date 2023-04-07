#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

perturbation_levels = np.linspace(0, params.perturbation_max_perturbation, num=params.perturbation_num_perturbations)

# TODO set fov in params?
fov_deg = 20
image_width = 1024
min_angular_tolerance_deg = 0.05

def run_at_perturbation(pipeline_params, db_path, perturbation):
    max_perturbation_pixels = math.sqrt(2 * (perturbation*2)**2)
    # TODO determine the most reasonable angular tolerance to set? The conservative maximum is
    # max_perturbation_pixels*2, if both stars are deflected away or toward each other, but that
    # results in some very large tolerances.
    angular_tolerance_deg = max(min_angular_tolerance_deg, 1.1 * fov_deg * (perturbation*2 / 1024))
    ran = runner.run_lost(['--generate', params.star_id_num_trials,
                           '--generate-centroids-only', 'true',
                           '--generate-random-attitudes', 'true',
                           '--generate-perturb-centroids', perturbation,
                           '--angular-tolerance', angular_tolerance_deg,
                           # TODO: this threshold may be too generous, giving a higher identification rate than reality (but probably it's fine):
                           '--centroid-compare-threshold', max_perturbation_pixels+0.5]
                          + params.perturbation_base_args
                          + pipeline_params
                          + ['--database', db_path,
                             '--compare-star-ids', '-'])
    # I have to admit, float division by default is nice
    return 100.0 * ran['starid_num_images_correct'] / params.star_id_num_trials

for star_id_algo_info in params.perturbation_star_id_algos:
    with star_id_algo_info.db as db_path:
        sky_coverages = [run_at_perturbation(star_id_algo_info.pipeline_params, db_path, pert) for pert in perturbation_levels]
        print(sky_coverages)
        ax.plot(perturbation_levels,
                sky_coverages,
                label=star_id_algo_info.name,
                marker='.')

ax.set_title('Star-ID Sky Coverage vs Centroid Error')
ax.set_xlabel('Centroid Error stddev (pixels)')
ax.set_ylabel('Sky Coverage (%)')
ax.legend()

plt.savefig(sys.argv[1])
