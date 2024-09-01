import pygame
import sys
import config
import movements
import random

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    config.direction = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    config.direction = [1, 0]
                elif event.key == pygame.K_UP:
                    config.direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    config.direction = [0, 1]

        movements.pacman_movement()
        movements.ghost_movement()

        if movements.checkcollision():
            print("Game Over")
            pygame.quit()
            sys.exit()
        if movements.win():
            print("You Win!")
            pygame.quit()
            sys.exit()

        config.screen_game.fill(config.black)
        config.maze_draw()
        config.dotsdraw()
        movements.food_dots()  # Verifica e remove as pecinhas que o Pac-Man comeu
        config.draw_pacman()
        config.draw_ghost()

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()

