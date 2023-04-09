#!/usr/bin/env python3

import sys
import json
import numpy as np

import common.runner as runner
import common.params as params

out_file = sys.argv[1]
scenarios_dir = sys.argv[2]

result = {}
for scenario in params.scenarios:
    print(f"Running {scenario.human_name} in Callgrind")

    centroid_instrss = []
    starid_instrss = []
    with runner.LostDatabase(scenario.lost_database_params) as db:
        for img_path in scenario.image_paths(params.comprehensive_num_callgrinds, scenarios_dir):
            callgrind_results = runner.run_callgrind_on_lost(scenario.lost_params +
                                                             ['--png', img_path,
                                                              '--database', db])
            centroid_instrss.append(callgrind_results[scenario.lost_centroid_function_name])
            starid_instrss.append(callgrind_results[scenario.lost_starid_function_name])

    centroid_avg_instrs = int(np.mean(centroid_instrss))
    starid_avg_instrs = int(np.mean(starid_instrss))
    result[scenario.machine_name] = {
        'lost_centroid_avg_instrs': centroid_avg_instrs,
        'lost_starid_avg_instrs': starid_avg_instrs,
        'lost_total_avg_instrs': centroid_avg_instrs+starid_avg_instrs,
    }
    
with open(out_file, 'w') as f:
    json.dump(result, f, indent=4)
