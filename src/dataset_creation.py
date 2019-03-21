import json
import os

from utils import post_processing


def create_dataset():
    """read the config file"""
    with open("/root/config.json", "r") as f:
        config = json.load(f)

    # create environmental variables
    for (key, value) in config.items():
        os.environ[key] = str(value)

    # run blender
    command = '/usr/lib/blender/blender {} --python {} --background'.\
        format("/root/models/default.blend", "/root/rendering.py")
    os.system(command)

    # post processing
    post_processing()


if __name__ == '__main__':
    create_dataset()