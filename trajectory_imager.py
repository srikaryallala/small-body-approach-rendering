import bpy
import os
import csv
import math
import mathutils
import numpy
import random


if __name__ == '__main__':
    # locations vars
    body_loc = [0,0,0] #units are in km
    #sun_loc = [-25,-35,0] #units are in km
    # paths
    dir = os.path.dirname(bpy.data.filepath) + os.sep
    stl_path = 'C:/Users/srika/Downloads/itokawa_f0049152.stl/itokawa_f0049152.stl' # stl file path
    blender_path = 'C:/Users/srika/Documents/SSDS_Research/' # path which contains the necessary files to be read (pos_xyz_filename, euler_pose_xyz_filename)
    pos_xyz_filename = 'filtered_pos_xyz.npy' # file which contains the time-correlated sequence of positions in the sequence
    euler_pose_xyz_filename = 'euler_filtered_pos_xyz.npy' # file which contains the time-correlated sequence of euler angle rotations in the sequence
    write_path = 'C:/Users/srika/Documents/SSDS_Research/Itokawa_images/' # path to folder where rendered images are written
    write_file_name = 'rendered_Itokawa'
    #''' SCENE SETUP '''
    #scene_setup(body_loc, sun_loc, stl_path)

    # load position and rotation files for the sequence
    pos_xyz = numpy.load(blender_path+pos_xyz_filename) # formatted as a list of lists which contain x,y,z positions at each time step
    euler_pose_xyz = numpy.load(blender_path+euler_pose_xyz_filename) # formatted as a list of lists which contain x,y,z euler angles at each time step
    len_pos_xyz = len(pos_xyz)
    
    #bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    
    # loop through each time step and render/save the camera view
    for i in range(len_pos_xyz):
        file_num = i
        multiplier = 1
        cam_loc = [pos_xyz[i,0],pos_xyz[i,1],pos_xyz[i,2]]
        camera_rot = [euler_pose_xyz[i,0],euler_pose_xyz[i,1],euler_pose_xyz[i,2]]
        
        scene = bpy.data.scenes["Scene"]
        
        # create and set up stereo camera. for monocular camera, see methods above
        scene.camera.location = cam_loc
        scene.camera.rotation_euler = camera_rot
        scene.camera.data.lens = 645000
        scene.camera.data.clip_start = 1e-6
        scene.camera.data.clip_end = 3e6
        
        #bpy.ops.object.camera_add(location=cam_loc, rotation=camera_rot)
        #bpy.context.scene.camera=bpy.data.objects['Camera']
        
        
        
        # set rendered image settings
        scene.render.resolution_x = 137
        scene.render.resolution_y = 137
        scene.render.resolution_percentage = 100
        scene.render.filepath = write_path + write_file_name + str(file_num) + '.png'
        # render and save image
        bpy.ops.render.render( write_still=True )
