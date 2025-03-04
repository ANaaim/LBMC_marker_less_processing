from pathlib import Path
import LBMC_marker_less
import toml
import os


organized_data_path = Path("E:\Argos\Processing\Organized")
formatted_data_path = Path("E:\Argos\Processing\Formatted")

# Method used for the data processing = transforms the video into points
config_path_DLC = None
config_path_P2S = Path("Config_Checkerboard_Montreal_Sujet_003.toml")
scaling = "1.0"

config_dict_P2S = toml.load(config_path_P2S)

subjects =["Sujet_003"]

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
