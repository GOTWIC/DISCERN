import torch
import sys, os, distutils.core

# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# Verify current directory
#print("Current Directory:", os.getcwd())

# Update paths based on the new current directory
# Assuming Detic is located at the same relative location to the script
#new_base_path = 'C:\\Users\\swagn\\detectron2'
#new_base_path = 'C:\\Users\\swagn\\Downloads\\csk_project\\detectron2'
#detic_path = os.path.join(new_base_path, 'Detic')
detic_path = 'Detic/'
#print("Detic Path:", detic_path)

# Verify the third_party and CenterNet2 directories
third_party_path = os.path.join(detic_path, 'third_party')
centernet2_path = os.path.join(third_party_path, 'CenterNet2')
#print("CenterNet2 Path:", centernet2_path)

# Check if CenterNet2 directory exists
#if os.path.exists(centernet2_path):
#    print("CenterNet2 directory found.")
#else:
#    print("CenterNet2 directory not found.")

# Add the correct paths to sys.path
sys.path.insert(0, centernet2_path)
sys.path.insert(0, detic_path)  # Add the Detic path to sys.path

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

# Detic libraries
from centernet.config import add_centernet_config
from detic.config import add_detic_config
from detic.modeling.utils import reset_cls_test

# Build the detector and download our pretrained weights
cfg = get_cfg()
add_centernet_config(cfg)
add_detic_config(cfg)

# Specify the full path to the configuration file
config_path = os.path.join(detic_path, 'configs', 'Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.yaml')

metadata_path = os.path.join(detic_path, 'datasets', 'metadata', 'lvis_v1_train_cat_info.json')

# Verify if the metadata file exists
#if os.path.exists(metadata_path):
#    print("Metadata file found:", metadata_path)
#else:
#    print("Metadata file not found:", metadata_path)

# Verify if the config file exists
#if os.path.exists(config_path):
#    print("Config file found:", config_path)
#else:
#    print("Config file not found:", config_path)

cfg.merge_from_file(config_path)

cfg.MODEL.WEIGHTS = 'https://dl.fbaipublicfiles.com/detic/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth'
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.2  # set threshold for this model
cfg.MODEL.ROI_BOX_HEAD.ZEROSHOT_WEIGHT_PATH = 'rand'
cfg.MODEL.ROI_HEADS.ONE_CLASS_PER_PROPOSAL = True  # For b

predictor = DefaultPredictor(cfg)

# Setup the model's vocabulary using build-in datasets
BUILDIN_CLASSIFIER = {
    'lvis': 'datasets/metadata/lvis_v1_clip_a+cname.npy',
    'objects365': 'datasets/metadata/o365_clip_a+cnamefix.npy',
    'openimages': 'datasets/metadata/oid_clip_a+cname.npy',
    'coco': 'datasets/metadata/coco_clip_a+cname.npy',
}

BUILDIN_METADATA_PATH = {
    'lvis': 'lvis_v1_val',
    'objects365': 'objects365_v2_val',
    'openimages': 'oid_val_expanded',
    'coco': 'coco_2017_val',
}

vocabulary = 'lvis'  # change to 'lvis', 'objects365', 'openimages', or 'coco'
metadata = MetadataCatalog.get(BUILDIN_METADATA_PATH[vocabulary])
classifier = BUILDIN_CLASSIFIER[vocabulary]
num_classes = len(metadata.thing_classes)
reset_cls_test(predictor.model, classifier, num_classes)

import logging
from PIL import Image

# Suppress findfont messages
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

def analyze_image(image_path):
    image = Image.open(image_path)
    im = np.array(image)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    outputs = predictor(im)
    instances = outputs["instances"].to("cpu")
    pred_classes = instances.pred_classes.tolist()
    pred_boxes = instances.pred_boxes.tensor.tolist()
    pred_masks = instances.pred_masks.numpy() 

    results = {}
    for idx, (cls, box, mask) in enumerate(zip(pred_classes, pred_boxes, pred_masks)):
        obj_name = metadata.thing_classes[cls]
        results[idx] = {
            "object_name": obj_name,
            "bounding_box": box,
            "mask": mask 
        }

    return results

