from pathlib import Path
import snippet_ezc3d as ezsnip
import ezc3d

# path to the c3d file
#folder_subject = Path("C:/Users/S2Mlab/Documents/github/LBMC_marker_less_processing/data_CRME/Processing/Organized/fake_subject_02")
folder_subject = Path("H:/Argos/Processing/Organized/Subject_10_CP")
folder_subject = Path("G:/Argos_CEPSUM/Export_video/Sujet_08")
folder_subject = Path("G:/Argos_CEPSUM/Processing/Organized/Sujet_014")
#path_to_c3d = Path("C:/Users/User/Documents/Alexandre/Github/LBMC_marker_less_processing/data_montreal/c3d/Sujet_000/extrinsics.c3d")
path_to_c3d = folder_subject / "calibration"/"c3d_extrinsics"/"extrinsics.c3d"
path_to_txt = folder_subject / "calibration"/"c3d_extrinsics"/"extrinsics.txt"

acq_c3d = ezc3d.c3d(str(path_to_c3d))
points_c3d, points_name_c3d, points_ind_c3d = ezsnip.get_points_ezc3d(acq_c3d)

# Check the unit of the file 
print(acq_c3d["parameters"]["POINT"]["UNITS"]["value"][0])

if acq_c3d["parameters"]["POINT"]["UNITS"]["value"][0] == "mm":
    print("The unit of the file is in mm")
    points_c3d = points_c3d / 1000  # convert to meters
    print("The unit of the file has been converted to m")
else:
    print("The unit of the file is already in m")

# export the output in the following text format [[0.0,  0.0,  0.0],
#                               [0.0,  0.45,  0.0],
#                               [1.2, 0.0,  0.0],
#                               [1.2, 0.45,  0.0],
#                               [1.488, 0.724,  1.692],
#                               [1.184, 0.837,  1.741],
#                               [1.021, 0.8925,  1.767],]

# path to the output file

# test if the file exists and if not create it or delete it if it exists
if path_to_txt.exists():
    path_to_txt.unlink()
else:
    path_to_txt.parent.mkdir(parents=True, exist_ok=True)

# put points_name in alphabetical order to be sure to have the same order in the txt file without scientific notation
points_name_c3d.sort()
for point_name in points_name_c3d:
    point = points_c3d[:,points_ind_c3d[point_name],0]
    print(point_name)
    print(points_ind_c3d[point_name])
    print(point)
    with open(path_to_txt, "a") as file:
        file.write(f"[{point[0]:.6f}, {point[1]:.6f}, {point[2]:.6f}],\n")
