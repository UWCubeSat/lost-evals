#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params

from common.centroid_helpers import evaluate_centroid

fig, ax = plt.subplots()

photoelectrons = np.linspace(params.centroid_shot_noise_min_photoelectrons, params.centroid_shot_noise_max_photoelectrons,
                             num=params.centroid_shot_noise_num_pts)
def params_at_photoelectrons(pes):
    saturation_photons = pes / params.centroid_shot_noise_photoelectron_sensitivity_ratio
    return ['--generate-zero-mag-photons', pes,
            '--generate-saturation-photons', saturation_photons,
            '--generate-exposure=1']
special_paramss = list(map(params_at_photoelectrons, photoelectrons))

evaluate_centroid(ax, special_paramss, photoelectrons)

ax.set_title('Centroid Error vs Photoelectrons (constant effective brightness)')
ax.set_xlabel('Photoelectrons for Zero-Magnitude Star')

plt.savefig(sys.argv[1])
