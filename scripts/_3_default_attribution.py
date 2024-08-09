from pprint import pprint
from copy import deepcopy

default_attributions = {
    "container": {
        "size": 0.30,
        "weight": 0.30,
        "fragile": 0.80,
        "sharpness": 0.10,
        "flexibility": 0.00,
        "filled": 0.50,
        "temperature": 0.30,
        "value": 0.50,
    },
    "utensil": {
        "size": 0.10,
        "weight": 0.10,
        "fragile": 0.10,
        "sharpness": 0.30,
        "flexibility": 0.00,
        "filled": 0.00,
        "temperature": 0.20,
        "value": 0.20,
    },
    "decoration": {
        "size": 1.00,
        "weight": 1.00,
        "fragile": 1.00,
        "sharpness": 0.00,
        "flexibility": 0.00,
        "filled": 0.00,   
        "temperature": 0.00,
        "value": 1.00,
    },
    "furniture": {
        "size": 1.00,
        "weight": 1.00,
        "fragile": 1.00,
        "sharpness": 0.00,
        "flexibility": 0.00,
        "filled": 0.00,   
        "temperature": 0.00,
        "value": 1.00,
    },
    "cookware": {
        "size": 0.50,
        "weight": 0.50,
        "fragile": 0.20,
        "sharpness": 0.10,
        "flexibility": 0.00,
        "filled": 0.50,
        "temperature": 0.80,
        "value": 0.50,
    },
}



def assign_default_attributes2(obj_dict):
    for item in obj_dict:
        def_attributes = default_attributions[obj_dict[item]['category']] 
        def_attributes['distance'] = obj_dict[item]["attributes"]["distance"]
        obj_dict[item]['attributes'] = def_attributes 
        print(f'Original Distance: {obj_dict[item]["attributes"]["distance"]}')
        print(f'Temp Distance: {def_attributes["distance"]}')
    pprint(obj_dict)
    return obj_dict
    
    
def assign_default_attributes(obj_dict):
    for item in obj_dict:
        def_attributes = deepcopy(default_attributions[obj_dict[item]['category']])
        def_attributes['distance'] = obj_dict[item]["attributes"]["distance"]
        obj_dict[item]['attributes'] = def_attributes
    return obj_dict