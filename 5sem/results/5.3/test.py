from os import path
from PIL import Image
import pandas as pd
from functools import cache
from itertools import product
import numpy as np

greek = [
    "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ",
    "μ", "ν", "ξ", "ο", "π", "ρ", "σ","τ","υ","φ","χ","ψ","ω"
] 
class FeatureImage:
    def __init__(self, img: Image, invert=True):
        if invert:
            self.img = 1 - np.array(img)
        else:
            self.img = np.array(img)

    @property
    def shape(self):
        return self.img.shape

    def __getitem__(self, key):
        return self.img[key]

    @cache
    def line_by_line_moment(self, p: int, q: int, start_x=None,
                            stop_x=None, start_y=None, stop_y=None) -> int:
        if start_x is None:
            start_x = 0
        if stop_x is None:
            stop_x = self.shape[0]
        if start_y is None:
            start_y = 0
        if stop_y is None:
            stop_y = self.shape[1]

        moment = 0

        for x in range(start_x, stop_x):
            for y in range(start_y, stop_y):
                print(self[x,y])
                moment += x ** p * y ** q * self[x, y]

        return moment

    def weight(self) -> int:

        return self.line_by_line_moment(0, 0)

    def area(self) -> int:
        return self.shape[0] * self.shape[1]

    def relative_weight(self) -> float:
        print("Moment = ",self.line_by_line_moment(0, 0))
        return self.weight() / self.area()

    def weight_I(self) -> int:
        hight = self.shape[0] // 2
        len = self.shape[1] // 2
        return self.line_by_line_moment(0, 0, start_x=0, stop_x=hight,
                                        start_y=0, stop_y=len)

    def relative_weight_I(self) -> float:
        area = self.area() // 4
        return self.weight_I() / area

    def weight_II(self) -> int:
        hight = self.shape[0] // 2
        len = self.shape[1] // 2
        return self.line_by_line_moment(0, 0, start_x=0, stop_x=hight,
                                        start_y=len, stop_y=self.shape[1])

    def relative_weight_II(self) -> float:
        area = self.area() // 4
        return self.weight_II() / area

    def weight_III(self) -> int:
        hight = self.shape[0] // 2
        len = self.shape[1] // 2
        return self.line_by_line_moment(0, 0, start_x=hight,
                                        stop_x=self.shape[0],
                                        start_y=0, stop_y=len)

    def relative_weight_III(self) -> float:
        area = self.area() // 4
        return self.weight_III() / area

    def weight_IV(self) -> int:
        start = self.shape[0] // 2
        start_y = self.shape[1] // 2
        hight = self.shape[0]
        len = self.shape[1]
        return self.line_by_line_moment(0, 0, start_x=start, stop_x=hight,
                                        start_y=start_y, stop_y=len)

    def relative_weight_IV(self) -> float:
        area = self.area() // 4
        return self.weight_IV() / area

    def center(self, axis: int) -> float:
        if axis not in (0, 1):
            raise ValueError("Invalid axis")

        p = int(not axis)
        q = axis
        return self.line_by_line_moment(p, q) / self.weight()

    def relative_center(self, axis: int) -> float:
        normalization_factor = self.shape[axis] - 1
        return (self.center(axis) - 1) / normalization_factor

    @cache
    def central_moment(self, p, q):
        x_bar = self.center(0)
        y_bar = self.center(1)
        moment = 0

        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                moment += (x - x_bar) ** p * (y - y_bar) ** q * self[x, y]

        return moment

    def inertia(self, axis):
        if axis not in (0, 1):
            raise ValueError("Invalid axis")

        p = axis * 2
        q = (1 - axis) * 2
        return self.central_moment(p, q)

    def relative_inertia(self, axis):
        return self.inertia(axis) / self.weight() ** 2


def axis_name(axis):
    return 'y' * (1 - axis) + 'x' * axis


def join_names(*args):
    return '_'.join(filter(lambda string: string != '', args))


def filename(n):
    return f"input/letter_{str(n + 1).zfill(2)}.png" 

if __name__ == '__main__':
    # Calculate features
    df = pd.DataFrame()
    feature_images = {letter: FeatureImage(Image.open(filename(i))) for i,
                      letter in enumerate(greek)}
    df['letter'] = feature_images.keys()
    non_directed_features = ['weight_I', 'weight_II', 'weight_III',
                             'weight_IV', 'weight']
    features = ['center', 'inertia']
    relativities = ['', 'relative']
    directions = [0, 1]

    for feature, relativity in product(non_directed_features, relativities):
        name = join_names(relativity, feature)
        df[name] = list(map(lambda img: getattr(img, name)(),
                            feature_images.values()))

    for feature, relativity, axis in product(features, relativities,
                                             directions):
        name = join_names(relativity, feature)
        df[f'{name}_{axis_name(axis)}'] = list(map(lambda img:
                                                   getattr(img, name)(axis),
                                                   feature_images.values()))

    df.to_csv('output/test.csv', index=False)