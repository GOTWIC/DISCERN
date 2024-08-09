from _1_vision_yolo import detect_objects
from _1_vision_detr import detect_objects_detr
from _1_vision_yolo_world import detect_objects_world
from _1_vision_detic_helper import detect_objects_detic
from _2_conceptnet_context import find_context_location
from _2_conceptnet_category import get_categories
from _2_conceptnet_category2 import get_categories2
from _3_default_attribution import assign_default_attributes
from _3_state_aware_attribution import assign_state_attributes, assign_state_attributes_vlm_disabled
from _4_order_optimizer import optimize_order, optimize_order2
from _4_image_output import show_output_img

import json
from PIL import Image
from pprint import pprint


def get_items_type_count(obj_dict):
    item_dict = {}
    for id,item in obj_dict.items():
        if item['type'] in item_dict:
            item_dict[item['type']] += 1
        else:
            item_dict[item['type']] = 1
    return item_dict

def save_obj_dict(obj_dict):
    with open('simulation\\output\\obj_dict.json', 'w') as f:
        json.dump(obj_dict, f)
    with open('obj_dict.json', 'w') as f:
        json.dump(obj_dict, f)
        
def save_order(order):
    temp = {"close": order[0], "far": order[1], "ignore": order[2]}
    with open('simulation\\output\\order.json', 'w') as f:
        json.dump(temp, f)


def add_image_size(obj_dict, image_path):
    image = Image.open(image_path)
    width, height = image.size

    for obj_id, obj_data in obj_dict.items():
        obj_data["dimensions"] = [height, width] 

    return obj_dict

def main(image_path, vlm_enabled=True, show_output=True, accelerated=False):   
     
    # yolov5
    obj_dict = detect_objects(image_path)   
    
    # Detr
    #obj_dict = detect_objects_detr(image_path) 
    
    # yolo world
    #obj_dict = detect_objects_world(image_path) 
    
    # detic
    #obj_dict = detect_objects_detic(image_path)
    
    obj_dict = add_image_size(obj_dict, image_path)
    
    # conceptnet
    location = find_context_location(list(get_items_type_count(obj_dict).keys()))
    
    # conceptnet
    #obj_dict = get_categories(obj_dict)
    
    # conceptnet (modified for detr + detic)
    obj_dict = get_categories2(obj_dict)
        
    # knowledge base
    obj_dict = assign_default_attributes(obj_dict)
    
    # gpt
    if vlm_enabled:
        obj_dict = assign_state_attributes(obj_dict, accelerated)
    else: 
        obj_dict = assign_state_attributes_vlm_disabled(obj_dict)

    
    # formula
    order = optimize_order2(obj_dict, reach=1)

    
    # display results
    if show_output:
        output = show_output_img(image_path, obj_dict, order)
    
    # output to unity
    save_obj_dict(obj_dict)
    save_order(order)
    
    
   
def main2():
    
    obj_dict = {}
    
    with open('obj_dict.json', 'r') as f:
        obj_dict = json.load(f)

    order = optimize_order(obj_dict,0.8)
    
    print(order)
    
    output = show_output_img("images/input/table_plain.png", obj_dict, order)





if __name__ == "__main__":
    main(image_path = "images/input/table_plain.png", vlm_enabled=False, show_output=True, accelerated=True)
    #main2()