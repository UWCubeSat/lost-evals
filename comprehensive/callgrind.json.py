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
    centroid_memorys = []
    starid_memorys = []
    with runner.LostDatabase(scenario.lost_database_params) as db:
        for img_path in scenario.image_paths(params.comprehensive_num_callgrinds, scenarios_dir):
            all_params = scenario.lost_params + ['--png', img_path, '--database', db]

            callgrind_results = runner.run_callgrind_on_lost(all_params)
            centroid_instrss.append(callgrind_results[scenario.lost_centroid_function_name])
            # sometimes will be zero, because there weren't enough stars in the image.
            starid_instrss.append(callgrind_results.get(scenario.lost_starid_function_name, 0))

            massif_results = runner.run_massif_on_lost(all_params)
            centroid_memorys.append(massif_results[scenario.lost_centroid_function_name])
            starid_memorys.append(massif_results.get(scenario.lost_starid_function_name, 0))

    centroid_avg_instrs = int(np.mean(centroid_instrss))
    starid_avg_instrs = int(np.mean(starid_instrss))
    centroid_avg_memory_kib = int(np.mean(centroid_memorys)) // 1024
    starid_avg_memory_kib = int(np.mean(starid_memorys)) // 1024
    result[scenario.machine_name] = {
        'lost_centroid_avg_instrs': centroid_avg_instrs,
        'lost_starid_avg_instrs': starid_avg_instrs,
        'lost_total_avg_instrs': centroid_avg_instrs+starid_avg_instrs,
        'lost_centroid_avg_memory_kib': centroid_avg_memory_kib,
        'lost_starid_avg_memory_kib': starid_avg_memory_kib,
    }
    
with open(out_file, 'w') as f:
    json.dump(result, f, indent=4)
