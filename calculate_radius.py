import json
import numpy as np

def getWorld2View2(R, t, translate=np.array([.0, .0, .0]), scale=1.0):
    Rt = np.zeros((4, 4))
    Rt[:3, :3] = R.transpose()
    Rt[:3, 3] = t
    Rt[3, 3] = 1.0

    C2W = np.linalg.inv(Rt)
    cam_center = C2W[:3, 3]
    cam_center = (cam_center + translate) * scale
    C2W[:3, 3] = cam_center
    Rt = np.linalg.inv(C2W)
    return np.float32(Rt)

def getNerfppNorm(cam_info):
    def get_center_and_diag(cam_centers):
        cam_centers = np.hstack(cam_centers)
        avg_cam_center = np.mean(cam_centers, axis=1, keepdims=True)
        center = avg_cam_center
        dist = np.linalg.norm(cam_centers - center, axis=0, keepdims=True)
        diagonal = np.max(dist)
        return center.flatten(), diagonal

    cam_centers = []

    for cam in cam_info:
        R = np.array(cam["transform_matrix"])[:3, :3]
        T = np.array(cam["transform_matrix"])[:3, 3]
        W2C = getWorld2View2(R, T)
        C2W = np.linalg.inv(W2C)
        cam_centers.append(C2W[:3, 3:4])

    center, diagonal = get_center_and_diag(cam_centers)
    radius = diagonal * 1.1

    translate = -center

    return {"translate": translate.tolist(), "radius": radius}

def load_json(file_path):
    """
    Load the JSON file from the given file path.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
        return None

def calculate_radius_and_translate(file_path):
    """
    Calculate the radius and translate for the JSON data in the given file path.
    """
    data = load_json(file_path)
    if data is None:
        return

    # Calculate radius and translate
    result = getNerfppNorm(data["frames"])
    print({"translate": result['translate'], "radius": result['radius']})
    print(f"Results for {file_path}:")
    print(f"  Translate: {result['translate']}")
    print(f"  Radius: {result['radius']}")
    return result

def main():
    # Paths to the train and test JSON files
    train_file_path = "./data/002/transforms_train.json"
    test_file_path = "./data/002/transforms_test.json"

    print("Calculating for training data...")
    train_result = calculate_radius_and_translate(train_file_path)

    print("\nCalculating for testing data...")
    test_result = calculate_radius_and_translate(test_file_path)

if __name__ == "__main__":
    main()
