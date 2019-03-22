import pygame
import random
import surf


class Menu:
    UNIVERSITIES = sorted(['Sherby', 'UOttawa', 'Conco', 'ETS', 'McGill', 'Laval', 'Poly', 'UQAM', 'UGuelph', 'URochester', 'UCarleton', 'UWindsor', 'UManitoba', 'UBrock', 'UdeM', 'ULaurentian', 'UYork', 'UQO'])

    def __init__(self, game):
        self.game = game
        self.background = pygame.image.load('assets/menu.png')
        self.background = pygame.transform.scale(self.background,(pygame.display.Info().current_w,pygame.display.Info().current_h))
        self.index = random.randint(0, len(self.UNIVERSITIES) - 1)
        self.font = pygame.font.SysFont("Arial", 100, True)
        self.bounce = False
        self.bounce_time = 0

        self.ready = False
        self.ready_time = 0

        self.game.reset_data()


    def run(self):
        self.game.display.blit(self.background, (0, 0))

        self.pressed = self.game.get_pressed()

        # shadow text
        name = self.font.render(self.UNIVERSITIES[self.index], 0, (153,132,0))
        text_rect = name.get_rect(center=(pygame.display.Info().current_w / 2 +5, pygame.display.Info().current_h / 2+5))
        self.game.display.blit(name, text_rect)

        # main text
        name = self.font.render(self.UNIVERSITIES[self.index], 0, (255,255,0))
        text_rect = name.get_rect(center=(pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2))
        self.game.display.blit(name, text_rect)

        if self.pressed[0] and not self.bounce and not self.ready:
            self.bounce = True
            self.bounce_time = pygame.time.get_ticks()
            self.index -= 1


        if self.pressed[1] and not self.bounce and not self.ready:
            self.bounce = True
            self.bounce_time = pygame.time.get_ticks()
            self.index += 1


        if self.pressed[3] and not self.ready:
            self.ready = True
            self.ready_time = pygame.time.get_ticks()

        elif not self.pressed[3]:
            self.ready = False

        self.index = self.index % len(self.UNIVERSITIES)

        if pygame.time.get_ticks() - self.bounce_time > 1000:
            self.bounce = False

        if self.ready:
            remaining = 5 - int((pygame.time.get_ticks() - self.ready_time) / 1000.0)

            if remaining <= -1:
                self.game.university = self.UNIVERSITIES[self.index]
                if pygame.key.get_pressed()[pygame.K_KP_PERIOD] and pygame.key.get_pressed()[pygame.K_KP1] and pygame.key.get_pressed()[pygame.K_KP3]:
                    self.game.titi = True
                    self.game.university = 'TITI'
                self.game.state = surf.Surf(self.game)
                return

            pygame.draw.rect(self.game.display, (0, 255, 0), (pygame.display.Info().current_w / 2 - 500/2, pygame.display.Info().current_h / 2 - 200/2, 500, 200))

            name = self.font.render("READY " + str(remaining), 0, (0, 0, 0))
            text_rect = name.get_rect(center=(pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2))
            self.game.display.blit(name, text_rect)
