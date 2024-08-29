from node import Node


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = set()

    def add_edge(self, node1, node2):
        if node1 in self.nodes:
            self.nodes[node1].add(node2)

    def get_neighbors(self, node):
        return self.nodes.get(node, set())

    def create_graph(self, board):
        rows = len(board)
        cols = len(board[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for i in range(rows):
            for j in range(cols):
                for k in range(rows):
                    for l in range(cols):
                        for turn in ['robber', 'policeman']:
                            if board[i][j] == '#' or board[k][l] == '#':
                                continue  # Skip positions with walls
                            node = Node((i, j), (k, l), turn)
                            self.add_node(node)
                            self.add_edges_for_node(node, board, directions)

    def add_edges_for_node(self, node, board, directions):
        rows = len(board)
        cols = len(board[0])
        if node.turn == 'robber':
            next_turn = 'policeman'
            start_pos, other_pos = node.robber, node.policeman
        else:
            next_turn = 'robber'
            start_pos, other_pos = node.policeman, node.robber

        for dx, dy in directions:
            new_pos = (start_pos[0] + dx, start_pos[1] + dy)
            if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and board[new_pos[0]][new_pos[1]] != '#':
                next_node = Node(new_pos if node.turn == 'robber' else node.robber,
                                 new_pos if node.turn == 'policeman' else node.policeman,
                                 next_turn)
                self.add_edge(node, next_node)

    def find_winning_states(self):
        winning_states = set()

        # Step 1: Add states where the robber and policeman are on the same spot
        for node in self.nodes:
            if node.robber == node.policeman:
                winning_states.add(node)

        # Step 2: Expand the winning states
        expanded = True
        while expanded:
            expanded = False
            new_winning_states = set()

            for node in self.nodes:
                if node in winning_states:
                    continue

                # Policeman's turn: Check if he can move into a winning state
                if node.turn == 'policeman':
                    for neighbor in self.get_neighbors(node):
                        if neighbor in winning_states:
                            new_winning_states.add(node)
                            expanded = True
                            break

                # Robber's turn: Check if every possible move leads to a winning state
                if node.turn == 'robber':
                    all_moves_lead_to_win = True
                    for neighbor in self.get_neighbors(node):
                        if neighbor not in winning_states:
                            all_moves_lead_to_win = False
                            break
                    if all_moves_lead_to_win:
                        new_winning_states.add(node)
                        expanded = True

            winning_states.update(new_winning_states)

        return winning_states

