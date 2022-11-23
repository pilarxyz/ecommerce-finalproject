import matplotlib.pyplot as plt

def visualization(image, label, confindence):
    plt.title(f'{label} {confindence}')
    plt.axis('off')
    plt.imshow(image)
    plt.show();