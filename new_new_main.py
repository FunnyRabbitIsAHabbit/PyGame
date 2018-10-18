"""PyGame project
Developer Ermokhin Stanislav Alexandrovich"""

import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)


class Py(object):
    """A fine class"""

    game_display = pygame.display.set_mode(SCREEN_SIZE)

    def __init__(self, _object=None):
        """A fine method"""

        self._object = _object
        self.game_display = Py.game_display
        pygame.display.set_caption("Screen Saver")

        self.steps = 20
        self.working = True
        self.points = []
        self.speeds = []
        self.show_help = False
        self.pause = False

        self.color_param = 0
        self.color = pygame.Color(0)

    def display_help(self):
        """A fine method"""

        self.game_display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("arial", 30)
        font2 = pygame.font.SysFont("serif", 30)
        data = [["F1", "Помощь"],
                ["R", "Перезапуск"],
                ["P", "Воспроизвести / Пауза"],
                ["Num+", "Добавить точку"],
                ["Num-", "Удалить точку"],
                ["W", "Быстрее (>> в обратную сторону)"],
                ["S", "Медленнее (>> в обратную сторону)"],
                ["BACKSPACE", "Удалить точку"],
                ["", ""],
                [str(self.steps), "текущих точек"]]

        pygame.draw.lines(self.game_display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for item, text in enumerate(data):
            self.game_display.blit(font1.render(
                text[0], True, (128, 128, 255)), (50, 100 + 30 * item))
            self.game_display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * item))

    def main(self):
        """A fine main"""

        pygame.init()

        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.points = []
                        self.speeds = []
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0
                    if event.key == pygame.K_w:
                        self.speeds = [(x+2, y+2) for (x, y) in self.speeds]
                    if event.key == pygame.K_s:
                        self.speeds = [(x-2, y-2) for (x, y) in self.speeds]

                    if event.key == pygame.K_BACKSPACE:
                        self._object.del_point(self.points, self.speeds)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.points.append(event.pos)
                    if not len(self.speeds) == 0:
                        self.speeds.append(self.speeds[-1])

                    else:
                        self.speeds.append((random() * 2, random() * 2))

            self.game_display.fill((0, 0, 0))
            self.color_param = (self.color_param + 1) % 360
            self.color.hsla = (self.color_param, 100, 50, 100)
            self._object.static_draw_points(self.points)
            self._object.static_draw_points(self._object.get_joint(self.steps), "line", 4, self.color)
            if not self.pause:
                self._object.set_points()
            if self.show_help:
                self.display_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


class Vector(object):
    """A fine class"""

    def __init__(self, x1=0, x2=0):
        """A fine method"""

        self.x1 = x1
        self.x2 = x2

    def __getitem__(self, item):
        """A fine method"""

        return self.x1 if item == 0 else self.x2

    def __repr__(self):
        """A fine method"""

        return self.x1, self.x2

    def __str__(self):
        """A fine method"""

        return str(self.x1) + ' ' + str(self.x2)

    def __add__(self, other):
        """A fine method"""

        return Vector(self.x1 + other.x1, self.x2 + other.x2)

    def __sub__(self, other):
        """A fine method"""

        return Vector(self.x1 - other.x1, self.x2 - other.x2)

    def __mul__(self, k):
        """A fine method"""

        return Vector(self.x1 * k, self.x2 * k)

    def length(self):
        """A fine method"""

        return sqrt(self.x1 * self.x1 + self.x2 * self.x2)

    def int_pair(self):
        """A fine method"""

        try:
            return int(self.x1), int(self.x2)

        except ValueError:
            return 0, 0


class Line(Py):
    """A fine class"""

    def __init__(self, obj):
        """A fine method"""

        super().__init__(obj)

    def set_points(self):
        """A fine method"""

        for point in range(len(self.points)):
            self.points[point] = Vector(self.points[point][0], self.points[point][1]) + \
                            Vector(self.speeds[point][0], self.speeds[point][1])
            if self.points[point][0] > SCREEN_SIZE[0] or self.points[point][0] < 0:
                self.speeds[point] = (- self.speeds[point][0], self.speeds[point][1])
            if self.points[point][1] > SCREEN_SIZE[1] or self.points[point][1] < 0:
                self.speeds[point] = (self.speeds[point][0], -self.speeds[point][1])

    def draw_points(self, style="points",
                    width=4, color=(255, 255, 255)):
        """A fine method"""

        if style == "line":
            for point_number in range(-1, len(self.points) - 1):
                pygame.draw.line(self.game_display, color,
                                 Vector(self.points[point_number][0],
                                        self.points[point_number][1]).int_pair(),
                                 Vector(self.points[point_number + 1][0],
                                        self.points[point_number + 1][1]).int_pair(), width)

        elif style == "points":
            for point in self.points:
                pygame.draw.circle(self.game_display, color,
                                   Vector(point[0], point[1]).int_pair(), width)

    @staticmethod
    def static_draw_points(lst, style="points",
                           width=4, color=(255, 255, 255)):
        """A fine method"""

        points = lst
        game_display = Line.game_display

        if style == "line":
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(game_display, color,
                                 Vector(points[point_number][0],
                                        points[point_number][1]).int_pair(),
                                 Vector(points[point_number + 1][0],
                                        points[point_number + 1][1]).int_pair(), width)

        elif style == "points":
            for point in points:
                pygame.draw.circle(game_display, color,
                                   Vector(point[0], point[1]).int_pair(), width)

    @staticmethod
    def get_point(points, alpha, deg=None):
        """A fine method"""

        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]

        a = Joint.get_point(points, alpha, deg - 1)

        return Vector(points[deg][0], points[deg][1])*alpha + Vector(a[0], a[1])*(1 - alpha)

    def get_points(self, base_points, count):
        """A fine method"""

        alpha = 1 / count
        result = list()
        for i in range(count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    @staticmethod
    def del_point(lst1, lst2, point=None):
        """A fine method"""

        if point is None and len(lst1) != 0:
            lst1.pop()
            lst2.pop()

        elif len(lst1) != 0:
            lst1.pop(point)
            lst2.pop(point)


class Joint(Line):
    """A fine class"""

    def __init__(self):
        """A fine method"""

        super().__init__(self)

    def get_joint(self, count):
        """A fine method"""

        if len(self.points) < 3:
            return []

        result = list()

        for i in range(-2, len(self.points) - 2):
            pnt = list()
            pnt.append((Vector(self.points[i][0], self.points[i][1]) +
                        Vector(self.points[i + 1][0], self.points[i + 1][1]))*0.5)
            pnt.append(Vector(self.points[i + 1][0], self.points[i + 1][1]))
            pnt.append((Vector(self.points[i + 1][0], self.points[i + 1][1]) +
                        Vector(self.points[i + 2][0], self.points[i + 2][1]))*0.5)

            result.extend(self._object.get_points(pnt, count))

        return result


Joint().main()
