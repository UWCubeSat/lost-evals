#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
import common.runner as runner

fig, ax = plt.subplots()

false_star_levels = np.linspace(0, params.false_max_false_stars, num=params.false_num_false_star_levels)

def run_at_false_stars(pipeline_params, db_path, num_false_stars):
    ran = runner.run_lost(['--generate', params.star_id_num_trials,
                           '--generate-centroids-only', 'true',
                           '--generate-random-attitudes', 'true',
                           '--generate-false-stars', num_false_stars]
                          # TODO: handle false star magnitude when we start testing Tetra
                          + params.false_base_args
                          + pipeline_params
                          + ['--database', db_path,
                             '--compare-star-ids', '-'])
    return 100 * ran['starid_num_images_correct'] / params.star_id_num_trials

for star_id_algo_info in params.false_star_id_algos:
    with star_id_algo_info.db as db_path:
        # TODO: also plot error rate?
        ax.plot(false_star_levels,
                [run_at_false_stars(star_id_algo_info.pipeline_params, db_path, false_star_level) for false_star_level in false_star_levels],
                label=star_id_algo_info.name,
                marker='.')

ax.set_title('Star-ID Sky Coverage vs False Stars')
ax.set_xlabel('Number of False Stars')
ax.set_ylabel('Sky Coverage (%)')
ax.legend()

plt.savefig(sys.argv[1])

