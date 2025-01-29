import os
from pathlib import Path
import json
import snip_h5py
import random
from collections import OrderedDict

def result_to_json(data, name_camera, path_to_json,keypoints_to_process, param_correction, testing=False):
    """
    A function to export the data from mmpose to json file respecting the formatting used by Openpose (or at least
    mimicking it)

    Parameters
    ---------
    data : dict
        A dictionary containing the 2D coordinate of the point to be exported
    name_camera : str
        The name of the camera to be exported
    path_to_json : Path
        Path where the data should be exported.
    keypoints_to_process : dict
        Dictionary containing the list of the point that should be exported in the annotation files for each camera

    Returns
    ---------
    None
    """

    point_2D = data[name_camera]
    list_points = list(point_2D.keys())
    nb_frame = point_2D[list_points[0]].shape[0]
    if testing:
        nb_frame = 100
        list_points = list_points[:10]
    for ind in range(nb_frame):
        mmpose_result = dict()
        mmpose_result["version"] = 1.3
        mmpose_result["people"] = list()
        mm_pose_data = dict()
        mm_pose_data["person_id"] = [-1]
        list_coordinate_score = []
        #for name_point in list_points:
        for key, value in keypoints_to_process.items():
            mm_pose_data["pose_keypoints_2d"] = mm_pose_data.get(
                "pose_keypoints_2d", []
            ) + [
                point_2D[key][ind, 0],
                point_2D[key][ind, 1],
                point_2D[key][ind, 2]/param_correction,
            ]
        mmpose_result["people"] = [mm_pose_data]
        # write the json file
        filename_json = f"{name_camera}_{ind:09}_keypoints.json"
        name_folder_camera = name_camera+"_json"
        full_path_folder = Path(path_to_json, name_folder_camera)
        full_path = full_path_folder / filename_json
        # Test if folder exists
        if not full_path_folder.exists():
            os.makedirs(full_path_folder)
        with open(full_path, "w") as outfile:
            json.dump(mmpose_result, outfile)


def result_to_annotation(data, name_camera, path_to_json, list_points):
    """
    A function to export the position of the point in images following the LIO training toolbox. This is used to format
    the coordinate of the point extracted from the reprojection of the 3D points measured on a 2D images for a camera

    This function zill generate an annotation file in the path_to_json folder.

    Parameters
    ----------
    data : dict
        A dictionary containing the 2D coordinate of the point to be exported for each camera
    name_camera : str
        The name of the camera to be exported
    path_to_json : Path
        Path where the data should be exported.
    list_points : list
        list of the point that should be exported in the annotation files

    Returns
    ---------
    None
    """

    point_2D = data[name_camera]
    all_points_list = list(point_2D.keys())
    nb_frame = point_2D[list_points[0]].shape[0]
    annotation_result = dict()
    for ind in range(nb_frame):
        data_frame = dict()
        data_frame["subject_id"] = 1
        data_frame["trial_id"] = "toto"

        x_min = 10000000
        y_min = 10000000
        x_max = -1
        y_max = -1

        list_coordinate = list()
        for name_point in all_points_list:
            if name_point in list_points:
                list_coordinate.append(point_2D[name_point][ind, 0])
                list_coordinate.append(point_2D[name_point][ind, 1])
            if point_2D[name_point][ind, 0] < x_min:
                x_min = point_2D[name_point][ind, 0]
            if point_2D[name_point][ind, 1] < y_min:
                y_min = point_2D[name_point][ind, 1]
            if point_2D[name_point][ind, 0] > x_max:
                x_max = point_2D[name_point][ind, 0]
            if point_2D[name_point][ind, 1] > y_max:
                y_max = point_2D[name_point][ind, 1]
        width = x_max - x_min
        height = y_max - y_min

        x_padding = random.uniform(0.05, 0.1)
        y_padding = random.uniform(0.05, 0.1)

        factor = 1
        x_min -= width * factor * x_padding
        x_max += width * factor * x_padding

        y_min -= height * factor * y_padding
        y_max += height * factor * y_padding

        if x_max > 1080:
            x_max = 1080
        if x_min < 0:
            x_min = 0
        if y_max > 1920:
            y_max = 1920
        if y_min < 0:
            y_min = 0

        data_frame["bbox"] = [x_min, y_min, x_max, y_max]
        data_frame["joints"] = list_coordinate

        name_frame = f"{ind+1:09}"
        annotation_result[name_frame] = data_frame

    # write the json file
    filename_json = "annotations.json"
    full_path_folder = Path(path_to_json, name_camera)
    full_path = full_path_folder / filename_json
    # Test if folder exists
    if not full_path_folder.exists():
        os.makedirs(full_path_folder)
    with open(full_path, "w") as outfile:
        json.dump(annotation_result, outfile)


def export_data_to_json(data_export, path_to_json, keypoints_to_process,param_correction, camera_to_export=None, testing=False):
    """
    Batch processing for all video of result_to_json

    Parameters
    --------
    data_export : dict
        A dictionary containing the 2D coordinate of the point to be exported for each camera
    path_to_json : Path
        Path where the data should be exported.
    keypoints_to_process : dict
        Dictionary containing the list of the point that should be exported in the annotation files for each camera
    param_correction : float
    value to correct the confidence value because some mmpose pose detection give a value between 10 and 0 instead of 1 and 0
    camera_to_export: list
    list of the camera that should be exported

    Returns
    ---------
    None
    """
    if camera_to_export is not None:
        for camera_name in data_export:
            if camera_name in camera_to_export:
                result_to_json(data_export, camera_name, path_to_json,keypoints_to_process,param_correction, testing)
    else:
        for camera_name in data_export:
            # test that the camera name is not metadata
            if camera_name != "metadata":
                result_to_json(data_export, camera_name, path_to_json,keypoints_to_process,param_correction, testing)


def export_data_to_annotation(data_export, path_to_json, list_points):
    """
    Batch processing for all video of result_to_json

    Parameters
    --------
    data_export : dict
        A dictionary containing the 2D coordinate of the point to be exported for each camera
    path_to_json : Path
        Path where the data should be exported.
    list_points : list
        list of the point that should be exported in the annotation files

    Returns
    ---------
    None
    """
    for camera_name in data_export:
        result_to_annotation(data_export, camera_name, path_to_json, list_points)


def save_hdf5(dict_for_hdf5, path_to_hdf5, filename):
    """ "
    Function to save a dictionary to a HDF5 file in a specific location.

    Parameters
    --------
    dict_for_hdf5 : dict
        dictionary to save

    Returns
    --------
    None

    """
    if not path_to_hdf5.exists():
        os.makedirs(path_to_hdf5)
    full_path_to_hdf5 = path_to_hdf5 / filename
    snip_h5py.save_dictionary_to_hdf(dict_for_hdf5, full_path_to_hdf5)
