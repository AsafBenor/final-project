import os
import subprocess
import re

from modelGeneration2 import generate_nusmv_model_1_cop
from modelGeneration_2_cops import generate_nusmv_model_2_cop
from output_simulator import visualize_cop_robber_game

NUXMV_PATH = r"C:\Users\97252\Desktop\final-Project\nuXmv-2.0.0-win64\bin"


def print_board(board):
    print("\n----cop and robber board----")
    for row in board:
        print(' '.join(row))
    print("---------------------\n")


def create_smv_file_1_cop(board, cop_position, robber_position):
    filename = 'cop_robber_1_cop.smv'
    n = len(board)
    m = len(board[0])

    content = generate_nusmv_model_1_cop(n, m, board, cop_position, robber_position)
    file_path = os.path.join(NUXMV_PATH, filename)

    with open(file_path, 'w') as file:
        file.write(content)

    print(f'File {filename} has been created.')

def create_smv_file_2_cops(board, cop1_position, cop2_position, robber_position):
    filename = 'cop_robber_2_cops.smv'
    n = len(board)
    m = len(board[0])

    content = generate_nusmv_model_2_cop(n, m, board, cop1_position, cop2_position, robber_position)
    file_path = os.path.join(NUXMV_PATH, filename)

    with open(file_path, 'w') as file:
        file.write(content)

    print(f'File {filename} has been created.')

def run_nuxmv_1_cop():
    filename = 'cop_robber_1_cop.smv'
    nuxmv_executable_path = os.path.join(NUXMV_PATH, 'nuXmv.exe')
    file_path = os.path.join(NUXMV_PATH, filename)
    command = [nuxmv_executable_path, file_path]

    result = subprocess.run(command, capture_output=True, text=True)
    print("Standard Output:\n", result.stdout)
    print("Standard Error:\n", result.stderr)
    return result.stdout

# def run_nuxmv_2_cops(): #BDD
#     filename = 'cop_robber_2_cops.smv'
#     nuxmv_executable_path = os.path.join(NUXMV_PATH, 'nuXmv.exe')
#     file_path = os.path.join(NUXMV_PATH, filename)
    
#     command = [nuxmv_executable_path, "-int", file_path]
    
#     nuxmvProcess = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
#     nuxmvProcess.stdin.write("go\n")
#     nuxmvProcess.stdin.write("check_ltlspec\n")
#     nuxmvProcess.stdin.write("quit\n")
    
#     stdout, stderr = nuxmvProcess.communicate()
    
#     print("Standard Output:\n", stdout)
#     #print("Standard Error:\n", stderr)
#     return stdout

def run_nuxmv_2_cops(): #SAT
    filename = 'cop_robber_2_cops.smv'
    nuxmv_executable_path = os.path.join(NUXMV_PATH, 'nuXmv.exe')
    file_path = os.path.join(NUXMV_PATH, filename)
    
    command = [nuxmv_executable_path, "-int", file_path]
    
    nuxmvProcess = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
    nuxmvProcess.stdin.write("go_bmc\n")
    nuxmvProcess.stdin.write(f"check_ltlspec_bmc -k 150\n")
    nuxmvProcess.stdin.write("quit\n")
    
    stdout, stderr = nuxmvProcess.communicate()
    
    print("Standard Output:\n", stdout)
    # print("Standard Error:\n", stderr)
    return stdout

# def run_nuxmv_2_cops(): #Normal
#     filename = 'cop_robber_2_cops.smv'
#     nuxmv_executable_path = os.path.join(NUXMV_PATH, 'nuXmv.exe')
#     file_path = os.path.join(NUXMV_PATH, filename)
#     command = [nuxmv_executable_path, file_path]

#     result = subprocess.run(command, capture_output=True, text=True)
#     print("Standard Output:\n", result.stdout)
#     print("Standard Error:\n", result.stderr)
#     return result.stdout

def get_positions_1_cop(board):
    cop_position = None
    robber_position = None

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 'C':
                cop_position = (i, j)
            elif cell == 'R':
                robber_position = (i, j)

    return cop_position, robber_position

def get_positions_2_cops(board):
    cop1_position = None
    cop2_position = None
    robber_position = None

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 'C1':
                cop1_position = (i, j)
            elif cell == 'C2':
                cop2_position = (i, j)
            elif cell == 'R':
                robber_position = (i, j)

    return cop1_position, cop2_position, robber_position

def parse_nuxmv_output_1_cop(output):
    def safe_int(value):
        try:
            return int(value)
        except ValueError:
            return None

    lines = output.strip().split('\n')
    positions = {
        "cop_row": None,
        "cop_col": None,
        "robber_row": None,
        "robber_col": None,
        "movement_cop": None,
        "movement_robber": None
    }

    explanation = []

    for line in lines:
        if 'cop_row =' in line:
            value = line.split('=')[1].strip()
            positions['cop_row'] = safe_int(value)
        elif 'cop_col =' in line:
            value = line.split('=')[1].strip()
            positions['cop_col'] = safe_int(value)
        elif 'robber_row =' in line:
            value = line.split('=')[1].strip()
            positions['robber_row'] = safe_int(value)
        elif 'robber_col =' in line:
            value = line.split('=')[1].strip()
            positions['robber_col'] = safe_int(value)
        elif 'movement_cop =' in line:
            positions['movement_cop'] = line.split('=')[1].strip()
        elif 'movement_robber =' in line:
            positions['movement_robber'] = line.split('=')[1].strip()

        if '-> State:' in line and None not in (
        positions['cop_row'], positions['cop_col'], positions['robber_row'], positions['robber_col']):
            cop_position = (positions['cop_row'], positions['cop_col'])
            robber_position = (positions['robber_row'], positions['robber_col'])

            if positions['movement_cop'] != '0' and positions['movement_cop']:
                move = positions['movement_cop']
                if move == 'd':
                    explanation.append(f"Cop moves down to {cop_position}")
                elif move == 'u':
                    explanation.append(f"Cop moves up to {cop_position}")
                elif move == 'l':
                    explanation.append(f"Cop moves left to {cop_position}")
                elif move == 'r':
                    explanation.append(f"Cop moves right to {cop_position}")

            if positions['movement_robber'] != '0' and positions['movement_robber']:
                move = positions['movement_robber']
                if move == 'd':
                    explanation.append(f"Robber moves down to {robber_position}")
                elif move == 'u':
                    explanation.append(f"Robber moves up to {robber_position}")
                elif move == 'l':
                    explanation.append(f"Robber moves left to {robber_position}")
                elif move == 'r':
                    explanation.append(f"Robber moves right to {robber_position}")

    return explanation


def parse_nuxmv_output_2_cop(output):
    def safe_int(value):
        try:
            return int(value)
        except ValueError:
            return None
    
    lines = output.strip().split('\n')
    positions = {
        "cop1_row": None,
        "cop1_col": None,
        "cop2_row": None,
        "cop2_col": None,
        "robber_row": None,
        "robber_col": None,
        "movement_cop1": None,
        "movement_cop2": None,
        "movement_robber": None
    }
    
    explanation = []
    
    for line in lines:
        if 'cop1_row =' in line:
            value = line.split('=')[1].strip()
            positions['cop1_row'] = safe_int(value)
        elif 'cop1_col =' in line:
            value = line.split('=')[1].strip()
            positions['cop1_col'] = safe_int(value)
        elif 'cop2_row =' in line:
            value = line.split('=')[1].strip()
            positions['cop2_row'] = safe_int(value)
        elif 'cop2_col =' in line:
            value = line.split('=')[1].strip()
            positions['cop2_col'] = safe_int(value)
        elif 'robber_row =' in line:
            value = line.split('=')[1].strip()
            positions['robber_row'] = safe_int(value)
        elif 'robber_col =' in line:
            value = line.split('=')[1].strip()
            positions['robber_col'] = safe_int(value)
        elif 'movement_cop1 =' in line:
            positions['movement_cop1'] = line.split('=')[1].strip()
        elif 'movement_cop2 =' in line:
            positions['movement_cop2'] = line.split('=')[1].strip()
        elif 'movement_robber =' in line:
            positions['movement_robber'] = line.split('=')[1].strip()
        
        if '-> State:' in line and None not in (
            positions['cop1_row'], positions['cop1_col'], 
            positions['cop2_row'], positions['cop2_col'], 
            positions['robber_row'], positions['robber_col']):
            cop1_position = (positions['cop1_row'], positions['cop1_col'])
            cop2_position = (positions['cop2_row'], positions['cop2_col'])
            robber_position = (positions['robber_row'], positions['robber_col'])
            
            if positions['movement_cop1'] != '0' and positions['movement_cop1']:
                move = positions['movement_cop1']
                if move == 'd':
                    explanation.append(f"Cop1 moves down to {cop1_position}")
                elif move == 'u':
                    explanation.append(f"Cop1 moves up to {cop1_position}")
                elif move == 'l':
                    explanation.append(f"Cop1 moves left to {cop1_position}")
                elif move == 'r':
                    explanation.append(f"Cop1 moves right to {cop1_position}")
            
            if positions['movement_cop2'] != '0' and positions['movement_cop2']:
                move = positions['movement_cop2']
                if move == 'd':
                    explanation.append(f"Cop2 moves down to {cop2_position}")
                elif move == 'u':
                    explanation.append(f"Cop2 moves up to {cop2_position}")
                elif move == 'l':
                    explanation.append(f"Cop2 moves left to {cop2_position}")
                elif move == 'r':
                    explanation.append(f"Cop2 moves right to {cop2_position}")
            
            if positions['movement_robber'] != '0' and positions['movement_robber']:
                move = positions['movement_robber']
                if move == 'd':
                    explanation.append(f"Robber moves down to {robber_position}")
                elif move == 'u':
                    explanation.append(f"Robber moves up to {robber_position}")
                elif move == 'l':
                    explanation.append(f"Robber moves left to {robber_position}")
                elif move == 'r':
                    explanation.append(f"Robber moves right to {robber_position}")
    
    return explanation


if __name__ == "__main__":
    board = [
        ['#', '#', '#', '#', '#'],
        ['#', 'R', '_', '_', '#'],
        ['#', '_', 'C', '_', '#'],
        ['#', '_', '_', '_', '#'],
        ['#', '#', '#', '#', '#']
    ]

#     board = [
#         ['#', '#', '#', '#', '#', '#'],
#         ['#', '_', 'C', '_', 'R', '#'],
#         ['#', '_', '#', '#', '_', '#'],
#         ['#', '_', '#', '#', '_', '#'],
#         ['#', '_', '_', '_', '_', '#'],
#         ['#', '#', '#', '#', '#', '#']
# ]

    # board_2_cops = [
    #     ['#', '#', '#', '#', '#'],
    #     ['#', '_', '_', 'R', '#'],
    #     ['#', 'C2', '_', '_', '#'],
    #     ['#', 'C1', '_', '_', '#'],
    #     ['#', '#', '#', '#', '#']
    # ]

    board_2_cops = [
    ['#', '#', '#', '#', '#', '#'],
    ['#', 'C1', 'C2', '_', '_', '#'],
    ['#', '_', 'X', 'X', 'R', '#'],
    ['#', '_', 'X', 'X', '_', '#'],
    ['#', '_', '_', '_', '_', '#'],
    ['#', '_', '_', '_', '_', '#'],
    ['#', '_', '_', '_', '_', '#'],
    ['#', '#', '#', '#', '#', '#']
]

    num = input("how many cops? 1 or 2\n")
    if num == "1":
        cop_position, robber_position = get_positions_1_cop(board)
        print_board(board)
        create_smv_file_1_cop(board, cop_position, robber_position)
        output = run_nuxmv_1_cop()
        moves = parse_nuxmv_output_1_cop(output)

        print_board(board)
        for move in moves:
            print(move)

        if len(moves) != 0:
            visualize_cop_robber_game(board,moves,1)

    else:
        cop1_position, cop2_position, robber_position = get_positions_2_cops(board_2_cops)
        print_board(board_2_cops)
        create_smv_file_2_cops(board_2_cops, cop1_position, cop2_position, robber_position)
        output = run_nuxmv_2_cops()
        moves = parse_nuxmv_output_2_cop(output)

        print_board(board_2_cops)
        for move in moves:
            print(move)
        
        if len(moves) != 0:
            visualize_cop_robber_game(board_2_cops,moves,2)









    





    



