#!/usr/bin/env python3

import common.params as params
import common.runner as runner
import csv
import sys

out_writer = csv.DictWriter(open(sys.argv[1], 'w'), fieldnames=['scenario', 'centroiding_ns', 'star_id_ns', 'centroiding_cycles', 'star_id_cycles'])
out_writer.writeheader()

# lost_args should NOT include --generate
def run_scenario(scenario_name, centroid_fn_name, star_id_fn_name, lost_args):
    # First run it natively
    lost_output = runner.run_lost(['--generate=10', '--print-speed=-'] + lost_args)
    # Now run it in callgrind
    try:
        cg_output = runner.run_callgrind_on_lost(['--generate=1'] + lost_args)
    except:
        print('Callgrind failed for scenario: ' + scenario_name)
        print('Most likely you forgot to disable ASAN. Re-run `make clean` then `CXXFLAGS=-O3 make LOST_DISABLE_ASAN=1`')
        exit(1)
    out_writer.writerow({
        'scenario': scenario_name,
        'centroiding_ns': lost_output['centroiding_average_ns'],
        'star_id_ns': lost_output['starid_average_ns'],
        'centroiding_cycles': cg_output[centroid_fn_name],
        'star_id_cycles': cg_output[star_id_fn_name]
    })

with runner.LostDatabase(['--kvector', '--min-mag=5', '--kvector-max-distance=12', '--kvector-min-distance=0.5']) as db15: # db for 15 fov, see
    with runner.LostDatabase(['--kvector', '--min-mag=5', '--kvector-max-distance=30', '--kvector-min-distance=0.5']) as db45: # db for 45 fov
        run_scenario('15 fov low noise', 'lost::CenterOfGravityAlgorithm::Go', 'lost::PyramidStarIdAlgorithm::Go',
                     ['--fov=15', '--generate-read-noise=0.05', '--generate-reference-brightness=40', '--generate-false-stars=100',
                      '--centroid-algo=cog', '--star-id-algo=py', '--database', db15])

