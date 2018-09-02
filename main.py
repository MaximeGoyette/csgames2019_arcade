#!/usr/bin/env python2
import pygame
import game
import os
from threading import Thread
import sys
from inputs import GPIO, Keyboard


ON_ARCADE = os.uname()[1] == 'raspberrypi'

def main():
    pygame.init()
    pygame.display.set_caption("ma-chine")

    pygame.font.init()

    if ON_ARCADE:
        border = pygame.display.set_mode((game.Game.SCREEN_WIDTH, game.Game.SCREEN_HEIGHT), pygame.FULLSCREEN) #, pygame.FULLSCREEN)
        inputs = GPIO()
    else:
        border = pygame.display.set_mode((game.Game.SCREEN_WIDTH, game.Game.SCREEN_HEIGHT))
        inputs = Keyboard()

    try:
        app = game.Game(border, inputs)

        print("Start game")
        app.run()
        print("Game stop")
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
