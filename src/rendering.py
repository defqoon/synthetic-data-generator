from math import pi
import os
import json

import bmesh
import bpy
import numpy as np


# useful shortcut
scene = bpy.context.scene
bpy.data.scenes["Scene"].use_nodes = True
tree = bpy.data.scenes["Scene"].node_tree
links = tree.links

# set up couple things
base_folder = os.environ["BASE_DIR"]
bpy.context.scene.render.filepath = base_folder
bpy.context.scene.unit_settings.system ='METRIC'

# stereo stuff
bpy.data.scenes["Scene"].render.use_multiview = True
bpy.data.scenes["Scene"].render.views_format = "STEREO_3D"
bpy.data.cameras['cam'].sensor_fit = "HORIZONTAL"

# create the nodes
rl = tree.nodes.new(type="CompositorNodeRLayers")
rl.location = 200, 200
rl.select = False

dm_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
dm_output_node.select = False
dm_output_node.base_path = os.environ["DEPTH_MAP_DIR"]
dm_output_node.format.file_format = "OPEN_EXR"
dm_output_node.location = 400, 400

st_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
st_output_node.select = False
st_output_node.base_path = os.environ["IMAGES_DIR"]
st_output_node.location = 400, 200
st_output_node.format.compression = 0

# set the render engine
bpy.data.scenes["Scene"].render.engine = "CYCLES"
bpy.data.scenes["Scene"].cycles.samples = 16  # int(os.environ["SAMPLES"])  # decrease if too slow
bpy.data.scenes["Scene"].cycles.device = "CPU"
bpy.data.scenes["Scene"].render.tile_x = int(os.environ["TILE_SIZE"])
bpy.data.scenes["Scene"].render.tile_y = int(os.environ["TILE_SIZE"])
bpy.data.scenes["Scene"].render.resolution_x = int(os.environ["RESOLUTION_X"])
bpy.data.scenes["Scene"].render.resolution_y = int(os.environ["RESOLUTION_Y"])
bpy.data.scenes["Scene"].render.image_settings.color_mode = "RGB"
bpy.data.scenes["Scene"].render.use_persistent_data = True

dataset_name = os.environ["DATASET_NAME"]
n_samples = int(os.environ["N_SAMPLES"])
r_boundaries = [0.5, 2]
x_boundaries = [-10, 10]
y_boundaries = [-3, 5]
z_boundaries = [-1, 7]

# create material
mat = bpy.data.materials.new('Sphere')
mat.diffuse_color = (1, 0, 0)

for i in range(n_samples):
    # create a random number of sphere
    nsphere = np.random.randint(0, 10)
    for j in range(nsphere):
        r = np.random.uniform(r_boundaries[0], r_boundaries[1])
        x = np.random.uniform(x_boundaries[0], x_boundaries[1])
        y = np.random.uniform(y_boundaries[0], y_boundaries[1])
        z = np.random.uniform(z_boundaries[0], z_boundaries[1])
        bpy.ops.mesh.primitive_ico_sphere_add(size=r, location=(x, y, z))
        bpy.ops.object.material_slot_add()
        bpy.context.object.material_slots[0].material = mat

    # deactivate multiview, save depth map
    dm_output_node.file_slots[0].path = '{}_{}_#'.format(dataset_name, i)
    bpy.data.scenes["Scene"].render.use_multiview = False
    l1 = links.new(rl.outputs['Depth'], dm_output_node.inputs['Image'])
    bpy.ops.render.render(write_still=False)
    links.remove(l1)

    # activate multiview, save stereo images
    st_output_node.file_slots[0].path = '{}_{}_#'.format(dataset_name, i)
    bpy.data.scenes["Scene"].render.use_multiview = True
    l2 = links.new(rl.outputs['Image'], st_output_node.inputs['Image'])
    bpy.ops.render.render(write_still=False)
    links.remove(l2)

    # delete all objects
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name != "background":
            o.select = True
        else:
            o.select = False
    bpy.ops.object.delete()
    bpy.context.scene.update()