class Player:
    def __init__(self, board):
        self.board = board
        self.x = None
        self.y = None

    
    def move(self):
        pass

class Robber(Player):
    
    def __init__(self, board):
        super().__init__(board)
    
    def handle_user_input(self):
        valid_inputs = ['w', 'a', 's', 'd']
        # Get user input and validate it
        while True:
            direction = input('Enter a direction (w, a, s, d): ').lower()
            if direction in valid_inputs:
                break
            else:
                print('Invalid direction. Try again.')
        return direction

    def move(self):
        # Update the robber's position on the board and check if the robber hits the board's boundary
        old_x = self.x
        old_y = self.y
        while True:
            direction = self.handle_user_input()
            if direction == 'w':
                if self.x == 0:
                    print('You hit a boundary. Try again.')
                else:
                    self.x -= 1
                    break
            elif direction == 'a':
                if self.y == 0:
                    print('You hit a boundary. Try again.')
                else:
                    self.y -= 1
                    break
            elif direction == 's':
                if self.x == self.board.size - 1:
                    print('You hit a boundary. Try again.')
                else:
                    self.x += 1
                    break
            elif direction == 'd':
                if self.y == self.board.size - 1:
                    print('You hit a boundary. Try again.')
                else:
                    self.y += 1
                    break
        if self.board.grid[self.x][self.y] == '-':
            self.board.grid[self.x][self.y] = 'R'
        elif self.board.grid[self.x][self.y] == 'C':
            self.board.grid[self.x][self.y] = 'X'
        self.board.grid[old_x][old_y] = '-'


        
        
    

class Cop(Player):
    def __init__(self, board):
        super().__init__(board)

    def move(self, robber_position):
        # TODO: Implement the cop's movement
        best_direction = self.find_best_direction(robber_position)
        self.move_in_direction(best_direction, robber_position)

    def find_best_direction(self, robber_position):
        cop_position = [self.x, self.y]

        # Calculate the direction to move towards the robber
        x_diff = robber_position[0] - cop_position[0]
        y_diff = robber_position[1] - cop_position[1]

        if abs(x_diff) > abs(y_diff):
            return 's' if x_diff > 0 else 'w'
        else:
            return 'd' if y_diff > 0 else 'a'
        
    def move_in_direction(self, direction, robber_position):
        old_x = self.x
        old_y = self.y
        if direction == 'w' and self.x>0:
            self.x -= 1
        elif direction == 'a' and self.y>0:
            self.y -= 1
        elif direction == 's' and self.x<self.board.size-1:
            self.x += 1
        elif direction == 'd' and self.y<self.board.size-1:
            self.y += 1

        if self.board.grid[self.x][self.y] == '-':
            self.board.grid[self.x][self.y] = 'C'
            self.board.grid[old_x][old_y] = '-'
        elif self.board.grid[self.x][self.y] == 'R':
            self.board.grid[self.x][self.y] = 'X'
            self.board.grid[old_x][old_y] = '-'
        else:
            self.handle_collision(old_x, old_y, robber_position)

    def handle_collision(self, old_x, old_y, robber_position):
        second_best_direction = self.find_second_best_direction(robber_position)
        if second_best_direction:
            self.move_in_direction(second_best_direction, robber_position)
        else:
            print('Cop is stuck. Cannot move. Skipping turn.')
        
    def find_second_best_direction(self, robber_position):
        best_direction = self.find_best_direction(robber_position)
        directions = ['w', 'a', 's', 'd']
        directions.remove(best_direction)
        for direction in directions:
            new_x, new_y = self.calculate_new_position(direction)
            if 0<=new_x<self.board.size and 0<=new_y<self.board.size and self.board.grid[new_x][new_y] == '-':
                return direction
        return None
    
    def calculate_new_position(self, direction):
        new_x = self.x
        new_y = self.y
        if direction == 'w':
            new_x -= 1
        elif direction == 'a':
            new_y -= 1
        elif direction == 's':
            new_x += 1
        elif direction == 'd':
            new_y += 1
        return new_x, new_y