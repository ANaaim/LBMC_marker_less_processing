from comparaison_2D import generate_3d_to_2d_hdf5,reduce_whole_body_coco_keypoints
from pathlib import Path
import snippet_ezc3d as snipC3D
import ezc3d
import numpy as np
import snip_h5py as snipH5
from scipy.signal import butter, filtfilt
import combinaison_camera



def reorient_marker_less(point):
    point_reorient = np.zeros(point.shape)
    # change ML orientation to be the same as ref
    point_reorient[0, :] = point[2, :] / 1000
    point_reorient[1, :] = point[0, :] / 1000
    point_reorient[2, :] = point[1, :] / 1000
    return point_reorient

def comparaisonto_mid_point():
    pass

def transform_zeros_to_nan(data):
    for i in range(data.shape[1]):
        if data[0, i] == 0.0 and data[1, i] == 0.0 and data[2, i] == 0.0:
            data[:, i] = np.nan
    return data

def calculate_percentage_nan(array):
    total_elements = array.size
    nan_elements = np.isnan(array).sum()
    percentage_nan = (nan_elements / total_elements) * 100
    return percentage_nan

def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data, axis=1)
    return y

path_to_data_labelled = Path("E:/Argos/Processing/C3D_labelled")
path_to_pose3d = Path("E:/Argos/Processing/Pose3d")
folder_data = Path("./Comparaison_3D")
# check if the folder_data exist
if not folder_data.exists():
    folder_data.mkdir()

# Generate 3d_to_2d hdf5 ------------------------------------------------

subjects_names = ["Sujet_000", "Sujet_001", "Sujet_002", "Sujet_003","Sujet_007", ]
sujet_to_list_task = {
        "Sujet_000": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_001": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_002": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_001", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_003": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_002", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_007": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"]}

camera_configurations = combinaison_camera.generate()

# Comparaison with data form mmpose ------------------------------------------------
list_model = ["all_body_hrnet_coco_dark_coco_hdf5","all_body_resnet_hdf5","all_body_rtm_coktail_14_hdf5"]
list_model = ["all_body_rtm_coktail_14_hdf5"]
# keypoints = reduce_whole_body_coco_keypoints()
# keypoints = {value: key for key, value in keypoints.items()}
points_to_compare = {
        "L_SJC" :"L_shoulder",
        "R_SJC": "R_shoulder",
        "L_EJC": "L_elbow",
        "R_EJC": "R_elbow",
        "L_WJC": "L_wrist",
        "R_WJC": "R_wrist"}

fq_file_c3d = 120
subject_to_fq_file_video = {"Sujet_000": 120, "Sujet_001": 60,
                            "Sujet_002": 60, "Sujet_003": 60,
                            "Sujet_007": 60}

# generation of 3d c3d file with center done in comparaison_2D.py
dict_data = dict()
dict_data_percentage = dict()
for name_config, list_camera in camera_configurations.items():
    dict_data[name_config] = dict()
    dict_data_percentage[name_config] = dict()
    for model in list_model:
        print(model)
        dict_data[name_config][model] = dict()
        dict_data_percentage[name_config][model] = dict()
        for subject in subjects_names:
            print(subject)
            dict_data[name_config][model] [subject] = dict()
            dict_data_percentage[name_config][model][subject] = dict()
            list_task = sujet_to_list_task[subject]
            for task in list_task:
                print(task)
                a=1
                name_c3d = f"{task}.c3d"
                path_to_c3d_ref = path_to_data_labelled / subject / "with_center" / name_c3d
                path_to_c3d_ML = path_to_pose3d / name_config / model / subject  / name_c3d
                # just read the two file
                c3d_ref = ezc3d.c3d(str(path_to_c3d_ref))
                c3d_ML = ezc3d.c3d(str(path_to_c3d_ML))
                points_data_ref, points_name_ref, points_ind_ref = snipC3D.get_points_ezc3d(c3d_ref)
                points_data_ML, points_name_ML, points_ind_ML = snipC3D.get_points_ezc3d(c3d_ML)
                dict_distance = dict()
                dict_percentage_nan = dict()
                fq_video = subject_to_fq_file_video[subject]
                for name_point_ref,name_point_ML in points_to_compare.items():
                    dict_distance[name_point_ref] = dict()
                    ref = points_data_ref[:, points_ind_ref[name_point_ref], ::int(fq_file_c3d/fq_video)]
                    # let s filter the point ML with a 5Hz filter butterwotrt
                    #ref = butter_lowpass_filter(ref, 5, fq_file_c3d, order=4)

                    ML = points_data_ML[:, points_ind_ML[name_point_ML], :]
                    ML = transform_zeros_to_nan(ML)
                    #ML = butter_lowpass_filter(points_data_ML[:,points_ind_ML[name_point_ML],:],5, fq_video, order=4)
                    ML_orient  = reorient_marker_less(ML)

                    # define the smaller array
                    if ref.shape[1] < ML_orient.shape[1]:
                        ML_orient = ML_orient[:,:ref.shape[1]]
                    else:
                        ref = ref[:,:ML_orient.shape[1]]
                    # calculate distance between two point
                    vector_distance = ref - ML_orient
                    dict_distance[name_point_ref]["norm"] = np.linalg.norm(vector_distance,axis=0)
                    dict_distance[name_point_ref]["X"] = vector_distance[0,:]
                    dict_distance[name_point_ref]["Y"] = vector_distance[1,:]
                    dict_distance[name_point_ref]["Z"] = vector_distance[2,:]

                    # calculate the percentage of Nan
                    dict_percentage_nan[name_point_ref] = calculate_percentage_nan(ML_orient)



                ref_LHM = points_data_ref[:, points_ind_ref["L_HMJC"], ::int(fq_file_c3d / fq_video)]
                ref_RHM = points_data_ref[:, points_ind_ref["R_HMJC"], ::int(fq_file_c3d / fq_video)]
                ML_RHM2 = points_data_ML[:, points_ind_ML["R_MCP_index"], :]
                ML_RHM5 = points_data_ML[:, points_ind_ML["R_MCP_little"], :]
                ML_LHM2 = points_data_ML[:, points_ind_ML["L_MCP_index"], :]
                ML_LHM5 = points_data_ML[:, points_ind_ML["L_MCP_little"], :]
                # for each frame i when the point[:,i]=[0.0,0.0,0.0] transform them to Nan
                ML_RHM2 = transform_zeros_to_nan(ML_RHM2)
                ML_RHM5 = transform_zeros_to_nan(ML_RHM5)
                ML_LHM2 = transform_zeros_to_nan(ML_LHM2)
                ML_LHM5 = transform_zeros_to_nan(ML_LHM5)

                # filter all point
                # ref_LHM = butter_lowpass_filter(ref_LHM, 5, fq_file_c3d, order=4)
                # ref_RHM = butter_lowpass_filter(ref_RHM, 5, fq_file_c3d, order=4)
                # ML_RHM2 = butter_lowpass_filter(ML_RHM2, 5, fq_video, order=4)
                # ML_RHM5 = butter_lowpass_filter(ML_RHM5, 5, fq_video, order=4)
                # ML_LHM2 = butter_lowpass_filter(ML_LHM2, 5, fq_video, order=4)
                # ML_LHM5 = butter_lowpass_filter(ML_LHM5, 5, fq_video, order=4)

                ML_RHM = (ML_RHM2 + ML_RHM5) / 2
                ML_LHM = (ML_LHM2 + ML_LHM5) / 2
                # define min size
                min_size_L = min(ref_LHM.shape[1],ML_LHM.shape[1])
                min_size_R = min(ref_RHM.shape[1],ML_RHM.shape[1])

                vector_dist_R_hand = ref_RHM[:,:min_size_R] - reorient_marker_less(ML_RHM[:,:min_size_R])
                vector_dist_L_hand = ref_LHM[:,:min_size_L] - reorient_marker_less(ML_LHM[:,:min_size_L])
                dict_distance["R_HMJC"] = dict()
                dict_distance["L_HMJC"] = dict()

                dict_distance["R_HMJC"]["norm"] = np.linalg.norm(ref_RHM[:,:min_size_R] - reorient_marker_less(ML_RHM[:,:min_size_R]),axis=0)
                dict_distance["R_HMJC"]["X"] = vector_dist_R_hand[0,:]
                dict_distance["R_HMJC"]["Y"] = vector_dist_R_hand[1,:]
                dict_distance["R_HMJC"]["Z"] = vector_dist_R_hand[2,:]

                dict_distance["L_HMJC"]["norm"] = np.linalg.norm(ref_LHM[:,:min_size_L] - reorient_marker_less(ML_LHM[:,:min_size_L]),axis=0)
                dict_distance["L_HMJC"]["X"] = vector_dist_L_hand[0,:]
                dict_distance["L_HMJC"]["Y"] = vector_dist_L_hand[1,:]
                dict_distance["L_HMJC"]["Z"] = vector_dist_L_hand[2,:]

                dict_percentage_nan["R_HMJC"] = calculate_percentage_nan(reorient_marker_less(ML_RHM))
                dict_percentage_nan["L_HMJC"] = calculate_percentage_nan(reorient_marker_less(ML_LHM))

                dict_data[name_config][model][subject][task] = dict_distance
                dict_data_percentage[name_config][model][subject][task] = dict_percentage_nan



list_points = [["L_SJC","R_SJC"],["L_EJC","R_EJC"],["L_WJC","R_WJC"],["L_HMJC","R_HMJC"]]
key_points = ["SJC","EJC","WJC","HMJC"]

dict_final = dict()
dict_final_percentage = dict()
for name_config, list_camera in camera_configurations.items():
    dict_final[name_config]=dict()
    dict_final_percentage[name_config] = dict()
    for model in list_model:
        dict_final[name_config][model]  = dict()
        dict_final_percentage[name_config][model] = dict()
        for ind_points,points in enumerate(list_points):
            points_name = key_points[ind_points]
            dict_final[name_config][model][points_name] = dict()   #
            dict_final[name_config][model][points_name]["norm"] = np.empty((1,))
            dict_final[name_config][model][points_name]["X"] = np.empty((1,))
            dict_final[name_config][model][points_name]["Y"] = np.empty((1,))
            dict_final[name_config][model][points_name]["Z"] = np.empty((1,))

            percentage = []
            for point in points:

                for subject in subjects_names:
                    for task in sujet_to_list_task[subject]:
                        percentage.append(dict_data_percentage[name_config][model][subject][task][point])
                        if dict_final[name_config][model][points_name]["norm"].shape[0] == 1:
                            dict_final[name_config][model][points_name]["norm"] = dict_data[name_config][model][subject][task][point]["norm"]
                            dict_final[name_config][model][points_name]["X"] = dict_data[name_config][model][subject][task][point]["X"]
                            dict_final[name_config][model][points_name]["Y"] = dict_data[name_config][model][subject][task][point]["Y"]
                            dict_final[name_config][model][points_name]["Z"] = dict_data[name_config][model][subject][task][point]["Z"]
                        else:
                            dict_final[name_config][model][points_name]["norm"] = np.append(dict_final[name_config][model][points_name]["norm"], dict_data[name_config][model][subject][task][point]["norm"])
                            dict_final[name_config][model][points_name]["X"] = np.append(dict_final[name_config][model][points_name]["X"], dict_data[name_config][model][subject][task][point]["X"])
                            dict_final[name_config][model][points_name]["Y"] = np.append(dict_final[name_config][model][points_name]["Y"], dict_data[name_config][model][subject][task][point]["Y"])
                            dict_final[name_config][model][points_name]["Z"] = np.append(dict_final[name_config][model][points_name]["Z"], dict_data[name_config][model][subject][task][point]["Z"])

            dict_final_percentage[name_config][model][points_name] = np.mean(percentage)
# save the dict_final
snipH5.save_dictionary_to_hdf(dict_final, folder_data / "comparaison_final_3d.h5")
# save the dict_data_percentage
snipH5.save_dictionary_to_hdf(dict_final_percentage, folder_data / "comparaison_percentage_3d.h5")
list_parameters = ["norm","X","Y","Z"]
# calculate the absolut mean and std of the data for each combinaison model, camera, points
dict_mean_std = dict()
for name_config, list_camera in camera_configurations.items():
    dict_mean_std[name_config] = dict()
    for model in list_model:
        dict_mean_std[name_config][model] = dict()
        for point in key_points:
            dict_mean_std[name_config][model][point] = dict()
            for name_param in list_parameters:
                dict_mean_std[name_config][model][point][name_param] = dict()
                mean = np.nanmean(np.abs(dict_final[name_config][model][point][name_param]),axis=0)
                std = np.nanstd(np.abs(dict_final[name_config][model][point][name_param]),axis=0)
                min = np.nanmin(np.abs(dict_final[name_config][model][point][name_param]),axis=0)
                max = np.nanmax(np.abs(dict_final[name_config][model][point][name_param]),axis=0)

                dict_mean_std[name_config][model][point][name_param]["mean"] = mean
                dict_mean_std[name_config][model][point][name_param]["std"] = std
                dict_mean_std[name_config][model][point][name_param]["min"] = min
                dict_mean_std[name_config][model][point][name_param]["max"] = max
# save the mean and std
snipH5.save_dictionary_to_hdf(dict_mean_std, folder_data/"mean_std_3d.h5")