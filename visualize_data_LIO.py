from pathlib import Path
import cv2
import json
import adress_folder
import math

def generate_images_from_folder(folder_path):
    # Read the json file
    path_to_json = Path(folder_path, "annotations.json")
    with open(path_to_json, "r") as file:
        data = json.load(file)

    for frame in data.keys():
        # Read the image
        print(frame)
        image_path = Path(folder_path, f"{frame}.png")
        image_init = cv2.imread(str(image_path))

        points = data[frame]["joints"]
        bbox = data[frame]["bbox"]
        # Generate the image with the points and bounding box
        image = generate_image_with_point_and_bounding_box(image_init, points, bbox)

        # Show the image

        cv2.imshow("image", image)
        cv2.waitKey(0)


def generate_image_with_point_and_bounding_box(image, points, bounding_box):
    # Draw the points on the image

    for i in range(0, len(points), 2):
        if not math.isnan(points[i]) and not math.isnan(points[i + 1]):
            cv2.circle(image, (int(points[i]), int(points[i + 1])), 5, (0, 0, 255), -1)
    # Draw the bounding box on the image
    cv2.rectangle(
        image,
        (int(bounding_box[0]), int(bounding_box[1])),
        (int(bounding_box[2]), int(bounding_box[3])),
        (0, 255, 0),
        2,
    )

    return image


if __name__ == "__main__":
    path_to_folder = (
        adress_folder.path_export_pose_framework() / "Sujet_002" / "01-eat-yoghurt" / "M11458"
    )
    generate_images_from_folder(path_to_folder)
