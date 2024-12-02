import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 60
ROWS, COLS = 8, 6
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
FPS = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cops and Robber Game")

# Define the game board
board = [
    ["#", "#", "#", "#", "#", "#"],
    ["#", "_", "_", "_", "_", "#"],
    ["#", "_", "X", "X", "_", "#"],
    ["#", "_", "X", "X", "_", "#"],
    ["#", "_", "_", "_", "_", "#"],
    ["#", "_", "_", "_", "_", "#"],
    ["#", "_", "_", "_", "_", "#"],
    ["#", "#", "#", "#", "#", "#"]
]

# Initial positions
cop1 = [1, 2]
cop2 = [1, 1]
robber = [1, 4]

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if board[row][col] == "#":
                pygame.draw.rect(screen, BLACK, rect)
            elif board[row][col] == "X":
                pygame.draw.rect(screen, GRAY, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

    # Draw cops
    pygame.draw.circle(screen, BLUE, (cop1[1] * CELL_SIZE + CELL_SIZE // 2, cop1[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    pygame.draw.circle(screen, BLUE, (cop2[1] * CELL_SIZE + CELL_SIZE // 2, cop2[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    
    # Draw robber
    pygame.draw.circle(screen, RED, (robber[1] * CELL_SIZE + CELL_SIZE // 2, robber[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

def is_valid_move(pos):
    return 0 <= pos[0] < ROWS and 0 <= pos[1] < COLS and board[pos[0]][pos[1]] != "#" and board[pos[0]][pos[1]] != "X"

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def move_robber(key):
    global robber
    new_pos = robber.copy()
    if key == pygame.K_w and is_valid_move([robber[0] - 1, robber[1]]):
        new_pos[0] -= 1
    elif key == pygame.K_s and is_valid_move([robber[0] + 1, robber[1]]):
        new_pos[0] += 1
    elif key == pygame.K_a and is_valid_move([robber[0], robber[1] - 1]):
        new_pos[1] -= 1
    elif key == pygame.K_d and is_valid_move([robber[0], robber[1] + 1]):
        new_pos[1] += 1
    robber = new_pos

def is_near_circle_wall(pos):
    for dy, dx in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        new_y, new_x = pos[0] + dy, pos[1] + dx
        if 0 <= new_y < ROWS and 0 <= new_x < COLS and board[new_y][new_x] == "X":
            return True
    return False

def move_cop_circle(cop, clockwise):
    y, x = cop[0], cop[1]
    
    if is_valid_move(cop):

        # Above the circle
        if board[y + 1][x] == 'X':  
            if clockwise:
                return [y, x + 1]  # Move right
            else:
                return [y, x - 1]  # Move left
        
        # Below the circle
        elif board[y - 1][x] == 'X':  
            if clockwise:
                return [y, x - 1]  # Move left
            else:
                return [y, x + 1]  # Move right
        
        # Left of the circle
        elif board[y][x + 1] == 'X':  
            if clockwise:
                return [y - 1, x]  # Move up
            else:
                return [y + 1, x]  # Move down
        
        # Right of the circle
        elif board[y][x - 1] == 'X':  
            if clockwise:
                return [y + 1, x]  # Move down
            else:
                return [y - 1, x]  # Move up
        
        # Corners
        # Upper-left corner of the circle
        elif board[y + 1][x + 1] == 'X':  
            if clockwise:
                return [y, x + 1]  # Move right
            else:
                return [y + 1, x]  # Move down
        
        # Upper-right corner of the circle
        elif board[y + 1][x - 1] == 'X':  
            if clockwise:
                return [y + 1, x]  # Move down
            else:
                return [y, x - 1]  # Move left
        
        # Lower-left corner of the circle
        elif board[y - 1][x + 1] == 'X':  
            if clockwise:
                return [y - 1, x]  # Move up
            else:
                return [y, x + 1]  # Move right
        
        # Lower-right corner of the circle
        elif board[y - 1][x - 1] == 'X':  
            if clockwise:
                return [y, x - 1]  # Move left
            else:
                return [y - 1, x]  # Move up
    
    # If none of these cases match, return the original position
    return cop

def move_cop(cop, is_cop1):
    global robber
    if is_near_circle_wall(cop) and is_near_circle_wall(cop2 if is_cop1 else cop1) and is_near_circle_wall(robber):
        return move_cop_circle(cop, is_cop1)
    
    # Find the move that most reduces Manhattan distance
    best_move = cop
    min_distance = manhattan_distance(cop, robber)
    
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = [cop[0] + dy, cop[1] + dx]
        if is_valid_move(new_pos):
            new_distance = manhattan_distance(new_pos, robber)
            if new_distance < min_distance:
                best_move = new_pos
                min_distance = new_distance
    
    if best_move != cop:
        return best_move
    
    # If the best move is blocked, follow these rules
    if cop[0] > robber[0] and is_valid_move([cop[0] - 1, cop[1]]):
        return [cop[0] - 1, cop[1]]
    elif cop[0] < robber[0] and is_valid_move([cop[0] + 1, cop[1]]):
        return [cop[0] + 1, cop[1]]
    elif cop[1] > robber[1] and is_valid_move([cop[0], cop[1] - 1]):
        return [cop[0], cop[1] - 1]
    elif cop[1] < robber[1] and is_valid_move([cop[0], cop[1] + 1]):
        return [cop[0], cop[1] + 1]
    
    return cop

# Main game loop
clock = pygame.time.Clock()
running = True
robber_turn = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and robber_turn:
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                move_robber(event.key)
                robber_turn = False

    if not robber_turn:
        cop1 = move_cop(cop1, True)
        cop2 = move_cop(cop2, False)
        robber_turn = True

    screen.fill(WHITE)
    draw_board()
    pygame.display.flip()
    clock.tick(FPS)

    if robber in [cop1, cop2]:
        print("Cops win!")
        running = False

pygame.quit()
sys.exit()