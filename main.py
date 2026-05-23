import pygame
from config import WIDTH, HEIGHT, FPS, TITLE, GROUND_Y, GROUND_HEIGHT, SKY_BLUE, BROWN
from models import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    player = Player()
    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.duck(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.duck(False)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump()

        player.update()

        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, BROWN, (0, GROUND_Y, WIDTH, GROUND_HEIGHT))
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
