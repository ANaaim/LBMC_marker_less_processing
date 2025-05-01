# Where are the data
On the 09.01.2025 :
On the acquisition computer, the data can be stored or in the SSD drive F:/Argos or in the HDD drive E:/Alex/Argos.
Or on the SSD portable Drive on the SSD drive of 2To.

The aim would be to store the data on the server of the lab in the q //10.89.24.15 / argos

The data should be considered in two states hot and cold.
the hot data are the data that are currently used and process. They should be accessed easily and quickly.
The cold data are the data that are just stored and should be accessed only if needed, so they do not need to be accessed quickly.(HDD or server might be ok)

On the 13.01.2025 :
The 14 To HDD is now available.
### Data final structure :
#### Raw data
This data are the data that are directly save from optitrack in a .tak format.
These data do not need to be accessed quickly and can be stored on the 14 To HDD in the folder Argos/raw_optitrack_data/Sujet_XXX. 
They are only used to export the video and the c3d files.

#### Organized data
These data are just the data that are organized after the export from optitrack to follow the P2S format. 
Here the video are not yet rotated and all the calibration matrix calculation are done from this folder
These do not need to be accessed quickly and can be stored on the 14 To HDD in the folder Argos/Processing/Organized/Sujet_XXX.

#### Formatted data
These video are the video that are rotated and the adapted rotated calibration matrix are calculated from the organized data.
These data are the one that are used to generate the pose2d data. They will be stored on the 2to SSD portable drive in the folder Argos/Processing/Formatted/Sujet_XXX 
as they need to be accessed quickly.

#### Pose2d data
These data are the pose2d data generated from the formatted video using mmpose.
They will be stored on the 14To SSD portable drive in the folder Argos/Processing/Pose2d/Model_XXX/Sujet_XXX.

#### Temp_folder data for P2S
Currently the triangulation is done using P2S. 
This tool-box needs the data to be in a specific format where for each video and frame a json files is geenrated.
These folders are generated just the time to generate the c3d date and are deleted after.
They will be generated on the computer HD.
When numerous json are generated on the 2To SSD each file take 1mo (probably a problem with the partitioning or the minimum size of the file system on the SSD)

#### Pose3d data
These data are the pose3d data generated from the pose2d data using the extrinsics parameters of the camera from the formatted folder.
They will be stored on the 14To HDD in the folder Argos/Processing/Pose3d/Model_XXX/Sujet_XXX.



# How to process data in the Argos project

## Organize video after export from optitrack
First verify that there is no duplicate video from export before running the code.

A function called formatting_montreal_data.py is available in the argos project to organize the video files after export from optitrack.
It will create a folder with the name of the task containing for each camera a folder with the name of the subject containing the video files, following 
the format used in pose2sim.
```python 
source_folder = Path("D:/Argos/Sujet_003")
restructure_files(source_folder)
````

Following this step it is possible to calculate the extrinsics and intrinsics parameters of the camera.

## Obtaining the calibration data
The intrinsics parameters of the camera have been calculated one time for the camera each time their focal is changed.

Currently, 
Subject 000,001,002,003,004,005,006,007 have been using the same focal lenght. The original calibration data are contained in test_ariane_novembre

in the folder Organized/Suject_XXX/calibration
create one folder extrinsics and one folder intrinsics and one c3d_extrinsics
- In the extrinsics folder add one folder for each camera with the name of the camera as the name of the folder and the video inside as name_camera.avi.
- For the intrinsics calibration (the intrinsics folder should be empty) add a previous complete calibration (such as Calib_scene.toml) in the calibration folder to obtain directly the intrinsics parameters in the process
- From there the data for the scene should be generated from the extrinsics.c3d. For that the user should label the point in the c3d file in a specific order. These data can be put in a folder c3d_extrinsics.
- Then the user should run the function extract_calibrations_scene_point_coordinate.py to be used as the input in the pose2sim option files in the [calibration] part. it will look like this :
```toml
   [calibration.calculate]
      # Camera properties, theoretically need to be calculated only once in a camera lifetime
      [calibration.calculate.intrinsics]
.....
         [calibration.calculate.extrinsics.scene]
         show_reprojection_error = true # true or false (lowercase)
         extrinsics_extension = 'avi' # any video or image extension
         # list of 3D coordinates to be manually labelled on images. Can also be a 2 dimensional plane.
         # in m -> unlike for intrinsics, NOT in mm!
         object_coords_3d =     [[0.004644, 0.000034, 0.005962],
                                [2.290803, 0.001110, 0.016975],
                                [2.264257, 1.218686, 0.020926],
                                [0.041503, 1.218982, 0.015180],
                                [1.173410, 0.303591, 0.012748],
                                [1.172003, 0.912014, 0.016960],
                                [0.831911, 0.070315, 0.738973],
                                [1.418195, 0.053579, 0.743392],
                                [1.457477, 1.187996, 0.747479],
                                [0.867250, 1.197984, 0.744521],
                                [1.079364, 0.449062, 1.484198],
                                [1.270512, 0.439477, 1.484014],
                                [1.278089, 0.693037, 1.486048],
                                [1.084153, 0.700204, 1.486283],]
         [calibration.calculate.extrinsics.keypoints]
         # Coming soon!

```

From their the calibration can be run using the pose2sim with the scene mode using the pipeline_checkerboard_Montreal.py
This should generate the calibration file and also rotate the video and export them in the Formatted folder.


Now the calibration integrating the rotation of the video is done. We now have to choose if we remove the video without rotation or not to save space.

Calibration can be verified using the function projection_on_video.py which will allow to reproject directly the c3d on the video using a formatted folder and the c3d files.
It is proposed here to have the 


## Formatting data
TODO : Create a config file just for formatting the data ==» It should ease the process of formatting the data for the user.


## Generating the pose2d data.
In our project we want to generate the pose2d data from different model of pose estimation to be able to compare them.
As a result we will create a specific folder called pose2d at the same level as the Organized folder and the Formatted folder.

The generation of the pose2d data is currently done in the project analysis_mmpose.
From a formatted file containing all the video rotated we should be able to use mmpose to generate the pose2d data.

The sturcture of the folder should be the following :
```tree
pose2d
├── Model_1
│   ├── Subject_000
│   │   ├── tache_001
│   │   │   └── task_1.h5
│   │   │   ...
│   │   └── task_XXX
│   │       └── task_n.h5
│   ...  
│   └── Subject_XXX
│       ├── tache_001
│       │   └── task_1.h5
│       │   ...
│       └── task_XXX
│           └── task_n.h5
... 
└── Model_XXX
    ├── Subject_000
    │   ├── tache_001
    │   │   └── task_1.h5
    │   │   ...
    │   └── task_XXX
    │       └── task_n.h5
    ...
    └── Subject_XXX
        ├── tache_001
        │   └── task_1.h5
        │   ...
        └── task_XXX
            └── task_n.h5
````
The hdf5 file has the following structure :
keypoints_XXX is the name of the keypoints of the model used. It can be the true name or just the 
[indices of the keypoints](https://mmpose.readthedocs.io/en/latest/dataset_zoo/2d_wholebody_keypoint.html) in the 
model.

```
File
├── Metadata
│   ├── Sujet
│   ├── Tache
│   └── Model used
│
├── Camera_001
│   ├── keypoints_001
│   │   └── numpy_array (3xnb_frame) X Y Confidence for each frame
│   ...
│   └── keypoints_XXX
│       └── numpy_array (3xnb_frame) X Y Confidence for each frame
...
└──Camera_XXX
    ├── keypoints_001
    │   └── numpy_array (3xnb_frame) X Y Confidence for each frame
    ...
    └── keypoints_XXX
        └── numpy_array (3xnb_frame) X Y Confidence for each frame
```        

## Generating the pose3d data.
The 3d point coordinates are generated from the pose2d data using the extrinsics parameters of the camera from the formatted 
folder. This is done by doing a triangulation using Pose2Sim. In order to be able to do that a fake folder is generated using
the information from the formatted. 

In order to process the data the user should create a temporary folder with the same structure as the pose2d folder with the following structure :
```tree
Subject_XXX
├── calibration
│   └── Calib_scene.toml
├── tache_001
│   └── pose
│       ├── camera_001_json
│       │   ├── camera_001_000000000_keypoints.json
│       │   ...
│       │   └── camera_001_XXXXXXXXX_keypoints.json
│       ...
│       └── camera_XXX_json
│           ├── camera_XXX_000000000_keypoints.json
│           ...
│           └── camera_XXX_XXXXXXXXX_keypoints.json
...
└── task_XXX
    └── pose
        ├── camera_001_json
        │   ├── camera_001_000000000_keypoints.json
        │   ...
        │   └── camera_001_XXXXXXXXX_keypoints.json
        ...
        └── camera_XXX_json
            ├── camera_XXX_000000000_keypoints.json
            ...
            └── camera_XXX_XXXXXXXXX_keypoints.json
```


Then pose2sim with only the triangulation option can be used to generate the pose3d data. The trc files generated can be copied in the pose3d folder and the
 temporary folder can be deleted.


The final structure folder of the pose3D data should be the following (similar to the pose2d data) :
```tree
pose3d
├── Model_1
│   ├── Subject_000
│   │   ├── tache_001
│   │   │   └── task_1.c3d
│   │   │   ...
│   │   └── task_XXX
│   │       └── task_n.c3d
│   ...  
│   └── Subject_XXX
│       ├── tache_001
│       │   └── task_1.c3d
│       │   ...
│       └── task_XXX
│           └── task_n.c3d
... 
└── Model_XXX
    ├── Subject_000
    │   ├── tache_001
    │   │   └── task_1.c3d
    │   │   ...
    │   └── task_XXX
    │       └── task_n.c3d
    ...
    └── Subject_XXX
        ├── tache_001
        │   └── task_1.c3d
        │   ...
        └── task_XXX
            └── task_n.c3d
````

From here all comparison can be done between both pose2d file compared with the reprojection of the c3d on the video or c3d file compared with the pose3d files. 