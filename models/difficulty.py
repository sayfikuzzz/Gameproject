from config import DIFFICULTY_INTERVAL, MAX_SPEED_MULTIPLIER, SPEED_INCREASE


class DifficultyManager:
    def __init__(self):
        self.speed_multiplier = 1.0
        self.birds_unlocked = False

    def update(self, score):
        multiplier = 1.0 + (score // DIFFICULTY_INTERVAL) * SPEED_INCREASE
        self.speed_multiplier = min(multiplier, MAX_SPEED_MULTIPLIER)
        self.birds_unlocked = score >= 3 * DIFFICULTY_INTERVAL

    def get_speed(self, base_speed):
        return base_speed * self.speed_multiplier
