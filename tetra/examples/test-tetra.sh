#!/usr/bin/env bash

# tmp_dir=$(mktemp -d)
tmp_dir="temp"

cd ..

mkdir "$tmp_dir"

# cd "$tmp_dir"
cd "examples"

# params: low and hi
function rand_int {
  lo=$1
  hi=$2
  echo $((lo + (RANDOM % (hi - lo + 1))))
}

# CHANGE THIS
n=5

echo "$PWD"

for _ in $(seq "${1:-$n}"); do

  ra=$(rand_int 0 359)
  # Ok I'm kinda cheating here with DEC, but I'm also too lazy to deal with negative numbers... rip
  # Should be -89 to 89
  de=$(rand_int 0 89)
  roll=$(rand_int 0 359)
  fov=$(rand_int 10 60)

  ./lost pipeline \
    --generate 1 \
    --generate-x-resolution 1024 \
    --generate-y-resolution 1024 \
    --fov "$fov" \
    --generate-reference-brightness 100 \
    --generate-spread-stddev 1 \
    --generate-read-noise-stddev 0.05 \
    --generate-ra "$ra" \
    --generate-de "$de" \
    --generate-roll "$roll" \
    --plot-raw-input "../$tmp_dir/raw-$ra-$de-$roll-$fov.png" \



done

output="$(python test_tetra3.py)"

raNone=$(echo "$output" | grep -o "RA = None" | wc -l)
decNone=$(echo "$output" | grep -o "Dec = None" | wc -l)
rollNone=$(echo "$output" | grep -o "Roll = None" | wc -l)

raFail=$(echo "$output" | grep -o "RA fail" | wc -l)
decFail=$(echo "$output" | grep -o "Dec fail" | wc -l)
rollFail=$(echo "$output" | grep -o "Roll fail" | wc -l)

# echo "OUTPUT IS $output"

echo "##################################################################"
echo "##################################################################"

echo "Total number of images: $n"
echo "None: $raNone, $decNone, $rollNone"
echo "RA fail: $raFail"
echo "Dec fail: $decFail"
echo "Roll fail: $rollFail"



cd ..

rm -rf $tmp_dir

echo "FINISHED"