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
