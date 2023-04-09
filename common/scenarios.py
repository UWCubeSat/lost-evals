from dataclasses import dataclass
import os
import pickle
import numpy as np
import quaternion

import common.runner as runner

@dataclass
class Scenario:
    """A scenario used in the comprehensive test"""
    human_name: str
    machine_name: str
    generate_params: [str]
    lost_params: [str]
    lost_database_params: [str]
    lost_centroid_function_name: str
    lost_starid_function_name: str

    def image_paths(self, num_pngs, scenarios_dir):
        """Return a list of paths, one for each generated image"""
        return [os.path.join(scenarios_dir, self.machine_name, 'images', str(i) + '.png') for i in range(num_pngs)]

    def generate_pngs(self, num_pngs, scenarios_dir):
        print(f"Generating {num_pngs} PNGs for {self.human_name} scenario")
        # Remove all the old pngs from the folder
        images_folder = os.path.join(scenarios_dir, self.machine_name, 'images')
        os.makedirs(images_folder, exist_ok=True)
        for f in os.listdir(images_folder):
            if f.endswith('.png'):
                os.remove(os.path.join(images_folder, f))

        expected_attitudes = []
        for i in range(num_pngs):
            seed = i + 123123123
            run_results = runner.run_lost(self.generate_params +
                                          ['--generate=1',
                                           '--generate-random-attitude=1',
                                           '--generate-seed', seed,
                                           '--plot-raw-input', os.path.join(scenarios_dir, self.machine_name, 'images', str(i) + '.png'),
                                           '--print-expected-attitude=-'])
            expected_attitudes.append(np.quaternion(run_results['expected_attitude_real'],
                                                    run_results['expected_attitude_i'],
                                                    run_results['expected_attitude_j'],
                                                    run_results['expected_attitude_k']))
        with open(os.path.join(scenarios_dir, self.machine_name, 'expected-attitudes.pkl'), 'wb') as f:
            pickle.dump(expected_attitudes, f)

    def read_expected_attitudes(self, scenarios_dir):
        with open(os.path.join(scenarios_dir, self.machine_name, 'expected-attitudes.pkl'), 'rb') as f:
            expected_attitudes = pickle.load(f)
        return expected_attitudes

    # Each of the following "run" functions returns a dictionary of things we might want to include in the final table, but not certainly.

    # def run_against_lost_callgrind(self, scenarios_dir):
    #     print(f"Running {self.human_name} scenario with Callgrind against LOST")
    #     centroid_cycles = []
    #     starid_cycles = []
    #     for i in range(params.comprehensive_num_pngs):
    #         callgrind_result = runner.run_callgrind_on_lost(self.lost_params +
    #                                                         ['--png', os.path.join(scenarios_dir, self.machine_name, 'images', str(i) + '.png')])
    #         centroid_cycles.append(callgrind_result[self.lost_centroid_function_name])
    #         starid_cycles.append(callgrind_result[self.lost_starid_function_name])
    #     centroid_avg_cycles = np.mean(centroid_cycles)
    #     starid_avg_cycles = np.mean(starid_cycles)
    #     return {
    #         'lost_centroid_avg_cycles': centroid_avg_cycles,
    #         'lost_starid_avg_cycles': starid_avg_cycles,
    #     }

    # def run_against_openstartracker(self, scenarios_dir):
    #     print(f"Running {self.human_name} scenario against OpenStarTracker")
    #     print('Calibrating OpenStarTracker...')
    #     # Create a folder for the calibration images
    #     calibration_images_dir = os.path.join(scenarios_dir, self.machine_name, 'ost-calibration-images')
    #     os.makedirs(calibration_images_dir, exist_ok=True)
    #     # Remove any existing calibration images
    #     for f in os.listdir(calibration_images_dir):
    #         os.remove(os.path.join(calibration_images_dir, f))
    #     # Hardlink images from the main scenario pngs folder into the calibration folder
    #     for i in range(params.comprehensive_num_ost_calibrations):
    #         os.link(os.path.join(scenarios_dir, self.machine_name, 'images', str(i) + '.png'),
    #                 os.path.join(calibration_images_dir, str(i) + '.png'))
    #     # Run OpenStarTracker calibration
        
