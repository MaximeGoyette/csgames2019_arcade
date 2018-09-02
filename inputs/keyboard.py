import pygame

class Keyboard:
    def get_pressed(self):
        pressed = pygame.key.get_pressed()

        return [pressed[pygame.K_a], pressed[pygame.K_d], pressed[pygame.K_w], pressed[pygame.K_s]]
