from ultralytics import YOLO
from PIL import Image
import numpy as np
import os
import math
import json
import glob

main_folder_path = 'images/'

def get_object_dict_deprecated():
    obj_dict = {}
    items = 0
    for subdir, dirs, files in os.walk(f'{main_folder_path}cache'):
        for file in files:
            file_path = os.path.join(subdir, file)
            obj_dict[items] = {"path":file_path.replace('\\','/'),"type":subdir.replace('\\','/').split('/')[-1].replace(' ','_')}
            items += 1
    
    return obj_dict

def crop_image(img, box):
    x1, y1, x2, y2 = int(box['x1']), int(box['y1']), int(box['x2']), int(box['y2'])
    cropped_img = img.crop((x1, y1, x2, y2))
    return cropped_img, (x1, y1, x2, y2)

def get_object_dict(orig_img_path, results_json):
    obj_dict = {}
    orig_img = Image.open(orig_img_path)
    items = 0
    for item in results_json:
        img, box = crop_image(orig_img, item['box'])
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        path = f'{main_folder_path}cache/img_{items}.jpg'
        item_type = item['name'].replace(' ', '_')
        img.save(path)
        obj_dict[items] = {"path": path, "type": item_type, "attributes": {"distance": item['distance']}, "box": box, "mask": []}        
        items += 1
    return obj_dict

def clear_cache():  
    files = glob.glob(os.path.join(f'{main_folder_path}cache', '*'))
    for f in files:
        if os.path.isfile(f):
            os.remove(f)
            
def get_center1(box):
    x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']
    return (x1+x2)/2, (y1+y2)/2

def get_absolute_dist1(coord1, coord2):
    return round(math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2),3)

def distance_between_coordinates1(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return abs(distance)

def estimate_distances1(json_str, path):
    distances = []
    img = Image.open(path)
    width, height = img.size
    farthest_distance = distance_between_coordinates((width/2,height), (width,0))
    for item in json_str:
        item_center = get_center(item['box'])
        distances.append(distance_between_coordinates(item_center, (width/2,height))/farthest_distance)
    return distances

def get_center(box):
    x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']
    return (x1 + x2) / 2, (y1 + y2) / 2

def distance_between_coordinates(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def estimate_distances(json_str, path, y_penalty_factor=1.7):
    distances = []
    img = Image.open(path)
    width, height = img.size
    farthest_distance = distance_between_coordinates((width / 2, height * y_penalty_factor), (width, 0))
    for item in json_str:
        item_center = get_center(item['box'])
        adjusted_item_center = (item_center[0], item_center[1] * y_penalty_factor)
        adjusted_bottom_center = (width / 2, height * y_penalty_factor)
        distances.append(distance_between_coordinates(adjusted_item_center, adjusted_bottom_center) / farthest_distance)
    return distances


def detect_objects(path):
    clear_cache()
    model = YOLO('yolo/yolov5xu.pt')
    img = Image.open(path)
    result = model(img, iou=0.9)[0]
    #result_json_norm = json.loads(result.tojson(normalize=True))
    result_json = json.loads(result.tojson(decimals=0))
    distances = estimate_distances(result_json, path)
    for i, item in enumerate(result_json):
        result_json[i]['distance'] = distances[i]    
    #result.show()
    return get_object_dict(path,result_json)

def main():
    detect_objects(f'{main_folder_path}input/dining_table_2.webp')
    
if __name__ == "__main__":
    main()