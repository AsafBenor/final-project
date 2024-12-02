import pygame
import time
import re

def visualize_cop_robber_game(board, movements, num_cops):
    pygame.init()
    
    # Constants
    CELL_SIZE = 60
    GRID_WIDTH = len(board[0])
    GRID_HEIGHT = len(board)
    WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
    WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (0, 191, 255)
    
    # Set up the display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Cop and Robber Game")
    
    def draw_board():
        screen.fill(WHITE)
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if cell == '#':
                    pygame.draw.rect(screen, GRAY, rect)
                elif cell == 'X':
                    pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
    
    def draw_agents(robber_pos, cop1_pos, cop2_pos=None):
        # Draw robber
        pygame.draw.circle(screen, RED, (robber_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                                         robber_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
        # Draw cop 1
        pygame.draw.circle(screen, BLUE, (cop1_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                                          cop1_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
        # Draw cop 2 if present
        if cop2_pos:
            pygame.draw.circle(screen, LIGHT_BLUE, (cop2_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                                                    cop2_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    
    def get_initial_positions():
        robber_pos = cop1_pos = cop2_pos = None
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell == 'R':
                    robber_pos = (y, x)
                elif cell == 'C' or cell == 'C1':
                    cop1_pos = (y, x)
                elif cell == 'C2':
                    cop2_pos = (y, x)
        return robber_pos, cop1_pos, cop2_pos
    
    def parse_movement(move):
        # Try to extract coordinates using regex
        match = re.search(r'\((\d+),\s*(\d+)\)', move)
        if match:
            return int(match.group(1)), int(match.group(2))
        
        # If regex fails, try to get the last two items split by spaces
        parts = move.split()
        if len(parts) >= 2:
            try:
                return int(parts[-2]), int(parts[-1])
            except ValueError:
                pass
        
        # If all else fails, return None
        print(f"Warning: Could not parse movement from '{move}'")
        return None

    initial_robber_pos, initial_cop1_pos, initial_cop2_pos = get_initial_positions()
    robber_pos, cop1_pos, cop2_pos = initial_robber_pos, initial_cop1_pos, initial_cop2_pos
    
    running = True
    movement_index = 0
    
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if movement_index >= len(movements):
            # Reset positions when we reach the end of movements
            robber_pos, cop1_pos, cop2_pos = initial_robber_pos, initial_cop1_pos, initial_cop2_pos
            movement_index = 0
            print("Resetting positions and movements")
        
        move = movements[movement_index]
        # print(f"Processing move {movement_index + 1}/{len(movements)}: {move}")
        
        new_pos = parse_movement(move)
        if new_pos:
            if 'Robber moves' in move:
                robber_pos = new_pos
                print(f"Robber new position: {robber_pos}")
            elif 'Cop1 moves' in move or (num_cops == 1 and 'Cop moves' in move):
                cop1_pos = new_pos
                print(f"Cop1 new position: {cop1_pos}")
            elif num_cops == 2 and 'Cop2 moves' in move:
                cop2_pos = new_pos
                print(f"Cop2 new position: {cop2_pos}")
        else:
            print(f"Could not update position for move: {move}")
        
        draw_board()
        draw_agents(robber_pos, cop1_pos, cop2_pos if num_cops == 2 else None)
        pygame.display.flip()
        
        movement_index += 1
        clock.tick(2)  # Limit to 2 frame per second (1 move per second)
    
    pygame.quit()