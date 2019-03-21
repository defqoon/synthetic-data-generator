import array
import glob
import Imath
import os

import OpenEXR
import numpy as np


def post_processing():
    """couple postprocessing steps
    - clean images name
    - change depth to npy file format"""
    # rename images
    paths = glob.glob(os.environ["IMAGES_DIR"] + "*.png")
    for p in paths:
        new_name = os.path.basename(p).replace("_28", "")
        destination = os.path.join(os.path.dirname(p), new_name)
        os.rename(p, destination)

    # changing depth map to npy format
    # from https://www.excamera.com/sphinx/articles-openexr.html
    paths = glob.glob(os.environ["DEPTH_MAP_DIR"] + "*.exr")
    for p in paths:
        file = OpenEXR.InputFile(p)

        # get the size
        dw = file.header()['dataWindow']
        sz = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

        # only need one channel, they are all equal
        float = Imath.PixelType(Imath.PixelType.FLOAT)
        R = array.array('f', file.channel("R", float)).tolist()
        R = np.array(R)
        R = R.reshape(sz, order="F")

        output_file = os.path.join(os.environ["DEPTH_MAP_DIR"],
                                   'depth_map_' + os.path.basename(p).replace("_28.exr", ""))
        np.save(output_file, R)
        os.remove(p)
