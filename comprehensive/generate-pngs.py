#!/usr/bin/env python3

import sys
import os

import common.params as params

scenarios_dir = sys.argv[1]

for scenario in params.scenarios:
    # Create directory of scenario.machine_name
    scenario.generate_pngs(params.comprehensive_num_pngs, scenarios_dir)
