#!/usr/bin/env python3

import sys
import os
from common.scenarios import ScenarioConfig

scenarios_dir = sys.argv[1]
scenario_config = ScenarioConfig.from_dir(scenarios_dir)

for scenario in params.scenarios:
    # Create directory of scenario.machine_name
    scenario_dir = os.path.join(scenarios_dir, scenario.machine_name)
    os.makedirs(scenario_dir, exist_ok=True)
    # Remove all pngs currently in that dir
    for f in os.listdir(scenario_dir):
        if f.endswith(".png"):
            os.remove(os.path.join(scenario_dir, f))
    # Generate pngs
    scenario.generate_pngs(scenario_config)
