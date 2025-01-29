import numpy as np
from utils import norm_vector


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
    CV7 = points_c3d[0:3, points_ind_c3d["C7"], :]
    SJN = points_c3d[0:3, points_ind_c3d["IJ"], :]
    TV8 = points_c3d[0:3, points_ind_c3d["T10"], :]

    RSAT = points_c3d[0:3, points_ind_c3d["R_AC"], :]
    LSAT = points_c3d[0:3, points_ind_c3d["L_AC"], :]

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
    CV7 = points_c3d[0:3, points_ind_c3d["C7"], :]
    SJN = points_c3d[0:3, points_ind_c3d["IJ"], :]
    TV8 = points_c3d[0:3, points_ind_c3d["T10"], :]

    RSAT = points_c3d[0:3, points_ind_c3d["R_AC"], :]
    LSAT = points_c3d[0:3, points_ind_c3d["L_AC"], :]

    Z_thorax = norm_vector(np.cross(SJN - TV8, CV7 - TV8, axisa=0, axisb=0, axisc=0))

    Y_temp = norm_vector(
        np.cross(Z_thorax, SJN - CV7, axisa=0, axisb=0, axisc=0)
    )  # temporary coordinate system for CJC construction
    X_temp = norm_vector(np.cross(Y_temp, Z_thorax, axisa=0, axisb=0, axisc=0))

    # Calcul distance inter SAT
    dist_SAT = np.nanmean(np.linalg.norm(RSAT - LSAT, axis=0))
    R_SJC = RSAT - 17 / 100 * dist_SAT * Y_temp
    L_SJC = LSAT - 17 / 100 * dist_SAT * Y_temp

    return R_SJC, L_SJC

def elbow_midpoint(points_c3d, points_ind_c3d):
    """ "
    Calculation of the 3D coordinate of the elbow joint center using the midpoint between the medial and lateral epicondyles

    Parameters
    ---------
    points_c3d : np.array
    points_ind_c3d : dict

    Returns
    ---------
    R_EJC : np.array
    L_EJC : np.array
    """
    ## Solid : ARM
    RLE = points_c3d[0:3, points_ind_c3d["R_EL"], :]
    LLE = points_c3d[0:3, points_ind_c3d["L_EL"], :]
    RME = points_c3d[0:3, points_ind_c3d["R_EM"], :]
    LME = points_c3d[0:3, points_ind_c3d["L_EM"], :]

    R_EJC = (RLE + RME) / 2
    L_EJC = (LLE + LME) / 2

    return R_EJC, L_EJC

def wrist_midpoint(points_c3d, points_ind_c3d):
    """ "
    Calculation of the 3D coordinate of the wrist joint center using the midpoint between the radial and ulnar styloids

    Parameters
    ---------
    points_c3d : np.array
    points_ind_c3d : dict

    Returns
    ---------
    R_WJC : np.array
    L_WJC : np.array
    """
    ## Solid : HAND
    RRS = points_c3d[0:3, points_ind_c3d["R_RS"], :]
    LRS = points_c3d[0:3, points_ind_c3d["L_RS"], :]
    RUS = points_c3d[0:3, points_ind_c3d["R_US"], :]
    LUS = points_c3d[0:3, points_ind_c3d["L_US"], :]

    R_WJC = (RRS + RUS) / 2
    L_WJC = (LRS + LUS) / 2

    return R_WJC, L_WJC

def hand_midpoint(points_c3d, points_ind_c3d):
    """ "
    Calculation of the 3D coordinate of the hand joint center using the midpoint between the 2nd and 5th metacarpals

    Parameters
    ---------
    points_c3d : np.array
    points_ind_c3d : dict

    Returns
    ---------
    R_HJC : np.array
    L_HJC : np.array
    """
    ## Solid : HAND
    RHM2 = points_c3d[0:3, points_ind_c3d["R_HM2"], :]
    LHM2 = points_c3d[0:3, points_ind_c3d["L_HM2"], :]
    RHM5 = points_c3d[0:3, points_ind_c3d["R_HM5"], :]
    LHM5 = points_c3d[0:3, points_ind_c3d["L_HM5"], :]

    R_HMJC = (RHM2 + RHM5) / 2
    L_HMJC = (LHM2 + LHM5) / 2

    return R_HMJC, L_HMJC