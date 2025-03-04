from pathlib import Path
from P2S_function import read_toml
import save_and_export
import adress_folder
import cv2
import os
import subprocess
import projection_on_video_montreal

def extract_images_from_video(video_path, output_folder):
    """ "
    This function allow to transform video to images knowing the path to the video and the folder to put the imags in.

    Parameters
    ---------
    video_path : Path object
    output_folder : Path object

    Returns
    ---------
    None
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    frame_count = 1

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Construct the output file path
        output_file = os.path.join(output_folder, f"{frame_count:09d}.png")

        # Save the frame as a JPEG file
        cv2.imwrite(output_file, frame)
        frame_count += 1

    # Release the video capture object
    cap.release()


def extract_images_from_video_ffmpeg(video_path, output_folder, decimation):
    """ "
    This function allow to transform video to images knowing the path to the video and the folder to put the imags in.
    This function use ffmepg via a subprocess to increase speed relative to opencv

    Parameters
    ---------
    video_path : Path object
    output_folder : Path object

    Returns
    ---------
    None
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construct the ffmpeg command
    frame_interval = decimation
    command = ["ffmpeg", "-i", str(video_path),
               "-vf", f"select='not(mod(n\,{frame_interval}))',metadata=print",
                "-vsync", "vfr"
               ,os.path.join(output_folder, "%09d.png")]
    # Run the ffmpeg command and suppress the output
    with open(os.devnull, "w") as devnull:
        subprocess.run(command, stdout=devnull, stderr=devnull, check=True)



def main(path_global_c3d, path_global_video, path_export, list_points, list_task, fq_data, fq_data_export_video, generate_image=True):
    """ "
    Bacth processing to generate from a folder containing the c3d file and a file containing the video file a folder containing
    an annotation files and a file containing all the images contained in the video file.

    Parameters
    ---------
    path_global_c3d : Path
        The path to the c3d data organised as follown Path/suject/subject_task.c3d
    path_global_video : Path
        the path to the video data organised as follow Path/subject/subject/task/videos/camera_name/camera_name.extension_video
    path_export : Path
        path to export the data
    list_points : list
        list of the point that should be exported in the annotation files
    list_task : dict
        dictionary containing the task for each subject
    fq_data : dict
        dictionary containing the frequency of the data for both marker based and marker less data
    generate_image : bool
        A boolean to allow to not having to regenerate the image but just the annotation as the process is quite long
    Retunrs
    ---------
    None
        For each combinaison of task and subject a annotation file and a folder image is generated
    """
    # Get the complete list of the subject where we have access to video
    file_list = [file for file in path_global_video.glob("*") if file.name in list_task.keys()]
    # Information necessary for the projection
    conversion_factor = 1  # mm to m
    add_video = False
    extension_video = ".avi"
    name_calib = "Calib_Scene.toml"

    for file in file_list:
        subject_name = file.name
        fq_file_c3d = fq_data[subject_name][0]
        fq_file_video = fq_data[subject_name][1]
        # check that the fq_data_export_video is a multiple of fq_file_video
        if fq_file_video % fq_data_export_video != 0:
            raise ValueError("The fq_data_export_video should be a multiple of fq_file_video")
        if fq_file_c3d % fq_data_export_video != 0:
            raise ValueError("The fq_file_c3d should be a multiple of fq_file_video")

        # As the data in data_export is already set at the same frequency we can use the same decimation
        decimation = fq_file_video // fq_data_export_video
        #decimation_c3d = fq_file_c3d // fq_data_export_video

        path_final = file
        final_task = [
            folder for folder in path_final.glob("*") if folder.name in list_task[subject_name]
        ]
        camera_calibration_matrix_path = (
            path_final / "calibration" / name_calib
        )
        all_camera_name, _, _, _, _, _ = read_toml(camera_calibration_matrix_path)

        for final_folder in final_task:
            task = final_folder.name
            final_name = task + ".c3d"

            c3d_full_path = path_global_c3d / subject_name / final_name
            print(f"Processing {subject_name} {task}, projecting 3D to 2D")
            data_to_export = projection_on_video_montreal.process_folder(
                path_global_video,
                c3d_full_path,
                subject_name,
                task,
                fq_file_c3d,
                fq_file_video,
                conversion_factor,
                add_video,
                "pas_importnat",
                "pas_importnat",
            )

            # The batch processing of the video is done in save_and_export
            path_to_annotation = Path(path_export, subject_name, task)
            # TODO : Change the number of point to export
            save_and_export.export_data_to_annotation(
                data_to_export, path_to_annotation, list_points, decimation
            )

            # extract images for each video
            if generate_image:
                for camera_name in data_to_export.keys():
                    path_to_export_image = Path(
                        path_export,
                        subject_name,
                        task,
                        camera_name,
                    )
                    # Camera
                    print(f"Extracting images from {camera_name}")
                    final_name_video = camera_name + extension_video
                    path_to_video = (
                        path_global_video
                        / subject_name
                        / task
                        / "videos"
                        / camera_name
                        / final_name_video
                    )
                    extract_images_from_video_ffmpeg(path_to_video, path_to_export_image, decimation)

            print(f"Processing {subject_name} {task}, projecting 3D to 2D done")


if __name__ == "__main__":
    fq_file_c3d = 120
    subject_to_fq_file_video = {"Sujet_000": [fq_file_c3d,120],"Sujet_001": [fq_file_c3d,60],
                                "Sujet_002": [fq_file_c3d,60],"Sujet_003": [fq_file_c3d,60],
                                "Sujet_004": [fq_file_c3d, 60], "Sujet_005": [fq_file_c3d, 60],
                                "Sujet_006": [fq_file_c3d, 60], "Sujet_007": [fq_file_c3d, 60],}

    sujet_to_list_task = {
        "Sujet_000": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_001": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_002": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_001", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_003": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_002", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_004": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
        "Sujet_005": ["01-eat-yoghurt_001", "02-cut-food", "13-playdoe", "06-drawing_001", "16-comb-hair", "17-hand-to-back_001"],
        "Sujet_006": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
        "Sujet_007": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"]}

    # sujet_to_list_task = {
    #     "Sujet_000": ["01-eat-yaourt"],
    #     "Sujet_001": ["01-eat-yoghurt"],
    #     "Sujet_002": ["01-eat-yoghurt" ],
    #     "Sujet_003": ["01-eat-yoghurt" ],
    #     "Sujet_007": ["01-eat-yoghurt"]}

    list_points = ["IJ","PX","C7","T10","L_EL","L_EM","R_EM","R_EL","L_RS","L_US","R_RS","R_US"]
    # TODO : Do a function to generate the description of data to use in the function
    generate_image = False
    fq_to_export_video = 5
    # Final folder structure
    path_global_c3d = adress_folder.path_global_c3d()
    path_global_video = adress_folder.path_global_video()
    path_export = adress_folder.path_export_pose_framework()

    main(path_global_c3d, path_global_video, path_export,list_points, sujet_to_list_task, subject_to_fq_file_video,fq_to_export_video, generate_image)
