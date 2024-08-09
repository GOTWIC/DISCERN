import base64
import requests
import os
import ast
from copy import deepcopy

api_key = os.environ.get("OPENAI_API_KEY")

attribute_examples = {
	"container": 
    """
 	A container could include plates, cups, wine glasses, of different sizes and materials. 
	For example, a wine glass has higher fragility, a lower weight, lower size. Hence, its attributes might be as follows:
 
	"size": 0.20,
	"weight": 0.20,
	"fragil": 1.00,
	"sharpness": 0.10,
	"flexibility": 0.00,
	"filled": 0.50,
	"temperature": 0.10,
	"value": 0.70,
 
 	whereas a plate might have a bigger size and weight, but be less fragile, like so: 
  
	"size": 0.30,
	"weight": 0.30,
	"fragile": 0.80,
	"sharpness": 0.10,
	"flexibility": 0.00,
	"filled": 0.50,
	"temperature": 0.30,
	"value": 0.50,
 
	Additonally, a container of any kind might be filled, such as a plate with food, a bowl with soup, or a cup with water. Please idenitfy how much the container is filled, and adjust the "filled" attribute accordingly
 
  	""",
	"utensil":
    """  
    A utensil could include forks, knives, spoons, of different sizes and materials. For example, a spoon usually has virtually no sharpness, so its sharpness value can be set to 0.
    
    Generally, utensil have similar weight and size, so it many times you won't need to change the size or weight. 
    
    However, there can be exceptions. For example, a meat knife might be longer and heavier, so adjust the size and weight accordingly. Note that a butter knife is likely to have a lower size and weight than a meat knife.
    
    Items like forks and spoons are often sharp, although knives tend to be sharper. Hence, it would be reasonable to set the sharpness value of a fork or spoon to 0.4-0.6, and the sharpness value of a knife to 0.7-0.9.
    However, a butter knife might have a lower sharpness value than a meat knife, so a sharpness value of around 0.2-0.3 would be appropriate.
    
	sometimes, the utensils might seem valuable, such as a silver spoon, or a gold plated fork. In such cases, the value attribute can be set to 0.7-0.9. However, a plastic spoon would have a lower value (than a metal one), so a value of 0-0.1 would be appropriate.
  	""",
	"cookware":
    """
    
    cookware can be pots, pans, baking trays, and other items used for cooking. Depending on the type of cookware, you may need to adjust values accordingly.
 	
  	""",
}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
       return base64.b64encode(image_file.read()).decode('utf-8')
  
def convert_to_dict(inp):
	inp = inp.replace("\n", "").replace("\t", "").replace('python', '').replace('json','').replace('```','').replace('yaml','')
	#print(inp)
	return ast.literal_eval(inp)


def state_aware_attribution(item):
	base64_image = encode_image(item["path"])

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {api_key}"
	}
	payload = {
		"model": "gpt-4o-mini",
		"messages": [
		{
			"role": "user",
			"content": [
			{
				"type": "text",
				"text": f"""
    
					This image is of a {item['type']}, and was categorized as a {item['category']}.
     
					The default attributes of a {item['category']} are: 
     				
         			{item['attributes']}
            
					where each attribute is a value from 0 to 1, with 0 being the lowest and 1 being the highest of that attribute.
            
					However, there are different types of {item['category']}s, and different items that classify as a {item['category']} can have different attributes.
     
					Here are some examples:
     
					{attribute_examples[item['category']]}
    
					Based on what you see in the image, and the examples provided, return the modified attributes you would assign to this object in the exact same format as the default attributes.
     				Not all attributes have to be changed if some of the default attributes are appropriate.
         
         			If you would not change any attributes, return the default attributes as is.

					Do not include ANYTHING other than the attributes in dictionary format in your output. Do not include any comments, including an acknowledgement of this prompt.
				"""
			},
			{
				"type": "image_url",
				"image_url": {
				"url": f"data:image/jpeg;base64,{base64_image}",
				"detail": "low"
				}
			}
			]
		}
		],
		"max_tokens": 300
	}

	response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
	if response.status_code != 200:
		raise Exception(f"Failed to connect to OpenAI GPT-4o API: {response.json()}")
	gpt_attr = convert_to_dict(response.json().get("choices")[0].get("message").get("content"))
	gpt_attr['distance'] = item['attributes']['distance']
	item["gpt_attributes"] = deepcopy(gpt_attr)
	return item



def assign_state_attributes(obj_dict, accelerated):
    count = 0
    for id, item in obj_dict.items():
        if item['category'] != 'furniture' and item['category'] != 'decoration' and (not accelerated or item['category'] != 'utensil'):
            state_aware_attribution(item)
        else:
            item['gpt_attributes'] = item['attributes']
            count += 1
    if accelerated:
        print(f"Accelerated: {count} items skipped")
    return obj_dict

def assign_state_attributes_vlm_disabled(obj_dict):
	for id, item in obj_dict.items():
		item['gpt_attributes'] = deepcopy(item['attributes'])
	return obj_dict

