from data.objects import *
import math


maps = [[[0 for _ in range(16)] for _ in range(16)],
        [[1 for _ in range(16)] for _ in range(16)]]


def get_map(num_map, canvas):
    hole = Object(0, 0, 25, 25, 'hole.png', canvas)
    walls = Group()

    if num_map == 0:
        all_map = Field(200, 0, 16, 16, 50, canvas, f'sfdsf_{num_map}')
        hole.go_to(400, 500)

        obj = WallObject(205, 0, 205, 800, 10, canvas)
        walls.add_objects(obj)
        obj = WallObject(200, 5, 1000, 5, 10, canvas)
        walls.add_objects(obj)

        obj = WallObject(995, 0, 995, 800, 10, canvas)
        walls.add_objects(obj)
        obj = WallObject(200, 795, 1000, 795, 10, canvas)
        walls.add_objects(obj)
        print('------------------')

        obj = WallObject(800, 200, 500, 300, 10, canvas)
        walls.add_objects(obj)

    else:
        all_map = Field(200, 0, 16, 16, 50, canvas, '')

    return hole, all_map.group, walls, (all_map.player_1_x, all_map.player_1_y,
                                        all_map.player_2_x, all_map.player_2_y), all_map


class WallObject():
    def __init__(self, x1, y1, x2, y2, w, canvas, img=None, visibility=True):
        if x1 > x2:
            x2, x1 = x1, x2
            y2, y1 = y1, y2
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.w = w
        self.canvas = canvas
        self.rotate = self.set_rotate()
        print(self.rotate)

        self.obj = None
        self.img = img
        self.visibility = visibility
        self.create_obj()


    def create_obj(self):
        if self.visibility:
            if self.obj is None:
                self.obj = self.canvas.create_line(self.x1, self.y1, self.x2,
                                                   self.y2, width=self.w)
            else:
                self.obj = self.canvas.create_line(self.x1, self.y1, self.x2,
                                                   self.y2, width=self.w)

    def hide(self):
        self.visibility = False
        self.canvas.delete(self.obj)

    def check_point(self, x, y, dop=0, r=13):

        if self.x1 <= self.x2:
            rez_x = x >= self.x1 - self.w / 2 - r and x <= self.x2 + self.w / 2 + r
        else:
            rez_x = x >= self.x2 - self.w / 2 - r and x <= self.x1 + self.w / 2 + r
        if self.y1 <= self.y2:
            rez_y = y >= self.y1 - self.w / 2 - r and y <= self.y2 + self.w / 2 + r
        else:
            rez_y = y >= self.y2 - self.w / 2 - r and y <= self.y1 + self.w / 2 + r


        if rez_x and rez_y:
            x2 = self.x2 - self.x1
            y2 = self.y2 - self.y1
            x = x - self.x1
            y = y - self.y1

            if x2 != 0:
                k = y2 / x2
            else:
                k = 800
            a = (x2 * x + y2 * y) / (y2 * k + x2)
            rez = ((a - x) ** 2 + (k * a - y) ** 2) ** 0.5

            return rez < self.w / 2 + (r - 2.7) + dop
        else:
            return False

    def get_rotation(self, ball_rotate):
        return ball_rotate + 180 + (self.rotate - ball_rotate) * 2


    def show(self):
        self.visibility = True
        self.create_obj()

    def set_rotate(self):
        if self.y1 - self.y2 >= 0 and self.x1 - self.x2 >= 0:
            if self.x1 - self.x2 != 0:
                rotate = math.atan(
                    (self.y1 - self.y2) / (self.x1 - self.x2)) * 180 / math.pi
            else:
                rotate = 0

        elif self.y1 - self.y2 >= 0 and self.x1 - self.x2 <= 0:
            if self.x1 - self.x2 != 0:
                rotate = math.atan(
                    (self.y1 - self.y2) / (self.x1 - self.x2)) * 180 / math.pi
                rotate *= -1
            else:
                rotate = 0

        elif self.y1 - self.y2 <= 0 and self.x1 - self.x2 <= 0:
            if self.x1 - self.x2 != 0:
                rotate = math.atan(
                    (self.y1 - self.y2) / (self.x1 - self.x2)) * 180 / math.pi
                rotate *= -1
            else:
                rotate = -90
        else:
            if self.x1 - self.x2 != 0:
                rotate = math.atan(
                    (self.y1 - self.y2) / (self.x1 - self.x2)) * 180 / math.pi
            else:
                rotate = 180
        return rotate


class Wall():
    def __init__(self, x1, y1, x2, y2, w, rotate):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.w = w
        self.rotate = rotate

    def get_rotation(self, ball_rotate):
        return ball_rotate + 180 + (self.rotate - ball_rotate) * 2

    def check_point(self, x, y):
        x1 = 0
        y1 = 0
        x2 = self.x2 - self.x1
        y2 = self.y2 - self.y1
        x = x - self.x1
        y = y - self.y1

        if x2 != 0:
            k = y2 / x2
        else:
            k = 800
        a = (x2 * x + y2 * y) / (y2 * k + x2)
        rez = ((a - x) ** 2 + (k * a - y) ** 2) ** 0.5

        if self.rotate >= 0:
            if rez < 12:
                print(self.rotate)
                print(1)
            return rez < 1
        else:
            if rez < 12:
                print(self.rotate)
                print(2)
            return rez < 12


