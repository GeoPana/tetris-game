import sys
print(sys.path)
import pygame
import random

pygame.font.init()

# Global Variables
screen_width = 800
screen_height = 700
playing_space_width = 300  # 10 blocks size
playing_space_height = 600  # 20 blocks size
block_size = 30

top_left_x = (screen_width - playing_space_width) // 2  # top left point height of the playing space
top_left_y = screen_height - playing_space_height

# Shape Formats

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....' ]]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]  # holds all shapes
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    def __init__(self, x, y, shape) :
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos) :
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]  

    for i in range(len(grid)) :
        for j in range(len(grid[i])) :
            if (j, i) in locked_pos :
                color = locked_pos[(j, i)]
                grid[i][j] = color
    return grid

def convert_shape_format(shape) :
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format) :
        row = list(line)
        for j, column in enumerate(row) :
            if column == '0' :
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions) :
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape, grid) :
    valid_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    valid_pos = [point for line in valid_pos for point in line]

    formatted_shape = convert_shape_format(shape)
    
    for pos in formatted_shape :
        if pos not in valid_pos :
            if pos[1] > -1 :
                return False
    return True

def check_lost(positions) :
    for pos in positions :
        x, y = pos
        if y < 1 :
            return True
    return False

def get_shape() : # choses a random shape from shapes list and returns it
    return Piece(5, 0, random.choice(shapes))

def draw_grid(surface, grid) :
    start_x = top_left_x
    start_y = top_left_y

    for i in range(len(grid)) :
        pygame.draw.line(surface, (128, 128, 128), (start_x, start_y + i * block_size), (start_x + playing_space_width, start_y + i * block_size))
        for j in range(len(grid[i])) :
            pygame.draw.line(surface, (128, 128, 128), (start_x + j * block_size, start_y), (start_x + j * block_size, start_y + playing_space_height))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc) # moves the quare down by inc
                locked[newKey] = locked.pop(key)   # keeps the same color to the new position

    return inc      

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + playing_space_width + 50
    sy = top_left_y + playing_space_height/2 -100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
     
    surface.blit(label, (sx - 5, sy - 50))
    
def draw_window(surface, grid, score, last_score = 0) :
    surface.fill((0, 0, 0))  # paints the surface black

    pygame.font.init()  # means we set up font and we get ready to draw to the screen
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', True, (255, 255, 255))
    surface.blit(label, (top_left_x + playing_space_width / 2 - (label.get_width() / 2), 30))

    # Score board
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    sx = top_left_x + playing_space_width + 50
    sy = top_left_y + playing_space_height/2 -100
    surface.blit(label, (sx + 10, sy + 200))

    # Last Biggest Score
    font = pygame.font.SysFont('comicsans', 22)
    label = font.render('Highest Score: ' + last_score, 1, (255, 255, 255))
    sx = top_left_x - 245
    sy = top_left_y + 80
    surface.blit(label, (sx + 10, sy + 200))

    for i in range(len(grid)) :
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
    
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, playing_space_width, playing_space_height), 3)

    draw_grid(surface, grid)

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + playing_space_width / 2 - (label.get_width() / 2), top_left_y + playing_space_height / 2 - (label.get_height() / 2)))

def update_score(newScore):
    with open("scores.txt", "r") as file:
        lines = file.readlines()
        score = lines[0].strip()
    
    with open("scores.txt", "w") as file:
        if newScore > int(score):
            file.write(str(newScore))
        else:
            file.write(score)

def max_score():
    with open("scores.txt", "r") as file:
        lines = file.readlines()
        score = lines[0].strip()

    return score
    

def main(window):

    last_score = max_score()

    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.3
    level_time = 0
    score = 0

    while run :
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()  # in milliseconds, so 1 sec will be 1000 msec 
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5: # increase spit after every 5 seconds
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed :
            fall_time = 0
            current_piece.y += 1
            if (not(valid_space(current_piece, grid)) and current_piece.y > 0) :
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT :
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)) :
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT :
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)) :
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN :
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)) :
                        current_piece.y -= 1
                if event.key == pygame.K_DOWN :
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)) :
                        current_piece.rotation -= 1
        
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)) :
            x, y = shape_pos[i]
            if y > -1 :
                grid[y][x] = current_piece.color

        if change_piece :
            for pos in shape_pos :
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(window, "Game Over", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)
    

def main_menu(window):
    run = True
    while run:
        window.fill((0, 0, 0))
        draw_text_middle(window, "Press Any key to Play", 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(window)

    pygame.display.quit()

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu(window) 
                     








         


