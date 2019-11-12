import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)


class Vector:

    def __init__(self, x):
        self.x = x

    def __sub__(self, other):  # разность векторов
        return self.x[0] - other.x[0], self.x[1] - other.x[1]

    def __add__(self, other):  # сумма векторов
        return self.x[0] + other.x[0], self.x[1] + other.x[1]

    def __len__(self):  # длинна вектора
        return sqrt(self.x[0] * self.x[0] + self.x[1] * self.x[1])

    def __mul__(self, other):
        if self.x != int or self.x != float:
            return self.x[0] * other, self.x[1] * other
        else:
            return self.x[0] * other.x[0], self.x[1] * other.x[1]

    def int_pair(self):
        return int(self.x[0]), int(self.x[1])


class Line:

    def __init__(self):
        self.speeds = []
        self.points = []

    def draw_points(self, points, style="points", width=4, color=(255, 255, 255)):
        if style == "line":
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (int(points[point_number][0]), int(points[point_number][1])),
                                 (int(points[point_number + 1][0]), int(points[point_number + 1][1])), width)

        elif style == "points":
            for point in points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(point[0]), int(point[1])), width)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return Vector(Vector(points[deg]) * alpha) + Vector(Vector(self.get_point(points, alpha, deg - 1)) * (1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        result = []
        for i in range(count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def set_points(self, points, speeds):
        for point in range(len(points)):
            points[point] = Vector(points[point]) + Vector(speeds[point])
            if points[point][0] > SCREEN_SIZE[0] or points[point][0] < 0:
                speeds[point] = (- speeds[point][0], speeds[point][1])
            if points[point][1] > SCREEN_SIZE[1] or points[point][1] < 0:
                speeds[point] = (speeds[point][0], -speeds[point][1])

    def delete_point(self, index):
        points.pop(index)
        speeds.pop(index)

    def change_speed(self, n):
        for i in range(len(speeds)):
            if -20 < speeds[i][0] < 20 and -20 < speeds[i][1] < 20:
                speeds[i] = Vector(speeds[i]) * n
            else:
                if n < 2:
                    speeds[i] = Vector(speeds[i]) * n


class Joint(Line):

    def __init__(self):
        super().__init__()

    def get_joint(self, count):
        if len(points) < 3:
            return []
        result = []
        for i in range(-2, len(points) - 2):
            pnt = list()
            pnt.append(Vector((Vector(points[i]) + Vector(points[i + 1]))) * 0.5)
            pnt.append(points[i + 1])
            pnt.append(Vector((Vector(points[i + 1]) + Vector(points[i + 2]))) * 0.5)

            result.extend(self.get_points(pnt, count))
        return result


def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = list()
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(['Delete', "Удалить одну из точек"])
    data.append(["Arrow UP", "Повысить скорость"])
    data.append(["Arrow DOWN", "Понизить скорость"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    points = []
    speeds = []
    show_help = False
    pause = False
    joint = Joint()

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_DELETE:
                    if len(points) > 0:
                        joint.delete_point(-1)
                if event.key == pygame.K_UP:
                    joint.change_speed(2)
                if event.key == pygame.K_DOWN:
                    joint.change_speed(0.5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(event.pos)
                speeds.append((random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        joint.draw_points(points)
        joint.draw_points(joint.get_joint(steps), "line", 4, color)
        if not pause:
            joint.set_points(points, speeds)
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

