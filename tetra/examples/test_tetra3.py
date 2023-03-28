"""
This example loads the tetra3 default database and solves for every image in the tetra3/test_data directory.

Note: Requires PIL (pip install Pillow)
"""
import sys
sys.path.append('..')
from tetra3 import Tetra3
from PIL import Image
from pathlib import Path


def cmp(real, ours, varTest):
    if ours is None:
        print(f"{varTest} = None")
        return
    if abs(real-ours) % 360 > 0.1:
        print(f"{varTest} fail")

##############################################################################################

# Create instance and load default_database (built with max_fov=12 and the rest as default)
t3 = Tetra3("large_db")

# Path where images are
# path = Path('../test_data/')
path = Path("../temp/")
for impath in path.glob('*.png'):

    iname = str(impath).split("-")
    print(iname)

    ra = float(iname[1])
    de = float(iname[2])
    roll = float(iname[3])
    fov = float(iname[4].replace(".png", ""))
    print(ra, de, roll, fov)

    # print('Solving for image at: ' + str(impath))
    with Image.open(str(impath)) as img:
        solved = t3.solve_from_image(img, fov_estimate=fov)  # Adding e.g. fov_estimate=11.4, fov_max_error=.1 improves performance
    print('Solution: ' + str(solved))

    raSolved = solved["RA"]
    deSolved = solved["Dec"]
    rollSolved = solved["Roll"]
    if rollSolved is not None:
        rollSolved = 360 - rollSolved
    fovSolved = solved["FOV"]

    cmp(ra, raSolved, "RA")
    cmp(de, deSolved, "Dec")
    cmp(roll, rollSolved, "Roll")


    print("#############################################################################")

print("========================== DONE =================================")

