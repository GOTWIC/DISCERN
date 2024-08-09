import os
import time
from _0_main import main

image_folder = "simulation\\input"

print("Started Algorithm")

while True:
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        time.sleep(1)
        continue

    image_path = os.path.join(image_folder, images[0])
    
    vlm_enabled = True
    
    if "False" in image_path:
        vlm_enabled = False
    
    main(image_path, vlm_enabled=vlm_enabled, show_output=True, accelerated=True)
    os.remove(image_path)
    time.sleep(0.5)
