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
