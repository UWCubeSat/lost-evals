import math

import common.runner as runner
import common.params as params

def evaluate_centroid(ax, special_paramss, x_vals):
    for algo_name, algo_params in params.centroid_algos:
        y_vals = []
        for special_params in special_paramss:
            ran = runner.run_lost(['--generate', params.centroid_num_trials,
                                   '--generate-random-attitudes=true',
                                   '--compare-centroids=-']
                                  + params.centroid_base_args
                                  + algo_params
                                  + special_params)
            if 'centroids_mean_error' in ran:
                y_vals.append(ran['centroids_mean_error'])
            else:
                print('WARNING! No centroids detected!')
                y_vals.append(math.nan)
        ax.plot(x_vals, y_vals,
                label=algo_name,
                marker='.')

    ax.set_ylabel('Centroid Error (pixels, average)')
    ax.legend()
