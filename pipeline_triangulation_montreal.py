from pathlib import Path
import LBMC_marker_less
import toml
import os

from create_fake_P2S_folder import model_to_process

model_to_process = ["all_body_rtm_coktail_14_hdf5"]

organized_data_path = Path("D:\Argos\Processing\Organized")
formatted_data_path = Path("D:\Argos\Processing\temp_P2S")

# Method used for the data processing = transforms the video into points
config_path_DLC = None
config_path_P2S = Path("P2S_config_files","Config_Checkerboard_Montreal_Sujet_test.toml")
scaling = "1.0"

config_dict_P2S = toml.load(config_path_P2S)

subjects =["Sujet_test"]


for subject in subjects:
        config_dict_P2S["markerAugmentation"]["participant_height"] = 1.83  # m
        config_dict_P2S["markerAugmentation"]["participant_mass"] = 75  # kg
        LBMC_marker_less.global_analysis.global_analysis(
                organized_data_path,
                formatted_data_path,
                subject,
                config_dict_P2S,
                folder_temp_video=None,
                dict_camera_to_remove=None,
                config_path_DLC=None,
            )
