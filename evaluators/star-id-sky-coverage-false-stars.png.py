#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

false_star_levels = np.linspace(0, params.false_max_false_stars, num=params.false_num_false_star_levels)

def run_at_false_stars(algo, db_path, num_false_stars):
    ran = runner.run_lost(['--generate', params.false_num_trials,
                           '--generate-centroids-only', 'true',
                           '--generate-random-attitudes', 'true',
                           '--generate-false-stars', num_false_stars]
                          # TODO: handle false star magnitude when we start testing Tetra
                          + params.false_base_args
                          + ['--star-id-algo', algo,
                             '--database', db_path,
                             '--compare-star-ids', '-'])
    return ran['starid_num_images_correct'] / params.false_num_trials

for algo_name, algo_code in params.star_id_algos:
    with runner.LostDatabase(params.star_id_db_params[algo_code]) as db_path:
        # TODO: also plot error rate?
        ax.plot(false_star_levels,
                [run_at_false_stars(algo_code, db_path, false_star_level) for false_star_level in false_star_levels],
                label=algo_name,
                marker='.')

ax.set_title('Star-ID Sky Coverage vs False Stars')
ax.set_xlabel('Number of False Stars')
ax.set_ylabel('Sky Coverage (%)')
ax.legend()

plt.savefig(sys.argv[1])

