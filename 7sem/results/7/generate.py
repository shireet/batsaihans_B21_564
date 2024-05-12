import os
import numpy as np
import pandas as pd
from PIL import Image, ImageFont
from PIL.ImageOps import invert



def generate_sentence(sentence, name, font_size):
    font = ImageFont.truetype("times-new-roman-greek.ttf", size=font_size)
    mask_image = font.getmask(sentence, "L")
    img = Image.new("L", mask_image.size)
    img.im.paste((255), (0, 0) + mask_image.size, mask_image)
    invert(img).save(name)