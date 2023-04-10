#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params

from common.centroid_helpers import evaluate_centroid

fig, ax = plt.subplots()

blur_exposures = np.linspace(0.1, 1, num=params.centroid_blur_num_pts)
def blur_params_from_length(length):
    return ['--generate-blur-ra=.3',
            '--generate-blur-de=.15',
            '--generate-blur-roll=0',
            '--generate-exposure', length]
special_paramss = list(map(blur_params_from_length, blur_exposures))

evaluate_centroid(ax, special_paramss, blur_exposures)

ax.set_title('Centroid error vs Motion Blur')
ax.set_xlabel('Blur angle')

plt.savefig(sys.argv[1])
