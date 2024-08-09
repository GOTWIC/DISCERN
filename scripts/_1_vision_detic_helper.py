from PIL import Image
import os
import math
import glob
import random
import numpy as np
from pprint import pprint
from _1_vision_detic import analyze_image

main_folder_path = 'images/'

def crop_image(img, box):
    x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    cropped_img = img.crop((x1, y1, x2, y2))
    return cropped_img, (x1, y1, x2, y2)

def get_object_dict(orig_img_path, results, num_raycast_points=100):
    obj_dict = {}
    orig_img = Image.open(orig_img_path)
    items = 0
    for key, data in results.items():
        box = data['bounding_box']
        img, cropped_box = crop_image(orig_img, box)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        path = f'{main_folder_path}cache/img_{items}.jpg'
        item_type = data['object_name'].replace(' ', '_')
        dist = data.get('distance', None)

        mask = data['mask']
        mask_points = select_random_mask_points(mask, num_raycast_points)

        img.save(path)
        obj_dict[items] = {
            "path": path,
            "type": item_type,
            "attributes": {"distance": dist},
            "box": cropped_box,
            "mask": mask_points 
        }
        items += 1
    return obj_dict

def select_random_mask_points(mask, num_points):
    y_indices, x_indices = np.where(mask > 0)

    if len(x_indices) == 0 or len(y_indices) == 0:
        return []  

    
    points_to_select = min(num_points, len(x_indices))


    selected_indices = random.sample(range(len(x_indices)), points_to_select)
    selected_points = [(int(x_indices[i]), int(y_indices[i])) for i in selected_indices]  # Convert to native Python int

   
    flattened_points = [coord for point in selected_points for coord in point]
    return flattened_points

def clear_cache():
    files = glob.glob(os.path.join(f'{main_folder_path}cache', '*'))
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

def get_center(box):
    x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
    return (x1 + x2) / 2, (y1 + y2) / 2

def distance_between_coordinates(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def estimate_distances(results, path, y_penalty_factor=1.7):
    distances = []
    img = Image.open(path)
    width, height = img.size
    farthest_distance = distance_between_coordinates((width / 2, height * y_penalty_factor), (width, 0))
    for key, data in results.items():
        item_center = get_center(data['bounding_box'])
        adjusted_item_center = (item_center[0], item_center[1] * y_penalty_factor)
        adjusted_bottom_center = (width / 2, height * y_penalty_factor)
        distances.append(distance_between_coordinates(adjusted_item_center, adjusted_bottom_center) / farthest_distance)
    return distances

def detect_objects_detic(path):
    clear_cache()
    results = analyze_image(path)
    
    distances = estimate_distances(results, path)
    for i, (key, data) in enumerate(results.items()):
        results[key]['distance'] = distances[i]
    
    temp = get_object_dict(path, results)
    return temp

def main():
    result_dict = detect_objects_detic(f'{main_folder_path}input/table_plain.png')
    pprint(result_dict)

if __name__ == "__main__":
    main()
