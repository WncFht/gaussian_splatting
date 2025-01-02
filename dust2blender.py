import json
import math
import numpy as np
import os
import random

def calculate_transform_matrix(position, rotation):
    transform_matrix = np.eye(4)
    transform_matrix[:3, :3] = np.array(rotation)
    transform_matrix[:3, 3] = np.array(position)
    return transform_matrix.tolist()

def convert_camera_params(data):
    fx = data[0]['fx']  # Assuming fx is the same for all cameras
    camera_angle_x = 2 * math.atan(data[0]['width'] / (2 * fx))

    frames = []
    for camera in data:
        # Ensure file paths and extensions are removed
        img_name = os.path.splitext(camera['img_name'])[0]  # Remove file extension

        transform_matrix = calculate_transform_matrix(camera['position'], camera['rotation'])

        frame = {
            "file_path": f"./images/{img_name}",
            "rotation": 0.012566370614359171,  # Example rotation, can be adjusted
            "transform_matrix": transform_matrix
        }
        frames.append(frame)

    result = {
        "camera_angle_x": camera_angle_x,
        "frames": frames
    }
    return result

def split_data(data, train_ratio=5):
    frames = data["frames"]
    random.shuffle(frames)  # Shuffle the frames to ensure randomness

    split_index = int(len(frames) * train_ratio / (train_ratio + 1))
    train_frames = frames[:split_index]
    test_frames = frames[split_index:]

    train_data = {
        "camera_angle_x": data["camera_angle_x"],
        "frames": train_frames
    }
    test_data = {
        "camera_angle_x": data["camera_angle_x"],
        "frames": test_frames
    }

    return train_data, test_data

def main():
    # Read input file path from the user
    input_file_path = input("Please provide the path to the input JSON file: ").strip()

    # Read JSON data from the file
    try:
        with open(input_file_path, 'r') as f:
            camera_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
        return

    # Convert the data
    converted_data = convert_camera_params(camera_data)

    # Split the data into training and testing sets
    train_data, test_data = split_data(converted_data)

    # Write the output files
    train_output_path = "transforms_train.json"
    test_output_path = "transforms_test.json"

    with open(train_output_path, 'w') as train_file:
        json.dump(train_data, train_file, indent=4)

    with open(test_output_path, 'w') as test_file:
        json.dump(test_data, test_file, indent=4)

    print(f"Training data saved to {train_output_path}")
    print(f"Testing data saved to {test_output_path}")

if __name__ == "__main__":
    main()
