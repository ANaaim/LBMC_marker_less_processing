#import adress_folder
import ezc3d
import numpy as np
import math

import save_and_export
import snippet_ezc3d as snip_ezc3d
import cv2
from P2S_function import read_toml, read_and_transform_calib
from pathlib import Path
import os
import json
from collections import defaultdict
#import joint_center_calculation


def add_point_on_video_and_export(path_to_video, point_2D, output_path):
    # Open the video file
    cap = cv2.VideoCapture(str(path_to_video))

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Create a VideoWriter object
    out = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (frame_width, frame_height))
    frame_number = 0

    # Precompute points to avoid redundant calculations
    points = np.array(point_2D)
    points[np.isnan(points)] = 0
    points = points.astype(int)

    while cap.isOpened():
        ret, frame = cap.read()
        # we should check if are not in the last frame that could not exist in the c3d files as the number of frame is not the sam
        if frame_number >= points.shape[1]:
            break
        if ret:
            # Draw a point on the frame
            for point in points:
                X = point[frame_number][0][0]
                Y = point[frame_number][0][1]

                frame = cv2.circle(
                    frame,
                    (int(X), int(Y)),
                    radius=3,
                    color=(0, 0, 255),
                    thickness=-1,
                )
            out.write(frame)
            frame_number += 1
        else:
            break

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()


def reproject_point_3d_on_video(point_3d, camera_name, path_to_calib):
    all_camera_names, skew, distortion, intrinsic, rotation, translation = read_toml(path_to_calib)
    if camera_name not in all_camera_names:
        raise ValueError(f"camera_name {camera_name} not in the list of camera names")
    else:
        ind_camera = all_camera_names.index(camera_name)
    point_3d_transpose = point_3d.transpose()
    point_3d_reshape = point_3d_transpose[:, 0:3]
    point_2d, _ = cv2.projectPoints(
        point_3d_reshape, rotation[ind_camera], translation[ind_camera], intrinsic[ind_camera], distortion[ind_camera]
    )

    return point_2d


def get_equivalent_first_frame_video_and_in_c3d(acq_c3d, ratio_fq):
    # Calculation of the new_first frame for both the video and the c3d file
    #original_first_frame_c3d = acq_c3d["parameters"]["PROCESSING"]["Cropped Measurement Start Frame"]["value"][0] - 1
    original_first_frame_c3d = 0
    original_first_frame_c3d_in_video = original_first_frame_c3d / int(ratio_fq)
    # if the first frame is not an integer, we have to round it to the upper integer
    original_first_frame_c3d_in_video = math.ceil(original_first_frame_c3d_in_video)
    equivalent_first_frame_c3d_in_c3d = original_first_frame_c3d_in_video * ratio_fq

    first_new_frame_points_c3d = int(equivalent_first_frame_c3d_in_c3d - original_first_frame_c3d)
    return first_new_frame_points_c3d, original_first_frame_c3d_in_video


def extract_c3d_equivalent_video(path_2_c3d, path_2_video, camera_name, fq_file_c3d, fq_file_video):
    ratio_fq = fq_file_c3d / fq_file_video

    # Extract point
    acq_c3d = ezc3d.c3d(str(path_2_c3d))
    points_c3d, points_name_c3d, points_ind_c3d = snip_ezc3d.get_points_ezc3d(acq_c3d)

    first_new_frame_points_c3d, original_first_frame_c3d_in_video = get_equivalent_first_frame_video_and_in_c3d(
        acq_c3d, ratio_fq
    )

    # case where the C3D file is longer than the trc file
    points_c3d_nb_frame = points_c3d.shape[2]
    # get the number of frame in the video
    cap = cv2.VideoCapture(str(path_2_video))
    points_video_nb_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if points_c3d_nb_frame / ratio_fq > points_video_nb_frame:
        points_c3d = points_c3d[:, :, 0 : points_video_nb_frame * int(ratio_fq)]

    # We extract the point from the c3D file every ratio_fq frame
    new_points_c3d = points_c3d[:, :, first_new_frame_points_c3d :: int(ratio_fq)]
    nb_frame_c3d_video = new_points_c3d.shape[2]

    points_from_c3d_to_export = np.zeros((4, len(points_name_c3d), nb_frame_c3d_video))
    points_from_c3d_to_export[3, :, :] = 1
    points_from_c3d_to_export[0:3, :, :] = new_points_c3d

    c3d_points = dict()
    c3d_points["points"] = points_from_c3d_to_export
    c3d_points["name"] = points_name_c3d
    c3d_points["ind2name"] = points_ind_c3d

    return c3d_points


def project_points_on_video(c3d_points, path_2_video, path_to_calib, camera_name, conversion_factor, type_calib):

    points_c3d = c3d_points["points"]
    points_name_c3d = c3d_points["name"]
    points_ind_c3d = c3d_points["ind2name"]

    list_points_to_put_in_video = points_name_c3d
    if type_calib == "board":
        x_coordinate = [round(x * 0.15, 2) for x in range(10)]
        y_coordinate = [round(x * 0.15, 2) for x in range(4)]

        for x in x_coordinate:
            for y in y_coordinate:
                list_points_to_put_in_video.append(f"point_x_{x}y__{y}")
                points_ind_c3d[f"point_x_{x}y__{y}"] = len(list_points_to_put_in_video) - 1
                point_to_add = np.zeros((4,1, points_c3d.shape[2]))
                point_to_add[0, :, :] = x
                point_to_add[1, :, :] = y
                point_to_add[2, :, :] = 0
                point_to_add[3, :, :] = 1
                points_c3d = np.concatenate((points_c3d, point_to_add), axis=1)


    point_2D = list()
    for name_point in list_points_to_put_in_video:
        if name_point in points_name_c3d:
            # We reproject the point on the video
            temp_point = points_c3d[:, points_ind_c3d[name_point], :] / conversion_factor
            point_2D.append(reproject_point_3d_on_video(temp_point, camera_name, path_to_calib))
    list_name_point = [name_point for name_point in list_points_to_put_in_video if name_point in points_name_c3d]


    return point_2D, list_name_point


def result_to_json(data, name_camera, path_to_json):
    point_2D = data[name_camera]
    list_points = list(point_2D.keys())
    nb_frame = point_2D[list_points[0]].shape[0]
    for ind in range(nb_frame):
        mmpose_result = dict()
        mmpose_result["version"] = 1.3
        mmpose_result["people"] = dict()
        mmpose_result["people"]["person_id"] = [-1]
        list_coordinate_score = []
        for name_point in list_points:
            mmpose_result["people"]["pose_keypoints_2d"] = mmpose_result["people"].get("pose_keypoints_2d", []) + [
                point_2D[name_point][ind, 0],
                point_2D[name_point][ind, 1],
                point_2D[name_point][ind, 2],
            ]

        # write the json file
        filename_json = f"{name_camera}_{ind:09}_keypoints.json"
        full_path_folder = Path(path_to_json, name_camera)
        full_path = full_path_folder / filename_json
        # Test if folder exists
        if not full_path_folder.exists():
            os.makedirs(full_path_folder)
        with open(full_path, "w") as outfile:
            json.dump(mmpose_result, outfile)

def generate_data_LIO(path_video, c3d_full_path, subject, task, fq_file_c3d, fq_file_video, conversion_factor, add_video):

    camera_calibration_matrix_path = path_video / subject / subject / "calibration" / "Calib_Qualisys.toml"
    all_camera_name, _, _, _, _, _ = read_toml(camera_calibration_matrix_path)

    data_to_export = defaultdict(dict)
    for camera_name in all_camera_name:
        video_full_path = path_video / subject / subject / task / "videos" / camera_name / (camera_name + ".avi")
        c3d_points_to_project = extract_c3d_equivalent_video(
            c3d_full_path, video_full_path, camera_name, fq_file_c3d, fq_file_video
        )

        points_2D, name_point = project_points_on_video(
            c3d_points_to_project, video_full_path, camera_calibration_matrix_path, camera_name, conversion_factor
        )


def process_folder(path_video, c3d_full_path, subject, task, fq_file_c3d, fq_file_video, conversion_factor, add_video, path_video_export, type_calib):

    camera_calibration_matrix_path = path_video / subject / "calibration" / "Calib_scene.toml"
    all_camera_name, _, _, _, _, _ = read_toml(camera_calibration_matrix_path)

    data_to_export = defaultdict(dict)
    for camera_name in all_camera_name:
        video_full_path = path_video / subject / task / "videos" / camera_name / (camera_name + ".avi")
        c3d_points_to_project = extract_c3d_equivalent_video(
            c3d_full_path, video_full_path, camera_name, fq_file_c3d, fq_file_video
        )

        points_2D, name_point = project_points_on_video(
            c3d_points_to_project, video_full_path, camera_calibration_matrix_path, camera_name, conversion_factor,
        type_calib)
        if add_video:
            # Add the name of the c3d to the camera name for the video removing the extension .c3d
            video_name = camera_name + "_" + c3d_full_path.stem
            video_name = video_name + ".avi"
            # Check if the folder exists
            if not path_video_export.exists():
                path_video_export.mkdir(parents=True)

            path_video_export_camera = path_video_export / video_name
            add_point_on_video_and_export(video_full_path, points_2D, path_video_export_camera)

        for name in name_point:
            value_to_export = np.zeros((points_2D[name_point.index(name)].shape[0], 3))
            # Confidence to one
            value_to_export[:, 0:2] = np.squeeze(points_2D[name_point.index(name)])
            value_to_export[:, 2] = 1.0
            data_to_export[camera_name][name] = value_to_export
    return data_to_export


if __name__ == "__main__":

    verif_raw_data = True
    # Folder
    path_to_data = Path("./data_CRME")
    path_video = path_to_data / "Processing" / "Formatted"
    export_video_folder = Path("./Check_calibration")
    export_folder_data = Path("./Pose2d/3D_to_2D")

    fq_file_c3d = 120
    subject_to_fq_file_video = {"Sujet_000":120,"Sujet_001":60,
                                "Sujet_002":60,"Sujet_003": 60,
                                "Sujet_007": 60,"fake_subject": 120,"fake_subject_02": 120}


    sujet_to_list_task = {
        "Sujet_000": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_001": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_002": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_001", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_003": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_002", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_004": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_005": ["01-eat-yoghurt_001", "02-cut-food", "13-playdoe", "06-drawing_001", "16-comb-hair", "17-hand-to-back_001"],
        "Sujet_006": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_007": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"]}


    if verif_raw_data:
        path_c3d = path_to_data/ "raw_c3d"
        subjects = ["fake_subject_02"]
        tasks = ["verification"]
    else:
        path_c3d = path_to_data / "Processing" / "C3D_labelled"
        subjects = ["Sujet_000", "Sujet_001", "Sujet_002", "Sujet_003","Sujet_004","Sujet_005","Sujet_006","Sujet_007"]
        subjects = ["Sujet_003"]

    add_video = True


    for subject in subjects:
        fq_file_video = subject_to_fq_file_video[subject]
        if not verif_raw_data:
            tasks = sujet_to_list_task[subject]

        for ind_task,task in enumerate(tasks):
            export_video_folder_subject = export_video_folder / subject / task
            final_name = task + ".c3d"
            if verif_raw_data:
                c3d_full_path = path_c3d / subject  / final_name
            else:
                c3d_full_path = path_c3d / subject / "with_center" /final_name
            type_calib = "scene"
            # Extract the unit of the c3d file in order to be able to define the conversion_factor
            acq = ezc3d.c3d(str(c3d_full_path))
            unit_point = acq["parameters"]["POINT"]["UNITS"]["value"][0]
            if unit_point == "mm":
                conversion_factor = 1000
            elif unit_point == "m":
                conversion_factor = 1
            else:
                raise ValueError(f"unit_point {unit_point} not recognized")
            if ind_task == 0:
                add_video = True
            else:
                add_video = False
            # for each subject only one video should be exported
            data_to_export = process_folder(
                path_video, c3d_full_path, subject, task, fq_file_c3d, fq_file_video, conversion_factor, add_video, export_video_folder_subject,
            type_calib)

            #path_to_json_folder = Path(export_folder, subject, task, "3D_to_2D")

            path_to_hdf5 = Path(export_folder_data, subject, task)
            #path_to_annotation = Path(export_folder, subject, task, "annotation")
            #filename = f"{subject}_{task}.h5"
            filename = f"{task}.h5"
            save_and_export.save_hdf5(data_to_export, path_to_hdf5, filename)
            #save_and_export.export_data_to_json(data_to_export, path_to_json_folder)
            #save_and_export.export_data_to_annotation(data_to_export, path_to_annotation, ["RHJC","RKJC","RAJC"])
