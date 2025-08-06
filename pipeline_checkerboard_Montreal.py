from pathlib import Path
import LBMC_marker_less
import toml
import os


# organized_data_path = Path(".\data_CRME\Processing\Organized")
# formatted_data_path = Path(".\data_CRME\Processing\Formatted")

# Hard drive CRME
organized_data_path = Path("H:\Argos\Processing\Organized")
formatted_data_path = Path("H:\Argos\Processing\Formatted")

# Hard drive S2M
organized_data_path = Path("G:\Argos_CEPSUM\Processing\Organized")
formatted_data_path = Path("G:\Argos_CEPSUM\Processing\Formatted")

# Method used for the data processing = transforms the video into points
config_path_DLC = None
#config_path_P2S = Path("P2S_config_files","Config_Checkerboard_formatting_CRME.toml")
#config_path_P2S = Path("P2S_config_files","Config_Checkerboard_Montreal_formatting_only.toml")
#config_path_P2S = Path("P2S_config_files","Config_Checkerboard_Montreal_just_rotation.toml")
config_path_P2S = Path("P2S_config_files","Config_Checkerboard_Montreal_Sujet_008.toml")

scaling = "1.0"

config_dict_P2S = toml.load(config_path_P2S)
print(config_dict_P2S)
subjects =["Sujet_008"]

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
