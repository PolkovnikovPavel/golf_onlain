from data.objects import *


maps = [[[0 for _ in range(16)] for _ in range(16)],
        [[1 for _ in range(16)] for _ in range(16)]]


def get_map(num_map, canvas):
    hole = Object(0, 0, 25, 25, 'hole.png', canvas)
    grass = Group()
    walls = Group()
    x_1, y_1 = 400, 500
    x_2, y_2 = 425, 500
    if num_map == 0:
        hole.go_to(400, 500)
        for i in range(len(maps[num_map])):
            for j in range(len(maps[num_map][i])):
                if maps[num_map][i][j] == 1:
                    obj = Object(200 + j * 50, i * 50, 50, 50, 'grass_2.png', canvas)
                    obj.container = {'id': maps[num_map][i][j], 'speed': 0.35}
                else:
                    obj = Object(200 + j * 50, i * 50, 50, 50, 'grass_1.png',
                                 canvas)
                    obj.container = {'id': maps[num_map][i][j], 'speed': 1}
                grass.add_objects(obj)

    return hole, grass, walls, (x_1, y_1, x_2, y_2)


