import numpy as np
import matplotlib.cm as cm
import common.runner as runner
import common.params as params

def evaluate_starid(axes, special_paramss, x_vals):
    """axes is some matplotlib axes. star_id_algos list of starid info objects. Base params are params for every run. Special params is a 2-nested list, with the inner ones being the options for each test case. x_vals is the same length as special_params, the stuff plotted along the bottom"""
    ax_availability = axes
    ax_error = ax_availability.twinx()

    num_algos = len(params.star_id_algos)
    for star_id_algo_info, availability_color, error_color \
        in zip(params.star_id_algos,
               cm.Blues(np.linspace(.8,.4,num_algos)),
               cm.Reds(np.linspace(.8,.4,num_algos))):

        with star_id_algo_info.db as db_path:
            availabilities = []
            error_rates = []
            for special_params in special_paramss:
                ran = runner.run_lost(['--generate', params.star_id_num_trials,
                                       '--generate-centroids-only=true',
                                       '--generate-random-attitudes=true',
                                       '--database', db_path,
                                       '--compare-star-ids=-']
                                      + star_id_algo_info.pipeline_params
                                      + params.starid_base_args
                                      + special_params)
                availabilities.append(100.0 * ran['starid_num_images_correct'] / params.star_id_num_trials)
                error_rates.append(100.0 * ran['starid_num_images_incorrect'] / params.star_id_num_trials)

            ax_availability.plot(x_vals,
                                 availabilities,
                                 label=star_id_algo_info.name,
                                 color=availability_color,
                                 marker='.')
            ax_error.plot(x_vals,
                          error_rates,
                          label=star_id_algo_info.name,
                          color=error_color,
                          marker='.')

    ax_availability.set_ylabel('Availability (%)')
    ax_availability.set_ylim(bottom=0, top=100)
    ax_availability.legend(title='Availability',
                           loc='upper left')

    ax_error.set_ylabel('Error Rate (%)')
    # Ensure there's lots of empty space above the error
    ymin, ymax = ax_error.get_ybound()
    ax_error.set_ylim(bottom=0, top=min(100, max(ymax*3, 5.0)))
    ax_error.set_ylim(bottom=0)
    ax_error.legend(title='Error Rate',
                    loc='upper right')

        
