# Most of the "configuration" for the evaluation is in this file
import math

import common.runner as runner
from common.scenarios import Scenario, TetraParams

class StarIdAlgoParams:
    def __init__(self, name, pipeline_params, db_params):
        self.name = name
        self.pipeline_params = pipeline_params
        self.db = runner.LostDatabase(db_params)

# Which algorithms to evaluate
centroid_algos = [
    ('Center of Gravity', ['--centroid-algo=cog']),
    ('Iterative CoG', ['--centroid-algo=iwcog']),
    ('1D Gaussian Fit', ['--centroid-algo=lsgf1d']),
    ('2D Gaussian Fit', ['--centroid-algo=lsgf2d', '--centroid-fit-radius=3']),
    ('Gaussian Grid', ['--centroid-algo=ggrid', '--centroid-fit-radius=3']),
]

database_catalog_params = ['--max-stars', 5000,
                           '--min-separation', 0.5]
database_kvector_params = ['--kvector',
                           '--kvector-min-distance', 0.5,
                           '--kvector-max-distance', 10,
                           '--kvector-distance-bins', 10000]
database_tetra_params = ['--tetra', '--min-separation=0.0']

star_id_algos = [
    StarIdAlgoParams('Pyramid', ['--star-id-algo=py'], database_catalog_params + database_kvector_params),
    StarIdAlgoParams('Tetra', ['--star-id-algo=tetra'], database_catalog_params + database_tetra_params),
]

centroid_base_args = ['--fov=25',
                      '--generate-zero-mag-photons=20000',
                      '--generate-exposure=0.2',
                      '--generate-saturation-photons=50',
                      '--generate-read-noise=0.04', # 2/50
                      '--generate-dark-current=0.2',
                      '--centroid-filter-brightest=5']
centroid_num_trials = 100

starid_base_args = [
    '--fov=25',
    '--generate-cutoff-mag=5',
    '--generate-perturb-centroids=0.3',
    '--generate-false-stars=100',
]
star_id_num_trials = 1000

# CENTROID MOTION BLUR TESTING PARAMS
centroid_blur_num_pts = 10
centroid_blur_base_args = centroid_base_args + ['--generate-saturation-photons=20']

# CENTROID READ NOISE PARAMS
centroid_noise_max_noise = 0.1 # 5*.1 + 0.25 = 0.75, hopefully some stars will still be brighter than that.
centroid_noise_num_pts = 10
centroid_noise_base_args = centroid_base_args

# CENTROID SHOT NOISE PARAMS
centroid_shot_noise_base_args = centroid_base_args
# To effectively vary sensitivity, we need to adjust the zero magnitude photoelectrons
# proportionally with the saturation photons. This way, the effective brightness of the stars stays
# the same, and we only are effectively editing the shot noise. We'll use an exposure of 1.0 for
# simplicity.
centroid_shot_noise_min_photoelectrons = 2000
centroid_shot_noise_max_photoelectrons = 20000
centroid_shot_noise_photoelectron_sensitivity_ratio = 100
centroid_shot_noise_num_pts = 10

# PERTURBATION VS SKY COVERAGE PARAMS
perturbation_max_perturbation = 1.5
perturbation_num_pts = 10
perturbation_base_args = []

# FALSE STARS VS SKY COVERAGE PARAMS
false_max_false_stars = 700
false_num_false_star_levels = 10
false_base_args = []

# DIMMEST VISIBLE STAR
dimmest_brightest = 3
dimmest_dimmest = 6
dimmest_num_pts = 10





# COMPREHENSIVE

low_noise_params = [
    '--generate-cutoff-mag=5.0',
    '--generate-zero-mag-photons=20000',
    '--generate-saturation-photons=50',
    '--generate-exposure=0.2',
    '--generate-dark-current=0.25',
    '--generate-read-noise=0.02'
]

high_noise_params = [
    '--generate-false-stars=1000',
    '--generate-zero-mag-photons=10000',
    '--generate-saturation-photons=25',
    '--generate-blur-ra=0.3',
    '--generate-blur-de=0',
    '--generate-blur-roll=4',
    '--generate-exposure=0.2',
]

comprehensive_num_pngs = 100
comprehensive_num_callgrinds = comprehensive_num_pngs // 10 # to keep speed alright
comprehensive_num_ost_calibrations = comprehensive_num_pngs // 10
comprehensive_attitude_tolerance = math.radians(0.5)

comprehensive_columns = {
    'lost_desktop_total_avg_us': 'LOST Desktop Speed (μs)',
    # 'lost_raspi_total_speed': 'LOST Raspi Speed (μs)',
    'lost_total_avg_instrs': 'LOST CPU Instructions',
    # 'lost_max_memory': 'LOST Memory (KiB)',
    'lost_availability': 'LOST Availability (%)',
    'lost_error_rate': 'LOST Error Rate (%)',
    'lost_attitude_error_deg': 'LOST Attitude Error (deg)'

    # 'openstartracker_total_speed': 'OST Desktop Speed (μs)',
    # 'openstartracker_starid_speed': 'OST StarID Desktop Speed (μs)',
    # 'ost_availability': 'OST Availability (%)',
    # 'ost_error_rate': 'OST Error Rate (%)',

    # 'c_tetra_starid_speed': 'C-Tetra StarID Desktop Speed (μs)',
    # 'c_tetra_availability': 'C-TETRA Availability (%)',
    # 'c_tetra_error_rate': 'C-TETRA Error Rate (%)',
}

scenarios = [
    Scenario('20-deg FOV Low Noise', '20-low-noise',
             generate_params = ['--fov=20', '--centroid-algo=cog'] + low_noise_params,
             lost_database_params = ['--kvector',
                                     '--kvector-max-distance=15',
                                     '--min-mag=5.5'],
             lost_params = ['--fov=20',
                            '--centroid-algo=cog',
                            '--star-id-algo=py',
                            '--attitude-algo=dqm'],
             lost_centroid_function_name = 'lost::CenterOfGravityAlgorithm::Go',
             lost_starid_function_name = 'lost::PyramidStarIdAlgorithm::Go',
             tetra_params = TetraParams('tetra_pattern_catalog_20_5.0', 'stars_5.0',
                                        0.494, 132717936, 1560),
             )
    # Scenario('20-deg FOV High Noise', '20-high-noise',
    #          ['--fov=20'] + high_noise_params),
    # # Higher FOV gives more stars but worse centroid accuracy
    # Scenario('45-deg FOV Low Noise', '45-low-noise',
    #          ['--fov=45'] + low_noise_params),
    # Scenario('45-deg FOV High Noise', '20-high-noise',
    #          ['--fov=45'] + high_noise_params),
]
