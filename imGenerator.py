from PIL import Image
import copy

IMG_WIDTH = 2
# IMG_HEIGHT = 512


class Color(object):
    def __init__(self, r=255, g=255, b=255):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f"({self.r}, {self.g}, {self.b})"


def create_cube(size):
    tmp_buffer = [255] * 3 * size ** 2
    fill_ring(tmp_buffer, size, 0, [255, 0, 0])
    return tmp_buffer


def fill_ring(tmp_buffer, cube_size, ring_idx, color):
    """ring_idx start at 0 (outside) and finish at cube_size - 1 (center)"""
    # Top line
    for x in range(ring_idx, cube_size, 3):
        tmp_buffer[ring_idx][x + 0] = 12# color[0]
        tmp_buffer[ring_idx][x + 1] = color[1]
        tmp_buffer[ring_idx][x + 2] = color[2]
    # Bottom line
    for x in range(ring_idx, cube_size, 3):
        tmp_buffer[cube_size - ring_idx][x + 0] = color[0]
        tmp_buffer[cube_size - ring_idx][x + 1] = color[1]
        tmp_buffer[cube_size - ring_idx][x + 2] = color[2]


if __name__ == '__main__':
    img_buffer = []
    line = []
    for i in range(IMG_WIDTH):
        line.append(Color())
    for i in range(IMG_WIDTH):
        img_buffer.append(copy.deepcopy(line))

    for line in img_buffer:
        print(line)
    print("-"*10)
    img_buffer[0][0].r = 0
    for line in img_buffer:
        print(line)


    exit()
    cube_size = 16
    tmp_cube = create_cube(cube_size*3)
    for x in range(cube_size*3):
        for y in range(cube_size*3):
            img_buffer[x][y] = tmp_cube[x][y]


    im = Image.frombytes("RGB", (IMG_WIDTH, IMG_WIDTH), bytes(img_buffer))
    im.save("./test.png", "PNG")
