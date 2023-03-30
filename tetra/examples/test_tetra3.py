import sys
sys.path.append('..')
from tetra3 import Tetra3
from PIL import Image
from pathlib import Path

import time

error = {"RA": 0, "Dec": 0, "Roll": 0}
fail = {"RA": 0, "Dec": 0, "Roll": 0}

# I expect that if one param is None, all the others will be too
nones = {"RA": 0, "Dec": 0, "Roll": 0}

th = 0.1

def cmp(real, ours, varTest):

    if ours is None:
        nones[varTest] += 1
        # print(f"{varTest} = None")
        return

    error[varTest] += (abs(real-ours) % 360)
    if abs(real-ours) % 360 > th:
        # print(f"{varTest} fail")
        fail[varTest] += 1

##############################################################################################

t3 = Tetra3("default_database")

# Path where images are
# path = Path('../test_data/')
n = 0
totalTime = 0


path = Path("../temp/")
for impath in path.glob('*.png'):

    n += 1

    iname = str(impath).split("-")
    # print(iname)

    ra = float(iname[1])
    de = float(iname[2])
    roll = float(iname[3])
    fov = float(iname[4].replace(".png", ""))
    # print(ra, de, roll, fov)

    with Image.open(str(impath)) as img:
        startTime = time.time()
        solved = t3.solve_from_image(img, fov_estimate=fov)

        totalTime += (time.time() - startTime)
    # print('Solution: ' + str(solved))

    raSolved = solved["RA"]
    deSolved = solved["Dec"]
    rollSolved = solved["Roll"]
    if rollSolved is not None:
        rollSolved = 360 - rollSolved
    fovSolved = solved["FOV"]

    cmp(ra, raSolved, "RA")
    cmp(de, deSolved, "Dec")
    cmp(roll, rollSolved, "Roll")


numNotNone = n - nones["RA"]

print("n", n)
print("Total time (seconds)", totalTime)
print("Total error", error)
print("Total fails", fail)
print("Nones", nones)
print("Mean error", )

if numNotNone > 0:
    for key in error:
        print(key, error[key] / numNotNone)
else:
    print("ALL NONES, no mean error calculated")

print("========================== DONE =================================")

