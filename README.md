# LOST Evaluation

This repo contains Python scripts which run LOST evaluations, generating appropriate tables and graphs which can be subsequently included into the paper.

## Setup

### LOST

Compile [LOST](https://github.com/uwcubesat/lost). Symlink the `lost` executable and
`bright-star-catalog.tsv` into the current directory (`ln -s /home/my-user/development/lost/lost
./lost`, for example. Always make sure to use an absolute filepath as the first argument to `ln
-s`!)

### OpenStarTracker

Clone [OpenStarTracker](https://github.com/UBNanosatLab/openstartracker). Install all the dependencies they say they need, including the dependencies necessary for "calibration and unit testing". Also get the Astrometry index files, which are provided in the Debian/Ubuntu package `astrometry-data-tycho2-10-19` for wide-angle cameras (like the ones we use). (these index files are smaller than a TETRA database -- maybe astrometry is more suitable for star tracking than I thought?)

Go into their `beast` folder and run `make` (you may need to override the `PYTHONHEADERS` variable
in the `Makefile` for your installed version of python).

Then, symlink `calibrate.py` and `startracker.py` from the `tests` directly into the root directory here.

### Evals

Install Python dependencies from `requirements.txt`. There are any number of ways to do this, but I recommend creating either a virtualenv or a conda environment, then running `pip install -r requirements.txt`.

Python 3.11 recommended.

Conda is probably the best way to go, because it also lets you install the correct Python version. You'd first create an environment by running `conda create -n lost-evals python=3.11`, then whenever you need to use it, run `conda activate lost-evals`.

## Running

To do everything (just kidding, I only mean run all the LOST evaluations), run `make`. There are no prerequisite rules set up in the Makefile, so each time you run `make`, all the evaluations will be re-run.

As a side-effect of using Make, it's really easy to run only certain evaluations! Just run `make out/centroid-speed.png`, for example.

To send output to the `out5/` folder, for example, use `make OUT_PREFIX=out5`. Note that to specify a certain file to generate when using a custom prefix, you must also use the custom prefix if you want to run only one evaluation. For example, `make OUT_PREFIX=out5 out5/centroid-speed.png`.
