import pygame
import math
import random

HORIZON_Y = 121

SKY_COLOR = (158, 233, 247)
WATER_COLOR = (26, 96, 237)

def add((x1, y1), (x2, y2)):
    return (x1 + x2, y1 + y2)


def mul((x, y), k):
    return (x * k, y * k)


def mapf(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


class Entity:
    def __init__(self, surf):
        self.surf = surf
        self.x = 0
        self.y = 0

    def map_pos(self, x, y):
        y_p = mapf(y, 0, 1, HORIZON_Y, self.surf.game.SCREEN_HEIGHT)
        x_p = mapf(x, 0, 1, -1, 1) * mapf(y, 0, 1, 50, 350) + self.surf.game.SCREEN_WIDTH / 2

        return (x_p, y_p)

class Player(Entity):
    BOARD_WIDTH = 20
    PLAYER_BASE_Y = 0.8
    VELOCITY_X = 0.05
    DRAG = 8.0

    def __init__(self, surf):
        Entity.__init__(self, surf)

        self.real_x = 0.5
        self.x = 0.5
        self.y = self.PLAYER_BASE_Y


    def update(self):
        if self.surf.pressed[0]:
            self.x -= self.VELOCITY_X

        elif self.surf.pressed[1]:
            self.x += self.VELOCITY_X


        if self.x > 1:
            self.x = 1

        if self.x < 0:

            self.x = 0


        self.real_x += (self.x - self.real_x) / self.DRAG


    def render(self):
        x, y = self.map_pos(self.real_x, self.y)

        pygame.draw.rect(self.surf.game.display, (255, 0, 0), (x, y, 20, 40))

        p1 = self.map_pos(0.5, 0)

        pygame.draw.line(self.surf.game.display, (0, 0, 0), (x + self.BOARD_WIDTH / 2, y), p1)

        p1 = self.map_pos(1, 0)
        p2 = self.map_pos(1, 1)

        pygame.draw.line(self.surf.game.display, (0, 0, 0), p1, p2)

        p1 = self.map_pos(0, 0)
        p2 = self.map_pos(0, 1)

        pygame.draw.line(self.surf.game.display, (0, 0, 0), p1, p2)




class Rock(Entity):
    SPEED = 0.015
    COLOR = (255, 255, 0)

    def __init__(self, surf):
        Entity.__init__(self, surf)

        self.x = random.random()
        self.y = -0.2
        self.size = self.surf.rock.get_rect().size



    def update(self):
        self.y += self.SPEED

        factor = mapf(self.y, 0, 1, 0.25, 1)
        self.scaled_size = (int(self.size[0] * factor), int(self.size[1] * factor))
        self.scaled = pygame.transform.scale(self.surf.rock, self.scaled_size)

        if self.y > 1:
            print 'removing self...'
            self.surf.entities.remove(self)

    def render(self):
        x, y = self.map_pos(self.x, self.y)

        self.surf.game.display.blit(self.scaled, (x -  self.scaled_size[0] / 2, y))


class Cone(Entity):
    COLOR = (255, 255, 0)

    def __init__(self, surf):
        Entity.__init__(self, surf)

        self.x = random.random()
        self.y = surf.y
        self.size = self.surf.cone.get_rect().size

    def update(self):
        self.real_y = self.surf.y - self.y

        if self.real_y < 0:
            return

        factor = mapf(self.real_y, 0, 1, 0.2, 1)
        self.scaled_size = (int(self.size[0] * factor), int(self.size[1] * factor))
        self.scaled = pygame.transform.scale(self.surf.cone, self.scaled_size)

        if self.real_y > 1:
            print 'removing self...'
            self.surf.entities.remove(self)

    def render(self):
        if self.real_y < 0:
            return

        x, y = self.map_pos(self.x, self.real_y)

        self.surf.game.display.blit(self.scaled, (x -  self.scaled_size[0] / 2, y))


class Surf:
    DEFAULT_SPEED = 0.02

    def __init__(self, game):
        self.game = game
        self.player = Player(self)
        self.background = pygame.image.load('assets/background.jpg')
        self.rock = pygame.image.load('assets/rock.png').convert_alpha()
        self.cone = pygame.image.load('assets/cone.png').convert_alpha()
        self.frame = 0
        self.y = 0
        self.entities = []

        self.flag = True

        self.font = pygame.font.SysFont("Arial", 20)

        self.create_wall()

    def run(self):
        # self.game.display.fill(WATER_COLOR)
        # pygame.draw.rect(self.game.display, SKY_COLOR, (0, 0, self.game.SCREEN_WIDTH, HORIZON_Y))

        self.game.display.blit(self.background, (0, 0))

        self.pressed = self.game.get_pressed()

        self.player.update()

        for e in self.entities:
            e.update()

        entities = (self.entities + [self.player])
        entities.sort(key=lambda x: x.y)

        for e in entities:
            e.render()

        self.frame += 1

        if self.frame % 75 == 0:
            # self.entities.append(Cone(self))
            self.create_wall(0)

        self.y += self.DEFAULT_SPEED


        letter = self.font.render("frame: %d" % self.frame, 0, (255,255,0))
        self.game.display.blit(letter, (20, 20))

    def create_wall(self, x=0, dx=0.2, n=3):
        print 'create_wall'

        for i in range(3):
            c = Cone(self)
            c.x = x + dx * i


            self.entities.append(c)

    def create_corridor(self):
        pass
