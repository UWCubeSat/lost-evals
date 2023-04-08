from dataclasses import dataclass
import os
import pickle
import numpy as np
import quaternion

import common.runner as runner
import common.params as params

def compare_attitudes(actual, expected):
    """Return dict with availability, error rate, and average error for each correctly identified. It is important to pass arguments in the correct order, because expected shouldn't have any Nones in it, but actual can."""
    assert len(actual) == len(expected)
    actual = np.array(actual)
    expected = np.array(expected)
    available_booleans = np.array([a is not None for a in actual])
    actual_available = actual[available_booleans]
    expected_available = expected[available_booleans]
    all_angle_errors = (actual_available*expected_available.conjugate()).normalized().angle()
    correct_angle_booleans = all_angle_errors < params.comprehensive_attitude_tolerance
    availability = correct_angle_booleans.sum() / len(actual)
    error_rate = (len(correct_angle_booleans) - correct_angle_booleans.sum()) / len(actual)
    correct_error = all_angle_errors[correct_angle_booleans].mean()
    return {
        'availability': availability,
        'error_rate': error_rate,
        'attitude_error': correct_error,
    }

@dataclass
class Scenario:
    """A scenario used in the comprehensive test"""
    human_name: str
    machine_name: str
    generate_params: [str]
    lost_params: [str]
    lost_centroid_function_name: str
    lost_starid_function_name: str

    def generate_pngs(self, config):
        print(f"Generating {num_pngs} PNGs for {self.human_name} scenario")
        expected_attitudes = []
        for i in range(config.num_pngs):
            seed = i + 123123123
            run_results = runner.run_lost(self.generate_params +
                                          ['--generate=1',
                                           '--generate-random-attitude=1',
                                           '--generate-seed', seed,
                                           '--plot-raw-input', os.path.join(config.scenarios_dir, self.machine_name, 'images', str(i) + '.png'),
                                           '--print-expected-attitude=-'])
            expected_attitudes.append((run_results['expected_attitude_real'],
                                       run_results['expected_attitude_i'],
                                       run_results['expected_attitude_j'],
                                       run_results['expected_attitude_k']))
        with open(os.path.join(config.scenarios_dir, self.machine_name, 'expected-attitudes.pkl'), 'wb') as f:
            pickle.dump(expected_attitudes, f)

    def read_expected_attitudes(self, config):
        with open(os.path.join(config.scenarios_dir, self.machine_name, 'expected-attitudes.pkl'), 'rb') as f:
            expected_attitudes = pickle.load(f)
        return expected_attitudes

    # Each of the following "run" functions returns a dictionary of things we might want to include in the final table, but not certainly.

    def run_against_lost(self, scenarios_dir):
        print(f"Running {self.human_name} scenario against LOST")
        actual_attitudes = []
        starid_nss = []
        total_nss = []
        for i in range(params.comprehensive_num_pngs):
            run_results = runner.run_lost(self.lost_params +
                                          ['--png', os.path.join(scenarios_dir, self.machine_name, 'images', str(i) + '.png'),
                                           '--print-attitude=-'])

            attitude_available = run_results['attitude_available']
            if attitude_available:
                actual_quaternion = np.quaternion(run_results['attitude_real'],
                                                  run_results['attitude_i'],
                                                  run_results['attitude_j'],
                                                  run_results['attitude_k'])
                actual_attitudes.append(actual_quaternion)
            else:
                actual_attitudes.append(None)

            centroid_avg_nss.append(run_results['centroiding_avg_ns'])
            starid_nss.append(run_results['starid_avg_ns'])
            total_nss.append(run_results['total_avg_ns'])

        centroid_avg_ns = np.mean(centroid_avg_nss)
        starid_avg_ns = np.mean(starid_nss)
        attitude_comparison = compare_attitudes(actual_attitudes, self.read_expected_attitudes(scenarios_dir))
        return {
            'lost_centroid_avg_ns': centroid_avg_ns,
            'lost_starid_avg_ns': starid_avg_ns,
            'lost_attitude_error': attitude_comparison['attitude_error'],
            'lost_attitude_error_rate': attitude_comparison['error_rate'],
            'lost_attitude_availability': attitude_comparison['availability'],
        }

            
    def run_against_lost_callgrind(self, scenarios_dir):
        print(f"Running {self.human_name} scenario with Callgrind against LOST")
        centroid_cycles = []
        starid_cycles = []
        for i in range(params.comprehensive_num_pngs):
            callgrind_result = runner.run_callgrind_on_lost(self.lost_params +
                                                            ['--png', os.path.join(scenarios_dir, self.machine_name, 'images', str(i) + '.png')])
            centroid_cycles.append(callgrind_result[self.lost_centroid_function_name])
            starid_cycles.append(callgrind_result[self.lost_starid_function_name])
        centroid_avg_cycles = np.mean(centroid_cycles)
        starid_avg_cycles = np.mean(starid_cycles)
        return {
            'lost_centroid_avg_cycles': centroid_avg_cycles,
            'lost_starid_avg_cycles': starid_avg_cycles,
        }

    def run_against_openstartracker(self, scenarios_dir):
        print(f"Running {self.human_name} scenario against OpenStarTracker")
        print('Calibrating OpenStarTracker...')
        # Create a folder for the calibration images
        calibration_images_dir = os.path.join(scenarios_dir, self.machine_name, 'ost-calibration-images')
        os.makedirs(calibration_images_dir, exist_ok=True)
        # Remove any existing calibration images
        for f in os.listdir(calibration_images_dir):
            os.remove(os.path.join(calibration_images_dir, f))
        # Hardlink images from the main scenario pngs folder into the calibration folder
        for i in range(params.comprehensive_num_ost_calibrations):
            os.link(os.path.join(scenarios_dir, self.machine_name, 'images', str(i) + '.png'),
                    os.path.join(calibration_images_dir, str(i) + '.png'))
        # Run OpenStarTracker calibration
        
