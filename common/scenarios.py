from dataclasses import dataclass
import os
import pickle
import numpy as np
import quaternion

import common.runner as runner

@dataclass
class TetraParams:
    pattern_catalog_path: str
    stars_path: str
    max_fov: float
    num_catalog_patterns: int
    num_stars: int

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

    tetra_params: TetraParams

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
        output_centroids = [] # [[(x,y,id_name)]], inner array is centroids per image. id_name may be None
        for i in range(num_pngs):
            seed = i + 123123123
            run_results = runner.run_lost(self.generate_params +
                                          ['--generate=1',
                                           '--generate-random-attitude=1',
                                           '--generate-seed', seed,
                                           '--plot-raw-input', os.path.join(scenarios_dir, self.machine_name, 'images', str(i) + '.png'),
                                           '--print-expected-attitude=-',
                                           '--print-actual-centroids=-'])
            expected_attitudes.append(np.quaternion(run_results['expected_attitude_real'],
                                                    run_results['expected_attitude_i'],
                                                    run_results['expected_attitude_j'],
                                                    run_results['expected_attitude_k']))
            cur_centroids = []
            for i in range(run_results['num_actual_centroids']):
                cur_centroids.append((run_results[f'actual_centroid_{i}_x'],
                                      run_results[f'actual_centroid_{i}_y'],
                                      # .get defaults to None but we specify it explicitly here because it's my first time using it and I feel like copilot is going to destroy my brain cells
                                      run_results.get(f'input_centroid_{i}_id', None)))
            output_centroids.append(cur_centroids)

        with open(os.path.join(scenarios_dir, self.machine_name, 'expected-attitudes.pkl'), 'wb') as f:
            pickle.dump(expected_attitudes, f)
        with open(os.path.join(scenarios_dir, self.machine_name, 'output-centroids.pkl'), 'wb') as f:
            pickle.dump(output_centroids, f)

    def read_expected_attitudes(self, scenarios_dir):
        with open(os.path.join(scenarios_dir, self.machine_name, 'expected-attitudes.pkl'), 'rb') as f:
            return pickle.load(f)

    def read_output_centroids(self, scenarios_dir):
        with open(os.path.join(scenarios_dir, self.machine_name, 'output-centroids.pkl'), 'rb') as f:
            return pickle.load(f)
