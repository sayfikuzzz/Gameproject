import pygame
from config import (
    PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT,
    PLAYER_DUCK_HEIGHT, GROUND_Y, GRAVITY, JUMP_SPEED,
    GREEN, DARK_GREEN, WHITE, BLACK
)


class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.is_dead = False
        self.on_ground = True
        self.score = 0

    def jump(self):
        if self.on_ground and not self.is_dead:
            self.vel_y = JUMP_SPEED
            self.is_jumping = True
            self.on_ground = False

    def duck(self, active):
        if self.is_dead:
            return
        self.is_ducking = active

    def update(self):
        if self.is_dead:
            return

        self.vel_y += GRAVITY
        self.y += self.vel_y

        ground_level = GROUND_Y - self.height
        if self.y >= ground_level:
            self.y = ground_level
            self.vel_y = 0
            self.is_jumping = False
            self.on_ground = True

    def die(self):
        self.is_dead = True

    def draw(self, screen):
        x, y = int(self.x), int(self.y)
        h = max(int(self.height), 6)
        w = int(self.width)

        current_height = self._get_draw_height()
        y_offset = self.height - current_height

        body_y = y + y_offset

        tail_color = DARK_GREEN
        pygame.draw.line(screen, tail_color, (x - 18, body_y + current_height // 2),
                         (x, body_y + current_height // 2 + 2), 4)

        body_rect = pygame.Rect(x, body_y, w, current_height)
        pygame.draw.ellipse(screen, GREEN, body_rect)

        head_radius = 10
        head_x = x + w + 2
        head_y = body_y + current_height // 2
        pygame.draw.circle(screen, GREEN, (head_x, head_y), head_radius)

        eye_radius = 3
        pygame.draw.circle(screen, WHITE, (head_x + 4, head_y - 3), eye_radius)
        pygame.draw.circle(screen, WHITE, (head_x + 4, head_y + 3), eye_radius)
        pygame.draw.circle(screen, BLACK, (head_x + 5, head_y - 3), 1)
        pygame.draw.circle(screen, BLACK, (head_x + 5, head_y + 3), 1)

        leg_color = DARK_GREEN
        leg_length = 7
        if current_height > 8:
            for offset in [5, 15, 25, 35]:
                if offset <= w:
                    leg_x = x + offset
                    leg_end = body_y + current_height + leg_length
                    pygame.draw.line(screen, leg_color, (leg_x, body_y + current_height),
                                     (leg_x, leg_end), 3)

        spot_color = DARK_GREEN
        if current_height > 10:
            spots = [(10, 3), (22, 6), (30, 4)]
            body_bottom = body_y + current_height
            for sx, sy in spots:
                if sx < w:
                    spot_y = body_y + sy
                    if spot_y < body_bottom:
                        pygame.draw.circle(screen, spot_color, (x + sx, spot_y), 2)

    def _get_draw_height(self):
        if self.is_ducking and self.on_ground and not self.is_jumping:
            return PLAYER_DUCK_HEIGHT
        return self.height

    def get_rect(self):
        h = self._get_draw_height()
        y_offset = self.height - h
        return pygame.Rect(self.x, self.y + y_offset, self.width, h)
