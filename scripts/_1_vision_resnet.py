import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torch
import json
import urllib.request

url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
filename = "imagenet_classes.json"

urllib.request.urlretrieve(url, filename)

with open(filename) as f:
    classes = json.load(f)

model = models.resnet50(pretrained=True)
model.eval() 

image_path = 'images/input/dining_table_1.jpg'
input_image = Image.open(image_path)
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
input_tensor = preprocess(input_image)
input_batch = input_tensor.unsqueeze(0)  

if torch.cuda.is_available():
    input_batch = input_batch.to('cuda')
    model.to('cuda')

with torch.no_grad():
    output = model(input_batch)

probabilities = torch.nn.functional.softmax(output[0], dim=0)

_, indices = torch.sort(output, descending=True)
percentage = torch.nn.functional.softmax(output, dim=1)[0] * 100

top_classes = [(classes[idx.item()], percentage[idx.item()].item()) for idx in indices[0][:5]]
print(top_classes)