import base64
import torch

from torchvision import transforms
from PIL import Image , ImageOps

def process_image(input_image):
    image = Image.open(input_image)

    resize_image = image.resize((128, 128))  

    if image.mode == 'RGB':
        image = image.convert('L')
        image = ImageOps.invert(image)
    else:
        image = image.convert('L')
    
    image_transforms = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.5), (0.5))
    ])

    tensor_image = image_transforms(image).float()
    tensor_image = torch.unsqueeze(tensor_image, 0)

    return tensor_image, resize_image    