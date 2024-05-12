from os import path
from math import ceil
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
import numpy as np


font_path = path.join('times-new-roman-greek.ttf')
font_size = 52
greek = [
    "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ",
    "μ", "ν", "ξ", "ο", "π", "ρ", "σ","τ","υ","φ","χ","ψ","ω"
]

def calculate_profile(img: np.array, axis: int) -> np.array:
    return np.sum(img, axis=1 - axis)


def cut_white(img: np.array, profile: np.array, axis: int) -> np.array:
    start = profile.nonzero()[0][0]
    end = profile.nonzero()[0][-1] + 1

    if axis == 0:
        return img[start:end, :], profile[start:end]
    elif axis == 1:
        return img[:, start:end], profile[start:end]
    
def filename(n):
    return f"results/letter_{str(n)}.png"

def simple_bin(img: np.array, thres: int = 40):
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = semitone(img)

    res_img = np.empty_like(img)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            res_img[x, y] = 255 if img[x, y] > thres else 0
    return res_img


def semitone(img):
    return (0.3 * img[:, :, 0] + 0.59 * img[:, :, 1] + 0.11 *
            img[:, :, 2]).astype(np.uint8)

class FontDrawer:
    def __init__(self):
        self.font = TTFont(font_path)
        self.img_font = ImageFont.truetype(font_path, font_size)
        self.cmap = self.font['cmap']
        self.t = self.cmap.getcmap(3, 1).cmap
        self.s = self.font.getGlyphSet()
        self.units_per_em = self.font['head'].unitsPerEm

    def render_text(self, text):
        img = Image.new(mode="RGB",
                        size=(ceil(self.get_text_width(text, font_size)),
                              font_size),
                        color="white")

        draw = ImageDraw.Draw(img)
        draw.text((0, -5), text, (0, 0, 0), font=self.img_font)

        return img

    def render_binarized(self, text, level=100):
        img = self.render_text(text)
        return 255 - simple_bin(np.array(img), level)

    def get_char_width(self, c, point_size):
        assert len(c) == 1

        if ord(c) in self.t and self.t[ord(c)] in self.s:
            pts = self.s[self.t[ord(c)]].width

        else:
            pts = self.s['.notdef'].width

        return pts * float(point_size) / self.units_per_em

    def get_text_width(self, text, point_size):
        total = 100

        for c in text:
            total += self.get_char_width(c, point_size)

        return total


def save_arr_as_img(arr, file_name):
    binarized_letter = Image.fromarray(255 - arr, 'L')
    binarized_letter = binarized_letter.convert('1')
    binarized_letter.save(file_name)


if __name__ == '__main__':
    font_drawer = FontDrawer()
    for i, letter in enumerate(greek):
        binarized_arr = font_drawer.render_binarized(letter)
        for axis in (0, 1):
            letter_profile = calculate_profile(binarized_arr, axis)
            binarized_arr, _ = cut_white(binarized_arr, letter_profile, axis)

        save_arr_as_img(binarized_arr, filename(i))