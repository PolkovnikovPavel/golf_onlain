from PIL import Image, ImageTk
from data.functions import *


def get_image(name, w, h, mode=0):
    size = (w, h)
    img = Image.open(f'images/{name}')
    img = img.resize(size, Image.ANTIALIAS)

    if mode == 1:
        return ImageTk.PhotoImage(img), img
    return ImageTk.PhotoImage(img)


def resize_image(img, w, h):
    size = (w, h)
    img = img.resize(size, Image.ANTIALIAS)

    return ImageTk.PhotoImage(img)

