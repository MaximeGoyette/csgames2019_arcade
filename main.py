#!/usr/bin/env python2
import pygame
import game
import os
from threading import Thread
import sys
from inputs import GPIO, Keyboard


ON_ARCADE = os.uname()[1] == 'raspberrypi'
WINDOWED = '--windowed' in sys.argv

def main():
    pygame.init()
    pygame.display.set_caption("ma-chine")

    pygame.font.init()

    if ON_ARCADE:
        border = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #, pygame.FULLSCREEN)
        inputs = GPIO()
    elif WINDOWED:
        border = pygame.display.set_mode((1280, 760))
        inputs = Keyboard()
    else:
        border = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
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
