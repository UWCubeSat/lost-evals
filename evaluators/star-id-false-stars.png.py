#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import common.params as params
from common.starid_helpers import evaluate_starid

fig, ax = plt.subplots()

fov = np.radians(25)

false_star_levels = np.linspace(0, params.false_max_false_stars, num=params.false_num_false_star_levels)
# TODO look into spherical geometry to calculate this properly
false_star_levels_per_image = false_star_levels * fov*fov/(4*np.pi)
special_paramss = [['--generate-false-stars', num_false_stars] for num_false_stars in false_star_levels]

evaluate_starid(ax, params.false_star_id_algos, params.false_base_args, special_paramss, false_star_levels_per_image)

ax.set_title('Star-ID Availability & Error Rate vs False Stars')
ax.set_xlabel('Number of False Stars (per image, average)')
ax.set_xlim(left=0)

plt.savefig(sys.argv[1])

