import copy
import random

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


def create_cube(img_buffer, size, x_start, y_start, palette):
    for ring_idx in range(size//2):
        fill_ring(img_buffer, size, x_start, y_start, ring_idx, random.choice(palette))


def print_img_buffer(img_buffer):
    for line in img_buffer:
        print(line)


def fill_ring(img_buffer, size,  x_start, y_start, ring_idx, color):
    """ring_idx start at 0 (outside) and finish at cube_size - 1 (center)"""
    y = y_start + ring_idx
    final_x_start = x_start + ring_idx
    final_x_end = x_start + size - ring_idx
    final_y_start = y_start + ring_idx
    final_y_end = y_start + size - ring_idx
    # print(f"{'-'*10}\n{final_x_start}/{final_y_start}, {final_x_end}/{final_y_end}")

    # Horizontal
    for x in range(final_x_start, final_x_end + 1):
        img_buffer[final_y_start][x] = color
        img_buffer[final_y_end][x] = color
    # Vertical
    for y in range(final_y_start, final_y_end + 1):
        img_buffer[y][final_x_start] = color
        img_buffer[y][final_x_end] = color


if __name__ == '__main__':
    IMG_SIZE = 128
    black = Color(0, 0, 0)
    white = Color(255, 255, 255)
    red = Color(255, 0, 0)
    blue = Color(0, 0, 255)
    green = Color(0, 255, 0)
    palette = [black, red, blue, green]

    img_buffer = init_img_buffer(white)
    cube_size = 8
    for x in range(0, IMG_SIZE, cube_size):
        for y in range(0, IMG_SIZE, cube_size):
            create_cube(img_buffer, cube_size - 1, x, y, palette)

    # img_buffer is a list
    im = Image.frombytes("RGB", (IMG_SIZE, IMG_SIZE), prepare_img_buffer(img_buffer))
    im.save("./test.png", "PNG")
