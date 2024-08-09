import base64
import requests
import os
from PIL import Image
from io import BytesIO

api_key = os.environ.get("OPENAI_API_KEY")

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_info(image_path):
  base64_image = encode_image(image_path)

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
            "text": """
              Your task is to find and count objects in the image. All objects in the image should fall under the following categories: 
              utensil (forks, spoons etc),
              plate (plates, bowls, etc), 
              cup (mugs, glasses, shot glases, wine glasses, etc),
              cookware (pots, pans, skillets, casseroles, dutch ovens, etc),
              condiment (salt, pepper, ketchup, mustard, including condiment bottles and shakers),
              alcohol (beer, wine, liquor, etc),
              temporary (napkins, paper towels, menu cards, wrist watches, eye glasses, etc, coasters),
              permanent (vase, candle, candle holder, centerpiece, flowers, etc)

              For each object that you detect, you MUST use one of the categories above. If you are unsure about the category, you can use the category "other".

              In your output, please also provide the count of items in each category in a comma separated format. For example, if there are 2 forks, 2 spoons, 4 bowls, and a salt shaker, you should output:

              utensil,2,plate,4,condiment,1

              DO NOT include anything else in your output other than the comma separated list of categories and counts.

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

  return(response.json().get("choices")[0].get("message").get("content"))


def main():
  image_path = "images/input/dining_table_1.jpg"
  print(get_info(image_path))

if __name__ == "__main__":
  main()