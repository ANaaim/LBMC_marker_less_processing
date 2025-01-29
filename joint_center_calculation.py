import numpy as np
from utils import norm_vector


def hip(points_c3d, points_ind_c3d, sexe):
    """ "
    Calculation of the 3D coordinqte of the hip joint center using the Dumas et al. regression (2017) knowing the sexe
    and the position of RIAS, LIAS RIPS and LIPS landmarks

    Parameters
    ---------
    points_c3d : np.array
    points_ind_c3d : dict
    sexe : string

    Returns
    ---------
    R_HJC : np.array
    L_HJC : np.array
    """
    # HJC
    RASI = points_c3d[0:3, points_ind_c3d["RIAS"], :]
    LASI = points_c3d[0:3, points_ind_c3d["LIAS"], :]
    RPSI = points_c3d[0:3, points_ind_c3d["RIPS"], :]
    LPSI = points_c3d[0:3, points_ind_c3d["LIPS"], :]

    Xtemp = (RASI + LASI) / 2 - (RPSI + LPSI) / 2
    SACR = (LPSI + RPSI) / 2
    Ytemp = np.cross(RASI - SACR, LASI - SACR, axisa=0, axisb=0, axisc=0)
    Ztemp = np.cross(Xtemp, Ytemp, axisa=0, axisb=0, axisc=0)
    X_Pelvis = norm_vector(Xtemp)
    Y_Pelvis = norm_vector(Ytemp)
    Z_Pelvis = norm_vector(Ztemp)

    SACR = (RPSI + LPSI) / 2
    Z_pelvis_HJC = norm_vector(RASI - LASI)
    Y_pelvis_HJC = norm_vector(
        np.cross(Z_pelvis_HJC, (RASI + LASI) / 2 - SACR, axisa=0, axisb=0, axisc=0)
    )
    X_pelvis_HJC = norm_vector(
        np.cross(Y_pelvis_HJC, Z_pelvis_HJC, axisa=0, axisb=0, axisc=0)
    )
    width_pelvis = np.mean(np.linalg.norm(RASI - LASI, axis=0))

    if sexe == "M":
        R_HJC = (
            (RASI + LASI) / 2
            - 9.5 / 100 * width_pelvis * X_pelvis_HJC
            - 37 / 100 * width_pelvis * Y_pelvis_HJC
            + 36.1 / 100 * width_pelvis * Z_pelvis_HJC
        )
        L_HJC = (
            (RASI + LASI) / 2
            - 9.5 / 100 * width_pelvis * X_pelvis_HJC
            - 37 / 100 * width_pelvis * Y_pelvis_HJC
            - 36.1 / 100 * width_pelvis * Z_pelvis_HJC
        )
    elif sexe == "F":
        R_HJC = (
            (RASI + LASI) / 2
            - 13.9 / 100 * width_pelvis * X_pelvis_HJC
            - 33.6 / 100 * width_pelvis * Y_pelvis_HJC
            + 37.2 / 100 * width_pelvis * Z_pelvis_HJC
        )
        L_HJC = (
            (RASI + LASI) / 2
            - 13.9 / 100 * width_pelvis * X_pelvis_HJC
            - 33.6 / 100 * width_pelvis * Y_pelvis_HJC
            - 37.2 / 100 * width_pelvis * Z_pelvis_HJC
        )

    return R_HJC, L_HJC


def shoulder(points_c3d, points_ind_c3d, sexe):
    """ "
    Calculation of the 3D coordinate of the shoulder joint center using the Dumas et al. regression (2017)

    Parameters
    ---------
    points_c3d : np.array
    points_ind_c3d : dict
    sexe : string

    Returns
    ---------
    R_SJC : np.array
    L_SJC : np.array
    """
    ## Solid : THORAX
    CV7 = points_c3d[0:3, points_ind_c3d["CV7"], :]
    SJN = points_c3d[0:3, points_ind_c3d["SJN"], :]
    TV8 = points_c3d[0:3, points_ind_c3d["TV8"], :]

    RSAT = points_c3d[0:3, points_ind_c3d["RSAT"], :]
    LSAT = points_c3d[0:3, points_ind_c3d["LSAT"], :]

    Z_thorax = norm_vector(np.cross(SJN - TV8, CV7 - TV8, axisa=0, axisb=0, axisc=0))

    width_thorax = np.mean(np.linalg.norm(CV7 - SJN, axis=0))
    Y_temp = norm_vector(
        np.cross(Z_thorax, SJN - CV7, axisa=0, axisb=0, axisc=0)
    )  # temporary coordinate system for CJC construction
    X_temp = norm_vector(np.cross(Y_temp, Z_thorax, axisa=0, axisb=0, axisc=0))
    if sexe == "M":
        angle_R_SJC = 11 * np.pi / 180
        R_SJC = RSAT + 33 / 100 * width_thorax * (
            (np.cos(angle_R_SJC) * X_temp) - (np.sin(angle_R_SJC) * Y_temp)
        )
        L_SJC = LSAT + 33 / 100 * width_thorax * (
            (np.cos(angle_R_SJC) * X_temp) - (np.sin(angle_R_SJC) * Y_temp)
        )
    elif sexe == "F":
        angle_R_SJC = 5 * np.pi / 180
        R_SJC = RSAT + 36 / 100 * width_thorax * (
            (np.cos(angle_R_SJC) * X_temp) - (np.sin(angle_R_SJC) * Y_temp)
        )
        L_SJC = LSAT + 36 / 100 * width_thorax * (
            (np.cos(angle_R_SJC) * X_temp) - (np.sin(angle_R_SJC) * Y_temp)
        )

    return R_SJC, L_SJC


def shoulder_RAB(points_c3d, points_ind_c3d):
    """ "
    Calculation of the 3D coordinate of the shoulder joint center using the RAB regression (2017)

    Parameters
    ---------
    points_c3d : np.array
    points_ind_c3d : dict
    sexe : string

    Returns
    ---------
    R_SJC : np.array
    L_SJC : np.array
    """
    ## Solid : THORAX
    CV7 = points_c3d[0:3, points_ind_c3d["CV7"], :]
    SJN = points_c3d[0:3, points_ind_c3d["SJN"], :]
    TV8 = points_c3d[0:3, points_ind_c3d["TV8"], :]

    RSAT = points_c3d[0:3, points_ind_c3d["RSAT"], :]
    LSAT = points_c3d[0:3, points_ind_c3d["LSAT"], :]

    Z_thorax = norm_vector(np.cross(SJN - TV8, CV7 - TV8, axisa=0, axisb=0, axisc=0))

    Y_temp = norm_vector(
        np.cross(Z_thorax, SJN - CV7, axisa=0, axisb=0, axisc=0)
    )  # temporary coordinate system for CJC construction
    X_temp = norm_vector(np.cross(Y_temp, Z_thorax, axisa=0, axisb=0, axisc=0))

    # Calcul distance inter SAT
    dist_SAT = np.mean(np.linalg.norm(RSAT - LSAT, axis=0))
    R_SJC = RSAT - 17 / 100 * dist_SAT * Y_temp
    L_SJC = LSAT - 17 / 100 * dist_SAT * Y_temp

    return R_SJC, L_SJC
