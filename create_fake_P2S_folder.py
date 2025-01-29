from pathlib import Path
import shutil
import snip_h5py as sh5
import save_and_export as se
import combinaison_camera
from LBMC_marker_less.utils.extract_all_acquisition_from_folder import extract_all_acquisition_from_folder
import toml
from Pose2Sim import Pose2Sim
import os
import concurrent.futures

def triangulate_acquisition(acquisition, subject, formatted_data_path_by_subject, config_dict_P2S):
    print(f"Triangulating {subject} for {acquisition}")
    # do a copy of the dictionary
    new_dict = config_dict_P2S.copy()
    new_dict["project"]["project_dir"] = os.path.join(formatted_data_path_by_subject, acquisition)
    Pose2Sim.triangulation(config_dict_P2S)

def generate_text_for_config_P2S_from_hdf5(path_to_hdf5):
    # we extract all the point name from the hdf5 file
    data = sh5.load_dictionary_from_hdf(path_to_hdf5)
    list_camera = []
    list_points = []
    # get the list of camera name which are the first key of the dictionary
    for key_camera in data:
        list_camera.append(key_camera)


    for key in data[list_camera[0]]:
        list_points.append(key)
    # we generate the text for the config file
    # it should begin with the following lines
    # [pose.CUSTOM]
    # name = "Model__mmpose"
    # id = "None"
    # the caracter " should be added to the name

    text = f"[pose.CUSTOM]\n"
    text += f"name = \"Model__mmpose\"\n"
    text += "id = \"None\"\n"
    for i, point in enumerate(list_points):
        text += f"[[pose.CUSTOM.children]]\n"
        text += f"id = {i}\n"
        text += f"name = \"{point}\"\n"
    return text

def generate_text_for_config_P2S_from_dict(dict_keypoint_to_name):
    # we extract all the point name from the hdf5 file
    list_camera = []
    list_points = []
    # get the list of camera name which are the first key of the dictionary
    for key,value in dict_keypoint_to_name.items():
        list_points.append(value)

    # we generate the text for the config file
    # it should begin with the following lines
    # [pose.CUSTOM]
    # name = "Model__mmpose"
    # id = "None"
    # the caracter " should be added to the name

    text = f"[pose.CUSTOM]\n"
    text += f"name = \"Model__mmpose\"\n"
    text += "id = \"None\"\n"
    for i, point in enumerate(list_points):
        text += f"[[pose.CUSTOM.children]]\n"
        text += f"id = {i}\n"
        text += f"name = \"{point}\"\n"
    return text

def copy_c3d_remove_fake_P2S_folder(temp_folder, pose3d_folder, name_config_camera, model, subject, task):
    source_folder = temp_folder / model / subject / task / "pose-3d"
    source_folder_to_be_removed = temp_folder / model / subject / task
    destination_folder = pose3d_folder / name_config / model / subject

    # Ensure the destination folder exists
    destination_folder.mkdir(parents=True, exist_ok=True)
    c3d_files = list(source_folder.glob("*.c3d"))
    if len(c3d_files) != 1:
        raise ValueError(f"Expected exactly one .c3d file in {source_folder}, but found {len(c3d_files)}")

    c3d_file = c3d_files[0]
    destination_file = destination_folder / f"{task}.c3d"
    shutil.copy(c3d_file, destination_file)
    shutil.rmtree(source_folder_to_be_removed)

def read_and_export_toml_less_camera(file_path, blocks_to_export,output_file_path):
    # Read the TOML file
    with open(file_path, 'r') as file:
        data = toml.load(file)

    # Extract the required blocks and metadata
    extracted_data = {}
    for block in blocks_to_export:
        if block in data:
            extracted_data[block] = data[block]

    # Add metadata
    if 'metadata' in data:
        extracted_data['metadata'] = data['metadata']

    # Write the extracted data to the output file
    with open(output_file_path, 'w') as file:
        toml.dump(extracted_data, file)


formatted_folder = Path("E:/Argos/Processing/Formatted")
pose2d_folder = Path("E:/Argos/Processing/Pose2d")
pose3d_folder = Path("E:/Argos/Processing/Pose3d_demo")
# currently it seems that exporting small json on ssd create very large files'
temp_folder = Path("C:/Users/User/Documents/Alexandre/Github/LBMC_marker_less_processing/data_montreal/temp_P2S")

# These could be obtained directly from exploring the folder pose2d.
subject_to_process = ["Sujet_000","Sujet_001","Sujet_002","Sujet_003","Sujet_007"]
model_to_process = ["all_body_rtm_coktail_14_hdf5"]#,"all_body_resnet_hdf5","all_body_hrnet_coco_dark_coco_hdf5"]
model_correction_confidence = [10,1,1]
#model_to_process = ["all_body_resnet_hdf5","all_body_hrnet_coco_dark_coco_hdf5"]
#model_correction_confidence = [1,1]
#task_to_process = ["13-playdoe_002"]

sujet_to_list_task = {"Sujet_000": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                      "Sujet_001": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                      "Sujet_002": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_001", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                      "Sujet_003": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_002", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                      "Sujet_007": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"]}

# If None all camera will be used
with_group_unique_camera = False
camera_configurations = combinaison_camera.generate(with_group_unique_camera)
# get all the camera configuration that have been processed
# list all folder contained in pose3d_folder as a list
folder_names_already_processed = [f.name for f in pose3d_folder.iterdir() if f.is_dir()]
print(folder_names_already_processed)


for name_config, list_camera in camera_configurations.items():
    if name_config in folder_names_already_processed:
        print(f"Folder {name_config} already processed")
        continue
    for ind_model,model in enumerate(model_to_process):
        for subject in subject_to_process:
            task_to_process = sujet_to_list_task[subject]
            for task in task_to_process:
                print(f"Generating fake folder for  {model} with  {subject} for  {task}")
                # Get the calibration folder
                # knowing the subject we can find the calibration file
                calibration_path = formatted_folder / subject / "calibration" / "Calib_scene.toml"
                new_calibration_path = temp_folder / model / subject / "calibration"
                #test if the new calibration folder exists
                if not new_calibration_path.exists():
                    new_calibration_path.mkdir(parents=True)
                # copy the calibration file in function of the camera to integrate
                if list_camera is not None:
                    read_and_export_toml_less_camera(calibration_path, list_camera, new_calibration_path/"Calib_scene.toml")
                else:
                    shutil.copyfile(calibration_path, new_calibration_path/"Calib_scene.toml")

                # Get the hdf5 files
                filename = task+".h5"
                path_to_hdf5 = pose2d_folder / model/ subject/ task / filename

                # Generate the json from the hdf5 files
                data = sh5.load_dictionary_from_hdf(path_to_hdf5)
                path_to_json = temp_folder / model / subject / task / "pose"
                # test if the folder exists
                if not path_to_json.exists():
                    path_to_json.mkdir(parents=True)


                keypoints_to_process = {
                            "0000": "nose",
                            "0001": "L_eye",
                            "0002": "R_eye",
                            "0003": "L_ear",
                            "0004": "R_ear",
                            "0005": "L_shoulder",
                            "0006": "R_shoulder",
                            "0007": "L_elbow",
                            "0008": "R_elbow",
                            "0009": "L_wrist",
                            "0010": "R_wrist",
                            "0011": "L_hip",
                            "0012": "R_hip",
                            "0091": "L_base_hand",
                            "0093": "L_MCP_thumb",
                            "0096": "L_MCP_index",
                            "0100": "L_MCP_middle",
                            "0104": "L_MCP_ring",
                            "0108": "L_MCP_little",
                            "0112": "R_base_hand",
                            "0114": "R_MCP_thumb",
                            "0117": "R_MCP_index",
                            "0121": "R_MCP_middle",
                            "0125": "R_MCP_ring",
                            "0129": "R_MCP_little",
                        }

                se.export_data_to_json(data, path_to_json,keypoints_to_process,model_correction_confidence[ind_model],list_camera,testing=False)

            #text = generate_text_for_config_P2S(path_to_hdf5)
            text = generate_text_for_config_P2S_from_dict(keypoints_to_process)


            # run P2S : here it can be a generic configuration files as we are only doing the triangulation to generate the 3D points

            #TODO : We should have generate a configuration file with the point at the end adapted from the hdf5 file used.

            config_path_P2S = Path("Config_Checkerboard_Montreal_triangulation_only_without_model.toml")
            new_config_path_P2S = Path("config_P2S_temp_triangulation.toml")
            # Read the existing config file
            with open(config_path_P2S, "r") as file:
                config_content = file.read()
            # Append the generated text to the config content
            new_config_content = config_content + "\n" + text
            # Write the combined content to a new config file
            with open(new_config_path_P2S, "w") as file:
                file.write(new_config_content)

            config_dict_P2S = toml.load(new_config_path_P2S)
            # We do not care about the organized path here as it will not be used
            organized_data_path = None #Path("D:\Argos\Processing\Organized")
            formatted_data_path_by_subject = temp_folder / model / subject

            config_dict_P2S["project"]["calib_folder_name"] = "calibration"
            all_acquisition = extract_all_acquisition_from_folder(formatted_data_path_by_subject, config_dict_P2S["project"]["calib_folder_name"])
            # copy the config file in the sujet test folder
            shutil.copy(new_config_path_P2S, formatted_data_path_by_subject / "Config.toml")
            # TODO Here do a multithreading for the different acquisition they can be processed in parallel by doing a copy of each dictionary to be sure
            for acquisition in all_acquisition:
                print(f"Triangulating {subject} for {acquisition}")
                # copy the dictionat
                config_dict_P2S["project"]["project_dir"] = os.path.join(formatted_data_path_by_subject, acquisition)
                #Pose2Sim.personAssociation(config_dict_P2S)
                Pose2Sim.triangulation(config_dict_P2S)

            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     futures = [
            #         executor.submit(triangulate_acquisition, acquisition, subject, formatted_data_path_by_subject,
            #                         config_dict_P2S.copy())
            #         for acquisition in all_acquisition
            #     ]
            #     concurrent.futures.wait(futures)

            for task in task_to_process:
                copy_c3d_remove_fake_P2S_folder(temp_folder, pose3d_folder,name_config, model, subject, task)
            # We remove the full folder
            shutil.rmtree(temp_folder / model / subject)
            # all the .c3d file are contained in new_calibration_path = temp_folder / model / subject / task / pose-3d
            # we need to copy them in the folder pose3d_folder / model / subject
            # and remove the temp folder
        # We remove the folder of the model
        shutil.rmtree(temp_folder / model)