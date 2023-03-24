# Most of the "configuration" for the evaluation is in this file

# Which algorithms to evaluate
centroid_algos = [
    ('Center of Gravity', 'cog'),
    # TODO: Add gaussian
]

star_id_algos = [
    ('Pyramid', 'py'),
    # ('Geometric Voting', 'gv'),
    # 'tetra'
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
star_id_db_params = {
    'py': database_catalog_params + database_kvector_params,
    'gv': database_catalog_params + database_kvector_params,
    # add tetra here
}

centroid_base_args=[]
centroid_num_trials=20

# CENTROID MOTION BLUR TESTING PARAMS
centroid_blur_num_pts = 8
centroid_blur_max_exposure = 0.2
centroid_blur_base_args = centroid_base_args # TODO: I think the default args have some rotation, we
                                             # probably just want to have it not be rotation so that
                                             # all the stars have roughly the "same" blur

# CENTROID READ NOISE PARAMS
centroid_noise_max_noise = 0.15
centroid_noise_num_pts = 10
centroid_noise_base_args = centroid_base_args + ['--generate-dark-current', 0.25]

# PERTURBATION VS SKY COVERAGE PARAMS
perturbation_max_perturbation = 2
perturbation_num_perturbations = 5
perturbation_num_trials = 10
perturbation_base_args = []

# FALSE STARS VS SKY COVERAGE PARAMS
false_max_false_stars = 4000
false_num_false_star_levels = 10
false_num_trials = 100
false_base_args = []
