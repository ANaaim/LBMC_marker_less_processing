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


def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data, axis=1)
    return y

# def comparaison_two_data_set(path_to_mmpose_data,path_to_ref):
#     model_data = snipH5.load_dictionary_from_hdf(path_to_mmpose_data)
#     model_ref = snipH5.load_dictionary_from_hdf(path_to_ref)
#
#     # get all camera
#     cameras_name = model_ref.keys()
#     dict_comp = dict()
#     for camera in cameras_name:
#         print(f"Camera {camera}")
#         dict_comp[camera] = dict()
#         for key in new_dict.keys():
#             print(f"Key {key}")
#             # print(model_ref[camera][key])
#             # print(model_data[camera][new_dict[key]])
#             # print(model_ref[camera][key] - model_data[camera][key])
#             # get the value of nb frame
#             nb_frame_ref = model_ref[camera][key].shape[0]
#             nb_frame_model_data = model_data[camera][new_dict[key]].shape[0]
#             # use the min value of the two
#             min_nb_frame = min(nb_frame_ref, nb_frame_model_data)
#             dict_comp[camera][key] = np.linalg.norm(model_ref[camera][key][:min_nb_frame, 0:2] - model_data[camera][new_dict[key]][
#                                                                                 :min_nb_frame, 0:2],axis=1)
#         # specific comp
#         # R mid hand
#         R_mid_hand_model = (model_data[camera][new_dict["R_HM2"]][:min_nb_frame, :] + model_data[camera][
#                                                                                           new_dict["R_HM5"]][
#                                                                                       :min_nb_frame, :]) / 2
#         dict_comp[camera]["R_HMJC"] = np.linalg.norm(model_ref[camera]["R_HMJC"][:min_nb_frame, 0:2] - R_mid_hand_model[:,0:2],axis=1)
#         # L mid hand
#         L_mid_hand_model = (model_data[camera][new_dict["L_HM2"]][:min_nb_frame, :] + model_data[camera][
#                                                                                           new_dict["L_HM5"]][
#                                                                                       :min_nb_frame, :]) / 2
#         dict_comp[camera]["L_HMJC"] = np.linalg.norm(model_ref[camera]["L_HMJC"][:min_nb_frame, 0:2] - L_mid_hand_model[:,0:2],axis=1)
#
#     return dict_comp


path_to_data_labelled = Path("E:/Argos/Processing/C3D_labelled")
path_to_pose3d = Path("E:/Argos/Processing/Pose3d")

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
for name_config, list_camera in camera_configurations.items():
    dict_lvl_model = dict()
    for model in list_model:
        print(model)
        dict_lvl_model[model] = dict()
        for subject in subjects_names:
            print(subject)
            dict_lvl_model[model][subject] = dict()
            list_task = sujet_to_list_task[subject]
            for task in list_task:
                print(task)
                a=1
                name_c3d = f"{task}.c3d"
                path_to_c3d_ref = path_to_data_labelled / subject / "with_center" / name_c3d
                path_to_c3d_ML = path_to_pose3d / model / subject  / name_c3d
                # just read the two file
                c3d_ref = ezc3d.c3d(str(path_to_c3d_ref))
                c3d_ML = ezc3d.c3d(str(path_to_c3d_ML))
                points_data_ref, points_name_ref, points_ind_ref = snipC3D.get_points_ezc3d(c3d_ref)
                points_data_ML, points_name_ML, points_ind_ML = snipC3D.get_points_ezc3d(c3d_ML)
                dict_distance = dict()
                fq_video = subject_to_fq_file_video[subject]
                for name_point_ref,name_point_ML in points_to_compare.items():
                    ref = points_data_ref[:, points_ind_ref[name_point_ref], ::int(fq_file_c3d/fq_video)]
                    # let s filter the point ML with a 5Hz filter butterwotrt
                    ref = butter_lowpass_filter(ref, 5, fq_file_c3d, order=4)

                    ML = butter_lowpass_filter(points_data_ML[:,points_ind_ML[name_point_ML],:],5, fq_video, order=4)
                    ML_orient  = reorient_marker_less(ML)

                    # define the smaller array
                    if ref.shape[1] < ML_orient.shape[1]:
                        ML_orient = ML_orient[:,:ref.shape[1]]
                    else:
                        ref = ref[:,:ML_orient.shape[1]]
                    # calculate distance between two point
                    dict_distance[name_point_ref] = np.linalg.norm(ref - ML_orient,axis=0)
                ref_LHM = points_data_ref[:, points_ind_ref["L_HMJC"], ::int(fq_file_c3d / fq_video)]
                ref_RHM = points_data_ref[:, points_ind_ref["R_HMJC"], ::int(fq_file_c3d / fq_video)]
                ML_RHM2 = points_data_ML[:, points_ind_ML["R_MCP_index"], :]
                ML_RHM5 = points_data_ML[:, points_ind_ML["R_MCP_little"], :]
                ML_LHM2 = points_data_ML[:, points_ind_ML["L_MCP_index"], :]
                ML_LHM5 = points_data_ML[:, points_ind_ML["L_MCP_little"], :]
                # filter all point
                ref_LHM = butter_lowpass_filter(ref_LHM, 5, fq_file_c3d, order=4)
                ref_RHM = butter_lowpass_filter(ref_RHM, 5, fq_file_c3d, order=4)
                ML_RHM2 = butter_lowpass_filter(ML_RHM2, 5, fq_video, order=4)
                ML_RHM5 = butter_lowpass_filter(ML_RHM5, 5, fq_video, order=4)
                ML_LHM2 = butter_lowpass_filter(ML_LHM2, 5, fq_video, order=4)
                ML_LHM5 = butter_lowpass_filter(ML_LHM5, 5, fq_video, order=4)



                ML_RHM = (ML_RHM2 + ML_RHM5) / 2
                ML_LHM = (ML_LHM2 + ML_LHM5) / 2
                # define min size
                min_size_L = min(ref_LHM.shape[1],ML_LHM.shape[1])
                min_size_R = min(ref_RHM.shape[1],ML_RHM.shape[1])

                dict_distance["R_HMJC"] = np.linalg.norm(ref_RHM[:,:min_size_R] - reorient_marker_less(ML_RHM[:,:min_size_R]),axis=0)
                dict_distance["L_HMJC"] = np.linalg.norm(ref_LHM[:,:min_size_L] - reorient_marker_less(ML_LHM[:,:min_size_L]),axis=0)


                dict_lvl_model[model][subject][task] = dict_distance


list_points = [["L_SJC","R_SJC"],["L_EJC","R_EJC"],["L_WJC","R_WJC"],["L_HMJC","R_HMJC"]]
key_points = ["SJC","EJC","WJC","HMJC"]

dict_final = dict()
for model in list_model:
    dict_final[model] = dict()
    for ind_points,points in enumerate(list_points):
        points_name = key_points[ind_points]
        dict_final[model][points_name] =  np.empty((1,))  #
        for point in points:
            for subject in subjects_names:
                for task in sujet_to_list_task[subject]:
                    if dict_final[model][points_name].shape[0] == 1:
                        dict_final[model][points_name] = dict_lvl_model[model][subject][task][point]
                    else:
                        dict_final[model][points_name] = np.append(dict_final[model][points_name],dict_lvl_model[model][subject][task][point])
    # save the dict_final
snipH5.save_dictionary_to_hdf(dict_final, "comparaison_final_3d.h5")
# calculate the absolut mean and std of the data for each combinaison model, camera, points
dict_mean_std = dict()
for model in list_model:
    dict_mean_std[model] = dict()
    for points in key_points:
        mean = np.nanmean(np.abs(dict_final[model][points]),axis=0)
        std = np.nanstd(np.abs(dict_final[model][points]),axis=0)
        min = np.nanmin(np.abs(dict_final[model][points]),axis=0)
        max = np.nanmax(np.abs(dict_final[model][points]),axis=0)
        dict_mean_std[model][points] = [np.nanmean(np.abs(dict_final[model][points]),axis=0),np.nanstd(np.abs(dict_final[model][points]),axis=0)]

# save the mean and std
snipH5.save_dictionary_to_hdf(dict_mean_std, "mean_std_3d.h5")


#
# plot box plot for each model and joint
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Préparer les données pour le box plot
data = []
for model in list_model:
    for points in key_points:
        for value in dict_final[model][points]:
            data.append([model, points, value*1000])

# def remove_outliers(df, column):
#     Q1 = df[column].quantile(0.25)
#     Q3 = df[column].quantile(0.75)
#     IQR = Q3 - Q1
#     lower_bound = Q1 - 1.5 * IQR
#     upper_bound = Q3 + 1.5 * IQR
#     return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Example usage
df = pd.DataFrame(data, columns=['Model', 'Joint', 'Value'])
# df_cleaned = remove_outliers(df, 'Value')

# Plot the cleaned data
plt.figure(figsize=(15, 10))
sns.boxplot(x='Joint', y='Value', hue='Model', data=df,  showfliers=False)
plt.title('Box plots for all models and joints (outliers removed)')
plt.savefig("boxplots_all_models_joints_cleaned.svg",format="svg")
plt.show()