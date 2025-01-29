import numpy as np
import toml
import cv2

# FUNCTIONS


def read_and_transform_calib(file_name):
    camera_params, skew, distortion, intrinsic, rotation, translation = read_toml(file_name)
    rotation = [np.array(cv2.Rodrigues(r)[0]) for r in rotation]
    translation = np.array(translation) * 1000
    # Before it was ang_x=np.pi, ang_y=0, ang_z=0
    RT = [rotate_cam(r, t, ang_x=0, ang_y=0, ang_z=0) for r, t in zip(rotation, translation)]
    rotation = [rt[0] for rt in RT]
    translation = [rt[1] for rt in RT]
    # Befor it was used
    # RT = [world_to_camera_persp(r, t) for r, t in zip(rotation, translation)]
    # rotation = [rt[0] for rt in RT]
    # translation = [rt[1] for rt in RT]
    return camera_params, rotation, translation


def read_toml(toml_path):
    """
    Read an OpenCV .toml calibration file
    Returns 5 lists of size N (N=number of cameras):
    - S (image size),
    - D (distorsion),
    - K (intrinsic parameters),
    - R (extrinsic rotation),
    - T (extrinsic translation)
    """

    calib = toml.load(toml_path)
    C, S, D, K, R, T = [], [], [], [], [], []
    for cam in list(calib.keys()):
        if cam != "metadata":
            C += [calib[cam]["name"]]
            S += [np.array(calib[cam]["size"])]
            D += [np.array(calib[cam]["distortions"])]
            K += [np.array(calib[cam]["matrix"])]
            R += [np.array(calib[cam]["rotation"])]
            T += [np.array(calib[cam]["translation"])]

    return C, S, D, K, R, T


def rotate_cam(r, t, ang_x=np.pi, ang_y=0, ang_z=0):
    """
    Apply rotations around x, y, z in cameras coordinates
    """

    rt_h = np.block([[r, t.reshape(3, 1)], [np.zeros(3), 1]])

    r_ax_x = np.array([1, 0, 0, 0, np.cos(ang_x), -np.sin(ang_x), 0, np.sin(ang_x), np.cos(ang_x)]).reshape(3, 3)
    r_ax_y = np.array([np.cos(ang_y), 0, np.sin(ang_y), 0, 1, 0, -np.sin(ang_y), 0, np.cos(ang_y)]).reshape(3, 3)
    r_ax_z = np.array([np.cos(ang_z), -np.sin(ang_z), 0, np.sin(ang_z), np.cos(ang_z), 0, 0, 0, 1]).reshape(3, 3)
    r_ax = r_ax_z @ r_ax_y @ r_ax_x

    r_ax_h = np.block([[r_ax, np.zeros(3).reshape(3, 1)], [np.zeros(3), 1]])
    r_ax_h__rt_h = r_ax_h @ rt_h

    r = r_ax_h__rt_h[:3, :3]
    t = r_ax_h__rt_h[:3, 3]

    return r, t


def world_to_camera_persp(r, t):
    """
    Converts rotation R and translation T
    from Qualisys object centered perspective
    to OpenCV camera centered perspective
    and inversely.

    Qc = RQ+T --> Q = R-1.Qc - R-1.T
    """

    r = r.T
    t = -r @ t

    return r, t
