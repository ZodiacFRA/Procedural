import copy
import random
from os import listdir
from os.path import isfile, join

from PIL import Image


class Color(object):
    def __init__(self, r=255, g=255, b=255):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f"({self.r}, {self.g}, {self.b})"

    def get_list(self):
        return [self.r, self.g, self.b]


def init_img_buffer(color):
    img_buffer, line = [], []
    for i in range(IMG_SIZE):
        line.append(copy.deepcopy(color))
    for i in range(IMG_SIZE):
        img_buffer.append(copy.deepcopy(line))
    return img_buffer


def prepare_img_buffer(img_buffer):
    res = []
    for x in range(IMG_SIZE):
        for y in range(IMG_SIZE):
            res += img_buffer[x][y].get_list()
    return bytes(res)


def print_img_buffer(img_buffer):
    for line in img_buffer:
        print(line)


def get_rgb_from_hex(hex_code):
    res = tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))
    return res


def load_random_palette(dirpath):
    onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    return load_palette_from_file("./palettes/" + random.choice(onlyfiles))


def load_palette_from_file(filepath):
    palette = []
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read()
        if data[-1] == '\n':
            data = data[:-1]
        data = data.split('\n')
    for color_code in data:
        rgb = get_rgb_from_hex(color_code.lstrip('#'))
        palette.append(Color(*rgb))
    return palette


def create_cube(img_buffer, size, x_start, y_start, palette):
    for ring_idx in range(size//2):
        fill_ring(img_buffer, size, x_start, y_start, ring_idx, random.choice(palette))


def fill_ring(img_buffer, size,  x_start, y_start, ring_idx, color):
    """ring_idx start at 0 (outside) and finish at cube_size - 1 (center)"""
    y = y_start + ring_idx
    final_x_start = x_start + ring_idx
    final_x_end = x_start + size - ring_idx
    final_y_start = y_start + ring_idx
    final_y_end = y_start + size - ring_idx
    # print(f"{'-'*10}\n{final_x_start}/{final_y_start}, {final_x_end}/{final_y_end}", flush=True)

    # Horizontal
    for x in range(final_x_start, final_x_end + 1):
        img_buffer[final_y_start][x] = color
        img_buffer[final_y_end][x] = color
    # Vertical
    for y in range(final_y_start, final_y_end + 1):
        img_buffer[y][final_x_start] = color
        img_buffer[y][final_x_end] = color


if __name__ == '__main__':
    IMG_SIZE = random.choice([128, 256, 512, 1024])
    # palette = load_palette_from_file("./palettes/circus_III.palette")
    palette = load_random_palette("./palettes")
    bg_color = palette.pop(random.randint(0, len(palette) - 1))
    img_buffer = init_img_buffer(bg_color)
    cube_size = random.choice([8, 16, 32])
    for x in range(0, IMG_SIZE, cube_size):
        for y in range(0, IMG_SIZE, cube_size):
            create_cube(img_buffer, cube_size - 1, x, y, palette)

    # img_buffer is a list
    im = Image.frombytes("RGB", (IMG_SIZE, IMG_SIZE), prepare_img_buffer(img_buffer))
    im.save("./example.png", "PNG")
