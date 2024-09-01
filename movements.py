import config
import random
import math
import pygame
import collections

# Histórico de células visitadas
visited_cells = set()

def pacman_movement():
    # Converte a posição atual do Pac-Man para coordenadas de célula no labirinto
    cell_x = int(config.pos[0] // config.block_size)
    cell_y = int(config.pos[1] // config.block_size)
    current_cell = (cell_x, cell_y)

    # Adiciona a célula atual ao conjunto de células visitadas
    visited_cells.add(current_cell)

    # Calcula a próxima posição do Pac-Man
    nextpos = [config.pos[0] + config.direction[0] * config.speed, config.pos[1] + config.direction[1] * config.speed]

    # Converte a próxima posição para coordenadas de célula no labirinto
    next_cell_x = int(nextpos[0] // config.block_size)
    next_cell_y = int(nextpos[1] // config.block_size)
    next_cell = (next_cell_x, next_cell_y)

    # Verifica se o Pac-Man está prestes a colidir com uma parede
    if config.maze[next_cell_y][next_cell_x] == 'X':
        # Se houver uma colisão iminente, procure uma nova direção
        possible_directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # Esquerda, Direita, Cima, Baixo
        random.shuffle(possible_directions)  # Embaralha para dar variabilidade

        # Evita a direção oposta (não retrocede)
        opposite_direction = [-config.direction[0], -config.direction[1]]
        if opposite_direction in possible_directions:
            possible_directions.remove(opposite_direction)

        for new_direction in possible_directions:
            new_nextpos = [config.pos[0] + new_direction[0] * config.speed, config.pos[1] + new_direction[1] * config.speed]
            new_next_cell_x = int(new_nextpos[0] // config.block_size)
            new_next_cell_y = int(new_nextpos[1] // config.block_size)
            new_next_cell = (new_next_cell_x, new_next_cell_y)

            # Verifica se a nova direção é válida (não leva a uma parede)
            if config.maze[new_next_cell_y][new_next_cell_x] != 'X':
                config.direction = new_direction
                break  # Sai do loop após encontrar uma direção válida

    # Se a nova direção não é válida, verifica se já visitou a célula (caminho já percorrido)
    elif next_cell in visited_cells:
        possible_directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # Esquerda, Direita, Cima, Baixo
        random.shuffle(possible_directions)  # Embaralha para dar variabilidade

        # Evita a direção oposta (não retrocede)
        opposite_direction = [-config.direction[0], -config.direction[1]]
        if opposite_direction in possible_directions:
            possible_directions.remove(opposite_direction)

        for new_direction in possible_directions:
            new_nextpos = [config.pos[0] + new_direction[0] * config.speed, config.pos[1] + new_direction[1] * config.speed]
            new_next_cell_x = int(new_nextpos[0] // config.block_size)
            new_next_cell_y = int(new_nextpos[1] // config.block_size)
            new_next_cell = (new_next_cell_x, new_next_cell_y)

            # Verifica se a nova direção é válida (não leva a uma parede e evita caminhos visitados)
            if config.maze[new_next_cell_y][new_next_cell_x] != 'X' and new_next_cell not in visited_cells:
                config.direction = new_direction
                break  # Sai do loop após encontrar uma direção válida

    # Atualiza a posição do Pac-Man
    config.pos[0] += config.direction[0] * config.speed
    config.pos[1] += config.direction[1] * config.speed


def ghost_movement():
    possible_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    valid_directions = []

    for direction in possible_directions:
        next_pos = [config.pos_ghost[0] + direction[0] * config.speed_ghost, config.pos_ghost[1] + direction[1] * config.speed_ghost]
        row = int(next_pos[1] / config.block_size)
        col = int(next_pos[0] / config.block_size)
        
        if 0 <= row < len(config.maze) and 0 <= col < len(config.maze[0]) and config.maze[row][col] != 'X':
            valid_directions.append(direction)

    if valid_directions:
        chosen_direction = random.choice(valid_directions)
        config.pos_ghost[0] += chosen_direction[0] * config.speed_ghost
        config.pos_ghost[1] += chosen_direction[1] * config.speed_ghost

def checkcollision():
    pacman_rect = pygame.Rect(config.pos[0] - config.radius, config.pos[1] - config.radius, config.radius * 2, config.radius * 2)
    ghost_rect = pygame.Rect(config.pos_ghost[0] - config.radius, config.pos_ghost[1] - config.radius, config.radius * 2, config.radius * 2)
    return pacman_rect.colliderect(ghost_rect)

def food_dots():
    center = (config.pos[0], config.pos[1])
    removed = False

    # Iterate through each row of mazedots
    for row in config.mazedots:
        for mazedot in row[:]:  # Copy to iterate safely
            # Check if Pac-Man is close enough to "eat" the dot
            if (center[0] - mazedot[0]) ** 2 + (center[1] - mazedot[1]) ** 2 < (config.radius + 3) ** 2:
                print(f"Pac-Man comeu uma pecinha na posição {mazedot}")
                row.remove(mazedot)  # Remove dot from the list
                config.dots_eaten += 1
                removed = True
    
    if not removed:
        print("Nenhuma pecinha foi removida nesta rodada.")


def win():
    for row in config.mazedots:
        if row:
            return False
    return True
