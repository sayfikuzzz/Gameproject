import pygame
from config import GROUND_Y, GROUND_HEIGHT, BROWN


class Ground:
    def __init__(self, speed):
        self.y = GROUND_Y
        self.height = GROUND_HEIGHT
        self.speed = speed
        self.scroll = 0

    def update(self, speed_mult=1.0):
        self.scroll -= self.speed * speed_mult
        if self.scroll <= -20:
            self.scroll += 20

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (0, self.y, 800, self.height))
        for x in range(0, 800, 20):
            offset_x = x + self.scroll
            if offset_x < 0:
                offset_x += 800
            pygame.draw.rect(screen, (160, 120, 80), (offset_x, self.y, 1, self.height // 3))
