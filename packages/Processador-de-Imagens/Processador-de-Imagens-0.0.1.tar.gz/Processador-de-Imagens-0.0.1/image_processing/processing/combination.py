# Aqui é onde é feito a combinação das imagens.

from locale import normalize
import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def find_difference(image1, image2):
    """ Essa função returna a diferença normalizada entre as imagens"""
    assert image1.shape == image2.shape, "Specify 2 images with de same shape."
    # convertendo a imagem para tons de cinza:
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)
    # achando o score (vai de 0 á 1) e  difference_image (diferença entre as imagens):
    (score, difference_image) = structural_similarity(gray_image1, gray_image2, full=True)
    print("Similarity of the images: ", score)
    #normalizando difference_image:
    normalized_difference_image = (difference_image-np.min(difference_image))/(np.max(difference_image)-np.min(difference_image))
    return normalized_difference_image

def transfer_histogram(image1, image2):
    matched_image = match_histograms(image1, image2, multichannel=True)
    return matched_image