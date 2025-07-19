import math
import random
import sys

import pygame
from pygame.color import THECOLORS

WIDTH, HEIGHT = 500, 500
RES = 10
NUM_BLOBS = 2


class Blob:
    def __init__(self, screen, x, y, r, width=0, dx=0, dy=0, color=(255, 0, 0)):
        self.r = r
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.screen = screen
        self.color = color
        self.width = width

    def draw(self):
        pygame.draw.circle(
            self.screen, self.color, (self.x, self.y), self.r, self.width
        )

    def move(self):
        # self.pos = tuple(self.pos[i] + self.v[i] for i in range(2))
        pass

    def force_to(self, x, y, force=1):
        dx = x - self.x
        dy = y - self.y
        dist = math.hypot(dx, dy)
        self.dx += (dx) / dist**2 * force
        self.dy += (dy) / dist**2 * force

    def update(self):
        self.x += self.dx
        self.y += self.dy

        if self.x + self.r > WIDTH or self.x - self.r < 0:
            self.dx *= -1
        if self.y + self.r > HEIGHT or self.y - self.r < 0:
            self.dy *= -1


class Grid:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size

    def draw(self, blobs):
        font = pygame.font.SysFont("couriernew", self.size // 4)
        grid = []
        for y in range(0, HEIGHT + self.size, self.size):
            grid.append(list())
            for x in range(0, WIDTH + self.size, self.size):
                # cx = w + self.size // 2
                # cy = h + self.size // 2
                res = round(func(x, y, blobs), 2)
                grid[-1].append(res)

                # r = pygame.Rect(w, h, self.size, self.size)
                # pygame.draw.rect(screen, (100, 100, 100), r, 1)

                color = (0, 255 * res / (res + 1), 0)
                # color = (0, 255 * (res >= 1), 0)
                # r = pygame.Rect(x + 1, y + 1, self.size - 2, self.size - 2)
                # pygame.draw.rect(screen, color, r, 0)

                # r = pygame.Rect(x - 1, y - 1, 3, 3)
                # pygame.draw.rect(screen, (255, 255, 255 * (res < 1)), r, 0)

                # text = font.render(str(res), False, THECOLORS["white"])
                # self.screen.blit(text, (cx, cy))
        points = []
        for y in range(0, HEIGHT, self.size):
            for x in range(0, WIDTH, self.size):
                a, b, c, d = (
                    (x, y),
                    (x + self.size, y),
                    (x + self.size, y + self.size),
                    (x, y + self.size),
                )
                marching_squares(screen, a, b, c, d, grid)
        # pygame.draw.polygon(screen, (111, 111, 111), points)


def getState(a, b, c, d):
    return (a >= 1) * 8 + (b >= 1) * 4 + (c >= 1) * 2 + (d >= 1)


def linear_interpolation(p1, p2, a_val, b_val):
    if b_val == a_val:
        return (0, 0)
    t = (1 - a_val) / (b_val - a_val)
    # t=0.5

    return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)
    # return point_1 + (point_2 - point_1) * t


def marching_squares(screen, a, b, c, d, grid):
    a_val = grid[a[1] // RES][a[0] // RES]
    b_val = grid[b[1] // RES][b[0] // RES]
    c_val = grid[c[1] // RES][c[0] // RES]
    d_val = grid[d[1] // RES][d[0] // RES]

    state = getState(a_val, b_val, c_val, d_val)

    top = linear_interpolation(a, b, a_val, b_val)
    right = linear_interpolation(b, c, b_val, c_val)
    bottom = linear_interpolation(c, d, c_val, d_val)
    left = linear_interpolation(d, a, d_val, a_val)

    cases = {
        0: [],
        1: [(left, bottom)],
        2: [(bottom, right)],
        3: [(left, right)],
        4: [(right, top)],
        5: [(left, top), (right, bottom)],
        6: [(bottom, top)],
        7: [(left, top)],
        8: [(top, left)],
        9: [(bottom, top)],
        10: [(bottom, right), (top, left)],
        11: [(top, right)],
        12: [(right, left)],
        13: [(right, bottom)],
        14: [(bottom, left)],
        15: [],
    }

    for edge in cases[state]:
        pygame.draw.line(screen, (255, 255, 255), *edge)
    # return list(itertools.chain.from_iterable(cases[state]))


def func(x, y, blobs):
    return sum([b.r**2 / ((x - b.x) ** 2 + (y - b.y) ** 2 + 1e-6) for b in blobs])


def show_fps(screen, fps):
    font = pygame.font.SysFont("Arial", 50, bold=True)
    text = font.render(str(fps // 1), False, THECOLORS["white"])
    screen.blit(text, (10, 10))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

grid = Grid(screen, size=RES)
blob_center = Blob(screen, WIDTH // 2, HEIGHT // 2, r=20)
blobs = []

random.seed(1)
for i in range(NUM_BLOBS):
    r = random.randint(30, 50)
    x = random.randint(r, WIDTH - r)
    y = random.randint(r, HEIGHT - r)
    dx = random.randint(-4, 4)
    dy = random.randint(-4, 4)

    blobs.append(Blob(screen, x, y, r, 3, 0, 0, color=(100, 0, 0)))

clock = pygame.time.Clock()
pressed = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = True
        if event.type == pygame.MOUSEMOTION and pressed:
            blobs.append(Blob(screen, *event.pos, 10))
        if event.type == pygame.MOUSEBUTTONUP:
            pressed = False
    clock.tick()

    screen.fill(THECOLORS["black"])
    # blob_center.draw()
    for blob in blobs:
        blob.force_to(WIDTH // 2, HEIGHT // 2, 10)
        blob.update()
        if (blob.x - blob_center.x) ** 2 + (blob.y - blob_center.y) ** 2 < 10**2:
            blob_center.r = math.sqrt(blob_center.r**2 + blob.r**2)
            blobs.remove(blob)
    grid.draw(blobs + [blob_center])
    show_fps(screen, clock.get_fps())
    pygame.display.flip()
