import pygame
import copy
from config import WIDTH, HEIGHT, FPS, TITLE, SKY_BLUE, BASE_GROUND_SPEED
from models import Player, Ground, DifficultyManager, ObstacleManager, QuestionManager

PLAYING, QUESTION, COUNTDOWN, GAME_OVER = range(4)


class GameState:
    def __init__(self):
        self.player = Player()
        self.ground = Ground(BASE_GROUND_SPEED)
        self.difficulty = DifficultyManager()
        self.obstacles = ObstacleManager(BASE_GROUND_SPEED)
        self.obstacles.set_difficulty(self.difficulty)
        self.score = 0

    def copy(self):
        return copy.deepcopy(self)

    def reset(self):
        self.__init__()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 48)
    font_mid = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    question_mgr = QuestionManager()

    state = PLAYING
    gs = GameState()
    saved_state = None
    current_q = None
    q_selected = False
    q_result = None
    countdown_num = 3
    countdown_timer = 0
    result_timer = 0
    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if state == PLAYING:
                    if event.key == pygame.K_SPACE:
                        gs.player.jump()
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        gs.player.duck(True)

                elif state == QUESTION and not q_selected:
                    if event.key == pygame.K_ESCAPE:
                        state = GAME_OVER
                    elif event.key in (pygame.K_1, pygame.K_a):
                        q_selected = True
                        q_result = current_q["correct"] == 0
                    elif event.key in (pygame.K_2, pygame.K_b):
                        q_selected = True
                        q_result = current_q["correct"] == 1
                    elif event.key in (pygame.K_3, pygame.K_c):
                        q_selected = True
                        q_result = current_q["correct"] == 2
                    elif event.key in (pygame.K_4, pygame.K_d):
                        q_selected = True
                        q_result = current_q["correct"] == 3
                    if q_selected:
                        result_timer = 0

                elif state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        gs.reset()
                        saved_state = None
                        current_q = None
                        q_selected = False
                        q_result = None
                        state = PLAYING

                elif state == COUNTDOWN:
                    pass

            if event.type == pygame.KEYUP:
                if state == PLAYING:
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        gs.player.duck(False)

        if state == PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                gs.player.jump()

            speed_mult = gs.difficulty.get_speed(1.0)
            gs.player.update()
            gs.ground.update(speed_mult)
            gs.obstacles.update(speed_mult)

            if gs.obstacles.check_collision(gs.player.get_rect()):
                saved_state = gs.copy()
                gs.player.die()
                current_q = question_mgr.get_random()
                q_selected = False
                q_result = None
                state = QUESTION

            gs.score += 1
            gs.difficulty.update(gs.score)

        elif state == QUESTION:
            if q_selected:
                result_timer += dt
                if q_result:
                    if result_timer >= 1000:
                        state = COUNTDOWN
                        countdown_num = 3
                        countdown_timer = pygame.time.get_ticks()
                else:
                    if result_timer >= 1500:
                        state = GAME_OVER

        elif state == COUNTDOWN:
            now = pygame.time.get_ticks()
            if now - countdown_timer >= 1000:
                countdown_num -= 1
                countdown_timer = now
                if countdown_num <= 0:
                    gs = saved_state
                    saved_state = None
                    current_q = None
                    q_selected = False
                    q_result = None
                    state = PLAYING

        screen.fill(SKY_BLUE)

        if state in (PLAYING, QUESTION, COUNTDOWN):
            gs.ground.draw(screen)
            gs.obstacles.draw(screen)
            gs.player.draw(screen)

            score_text = font_mid.render(f"Score: {gs.score}", True, (50, 50, 50))
            screen.blit(score_text, (10, 10))

            speed_text = font_mid.render(
                f"x{gs.difficulty.speed_multiplier:.1f}", True, (100, 100, 100)
            )
            screen.blit(speed_text, (WIDTH - 80, 10))

        if state == QUESTION:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            q_text = font_large.render(current_q["question"], True, (255, 255, 255))
            q_rect = q_text.get_rect(center=(WIDTH // 2, 60))
            screen.blit(q_text, q_rect)

            labels = ["A", "B", "C", "D"]
            for i, opt in enumerate(current_q["options"]):
                color = (200, 200, 200)
                if q_selected:
                    if i == current_q["correct"]:
                        color = (50, 255, 50)
                    elif q_result is False and i == next(
                        (j for j, v in enumerate(current_q["options"])
                         if current_q["options"][current_q["correct"]] == v),
                        i
                    ):
                        pass

                opt_text = font_mid.render(
                    f"{labels[i]}) {opt}", True, color
                )
                opt_rect = opt_text.get_rect(center=(WIDTH // 2, 130 + i * 50))
                screen.blit(opt_text, opt_rect)

            if q_selected:
                if q_result:
                    result_text = font_large.render("Correct!", True, (50, 255, 50))
                else:
                    result_text = font_large.render("Wrong!", True, (255, 50, 50))
                result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
                screen.blit(result_text, result_rect)
            else:
                hint_text = font_small.render(
                    "Press A-D / 1-4 to answer, ESC to skip", True, (150, 150, 150)
                )
                hint_rect = hint_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
                screen.blit(hint_text, hint_rect)

        elif state == COUNTDOWN:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))

            if countdown_num > 0:
                cnt_text = font_large.render(str(countdown_num), True, (255, 255, 255))
            else:
                cnt_text = font_large.render("GO!", True, (50, 255, 50))
            cnt_rect = cnt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(cnt_text, cnt_rect)

        elif state == GAME_OVER:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            go_text = font_large.render("GAME OVER", True, (255, 50, 50))
            go_rect = go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            screen.blit(go_text, go_rect)

            final_score = font_mid.render(
                f"Score: {gs.score}", True, (255, 255, 255)
            )
            final_rect = final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
            screen.blit(final_score, final_rect)

            restart_text = font_mid.render(
                "Press SPACE to restart", True, (200, 200, 200)
            )
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
