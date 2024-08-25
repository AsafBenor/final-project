import os
import subprocess
import re

from modelGeneration2 import generate_nusmv_model_1_cop
from modelGeneration_2_cops import generate_nusmv_model_2_cop

NUXMV_PATH = r"C:\Users\asafb\OneDrive - Bar-Ilan University - Students\שולחן העבודה\FinalProject\nuXmv-2.0.0-win64\bin"


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


def run_nuxmv_2_cops():
    filename = 'cop_robber_2_cops.smv'
    nuxmv_executable_path = os.path.join(NUXMV_PATH, 'nuXmv.exe')
    file_path = os.path.join(NUXMV_PATH, filename)
    command = [nuxmv_executable_path, file_path]

    result = subprocess.run(command, capture_output=True, text=True)
    print("Standard Output:\n", result.stdout)
    print("Standard Error:\n", result.stderr)
    return result.stdout

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
    pass


if __name__ == "__main__":
    board = [
        ['#', '#', '#', '#', '#'],
        ['#', '_', '_', '_', '#'],
        ['#', 'R', '#', 'C', '#'],
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
    ['#', 'C1', 'C2', '_', 'R', '#'],
    ['#', '_', 'X', 'X', '_', '#'],
    ['#', '_', 'X', 'X', '_', '#'],
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

    else:
        cop1_position, cop2_position, robber_position = get_positions_2_cops(board_2_cops)
        print_board(board_2_cops)
        create_smv_file_2_cops(board_2_cops, cop1_position, cop2_position, robber_position)
        output = run_nuxmv_2_cops()








    





    


