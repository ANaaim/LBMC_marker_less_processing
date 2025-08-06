import ezc3d
import pdb
import math
import numpy as np
from typing import Union


def get_points_ezc3d(acq):
    """Points extraction with a dictionnary allowing to find
    the point position in the numpy array using text without
    using a dictionnary"""

    points_name = acq["parameters"]["POINT"]["LABELS"]["value"]

    points_data = acq["data"]["points"][0:3, :, :]
    points_ind = dict()
    for index_point, name_point in enumerate(points_name):
        points_ind[name_point] = index_point

    return points_data, points_name, points_ind


def add_point_from_dictionary(acq, point_to_add):
    points, points_name, points_ind = get_points_ezc3d(acq)
    # copy points informations
    new_list = points_name.copy()
    new_array = acq["data"]["points"]
    nb_frame = acq["data"]["points"].shape[2]

    for ind_point, (name_point, value_point) in enumerate(point_to_add.items()):
        new_point = np.zeros((4, 1, nb_frame))
        new_list.append(name_point)
        new_point[0:3, 0, :] = value_point[:, :]
        new_point[3, 0, :] = 1
        new_array = np.append(new_array, new_point, axis=1)

    # Add the new points to the c3d file
    acq["parameters"]["POINT"]["LABELS"]["value"] = new_list
    acq["parameters"]["POINT"]["DESCRIPTIONS"]["value"] = new_list.copy()

    # Some parameters need to be modified for the c3d to be working
    temp_residuals = np.zeros((1, new_array.shape[1], new_array.shape[2]))
    temp_residuals[0, : acq["data"]["meta_points"]["residuals"].shape[1], :] = acq["data"]["meta_points"]["residuals"]
    old_camera_mask = acq["data"]["meta_points"]["camera_masks"]
    temp_camera_mask = np.zeros((old_camera_mask.shape[0], new_array.shape[1], old_camera_mask.shape[2]))
    temp_camera_mask[:, :, :] = False
    temp_camera_mask[:, : acq["data"]["meta_points"]["residuals"].shape[1], :] = old_camera_mask
    acq["data"]["meta_points"]["residuals"] = temp_residuals
    acq["data"]["meta_points"]["camera_masks"] = temp_camera_mask.astype(dtype=bool)
    # Add the new analogs to the c3d file used for the type 2 platform
    acq["data"]["points"] = new_array

    return acq


def create_c3d_from_dictionary(filename,point_to_add,fq,unit):
    """Create a c3d file from a dictionary containing the points to add.
    The dictionary should be in the following format:
    point_to_add = {"point_name": np.array([[x1, y1, z1], [x2, y2, z2], ...])}
    where x, y, z are the coordinates of the point in meters"""

    # Create an empty c3d file
    acq = ezc3d.c3d()
    nb_frame = 0
    for ind_point, (name_point, value_point) in enumerate(point_to_add.items()):
        if value_point.shape[1] > nb_frame:
            # If the point has more frames than the previous one, update the number of frames
            nb_frame = value_point.shape[1]
    nb_point = len(point_to_add)

    new_array = np.zeros((4, nb_point, nb_frame))
    new_array[3,:,:] = 1
    new_list = []
    # Add the points to the c3d file
    for ind_point, (name_point, value_point) in enumerate(point_to_add.items()):
        print(f"Adding point {name_point}")
        nb_frame_temp = value_point.shape[1]
        new_array[0:3, ind_point, :nb_frame_temp] = value_point
        new_list.append(name_point)
    
    acq["data"]["points"] = new_array
    acq["parameters"]["POINT"]["LABELS"]["value"] = new_list
    acq['parameters']['POINT']['UNITS']['value'] = [unit]
    acq['parameters']['POINT']['RATE']['value'] = [fq]
    

    acq.write(filename)
