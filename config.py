import pygame
import random

# Inicializa o Pygame
pygame.init()

# Tamanho do bloco e dimensões do labirinto
block_size = 20
maze = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X.......................................X",
    "X.XXX.XXXX.XX.XXXX.XXXX.XXXX.XXXX.XXXXX.X",
    "X.XXX.XXXX.XX.XXXX.XXXX.XXXX.XXXX.XXXXX.X",
    "X.XXX.XXXX.XX.XXXX.XXXX.XXXX.XXXX.XXXXX.X",
    "X.................................XXXXX.X",
    "X.XXXX.XX.XXXX.XXXXXXXXXXX.XXXX.X.......X",
    "X.XXXX.XX.XXXX.XXXXXXXXXXX.XXXX.XXXX.XX.X",
    "X.XXXX.XX.XXXX.XXXXXXXXXXX.XXXX.XXXX.XX.X",
    "X...........XX.XXXXXXXXXXX.XX...........X",
    "X.XXXX.XXXX.XX.............XX.XXXX.XXXX.X",
    "X.XXXX.XXXX.XX.XXXX.XXXX.XXXX.XXXX.XXXX.X",
    "X.XXXX.XXXX.XX.XXXX.XXXX.XXXX.XXXX.XXXX.X",
    "X.......................................X",
    "XXXXXXXXXXXX..XXXXXXXXXXXXXXXX..XXXXXXXXX",
    "X.......................................X",
    "X.XXX.XXX.XX.XX.XX.XXXX.XXXX.XX.XX.XXXX.X",
    "X.XXX.XXX.XX.XX.XX.XXXX.XXXX....XX.XXXX.X",
    "X.XXX.XXX.XX.XX.XX.XXXX.XX...XX.XX.XXXX.X",
    "X.XXX.XXX.XX.XX.XX.XXXX.XX.XXXX.XX.XXXX.X",
    "X.XXX.XXX.XX.XX.XX.XXXX.XX.XXXX.XX.XXXX.X",
    "X.......................................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Define width and height based on the maze size
width = block_size * len(maze[0])
height = block_size * len(maze)

# Função para encontrar uma posição válida no labirinto
def find_valid_position(exclude_positions=None):
    if exclude_positions is None:
        exclude_positions = []

    while True:
        pos = (random.randint(0, len(maze[0]) - 1) * block_size + block_size // 2, 
               random.randint(0, len(maze) - 1) * block_size + block_size // 2)
        if pos not in exclude_positions and maze[int(pos[1] / block_size)][int(pos[0] / block_size)] != 'X':
            return pos

# Cores
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
red = (255, 0, 0)

# Configurações do Pac-Man
pacman_start_pos = find_valid_position()
pos = list(pacman_start_pos)  # Posição inicial de Pac-Man
speed = 4         # Velocidade de movimentação
radius = 8       # Raio de Pac-Man
direction = [1, 0]  # Começa movendo para a direita

# Configurações do Fantasma
ghost_start_pos = find_valid_position(exclude_positions=[pacman_start_pos])
pos_ghost = list(ghost_start_pos)  # Posição inicial do Fantasma
speed_ghost = 2
direction_ghost = [1, 0]  # Começa movendo para a direita

# Tela do jogo
screen_width = width
screen_height = height
screen_game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PAC-MAN')

# Pontos de comida no labirinto
mazedots = [
    [(col_idx * block_size + block_size // 2, row_idx * block_size + block_size // 2)
     for col_idx, col in enumerate(row) if col == '.']
    for row_idx, row in enumerate(maze)
]
dots_eaten=0

# Função para desenhar o labirinto
def maze_draw():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            if cell == 'X':
                pygame.draw.rect(screen_game, blue, rect)
            elif cell == '.':
                pygame.draw.rect(screen_game, black, rect)  # O fundo do caminho será preto

# Função para desenhar as peças no tabuleiro
def dotsdraw():
    for row in mazedots:
        for mazedot in row:
            pygame.draw.circle(screen_game, white, mazedot, 5)

# Função para desenhar o Pac-Man
def draw_pacman():
    pygame.draw.circle(screen_game, yellow, (int(pos[0]), int(pos[1])), radius)

# Função para desenhar o Fantasma
def draw_ghost():
    pygame.draw.circle(screen_game, red, (int(pos_ghost[0]), int(pos_ghost[1])), radius)
