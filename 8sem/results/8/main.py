import os
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

d=1
phi = [0, 90, 180, 270]

#histogram equalization
def contrast(img:np.array):
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    img2 = cdf[img]
    return img2

def haralick_matrix(img, d):
    haralick = np.zeros((256, 256))
    W, H = img.shape
    k = 4*W*H - 2*W - 2*H

    for x in range(d, img.shape[0] - d):
        for y in range(d, img.shape[1] - d):
            haralick[img[x - d, y], img[x, y]] += 1
            haralick[img[x + d, y], img[x, y]] += 1
            haralick[img[x, y - d], img[x, y]] += 1
            haralick[img[x, y + d], img[x, y]] += 1
    return np.uint8(haralick), k


def ASM(haralick, k):
    return np.sum(np.square(haralick*k)) 

def MPR(haralick, k):
    return np.max(haralick*k)

def TR(haralick, k):
    return np.trace(haralick*k)

def ENT(haralick, k):
    ent = 0
    matrix = haralick*k
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] > 0:
                ent -= matrix[i, j] * np.log2(matrix[i, j])
    return ent



if __name__ == "__main__":
    with open("output/result.txt", "w") as file:
        for i in os.listdir("input"):
            if i == ".DS_Store":
                continue
            img = Image.open('input/'+i).convert('L')
            img.save("output/grayscale/"+i+"")
            semi = np.array(Image.open(os.path.join('output', 'grayscale', i)).convert('L'))
            contrast_grayscale = contrast(semi)
            Image.fromarray(contrast_grayscale).save("output/contrast/"+i+"")

            #grayscale  
            matrix1, k = haralick_matrix(semi, 1)
            Image.fromarray(matrix1/k * 255/np.max(matrix1/k)).convert('L').save('output/grayscale/' + "haralick_"+i)
            
            hist, bins = np.histogram(semi.flatten(), 256, [0, 256])
            plt.bar(np.arange(hist.size), hist)
            plt.savefig("output/grayscale/"+"histogram_"+i)
            plt.clf()
            

            #contrast
            matrix2, k = haralick_matrix(contrast_grayscale, 1)
            Image.fromarray(matrix2/k * 255/np.max(matrix2/k)).convert('L').save('output/contrast/' + "haralick_"+i)
            
            hist, bins = np.histogram(contrast_grayscale.flatten(), 256, [0, 256])
            plt.bar(np.arange(hist.size), hist)
            plt.savefig("output/contrast/"+"histogram_"+i)
            plt.clf()




            file.write("Image: "+i+"\n")
            file.write("Grayscale Image:\n")
            file.write("ASM: "+str(ASM(matrix1, k))+"\n")
            file.write("MPR: "+str(MPR(matrix1, k))+"\n")
            file.write("TR: "+str(TR(matrix1, k))+"\n")
            file.write("ENT: "+str(ENT(matrix1, k))+"\n")
            file.write("Contrast Image:\n")
            file.write("ASM: "+str(ASM(matrix2, k))+"\n")
            file.write("MPR: "+str(MPR(matrix2, k))+"\n")
            file.write("TR: "+str(TR(matrix2, k))+"\n")
            file.write("ENT: "+str(ENT(matrix2, k))+"\n")
            file.write("\n")
        file.close()
    




        
    