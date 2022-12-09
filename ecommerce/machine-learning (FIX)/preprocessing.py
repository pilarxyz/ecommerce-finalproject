import base64
import torch
import numpy as np

from io import BytesIO
from PIL import Image
from torchvision.transforms import transforms

class Preprocessing:
    device = torch.device("cpu") 
    image_transforms_test = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5), (0.5))
    ])

    def __init__(self, img_name):
        self.img_name = img_name

    def load_image(self):
        image = Image.open(BytesIO(base64.b64decode(self.img_name)))
        image = self.image_transforms_test(image).float()
        image = image.to(self.device)
        self.image = image.unsqueeze(0)

    @property
    def real_image(self):
        return self.img_name

    @property
    def get_image_(self):
        return self.image

