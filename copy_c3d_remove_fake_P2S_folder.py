import shutil
from pathlib import Path


pose3d_folder = Path("E:/Argos/Processing/Pose3d")
temp_folder = Path("C:/Users/User/Documents/Alexandre/Github/LBMC_marker_less_processing/data_montreal/temp_P2S")
subject_to_process = ["Sujet_000","Sujet_001","Sujet_002","Sujet_003","Sujet_007"]
model_to_process = ["all_body_rtm_coktail_14_hdf5","all_body_resnet_hdf5","all_body_hrnet_coco_dark_coco_hdf5"]

sujet_to_list_task = {"Sujet_000": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                      "Sujet_001": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                      "Sujet_002": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_001", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                      "Sujet_003": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_002", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                      "Sujet_007": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"]}


# Define the source and destination paths
for model in model_to_process:
    for subject in subject_to_process:
        task_to_process = sujet_to_list_task[subject]
        for task in task_to_process:
            source_folder = temp_folder / model / subject / task / "pose-3d"
            destination_folder = pose3d_folder / model / subject



            # Ensure the destination folder exists
            destination_folder.mkdir(parents=True, exist_ok=True)
            c3d_files = list(source_folder.glob("*.c3d"))
            if len(c3d_files) != 1:
                raise ValueError(f"Expected exactly one .c3d file in {source_folder}, but found {len(c3d_files)}")

            c3d_file = c3d_files[0]
            destination_file = destination_folder / f"{task}.c3d"
            shutil.copy(c3d_file, destination_file)