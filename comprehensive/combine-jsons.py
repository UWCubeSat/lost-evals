#!/usr/bin/env python3

import pandas
import sys
import os

import common.params as params

output_file = sys.argv[1]
json_dir = sys.argv[2]

# Read all the JSONs and combine
# The first level of key is the machine name of the scenario, the second level is the machine column name
dfs = []
for json_file in os.listdir(json_dir):
    if json_file.endswith('json'):
        dfs.append(pandas.read_json(os.path.join(json_dir, json_file), orient='index'))

# the "0" axis is indices, so would stack the tables vertically. We want to stack side-by-side.
# Whatever axis you choose as the primary one gets no "folding" or "joining". All the data is concatenated. The "joining" only happens on other axes. The `merge()` function can do a full merge, but then you can only merge pairwise, and we don't want jsons to have duplicate columns anyway.
# Merge, concat, and join seem like they all could have been one function with the right parameters...instead we have three, and all with differently named arguments.
# verify_integrity makes sure we don't get duplicate column names (though, surprisingly, further operations still seem to work when columns get duplicated?)
combined_df = pandas.concat(dfs, axis=1, join='outer', verify_integrity=True)
column_name_map = params.comprehensive_columns
index_name_map = dict([(s.machine_name, s.human_name) for s in params.scenarios])
combined_df = combined_df[column_name_map.keys()].rename(columns=column_name_map, index=index_name_map)

combined_df.to_csv(output_file, index=True, index_label='Scenario')
