import pygame
from config import WIDTH, HEIGHT, FPS, TITLE, SKY_BLUE, BASE_GROUND_SPEED
from models import Player, Ground, DifficultyManager, ObstacleManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    player = Player()
    ground = Ground(BASE_GROUND_SPEED)
    difficulty = DifficultyManager()
    obstacles = ObstacleManager(BASE_GROUND_SPEED)
    obstacles.set_difficulty(difficulty)

    score = 0
    game_over = False
    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        player = Player()
                        ground = Ground(BASE_GROUND_SPEED)
                        difficulty = DifficultyManager()
                        obstacles = ObstacleManager(BASE_GROUND_SPEED)
                        obstacles.set_difficulty(difficulty)
                        score = 0
                        game_over = False
                    else:
                        player.jump()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not game_over:
                        player.duck(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.duck(False)

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player.jump()

            speed_mult = difficulty.get_speed(1.0)

            player.update()
            ground.update(speed_mult)
            obstacles.update(speed_mult)

            if obstacles.check_collision(player.get_rect()):
                player.die()
                game_over = True

            score += 1
            difficulty.update(score)

        screen.fill(SKY_BLUE)
        ground.draw(screen)
        obstacles.draw(screen)
        player.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (50, 50, 50))
        screen.blit(score_text, (10, 10))

        speed_text = font.render(f"x{game_over and ' ' or ''}{difficulty.speed_multiplier:.1f}", True, (100, 100, 100))
        screen.blit(speed_text, (WIDTH - 80, 10))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))

            go_font = pygame.font.Font(None, 48)
            go_text = go_font.render("GAME OVER", True, (255, 50, 50))
            go_rect = go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(go_text, go_rect)

            restart_text = font.render("Press SPACE to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
