#!/usr/bin/env python3

import sys
import os
import json
import numpy as np
import quaternion

import common.params as params
import common.runner as runner
import common.util as util

output_file = os.path.abspath(sys.argv[1])
scenarios_dir = os.path.abspath(sys.argv[2])

result = {}
for scenario in params.scenarios:
    print(f"Running {scenario.human_name} scenario against LOST")
    actual_attitudes = []
    centroid_nss = []
    starid_nss = []
    total_nss = []
    with runner.LostDatabase(scenario.lost_database_params) as db:
        for img_path in scenario.image_paths(params.comprehensive_num_pngs, scenarios_dir):
            run_results = runner.run_lost(scenario.lost_params +
                                        ['--png', img_path,
                                         '--database', db,
                                         '--print-speed=-',
                                         '--print-attitude=-'])

            assert run_results['attitude_known'] == 0 or run_results['attitude_known'] == 1
            attitude_known = run_results['attitude_known'] == 1
            if attitude_known:
                actual_attitudes.append(np.quaternion(run_results['attitude_real'],
                                                      run_results['attitude_i'],
                                                      run_results['attitude_j'],
                                                      run_results['attitude_k']))
            else:
                actual_attitudes.append(None)

            centroid_nss.append(run_results['centroiding_average_ns'])
            starid_nss.append(run_results['starid_average_ns'])
            total_nss.append(run_results['total_average_ns'])

        centroid_avg_us = np.mean(centroid_nss) // 1000
        starid_avg_us = np.mean(starid_nss) // 1000
        total_avg_us = np.mean(total_nss) // 1000
        attitude_comparison = util.compare_attitudes(actual_attitudes, scenario.read_expected_attitudes(scenarios_dir))
        result[scenario.machine_name] = {
            'lost_desktop_centroid_avg_us': centroid_avg_us,
            'lost_desktop_starid_avg_us': starid_avg_us,
            'lost_desktop_total_avg_us': total_avg_us,
            'lost_attitude_error_deg': np.degrees(attitude_comparison['attitude_error']),
            'lost_error_rate': attitude_comparison['error_rate'] * 100,
            'lost_availability': attitude_comparison['availability'] * 100,
            'lost_database_size': os.path.getsize(db),
        }

with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)
