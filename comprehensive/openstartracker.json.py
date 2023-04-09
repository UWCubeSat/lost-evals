#!/usr/bin/env python3

import sys
import os
import shutil
import json
import numpy as np
import quaternion

import common.params as params
import common.runner as runner
import common.util as util

out_file = sys.argv[1]
scenarios_dir = sys.argv[2]

openstartracker_dir = util.get_openstartracker_dir()

result = {}
for scenario in params.scenarios:
    testdir = os.path.join(scenarios_dir, scenario.machine_name, 'ost-testdir')

    # Start the server
    proc = runner.start_openstartracker_server(openstartracker_dir, testdir)
    # Identify!
    actual_attitudes = []
    expected_attitudes = scenario.read_expected_attitudes(scenarios_dir)
    centroid_ss = []
    starid_ss = []
    total_ss = []
    for i in range(params.comprehensive_num_pngs):
        times, ra, de, roll = runner.solve_openstartracker(os.path.join(scenarios_dir, scenario.machine_name, 'images', str(i) + '.png'), proc)
        if ra is not None:
            assert de is not None and roll is not None
            print('Solved', ra, de, roll)
            print('Expected', expected_attitudes[i])
            actual_attitudes.append(util.quaternion_from_celestial_euler_angles(ra, de, roll))
        else:
            actual_attitudes.append(None)
        # centroid: time2
        centroid_ss.append(times[1])
        # starid: time5-time2
        starid_ss.append(times[4] - times[1])
        # total: time6
        total_ss.append(times[5])

    runner.stop_openstartracker(proc)

    centroid_avg_us = int(np.mean(centroid_ss) * 1e6)
    starid_avg_us = int(np.mean(starid_ss) * 1e6)
    total_avg_us = int(np.mean(total_ss) * 1e6)

    attitude_comparison = util.compare_attitudes(actual_attitudes, expected_attitudes)

    result[scenario.machine_name] = {
        'openstartracker_desktop_centroid_avg_us': centroid_avg_us,
        'openstartracker_desktop_starid_avg_us': starid_avg_us,
        'openstartracker_desktop_total_avg_us': total_avg_us,
        'openstartracker_attitude_error_deg': np.degrees(attitude_comparison['attitude_error']),
        'openstartracker_availability': attitude_comparison['availability'],
        'openstartracker_error_rate': attitude_comparison['error_rate'],
    }
    
with open(out_file, 'w') as f:
    json.dump(result, f, indent=4)
