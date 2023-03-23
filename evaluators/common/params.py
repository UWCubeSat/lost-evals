# Most of the "configuration" for the evaluation is in this file

# Which algorithms to evaluate
centroid_algos = [
    'cog',
    # TODO: Add gaussian
]

star_id_algos = [
    'py',
    'gv',
    # 'tetra'
]

# We don't evaluate attitude algos against each other, so just specify which one to use for whole-pipeline evaluations
# TODO: check to see if there's any difference in the results between dqm and quest (shouldn't be anything that materially affects the results)
attitude_algo='quest'

centroid_base_args=[]
centroid_num_trials=20

# CENTROID MOTION BLUR TESTING PARAMS
centroid_blur_num_pts = 8
centroid_blur_max_exposure = 0.2
centroid_blur_base_args = centroid_base_args # TODO: I think the default args have some rotation, we
                                             # probably just want to have it not be rotation so that
                                             # all the stars have roughly the "same" blur
