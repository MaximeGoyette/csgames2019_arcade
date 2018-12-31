import pygame
from pygame.rect import Rect
from game_states import menu
from game_states import surf
from pygame.time import Clock
import sys
class Game:
    FPS = 24

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def __init__(self, display, inputs):
        self.display = display
        self.timer = Clock()
        self.state = menu.Menu(self)
        self.inputs = inputs


    def get_pressed(self):
        return self.inputs.get_pressed()

    def run(self):
        self.running = True

        while self.running:
            self.state.run()

            pygame.display.update()

            self.timer.tick(Game.FPS)

            if pygame.event.get([pygame.QUIT]) or pygame.key.get_pressed()[pygame.K_ESCAPE] or pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                pygame.quit()
                break
            elif pygame.key.get_pressed()[pygame.K_TAB]:
                self.state = menu.Menu(self)
