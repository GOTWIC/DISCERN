from PIL import Image, ImageDraw, ImageFont
import numpy as np



def show_output_img(orig_img_path, obj_dict, order, show_distance=False):
    close, far, ignore = order
    full_img = Image.open(orig_img_path)
    for id, item in obj_dict.items():
        if id in close:
            full_img = draw_box(full_img, item['box'], 'green', str(close.index(id) + 1))
        elif id in far:
            full_img = draw_box(full_img, item['box'], 'orange', str(len(close) + far.index(id) + 1))
        elif id in ignore:
            full_img = draw_box(full_img, item['box'], 'red', "N/A")
    if show_distance:
        full_img = draw_distance_field(full_img)
    full_img.show()
    if full_img.mode == 'RGBA':
        full_img = full_img.convert('RGB')
    full_img.save('output.jpg')
    return full_img

def draw_box(img, xyxy, color, number):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    
    draw = ImageDraw.Draw(img)
    
    # box
    left, top, right, bottom = xyxy
    draw.rectangle([left, top, right, bottom], outline=color, width=3)
    
    # sub box
    subbox_width = 20
    subbox_height = 20
    draw.rectangle([left, top, left + subbox_width, top + subbox_height], fill=color)
    
    # ranking
    font_size = 15
    font = ImageFont.truetype("arial.ttf", font_size)
    text = str(number)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = left + (subbox_width - text_width) / 2
    text_y = top + (subbox_height - text_height) / 2
    draw.text((text_x, text_y), text, fill="white", font=font)
    
    return img


def draw_distance_field(image, radii=[25*i for i in range(1,41)]):
    #image = Image.open(image_path)
    width, height = image.size
    bottom_center = (width // 2, height)
    draw = ImageDraw.Draw(image)

    for radius in radii:
        bbox = [
            (bottom_center[0] - radius, bottom_center[1] - radius/1.5),
            (bottom_center[0] + radius, bottom_center[1] + radius)
        ]
        draw.pieslice(bbox, 180, 360, outline="white", fill=None)

    return image