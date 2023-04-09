#!/usr/bin/env python3

import sys
import os
import shutil

import common.runner as runner
import common.params as params
import common.util as util

scenarios_dir = sys.argv[1]

openstartracker_dir = util.get_openstartracker_dir()

for scenario in params.scenarios:
    print(f"Calibrating OpenStarTracker for {scenario.human_name}")
    # Create a folder for the calibration images
    testdir = os.path.join(scenarios_dir, scenario.machine_name, 'ost-testdir')

    # Remove the testdir
    shutil.rmtree(testdir, ignore_errors=True)

    calibration_images_dir = os.path.join(testdir, 'samples')
    os.makedirs(calibration_images_dir) # also creates the whole test dir if not exists
    os.makedirs(os.path.join(testdir, 'calibration_data'))

    # Hardlink images from the main scenario pngs folder into the calibration folder
    for i in range(params.comprehensive_num_ost_calibrations):
        os.link(os.path.join(scenarios_dir, scenario.machine_name, 'images', str(i) + '.png'),
                os.path.join(calibration_images_dir, str(i) + '.png'))

    # Run OpenStarTracker calibration
    runner.run_openstartracker_calibrate(openstartracker_dir, testdir)
