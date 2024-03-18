import sys
import os
from PIL import Image

def is_valid_file(path):
    if not os.path.exists(path):
        print(f"{path} does not exist")
        return False
    if not (path.endswith(".png") or path.endswith(".bmp")):
        print(f"{path} is not a PNG or BMP file")
        return False
    
    return True

def semitone(image):
    image = image.convert("RGB")
    width, height = image.size
    new_image = Image.new("L", (width, height))
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            new_pixel = int(0.3 * r + 0.59 * g + 0.11 * b)
            new_image.putpixel((x, y), new_pixel)
    return new_image

def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_image(image, path):
    create_dir_if_not_exists("output")
    image.save(os.path.join("output", path))

def roberts_gradient_x(image, x, y):
    return image.getpixel((x+1,y+1)) - image.getpixel((x,y))

def roberts_gradient_y(image, x, y):
    return image.getpixel((x+1,y)) - image.getpixel((x,y+1))

def roberts_gradient(x,y):
    return abs(x)+abs(y)

def roberts_x(image):
    result = Image.new(image.mode, (image.width, image.height))
    gradient_x_max = 0
    gradient_x_matrix = list()

    for x in range(result.width - 1):
        gradient_x_matrix.append(list())
        for y in range(result.height - 1):
            gradient_x = roberts_gradient_x(image, x, y)

            if gradient_x > gradient_x_max:
                gradient_x_max = gradient_x

            gradient_x_matrix[x].append(gradient_x)

    for x in range(result.width - 1):
        for y in range(result.height - 1):
            result.putpixel((x, y), int(round(gradient_x_matrix[x][y] * 255 / gradient_x_max)))
    return result

def roberts_y(image):
    result = Image.new(image.mode, (image.width, image.height))
    gradient_y_max = 0
    gradient_y_matrix = list()

    for x in range(result.width - 1):
        gradient_y_matrix.append(list())
        for y in range(result.height - 1):
            gradient_x = roberts_gradient_y(image, x, y)

            if gradient_x > gradient_y_max:
                gradient_y_max = gradient_x

            gradient_y_matrix[x].append(gradient_x)

    for x in range(result.width - 1):
        for y in range(result.height - 1):
            result.putpixel((x, y), int(round(gradient_y_matrix[x][y] * 255 / gradient_y_max)))
    return result

def roberts(image):

    result = Image.new(image.mode, (image.width, image.height))
    gradient_max = 0
    gradient_matrix = list()

    for x in range(result.width - 1):
        gradient_matrix.append(list())
        for y in range(result.height - 1):
            gradient_x = roberts_gradient_x(image, x, y)
            gradient_y = roberts_gradient_y(image, x, y)
            gradient = roberts_gradient(gradient_x, gradient_y)

            if gradient > gradient_max:
                gradient_max = gradient

            gradient_matrix[x].append(gradient)

    for x in range(result.width - 1):
        for y in range(result.height - 1):
            result.putpixel((x, y), int(round(gradient_matrix[x][y] * 255 / gradient_max)))

    return result

def roberts_threshold(image, threshold):

    result = Image.new('1', (image.width, image.height))
    gradient_max = 0
    gradient_matrix = list()

    for x in range(result.width - 1):
        gradient_matrix.append(list())
        for y in range(result.height - 1):
            gradient_x = roberts_gradient_x(image, x, y)
            gradient_y = roberts_gradient_y(image, x, y)
            gradient = roberts_gradient(gradient_x, gradient_y)

            if gradient > gradient_max:
                gradient_max = gradient

            gradient_matrix[x].append(gradient)

    for x in range(result.width - 1):
        for y in range(result.height - 1):
            gradient_normalized = int(round(gradient_matrix[x][y] * 255 / gradient_max))
            result.putpixel((x, y), gradient_normalized > threshold)

    return result




if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("no files provided")
        sys.exit(1)

    for i in range(1, len(sys.argv)):
        if not is_valid_file(sys.argv[i]):
            print(f"Invalid file: {sys.argv[i]}")
            sys.exit(1)  

    original = list(map(lambda x: Image.open(x), sys.argv[1:]))
    semitones = list(map(semitone, original))
    G_x = list(map(roberts_x, semitones))
    G_y = list(map(roberts_y, semitones))
    G = list(map(roberts, semitones))
    G_bin = []
    for i in range(10, 20):
        G_bin.append(list(map(lambda x: roberts_threshold(x, i), semitones)))

    for i in range(len(original)):
        filename = os.path.basename(original[i].filename)
        save_image(original[i], f"original_{filename}")
        save_image(semitones[i], f"semitone_{filename}")
        save_image(G_x[i], f"horisontal_{filename}")
        save_image(G_y[i], f"vertical_{filename}")
        save_image(G[i], f"cross_{filename}")
        for j in range(10):
            save_image(G_bin[j][i], f"threshold_{j+10}_{filename}")



