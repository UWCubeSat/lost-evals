#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
from common.starid_helpers import evaluate_starid

fig, ax = plt.subplots()

perturbation_levels = np.linspace(0, params.perturbation_max_perturbation, num=params.perturbation_num_pts)

# TODO set fov in params?
fov_deg = 20
image_width = 1024
min_angular_tolerance_deg = 0.05

def lost_args_at_perturbation(perturbation):
    max_perturbation_pixels = math.sqrt(2 * (perturbation*2)**2)
    # TODO determine the most reasonable angular tolerance to set? The conservative maximum is
    # max_perturbation_pixels*2, if both stars are deflected away or toward each other, but that
    # results in some very large tolerances.
    angular_tolerance_deg = max(min_angular_tolerance_deg, 1.1 * fov_deg * (perturbation*2 / image_width))
    return ['--generate-perturb-centroids', perturbation,
            '--angular-tolerance', angular_tolerance_deg,
            '--centroid-compare-threshold', max_perturbation_pixels+0.5]

lost_special_paramss = list(map(lost_args_at_perturbation, perturbation_levels))

evaluate_starid(ax, lost_special_paramss, perturbation_levels)

ax.set_title('Star-ID Availability & Error Rate vs Centroid Error')
ax.set_xlabel('Centroid Error Stddev (pixels)')

plt.savefig(sys.argv[1])
