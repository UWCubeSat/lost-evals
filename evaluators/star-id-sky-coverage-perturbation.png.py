#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

perturbation_levels = np.linspace(0, params.perturbation_max_perturbation, num=params.perturbation_num_perturbations)

def run_at_perturbation(algo, db_path, perturbation):
    ran = runner.run_lost(['--generate', params.perturbation_num_trials,
                           '--generate-centroids-only', 'true',
                           '--generate-random-attitudes', 'true',
                           '--generate-perturb-centroids', perturbation,
                           # TODO: this threshold may be too generous, giving a higher identification rate than reality (but probably it's fine):
                           '--centroid-compare-threshold', perturbation*3+0.5]
                          + params.perturbation_base_args
                          + ['--star-id-algo', algo,
                             '--database', db_path,
                             '--compare-star-ids', '-'])
    # I have to admit, float division by default is nice
    return ran['starid_num_images_correct'] / params.perturbation_num_trials

for algo_name, algo_code in params.star_id_algos:
    with runner.LostDatabase(params.star_id_db_params[algo_code]) as db_path:
        ax.plot(perturbation_levels,
                [run_at_perturbation(algo_code, db_path, pert) for pert in perturbation_levels],
                label=algo_name,
                marker='.')

ax.set_title('Star-ID Sky Coverage vs Centroid Error')
ax.set_xlabel('Centroid Error stddev (pixels)')
ax.set_ylabel('Sky Coverage (%)')
ax.legend()

plt.savefig(sys.argv[1])
