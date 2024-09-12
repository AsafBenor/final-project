class Node:
    def __init__(self, robber, policeman, turn):
        self.robber = robber
        self.policeman = policeman
        self.turn = turn

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.robber == other.robber and self.policeman == other.policeman and self.turn == other.turn
        return False

    def __hash__(self):
        return hash((self.robber, self.policeman, self.turn))

    def __repr__(self):
        return f"Node(robber={self.robber}, policeman={self.policeman}, turn={self.turn})"

    def __str__(self):
        return f"Node with Robber at {self.robber}, Policeman at {self.policeman}, Turn: {self.turn}"