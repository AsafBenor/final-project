import os
import pickle
from graph import Graph, Node

PICKLE_FILENAME = "graph_data.pkl"


def generate_and_save_graph(board):
    graph = Graph()
    print("Generating graph from board...")
    graph.create_graph(board)

    # Save the graph to a pickle file
    with open(PICKLE_FILENAME, 'wb') as f:
        pickle.dump(graph, f)
    print(f"Graph saved to {PICKLE_FILENAME}.")


def load_graph():
    if os.path.exists(PICKLE_FILENAME):
        print(f"Loading graph from {PICKLE_FILENAME}...")
        with open(PICKLE_FILENAME, 'rb') as f:
            graph = pickle.load(f)
        print("Graph loaded successfully.")
    else:
        print(f"No existing graph found. Please generate a new graph.")
        return None
    return graph


def print_board(board, robber_pos, policeman_pos):
    # Create a copy of the board to modify
    board_copy = [list(row) for row in board]

    # Place the Robber (R) and Policeman (P) on the board
    board_copy[robber_pos[0]][robber_pos[1]] = 'R'
    board_copy[policeman_pos[0]][policeman_pos[1]] = 'P'

    # Convert rows back to strings and print the board
    print("\nCurrent board state:")
    for row in board_copy:
        print("".join(row))


def check_state(graph, board):
    try:
        rows = len(board)
        cols = len(board[0])

        # Enter the state details
        while True:
            robber_x = int(input(f"Enter the robber's x position (0-{rows - 1}): "))
            robber_y = int(input(f"Enter the robber's y position (0-{cols - 1}): "))
            policeman_x = int(input(f"Enter the policeman's x position (0-{rows - 1}): "))
            policeman_y = int(input(f"Enter the policeman's y position (0-{cols - 1}): "))

            if not (0 <= robber_x < rows and 0 <= robber_y < cols and
                    0 <= policeman_x < rows and 0 <= policeman_y < cols):
                print(
                    f"Invalid positions. Please enter values within the range [0, {rows - 1}] for x and [0, {cols - 1}] for y.")
                continue

            if board[robber_x][robber_y] == '#' or board[policeman_x][policeman_y] == '#':
                print(
                    "Invalid positions. Robber or Policeman cannot start on a wall ('#'). Please enter valid positions.")
                continue

            break

        turn = input("Enter the turn ('robber' or 'policeman'): ")

        if turn not in ['robber', 'policeman']:
            print("Invalid turn. Please enter 'robber' or 'policeman'.")
            return

        # Create the corresponding node
        node = Node((robber_x, robber_y), (policeman_x, policeman_y), turn)

        # Print the board with the current positions
        print_board(board, (robber_x, robber_y), (policeman_x, policeman_y))

        # Check if the node is a winning state
        winning_states, winning_state_parents = graph.find_winning_states()
        if node in winning_states:
            print("The entered state is a winning state.")
            parent = winning_state_parents.get(node)
            while parent:
                print(f"Parent state: {parent}")
                parent = winning_state_parents.get(parent)  # Trace back the parent chain

            simulate_game(graph, board, node)
        else:
            print("The entered state is NOT a winning state.")

    except ValueError:
        print("Invalid input. Please enter numeric values for positions.")


def simulate_game(graph, board, node):
    # Initial positions of robber and policeman
    robber_x = node.robber[0]
    robber_y = node.robber[1]
    policeman_x = node.policeman[0]
    policeman_y = node.policeman[1]

    # Start with robber's turn
    turn = node.turn

    # Get winning states and parent relations
    winning_states, winning_state_parents = graph.find_winning_states()

    # Define the movement for directions
    direction_map = {
        'A': (0, -1),  # Left: Decrease y
        'W': (-1, 0),  # Up: Decrease x
        'D': (0, 1),  # Right: Increase y
        'S': (1, 0)  # Down: Increase x
    }

    while True:
        if turn == 'robber':
            # Print the current state of the board
            print_board(board, (robber_x, robber_y), (policeman_x, policeman_y))
            print("\nRobber's Turn:")

            # Get the robber's move (A, W, D, S)
            move = input("Enter the robber's move (A for Left, W for Up, D for Right, S for Down): ").strip().upper()

            if move not in direction_map:
                print("Invalid move. Please enter A, W, D, or S.")
                continue

            # Calculate the new robber position
            delta_x, delta_y = direction_map[move]
            new_robber_x = robber_x + delta_x
            new_robber_y = robber_y + delta_y

            # Validate move
            if not (0 <= new_robber_x < len(board) and 0 <= new_robber_y < len(board[0])):
                print("Invalid move. The robber is out of bounds. Try again.")
                continue

            if board[new_robber_x][new_robber_y] == '#':
                print("You cannot move to a wall. Try again.")
                continue

            # Update robber's position
            robber_x, robber_y = new_robber_x, new_robber_y
            turn = 'policeman'  # Change turn to policeman

        elif turn == 'policeman':
            # Print the current state of the board
            print_board(board, (robber_x, robber_y), (policeman_x, policeman_y))
            print("\nPoliceman's Turn:")

            # Create the current state node
            current_node = Node((robber_x, robber_y), (policeman_x, policeman_y), 'policeman')

            if (robber_x, robber_y) == (policeman_x, policeman_y):
                print("Policeman has caught the robber! Game over.")
                break

            # Find the parent state for the policeman's move
            next_node = winning_state_parents.get(current_node)

            if next_node:
                # Update policeman's position to the one in the parent state
                policeman_x, policeman_y = next_node.policeman
                print(f"Policeman moves to position ({policeman_x}, {policeman_y})")
            else:
                print("No winning move found. Robber is safe... for now!")

            if (robber_x, robber_y) == (policeman_x, policeman_y):
                print("Policeman has caught the robber! Game over.")
                break

            turn = 'robber'  # Change turn to robber



def main():
    board = [
        "-----",
        "-----",
        "-----",
        "-----"
    ]  # Example board, modify as needed

    graph = load_graph()

    if not graph:
        generate_and_save_graph(board)
        graph = load_graph()

    # Find all winning states
    winning_states, winning_state_parents = graph.find_winning_states()
    print(f"Total winning states: {len(winning_states)}")

    # Option to check if a specific state is a winning state
    check_state_option = input(
        "Do you want to check if a specific state is a winning state? (yes/no): ").strip().lower()
    if check_state_option == 'yes':
        check_state(graph, board)


if __name__ == "__main__":
    main()