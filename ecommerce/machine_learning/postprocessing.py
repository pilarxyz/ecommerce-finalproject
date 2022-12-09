import matplotlib.pyplot as plt

def visualization(image, label, confindence):
    plt.title(f'{label} with confidence {round(confindence * 100, 3)}%')
    plt.axis('off')
    plt.imshow(image)
    plt.show();