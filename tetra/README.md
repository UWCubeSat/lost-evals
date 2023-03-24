# tetra3 Debugging

Code to test the ESA's implementation of `tetra3`

Some background info:
- I have not touched `tetra3.py`
- I also haven't touched `default_database.npz`, which is built with max FOV of 12 degrees
- `lost` and `bright-star-catalog.tsv` are copied over from LOST. I really only use the executable here to generate images

To run tests:
- Go into the `examples` directory
- Modify `test-tetra.sh` as needed. You only really need to change the `n` variable to control how many images are generated/tested on
- Run `bash test-tetra.sh`. This will generate images and run `test_tetra3.py`

Some concerning things I'm noticing at the moment
1. Given an image with FOV around 12 (less than or equal to 20 seems to be ok), tetra3 computes RA and Dec just fine. However, for almost every single image, the computed Roll is off by a significant amount
2. Given an image with much larger FOV (greater than 20ish), tetra3 fails to identify any stars/compute attitude

Example run with n=100 images:
- 73 images couldn't be identified at all
- For 27 images, the RA and Dec were ok. Roll was completely wrong