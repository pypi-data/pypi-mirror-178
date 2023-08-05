'''
image helper functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import cv2
import numpy as np


def load_image(image_path):
    '''
    load image as RGB float
    '''
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image.astype(np.float32) / 255.0
