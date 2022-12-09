import torch
import torch.nn as nn
import torchvision.models as models
from ecommerce.config import MODEL_FOLDER

class Model:
    model = models.mobilenet_v2(pretrained=True)
    model.features[0][0] = nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
    model.classifier[1] = nn.Sequential(
            nn.Linear(model.last_channel, 1000),
            nn.ReLU(),
            nn.Linear(1000, 11)
    )

    def __init__(self):
        self.load_model()

    def load_model(self):
        self.model.load_state_dict(torch.load(MODEL_FOLDER + "mods_3.pt", map_location=torch.device('cpu')), strict=False)
        self.model.eval()

    @property
    def get_model(self):
        return self.model
