#!/usr/bin/env python3

import sys
import os
import json
import csv
import numpy as np

import common.runner as runner
import common.params as params

out_file = sys.argv[1]
scenarios_dir = sys.argv[2]

# Read the BSC TSV from lost and create a map from BSC names to tetra ids
# The TSV is actually pipe separated |
# Each entry is a tuple ((x,y,z),name)
bsc_entries = []
with open('lost/bright-star-catalog.tsv') as bsc_file:
    bsc_reader = csv.reader(bsc_file, delimiter='|')
    for row in bsc_reader:
        ra = float(row[0])
        de = float(row[1])
        name = int(row[2])
        x = np.cos(np.radians(ra)) * np.cos(np.radians(de))
        y = np.sin(np.radians(ra)) * np.cos(np.radians(de))
        z = np.sin(np.radians(de))
        bsc_entries.append(((x,y,z),name))

# variables named the same way as in tetra's centroid_generation.py:
num_images = params.comprehensive_num_pngs
max_num_stars_per_image = 25 # If this is changed, Tetra.c must also be changed and recompiled

result = {}
for scenario in params.scenarios:
    print(f"Generating bsc->tetra map for scenario {scenario.human_name}", flush=True)
    num_tetra_star_vectors = scenario.tetra_params.num_stars
    tetra_stars_data_type = [("i", np.float64),("j", np.float64),("k", np.float64),("mag", np.float64),("id", np.uint32),("pad", np.uint32)]
    tetra_stars = np.memmap(scenario.tetra_params.stars_path, dtype=tetra_stars_data_type, mode='r', shape=(num_tetra_star_vectors,))

    bsc_to_tetra = {}
    max_bsc_to_tetra_dist = 5e-3 # unfortunately, it does seem like it needs to be this big in order
                                 # to work reliably. Not sure wth is going on here.
    # precalculate tetra vectors for speed
    tetra_unit_vectors = np.ndarray((num_tetra_star_vectors,3))
    for j in range(num_tetra_star_vectors):
        x, y, z, _, _, _ = tetra_stars[j]
        tetra_unit_vectors[j] = (x,y,z)

    bsc_unit_vectors = np.ndarray((len(bsc_entries),3))
    for i in range(len(bsc_entries)):
        bsc_unit_vectors[i] = bsc_entries[i][0]

    for i in range(len(bsc_entries)):
        # find the tetra entry nearest by euclidean distance
        distances = np.linalg.norm(tetra_unit_vectors - bsc_unit_vectors[i], axis=1)
        min_index = np.argmin(distances)
        min_distance = distances[min_index]
        if min_distance < max_bsc_to_tetra_dist:
            bsc_to_tetra[bsc_entries[i][1]] = min_index

    print(f"Running {scenario.human_name} C-Tetra", flush=True)
    output_centroids = scenario.read_output_centroids(scenarios_dir)

    c_tetra_dir = os.path.join(scenarios_dir, scenario.machine_name, 'c-tetra')
    os.makedirs(c_tetra_dir, exist_ok=True)

    # no expected centroids here, tetra will check for us!
    input_data_p_path = os.path.join(c_tetra_dir, 'input_data.p')
    centroid_data_p_path = os.path.join(c_tetra_dir, 'centroid_data.p')
    # it's almost certainly possible to just map this as a 2d array but i don't want to jinx it
    image_data = np.memmap(input_data_p_path, dtype=np.uint16, mode='w+', shape=(max_num_stars_per_image * num_images))
    centroid_data = np.memmap(centroid_data_p_path, dtype=np.float32, mode='w+', shape=(max_num_stars_per_image * num_images, 2))

    for i in range(num_images):
        # if there are too many images, only use the first max_num_stars_per_image
        num_centroids = min(len(output_centroids[i]), max_num_stars_per_image)
        for j in range(num_centroids):
            x, y, name = output_centroids[i][j]
            # Is this the only way to assign a tuple to a numpy array in Python? I'm not gonna f around and find out
            centroid_data[i * max_num_stars_per_image + j][0] = x-512
            centroid_data[i * max_num_stars_per_image + j][1] = 512-y # hardcode alert! hardcode alert!
            if name is not None:
                if name in bsc_to_tetra:
                    image_data[i * max_num_stars_per_image + j] = bsc_to_tetra[name]
                else:
                    pass
                    # print('Warning: BSC name %d not found in tetra star catalog' % name)

    # Now run it
    tetra_results = runner.run_c_tetra(scenario.tetra_params, num_images, centroid_data_p_path, input_data_p_path)

    avg_runtime_us = tetra_results['ms taken'] / num_images * 1000
    availability = tetra_results['number right'] / num_images
    error_rate = (tetra_results['num wrngordr'] + tetra_results['number wrong']) / num_images

    result[scenario.machine_name] = {
        'c_tetra_starid_avg_us': avg_runtime_us,
        'c_tetra_availability': availability,
        'c_tetra_error_rate': error_rate,
    }

with open(out_file, 'w') as f:
    json.dump(result, f, indent=4)
