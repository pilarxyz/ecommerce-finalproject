import torch
from inference import inference_process
from postprocessing import visualization
from preprocessing import process_image
from initialization import Model

# Input image file in jpg, jpeg, or png
input_image = input('Enter image file name: ')

# Initialization
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

PATH = 'model_25K_data_with_flip.pt'
model = Model()
model.load_state_dict(torch.load(PATH))
model.eval()

# Preprocessing
tensor_image, image = process_image(input_image)

# Prediction
label, confidence = inference_process(tensor_image, model)

# Post-processing
visualization(image, label, confidence)
