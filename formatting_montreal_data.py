import os
import shutil
from pathlib import Path
def restructure_files(source_folder):
    for filename in os.listdir(source_folder):
        if filename.endswith('.avi'):
            parts = filename.split('-')
            if len(parts) >= 2:
                nametask = '-'.join(parts[0:-1])
                camera_id = parts[-1].split(' ')[-1].split('(')[1].split(')')[0]

                if "intrinsic" in filename:
                    new_name_task = "intrinsic"
                    camera_to_export = nametask.split("_")[1]
                    if camera_id == camera_to_export:

                        new_dir = os.path.join(source_folder, new_name_task, camera_id)
                        new_filename = f"{camera_id}.avi"
                        os.makedirs(new_dir, exist_ok=True)

                        shutil.move(os.path.join(source_folder, filename), os.path.join(new_dir, new_filename))

                else:
                    new_dir = os.path.join(source_folder, nametask, camera_id)
                    os.makedirs(new_dir, exist_ok=True)
                    new_filename = f"{camera_id}.avi"
                    shutil.move(os.path.join(source_folder, filename), os.path.join(new_dir, new_filename))

# source_folder = 'D:\Users\naaim\Documents\LBMC_marker_less_processing\data_montreal\organized\test_extrinsics'
source_folder = Path("E:/Argos/temp_folder/Sujet_004_pb_fq/half_fq")

#source_folder = 'D:\Users\naaim\Documents\LBMC_marker_less_processing\data_montreal\organized\test_extrinsics'
restructure_files(source_folder)