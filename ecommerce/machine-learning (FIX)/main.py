import base64
import numpy as np

from init import Model
from preprocessing import Preprocessing
from inference import Inference

class Main:
    def __init__(self, img_input):
        self.img_input = img_input
        self.inference()
        self.postpreprocessing()

    def get_model(self):
        model = Model()
        model = model.get_model
        return model

    def prepare_input(self):
        prep = Preprocessing(img_name=self.img_input)
        prep.load_image()
        prep = prep.get_image_
        return prep

    def inference(self):
        model = self.get_model()
        prep = self.prepare_input()
        # print(model)
        model = Inference(model, prep)
        self.result = model.forward()

    def postpreprocessing(self):
        labels_data = {
            0: "Ankle Boot",
            1: "Bag",
            2: "Coat",
            3: "Dress",
            4: "Hat / Cap",
            5: "Pullover",
            6: "Sandal",
            7: "Shirt",
            8: "Sneaker",
            9: "T-Shirt",
            10: "Trouser"
        }
        label = labels_data[self.result.tolist()[0]]
        self._label = label

    @property
    def get_results(self):
        return self._label
