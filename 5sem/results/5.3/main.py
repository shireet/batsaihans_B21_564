from os import path
from PIL import Image
import pandas as pd
from functools import cache
from itertools import product

greek = [
    "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ",
    "μ", "ν", "ξ", "ο", "π", "ρ", "σ","τ","υ","φ","χ","ψ","ω"
]

def shape(image):
    return image.shape

def area(image):
    return image.size[0]*image.size[1]

def moment(p,q,image, start_x, end_x, start_y, end_y):
    m = 0
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            m += (x**p)*(y**q)*(image.getpixel((x,y))/255)
    
    return m

def compute_weights(image, start_x, end_x, start_y, end_y):
    return moment(0,0, image, start_x, end_x, start_y, end_y)

    

def center(image, axis: int):
    if axis not in (0, 1):
        raise ValueError("Invalid axis")
    p = int(not axis)
    q = axis
    return moment(p,q, image , 0, image.size[0], 0, image.size[1])/compute_weights(image, 0, image.size[0], 0, image.size[1])

def relative_center(image, axis: int):
    return center(image, axis) / area(image)

def central_moment(p, q, image):
    x_bar = center(image, 0)
    y_bar = center(image, 1)
    moment = 0    

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            moment += ((x - x_bar)**p)*((y - y_bar)**q)*(image.getpixel((x,y))/255)
        
    return moment

def inertia(image, axis):
    if axis not in (0, 1):
        raise ValueError("Invalid axis")

    p = axis * 2
    q = (1 - axis) * 2
    return central_moment(p, q, image)

def relative_inertia(image, axis):
    return inertia(image, axis)/(compute_weights(image, 0, image.size[0], 0, image.size[1])**2)





if __name__ == '__main__':
    features_list = []
    for i, letter in enumerate(greek):
        img_src = Image.open(f'input/letter_{str(i + 1).zfill(2)}.png').convert('L')

        features = {
            'letter': letter,
            'weight': compute_weights(img_src, 0, img_src.size[0], 0, img_src.size[1]),
            'relative_weight': compute_weights(img_src, 0, img_src.size[0], 0, img_src.size[1])/ area(img_src),
            'weight1' : compute_weights(img_src, 0, img_src.size[0]//2, 0,  img_src.size[1]//2),
            'relative_wight1' : compute_weights(img_src, 0, img_src.size[0]//2, 0,  img_src.size[1]//2)/ (area(img_src)//4),
            'weight2' :   compute_weights(img_src, 0, img_src.size[0]//2, img_src.size[1]//2, img_src.size[1]),
            'relative_weight2' : compute_weights(img_src, 0, img_src.size[0]//2, img_src.size[1]//2, img_src.size[1])/ (area(img_src)//4),
            'weight3' : compute_weights(img_src, img_src.size[0]//2, img_src.size[0] , 0, img_src.size[1]//2),
            'relative_weight3' : compute_weights(img_src, img_src.size[0]//2, img_src.size[0] , 0, img_src.size[1]//2)/ (area(img_src)//4),
            'weight4' :  compute_weights(img_src, img_src.size[0]//2, img_src.size[0] , img_src.size[1]//2, img_src.size[1]),
            'relative_weight4' : compute_weights(img_src, img_src.size[0]//2, img_src.size[0] , img_src.size[1]//2, img_src.size[1])/(area(img_src)//4),
            'center_x': center(img_src, 0),
            'center_y': center(img_src, 1),
            'relative_center_x': relative_center(img_src, 0),
            'relative_center_y': relative_center(img_src, 1),
            'inertia_x': inertia(img_src, 0),
            'inertia_y': inertia(img_src, 1),
            'relative_inertia_x': relative_inertia(img_src, 0),
            'relative_inertia_y': relative_inertia(img_src, 1),
        }
        features_list.append(features)
    df = pd.DataFrame(features_list)
    df.to_csv('output/features.csv', index=False)



