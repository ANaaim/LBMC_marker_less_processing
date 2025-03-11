from pathlib import Path
import ezc3d
import snippet_ezc3d as snipc3d
import snip_h5py as snipH5
import joint_center_calculation_montreal as joint_calc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_UL_joitn_centers(path_to_data):
    path_to_data_str = str(path_to_data)
    acq = ezc3d.c3d(path_to_data_str)

    points_data, points_name, points_ind = snipc3d.get_points_ezc3d(acq)
    # get the center of the joints
    R_SJC, L_SJC = joint_calc.shoulder_RAB(points_data, points_ind)
    R_EJC, L_EJC = joint_calc.elbow_midpoint(points_data, points_ind)
    R_WJC, L_WJC = joint_calc.wrist_midpoint(points_data, points_ind)
    R_HMJC, L_HMJC = joint_calc.hand_midpoint(points_data, points_ind)

    points_to_add = dict()
    points_to_add["R_SJC"] = R_SJC
    points_to_add["L_SJC"] = L_SJC
    points_to_add["R_EJC"] = R_EJC
    points_to_add["L_EJC"] = L_EJC
    points_to_add["R_WJC"] = R_WJC
    points_to_add["L_WJC"] = L_WJC
    points_to_add["R_HMJC"] = R_HMJC
    points_to_add["L_HMJC"] = L_HMJC

    snipc3d.add_point_from_dictionary(acq, points_to_add)
    # test if the folder with_center exists in the folder
    path_to_data_center = path_to_data.parent / "with_center"
    if not path_to_data_center.exists():
        path_to_data_center.mkdir()
    # save the file with the same name in the folder with_center
    path_to_new_file = path_to_data_center / path_to_data.name
    acq.write(str(path_to_new_file))

def generate_3d_to_2d_hdf5(path_to_data_labelled, subjects_names, sujet_to_list_task):

    for subject in subjects_names:
        task_to_process = sujet_to_list_task[subject]
        for task in task_to_process:
            # Step 1 export data with the center of the joints from the c3d labelled
            filename = task + ".c3d"
            path_to_data_subject = path_to_data_labelled / subject / filename
            print(path_to_data_subject)
            compute_UL_joitn_centers(path_to_data_subject)


def reduce_whole_body_coco_keypoints():
    keypoints = {
            0: "nose",
            1: "left_eye",
            2: "right_eye",
            3: "left_ear",
            4: "right_ear",
            5: "left_shoulder",
            6: "right_shoulder",
            7: "left_elbow",
            8: "right_elbow",
            9: "left_wrist",
            10: "right_wrist",
            11: "left_hip",
            12: "right_hip",
            91: "left_base_hand",
            92: "left_CMC_thumb",
            93: "left_MCP_thumb",
            96: "left_MCP_index",
            100: "left_MCP_middle",
            104: "left_MCP_ring",
            108: "left_MCP_little",
            112: "right_base_hand",
            114: "right_MCP_thumb",
            117: "right_MCP_index",
            121: "right_MCP_middle",
            125: "right_MCP_ring",
            129: "right_MCP_little",
        }

    return keypoints

def comparaison_two_data_set(path_to_mmpose_data,path_to_ref):
    model_data = snipH5.load_dictionary_from_hdf(path_to_mmpose_data)
    model_ref = snipH5.load_dictionary_from_hdf(path_to_ref)

    # get all camera
    cameras_name = model_ref.keys()
    dict_comp = dict()
    for camera in cameras_name:
        print(f"Camera {camera}")
        dict_comp[camera] = dict()
        for key in new_dict.keys():
            print(f"Key {key}")
            # print(model_ref[camera][key])
            # print(model_data[camera][new_dict[key]])
            # print(model_ref[camera][key] - model_data[camera][key])
            # get the value of nb frame
            nb_frame_ref = model_ref[camera][key].shape[0]
            nb_frame_model_data = model_data[camera][new_dict[key]].shape[0]
            # use the min value of the two
            min_nb_frame = min(nb_frame_ref, nb_frame_model_data)

            dict_comp[camera][key] = np.zeros((min_nb_frame, 2))
            dict_comp[camera][key][:,0] = np.linalg.norm(model_ref[camera][key][:min_nb_frame, 0:2] - model_data[camera][new_dict[key]][
                                                                                :min_nb_frame, 0:2],axis=1)
            dict_comp[camera][key][:, 1] = model_data[camera][new_dict[key]][:min_nb_frame, 2]
        # specific comp
        # R mid hand
        R_mid_hand_model = (model_data[camera][new_dict["R_HM2"]][:min_nb_frame, :] + model_data[camera][
                                                                                          new_dict["R_HM5"]][
                                                                                      :min_nb_frame, :]) / 2
        dict_comp[camera]["R_HMJC"] = np.zeros((min_nb_frame, 2))
        dict_comp[camera]["R_HMJC"][:,0] = np.linalg.norm(model_ref[camera]["R_HMJC"][:min_nb_frame, 0:2] - R_mid_hand_model[:,0:2],axis=1)
        dict_comp[camera]["R_HMJC"][:, 1] = dict_comp[camera]["R_HMJC"][:,1] = (model_data[camera][new_dict["R_HM5"]][:min_nb_frame, 2] + model_data[camera][new_dict["R_HM5"]][:min_nb_frame, 2])/2
        # L mid hand
        L_mid_hand_model = (model_data[camera][new_dict["L_HM2"]][:min_nb_frame, :] + model_data[camera][
                                                                                          new_dict["L_HM5"]][
                                                                                      :min_nb_frame, :]) / 2
        dict_comp[camera]["L_HMJC"] = np.zeros((min_nb_frame,2))
        dict_comp[camera]["L_HMJC"][:,0] = np.linalg.norm(model_ref[camera]["L_HMJC"][:min_nb_frame, 0:2] - L_mid_hand_model[:,0:2],axis=1)
        dict_comp[camera]["L_HMJC"][:,1] = (model_data[camera][new_dict["L_HM5"]][:min_nb_frame, 2] + model_data[camera][new_dict["L_HM5"]][:min_nb_frame, 2])/2

    return dict_comp

if __name__ == "__main__":
    path_to_data_labelled = Path("E:/Argos/Processing/C3D_labelled")
    path_to_pose2d = Path("E:/Argos/Processing/Pose2d")
    path_to_export = Path("./Comparaison_2D")
    # Generate 3d_to_2d hdf5 ------------------------------------------------

    subjects_names = ["Sujet_000", "Sujet_001", "Sujet_002", "Sujet_003", "Sujet_004", "Sujet_005", "Sujet_006", "Sujet_007"]
    #task_to_process = ["16-comb-hair.c3d"]
    # TODO : retrained all model sujet_005 17-hand-to-back_001
    sujet_to_list_task = {
        "Sujet_000": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_001": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_002": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_001", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_003": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_002", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_004": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_005": ["01-eat-yoghurt_001", "02-cut-food", "13-playdoe", "06-drawing_001", "16-comb-hair"],# "17-hand-to-back_001"],
        "Sujet_006": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_007": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"]}

    # sujet_to_list_task = {
    #     "Sujet_000": ["06-drawing"],
    #     "Sujet_001": ["06-drawing"],
    #     "Sujet_002": ["06-drawing"],
    #     "Sujet_003": ["06-drawing"],
    #     "Sujet_007": ["06-drawing"]}
    generate_3d_to_2d_hdf5(path_to_data_labelled, subjects_names, sujet_to_list_task)

    # Comparaison with data form mmpose ------------------------------------------------

    list_model = ["all_body_hrnet_coco_dark_coco_hdf5","all_body_resnet_hdf5","all_body_rtm_coktail_14_hdf5"]

    keypoints = reduce_whole_body_coco_keypoints()
    keypoints = {value: key for key, value in keypoints.items()}
    keypoints_coco_to_data = {
        "L_SJC" :"left_shoulder",
        "R_SJC": "right_shoulder",
        "L_EJC": "left_elbow",
        "R_EJC": "right_elbow",
        "L_WJC": "left_wrist",
        "R_WJC": "right_wrist",
        "R_HM2": "right_MCP_index",
        "L_HM2": "left_MCP_index",
        "R_HM5": "right_MCP_little",
        "L_HM5": "left_MCP_little",
    }
    # make the dictionary giving the link from the coco keypoint to the data keypoint
    new_dict = dict()
    for key in keypoints_coco_to_data:
        new_dict[key] = f"{keypoints[keypoints_coco_to_data[key]]:04}"
    print(new_dict)

    dict_lvl_model = dict()
    for model in list_model:
        dict_level_subject = dict()
        for subject in subjects_names:
            tasks = sujet_to_list_task[subject]
            dict_level_task = dict()
            for task in tasks:
                # compare two hdf5
                filename = task + ".h5"
                path_to_mmpose_data = path_to_pose2d / model / subject / task /filename
                path_to_ref = path_to_pose2d / "3D_to_2D" / subject / task /filename

                dict_level_task[task] = comparaison_two_data_set(path_to_mmpose_data,path_to_ref)
            dict_level_subject[subject] = dict_level_task
        dict_lvl_model[model] = dict_level_subject

    snipH5.save_dictionary_to_hdf(dict_lvl_model, path_to_export/ "comparaison.h5")
    # fusion of the data
    # Model->Camera->Points

    list_camera = dict_lvl_model[list_model[0]][subjects_names[0]][sujet_to_list_task[subjects_names[0]][0]].keys()
    list_camera = [["M11463"],['M11141','M11458'],['M11139','M11459'],['M11140','M11461'],['M11462']]
    name_camera = ["A","B","C","D","E"]

    list_points = [["L_SJC","R_SJC"],["L_EJC","R_EJC"],["L_WJC","R_WJC"],["L_HMJC","R_HMJC"]]
    key_points = ["SJC","EJC","WJC","HMJC"]
    dict_final = dict()
    for model in list_model:
        dict_final[model] = dict()
        for ind_group_camera, cameras in enumerate(list_camera):
            group_camera_name = name_camera[ind_group_camera]
            dict_final[model][group_camera_name] = dict()
            for camera in cameras:
                for ind_points,points in enumerate(list_points):
                    points_name = key_points[ind_points]
                    dict_final[model][group_camera_name][points_name] =  np.empty((1,2))  #
                    for point in points:
                        for subject in subjects_names:
                            for task in sujet_to_list_task[subject]:
                            # We append result to the dict final
                                # test if dict_final[model][camera][point][subject] exists if not we create it else we append the value at the end
                                # if
                                #     dict_final[model][camera][points_name] = dict_lvl_model[model][subject][task][camera][point]
                                # else:
                                nb_point = dict_lvl_model[model][subject][task][camera][point].shape[0]
                                dict_final[model][group_camera_name][points_name] = np.append(dict_final[model][group_camera_name][points_name],
                                                                                              dict_lvl_model[model][subject][task][camera][point],axis=0)

    # save the dict_final
    snipH5.save_dictionary_to_hdf(dict_final,  path_to_export/ "comparaison_final.h5")
    # calculate the absolut mean and std of the data for each combinaison model, camera, points
    dict_mean_std = dict()
    for model in list_model:
        dict_mean_std[model] = dict()
        for camera in name_camera:
            dict_mean_std[model][camera] = dict()
            for points in key_points:
                dict_mean_std[model][camera][points] = [np.nanmean(np.abs(dict_final[model][camera][points]),axis=0),np.nanstd(np.abs(dict_final[model][camera][points]),axis=0)]

    # save the mean and std
    snipH5.save_dictionary_to_hdf(dict_mean_std,  path_to_export/ "mean_std.h5")
    #snipH5.save_dictionary_to_hdf(dict_std, "std.h5")
    # Convert the dict_mean_std to a DataFrame
    # Convert the dict_mean_std to a DataFrame
    data = []
    for model, cameras in dict_mean_std.items():
        for camera, points in cameras.items():
            for point, values in points.items():
                mean, std = values
                data.append([model, camera, point, mean, std])

    df = pd.DataFrame(data, columns=['Model', 'Camera', 'Point', 'Mean', 'Std'])

    # Pivot the DataFrame to get the desired format
    df_pivot = df.pivot_table(index='Point', columns=['Camera', 'Model'], values=['Mean', 'Std'])

    # Flatten the multi-level columns
    df_pivot.columns = [f'{col[1]}_{col[0]}' for col in df_pivot.columns]

    # Reorder columns to place each mean next to its corresponding std
    ordered_columns = []
    for col in df_pivot.columns:
        if 'Mean' in col:
            std_col = col.replace('Mean', 'Std')
            ordered_columns.append(col)
            ordered_columns.append(std_col)

    df_pivot = df_pivot[ordered_columns]

    # Save the DataFrame to an Excel file
    df_pivot.to_excel('mean_std_ordered.xlsx')









