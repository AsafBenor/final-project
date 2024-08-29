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
        # Enter the state details
        robber_x = int(input("Enter the robber's x position: "))
        robber_y = int(input("Enter the robber's y position: "))
        policeman_x = int(input("Enter the policeman's x position: "))
        policeman_y = int(input("Enter the policeman's y position: "))
        turn = input("Enter the turn ('robber' or 'policeman'): ")

        if turn not in ['robber', 'policeman']:
            print("Invalid turn. Please enter 'robber' or 'policeman'.")
            return

        # Create the corresponding node
        node = Node((robber_x, robber_y), (policeman_x, policeman_y), turn)

        # Print the board with the current positions
        print_board(board, (robber_x, robber_y), (policeman_x, policeman_y))

        # Check if the node is a winning state
        winning_states = graph.find_winning_states()
        if node in winning_states:
            print("The entered state is a winning state.")
        else:
            print("The entered state is NOT a winning state.")

    except ValueError:
        print("Invalid input. Please enter numeric values for positions.")


def main():
    board = [
        "----",
        "-##-",
        "----"
    ]  # Example board, modify as needed

    graph = load_graph()

    if not graph:
        generate_and_save_graph(board)
        graph = load_graph()

    # Find all winning states
    winning_states = graph.find_winning_states()
    print(f"Total winning states: {len(winning_states)}")

    # Option to check if a specific state is a winning state
    check_state_option = input(
        "Do you want to check if a specific state is a winning state? (yes/no): ").strip().lower()
    if check_state_option == 'yes':
        check_state(graph, board)


if __name__ == "__main__":
    main()
