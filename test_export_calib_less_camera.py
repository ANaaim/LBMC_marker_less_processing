import toml
from pathlib import Path

# def read_and_export_toml_less_camera(file_path, blocks_to_export,output_file_path):
#     # Read the TOML file
#     with open(file_path, 'r') as file:
#         data = toml.load(file)
#
#     # Extract the required blocks and metadata
#     extracted_data = {}
#     for block in blocks_to_export:
#         if block in data:
#             extracted_data[block] = data[block]
#
#     # Add metadata
#     if 'metadata' in data:
#         extracted_data['metadata'] = data['metadata']
#
#     # Write the extracted data to the output file
#     with open(output_file_path, 'w') as file:
#         toml.dump(extracted_data, file)
#
# # Example usage
# file_path = Path("E:/Argos/Processing/Formatted/Sujet_000/calibration/Calib_scene.toml")
# file_path_export = Path("toto.toml")
# blocks_to_export = ['M11139', 'M11140', 'M11141']  # Specify the blocks you want to export
# extracted_data = read_and_export_toml_less_camera(file_path, blocks_to_export,file_path_export)
camera_configurations = {"full_camera": None,
                         "no_lat": ["M11139", "M11140", "M11141"],
                         }
for name_config, list_camera in camera_configurations.items():
    print(name_config)
    print(list_camera)