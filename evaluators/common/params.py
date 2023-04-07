# Most of the "configuration" for the evaluation is in this file
import common.runner as runner

class StarIdAlgoParams:
    def __init__(self, name, pipeline_params, db_params):
        self.name = name
        self.pipeline_params = pipeline_params
        self.db = runner.LostDatabase(db_params)

# Which algorithms to evaluate
basic_centroid_algos = [
    ('Center of Gravity', ['--centroid-algo=cog']),
    ('Iterative CoG', ['--centroid-algo=iwcog']),
    ('1D Gaussian Fit', ['--centroid-algo=lsgf1d']),
    ('2D Gaussian Fit', ['--centroid-algo=lsgf2d']),
    ('Gaussian Grid', ['--centroid-algo=ggrid']),
]

# We don't evaluate attitude algos against each other, so just specify which one to use for whole-pipeline evaluations
# TODO: check to see if there's any difference in the results between dqm and quest (shouldn't be anything that materially affects the results)
attitude_algo='quest'

database_catalog_params = ['--max-stars', 5000,
                           '--min-separation', 0.5]
database_kvector_params = ['--kvector',
                           '--kvector-min-distance', 0.5,
                           '--kvector-max-distance', 10,
                           '--kvector-distance-bins', 10000]
database_tetra_params = ['--tetra', '--min-separation=0.0']

basic_star_id_algos = [
    StarIdAlgoParams('Pyramid', ['--star-id-algo=py'], database_catalog_params + database_kvector_params),
    StarIdAlgoParams('Tetra', ['--star-id-algo=tetra'], database_catalog_params + database_tetra_params),
]

centroid_base_args = ['--generate-zero-mag-photons=20000',
                      '--generate-saturation-photons=50',
                      '--centroid-filter-brightest=5']
centroid_num_trials = 3

star_id_num_trials = 100

# CENTROID MOTION BLUR TESTING PARAMS
centroid_blur_num_pts = 10
centroid_blur_base_args = centroid_base_args + ['--generate-saturation-photons=20']

centroid_blur_algos = basic_centroid_algos

# CENTROID READ NOISE PARAMS
centroid_noise_max_noise = 0.1 # 5*.1 + 0.25 = 0.75, hopefully some stars will still be brighter than that.
centroid_noise_num_pts = 10
centroid_noise_base_args = centroid_base_args + ['--generate-dark-current', 0.25]

centroid_noise_algos = basic_centroid_algos

# CENTROID SHOT NOISE PARAMS
centroid_exposure_base_args = centroid_base_args
# To effectively vary sensitivity, we need to adjust the zero magnitude photoelectrons
# proportionally with the saturation photons. This way, the effective brightness of the stars stays
# the same, and we only are effectively editing the shot noise. We'll use an exposure of 1.0 for
# simplicity.
centroid_exposure_zero_mag_photoelectrons = 20000
# This one is scaled with exposure, from 1.0:
centroid_exposure_saturation_photoelectrons_at_exposure_1 = 200
centroid_exposure_min_exposure = 0.1
centroid_exposure_max_exposure = 1.0
centroid_exposure_num_pts = 10
centroid_exposure_algos = basic_centroid_algos

# PERTURBATION VS SKY COVERAGE PARAMS
perturbation_max_perturbation = 2
perturbation_num_perturbations = 5
perturbation_base_args = []

perturbation_star_id_algos = basic_star_id_algos

# FALSE STARS VS SKY COVERAGE PARAMS
false_max_false_stars = 4000
false_num_false_star_levels = 10
false_base_args = []

false_star_id_algos = basic_star_id_algos
