import pygame
import math
import random
import menu

HORIZON_Y = 121

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
        self.to_remove = False
        self.scaled_size=[]

    def remove(self):
        self.to_remove = True

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
        self.lives = 3



    def update(self):
        if self.lives <= 0:
            self.surf.end_game()

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

        pygame.draw.rect(self.surf.game.display, (255, 255, 0), (x, y, 20, 40))

        p1 = self.map_pos(0.5, 0)

        # pygame.draw.line(self.surf.game.display, (0, 0, 0), (x + self.BOARD_WIDTH / 2, y), p1)

        p1 = self.map_pos(1, 0)
        p2 = self.map_pos(1, 1)

        pygame.draw.line(self.surf.game.display, (0, 0, 0), p1, p2)

        p1 = self.map_pos(0, 0)
        p2 = self.map_pos(0, 1)

        pygame.draw.line(self.surf.game.display, (0, 0, 0), p1, p2)

        #Render Life
        lives_image = pygame.transform.scale(self.surf.amazon, (50,50))

        for i in range(self.lives):
            self.surf.game.display.blit(lives_image,(lives_image.get_size()[0] * i, 0))
    
    def get_rect(self):
        x, y = self.map_pos(self.real_x, self.y)
        return pygame.Rect(x, y, 20, 40)



class Rock(Entity):
    SPEED = 0.015
    COLOR = (255, 255, 0)

    def __init__(self, surf):
        Entity.__init__(self, surf)

        self.x = random.random()
        self.y = -0.2
        self.size = self.surf.rock.get_rect().size



    def update2(self):
        self.y += self.SPEED

        factor = mapf(self.y, 0, 1, 0.25, 1)
        self.scaled_size = (int(self.size[0] * factor), int(self.size[1] * factor))
        self.scaled = pygame.transform.scale(self.surf.rock, self.scaled_size)

        if self.y > 1:
            #print 'removing self...'
            #self.remove()
            self.y = self.surf.y + random.random()

    def update(self):
        self.real_y = self.surf.y - self.y

        if self.real_y < 0:
            return

        factor = mapf(self.real_y, 0, 1, 0.2, 1)
        self.scaled_size = (int(self.size[0] * factor), int(self.size[1] * factor))
        self.scaled = pygame.transform.scale(self.surf.rock, self.scaled_size)

        if self.real_y > 1:
            self.y = self.surf.y + random.random()


    def render2(self):
        x, y = self.map_pos(self.x, self.y)

        self.surf.game.display.blit(self.scaled, (x -  self.scaled_size[0] / 2, y))

    def render(self):
        if self.real_y < 0:
            return

        x, y = self.map_pos(self.x, self.real_y)

        self.surf.game.display.blit(self.scaled, (x -  self.scaled_size[0] / 2, y - self.scaled_size[1] / 2))

    def get_rect(self):
        x, y = self.map_pos(self.x, self.y)
        return pygame.Rect((x -  self.scaled_size[0] / 2, y), self.scaled_size)


class Tree(Entity):
    def __init__(self, surf):
        Entity.__init__(self, surf)

        self.y = surf.y
        self.size = self.surf.tree.get_rect().size


    def update(self):
        self.real_y = self.surf.y - self.y

        if self.real_y < 0:
            return

        factor = mapf(self.real_y, 0, 1, 0.2, 1)
        self.scaled_size = (int(self.size[0] * factor), int(self.size[1] * factor))
        self.scaled = pygame.transform.scale(self.surf.tree, self.scaled_size)

        if self.real_y > 1:
            self.y = self.surf.y + random.random()


    def render(self):
        if self.real_y < 0:
            return

        x, y = self.map_pos(self.x, self.real_y)

        self.surf.game.display.blit(self.scaled, (x -  self.scaled_size[0] / 2, y - self.scaled_size[1] / 2))




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
            self.remove()

    def render(self):
        if self.real_y < 0:
            return

        x, y = self.map_pos(self.x, self.real_y)

        self.surf.game.display.blit(self.scaled, (x -  self.scaled_size[0] / 2, y))

    def get_rect(self):
        if len(self.scaled_size)<2:
            return pygame.Rect(0,0,0,0)
        x, y = self.map_pos(self.x, self.real_y)
        return pygame.Rect((x -  self.scaled_size[0] / 2, y),self.scaled_size)



class Surf:
    DEFAULT_SPEED = 0.02
    BOOST_SPEED = 0.03
    SLOW_SPEED = 0.01
    SPEED_DAMP = 20.0 # steps required to change speed

    # Key mapping
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    def __init__(self, game):
        self.game = game
        self.player = Player(self)
        self.background = pygame.image.load('assets/background2.png')
        self.rock = pygame.image.load('assets/rock.png').convert_alpha()
        self.cone = pygame.image.load('assets/buoy.png').convert_alpha()
        #self.tree = pygame.image.load('assets/tree.png').convert_alpha()
        self.amazon = pygame.image.load('assets/18L.png').convert_alpha()
        self.frame = 0
        self.y = 0
        self.entities = []
        self.obstacle = []
        self.current_speed = self.DEFAULT_SPEED

        self.flag = True

        self.font = pygame.font.SysFont("Arial", 20)

        self.spawn_trees()

        self.create_wall()

        self.start_time = pygame.time.get_ticks()

    def run(self):
        self.game.display.blit(self.background, (0, 0))

        self.pressed = self.game.get_pressed()

        self.is_boosted = self.pressed[self.UP]

        self.player.update()

        for e in self.entities:
            e.update()

        #Check for collision
        for e in self.obstacle:
            if self.player.get_rect().colliderect( e.get_rect()):
                name = self.font.render("Perdu", 0, (0, 0, 0))
                text_rect = name.get_rect(center=(self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2))
                self.game.display.blit(name, text_rect)

                self.entities.remove(e)
                self.obstacle.remove(e)
                self.player.lives -= 1


        self.entities.sort(key=lambda x: x.y)


        self.player.render()

        for e in self.entities:
            e.render()


        self.entities = [e for e in self.entities if not e.to_remove]


        self.frame += 1

        if self.frame % 30 == 0:
            self.create_wall(random.random() * 0.4)
        #if self.frame % 20 == 0:
        #    self.create_rock(random.random() * 0.4)

        if self.is_boosted:
            target_speed = self.BOOST_SPEED
        elif  self.pressed[self.DOWN]:
            target_speed = self.SLOW_SPEED
        else:
            target_speed = self.DEFAULT_SPEED

        self.current_speed += (target_speed - self.current_speed) / self.SPEED_DAMP

        self.y += self.current_speed


        #letter = self.font.render("frame: %d y: %f" % (self.frame, self.y), 0, (255,255,0))
        #self.game.display.blit(letter, (20, 20))

        #Cheats
        if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
            self.player.lives += 1
        elif pygame.key.get_pressed()[pygame.K_KP_PLUS]:
            self.player.lives -= 1

    def end_game(self):
        
        self.surf.game.state = menu.Menu(self.surf.game)

    def create_wall(self, x=0, dx=0.2, n=3):
        print 'create_wall'

        for i in range(3):
            c = Cone(self)
            c.x = x + dx * i
            c.y += (random.random() ) / 10.0


            self.entities.append(c)
            self.obstacle.append(c)
    
    def create_rock(self, x=0, dx=0.2, n=3):
        print 'create_rock'

        for i in range(n):
            c = Rock(self)
            c.x = x + dx * i
            c.y += (random.random()-0.5)
            if c.y >= 0:
                c.y += 0.5
            c.y = c.y / 10.0

            self.entities.append(c)
            self.obstacle.append(c)


    def create_corridor(self):
        pass


    def spawn_trees(self):
        for i in range(10):
            t = Rock(self)

            if i % 2 == 0:
                t.x = -random.random() / 2 - 0.3
            else:
                t.x = random.random() / 2 + 1.5

            t.y = random.random()

            self.entities.append(t)
