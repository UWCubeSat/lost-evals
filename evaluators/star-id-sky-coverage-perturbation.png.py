#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
import common.params as params
import common.runner as runner

fig, ax_availability = plt.subplots()
ax_error = ax_availability.twinx()

perturbation_levels = np.linspace(0, params.perturbation_max_perturbation, num=params.perturbation_num_perturbations)

# TODO set fov in params?
fov_deg = 20
image_width = 1024
min_angular_tolerance_deg = 0.05

# Return tuple (availability, error rate)
def run_at_perturbation(pipeline_params, db_path, perturbation):
    max_perturbation_pixels = math.sqrt(2 * (perturbation*2)**2)
    # TODO determine the most reasonable angular tolerance to set? The conservative maximum is
    # max_perturbation_pixels*2, if both stars are deflected away or toward each other, but that
    # results in some very large tolerances.
    angular_tolerance_deg = max(min_angular_tolerance_deg, 1.1 * fov_deg * (perturbation*2 / image_width))
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
    return (100.0 * ran['starid_num_images_correct'] / params.star_id_num_trials,
            100.0 * ran['starid_num_images_incorrect'] / params.star_id_num_trials)

num_algos = len(params.perturbation_star_id_algos)
for star_id_algo_info, availability_color, error_color in zip(params.perturbation_star_id_algos,
                                                              cm.Blues(np.linspace(.8,.4,num_algos)),
                                                              cm.Reds(np.linspace(.8,.4,num_algos))):
    with star_id_algo_info.db as db_path:
        results = [run_at_perturbation(star_id_algo_info.pipeline_params, db_path, pert) for pert in perturbation_levels]
        print(results)
        ax_availability.plot(perturbation_levels,
                             [r[0] for r in results],
                             label=star_id_algo_info.name,
                             color=availability_color,
                             marker='.')
        ax_error.plot(perturbation_levels,
                      [r[1] for r in results],
                      label=star_id_algo_info.name,
                      color=error_color,
                      marker='.')

ax_availability.set_title('Star-ID Availability vs Centroid Error')
ax_availability.set_xlabel('Centroid Error stddev (pixels)')

ax_availability.set_ylabel('Availability (%)')
ax_availability.set_ylim(bottom=0, top=100)
ax_availability.legend()

ax_error.set_ylabel('Error Rate (%)')
ax_error.set_ylim(bottom=0)
ax_error.legend()

plt.savefig(sys.argv[1])
