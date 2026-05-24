import pygame
import random
from config import (
    CACTUS_WIDTH, CACTUS_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT,
    GROUND_Y, BIRD_FLY_HEIGHT_1, BIRD_FLY_HEIGHT_2, BIRD_FLY_HEIGHT_3,
    MIN_OBSTACLE_INTERVAL, MAX_OBSTACLE_INTERVAL, WIDTH,
    GREEN, DARK_GREEN, GRAY, DARK_GRAY, BLACK, RED, YELLOW
)


class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.passed = False

    def update(self, speed_mult):
        self.x -= self.speed * speed_mult

    def is_offscreen(self):
        return self.x + self.width < -50

    def get_rect(self):
        shrink = 4
        return pygame.Rect(
            self.x + shrink,
            self.y + shrink,
            self.width - shrink * 2,
            self.height - shrink * 2
        )


class Cactus(Obstacle):
    def __init__(self, x, speed):
        y = GROUND_Y - CACTUS_HEIGHT
        super().__init__(x, y, CACTUS_WIDTH, CACTUS_HEIGHT, speed)

    def draw(self, screen):
        x, y = int(self.x), int(self.y)
        body = pygame.Rect(x + 3, y + 5, self.width - 6, self.height - 5)
        pygame.draw.ellipse(screen, GREEN, body)

        pygame.draw.line(screen, DARK_GREEN, (x + 5, y + 5), (x + 5, y + self.height), 2)

        for arm_x in [x + 4, x + self.width - 4]:
            arm_y = y + self.height // 3
            pygame.draw.line(screen, GREEN, (arm_x, arm_y), (arm_x + (-4 if arm_x > x + 10 else 4), arm_y - 8), 3)

        for spike_y in [y + 10, y + 20, y + 30]:
            for spike_x in [x + 2, x + self.width - 2]:
                if 0 <= spike_y - y < self.height:
                    pygame.draw.circle(screen, DARK_GREEN, (spike_x, spike_y), 2)


class Bird(Obstacle):
    HEIGHTS = [BIRD_FLY_HEIGHT_1, BIRD_FLY_HEIGHT_2, BIRD_FLY_HEIGHT_3]

    def __init__(self, x, speed):
        height = random.choice(self.HEIGHTS)
        super().__init__(x, height, BIRD_WIDTH, BIRD_HEIGHT, speed)
        self.wing_up = False
        self.wing_timer = 0

    def update(self, speed_mult):
        super().update(speed_mult)
        self.wing_timer += 1
        if self.wing_timer >= 10:
            self.wing_up = not self.wing_up
            self.wing_timer = 0

    def draw(self, screen):
        x, y = int(self.x), int(self.y)
        body = pygame.Rect(x, y + 2, self.width, self.height - 4)
        pygame.draw.ellipse(screen, DARK_GRAY, body)

        eye_x, eye_y = x + self.width - 6, y + 4
        pygame.draw.circle(screen, RED, (eye_x, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 1)

        beak_points = [(x + self.width - 2, y + 5), (x + self.width + 6, y + 4), (x + self.width + 6, y + 8)]
        pygame.draw.polygon(screen, YELLOW, beak_points)

        if self.wing_up:
            wing = [(x + 6, y + 2), (x + 2, y - 8), (x + 10, y + 2)]
        else:
            wing = [(x + 6, y + 2), (x + 2, y + 12), (x + 10, y + 2)]
        pygame.draw.polygon(screen, GRAY, wing)

    def get_rect(self):
        shrink = 3
        return pygame.Rect(
            self.x + shrink,
            self.y + shrink,
            self.width - shrink * 2,
            self.height - shrink * 2
        )


class ObstacleManager:
    def __init__(self, base_speed):
        self.obstacles = []
        self.base_speed = base_speed
        self.spawn_timer = 0
        self.spawn_interval = self._random_interval()
        self.difficulty_manager = None

    def set_difficulty(self, difficulty_manager):
        self.difficulty_manager = difficulty_manager

    def _random_interval(self):
        return random.randint(MIN_OBSTACLE_INTERVAL, MAX_OBSTACLE_INTERVAL)

    def update(self, speed_mult):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_interval = self._random_interval()
            self._spawn_obstacle(speed_mult)

        for obs in self.obstacles[:]:
            obs.update(speed_mult)
            if obs.is_offscreen():
                self.obstacles.remove(obs)

    def _spawn_obstacle(self, speed_mult):
        birds_unlocked = False
        if self.difficulty_manager:
            birds_unlocked = self.difficulty_manager.birds_unlocked

        if birds_unlocked and random.random() < 0.35:
            self.obstacles.append(Bird(WIDTH, self.base_speed))
        else:
            self.obstacles.append(Cactus(WIDTH, self.base_speed))

    def check_collision(self, player_rect):
        for obs in self.obstacles:
            if player_rect.colliderect(obs.get_rect()):
                return True
        return False

    def check_passed(self, player_x):
        for obs in self.obstacles:
            if not obs.passed and obs.x + obs.width < player_x:
                obs.passed = True
                return True
        return False

    def draw(self, screen):
        for obs in self.obstacles:
            obs.draw(screen)

    def reset(self):
        self.obstacles.clear()
        self.spawn_timer = 0
