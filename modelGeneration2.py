#Update cops row and col according to movement
def cop_location_change(rows, columns):
    return f'''
tmp_cop_row :=
    case
        movement_cop = u & cop_row > 0 & !walls[cop_row - 1][cop_col]: cop_row - 1;
        movement_cop = d & cop_row < {rows - 1} & !walls[cop_row + 1][cop_col]: cop_row + 1;
        TRUE: cop_row;
    esac;

tmp_cop_col :=
    case
        movement_cop = r & cop_col < {columns - 1} & !walls[cop_row][cop_col + 1]: cop_col + 1;
        movement_cop = l & cop_col > 0 & !walls[cop_row][cop_col - 1]: cop_col - 1;
        TRUE: cop_col;
    esac;
    '''

def robber_location_change(rows, columns):
    return f'''
tmp_robber_row :=
    case
        movement_robber = u & robber_row > 0 & !walls[robber_row - 1][robber_col]: robber_row - 1;
        movement_robber = d & robber_row < {rows - 1} & !walls[robber_row + 1][robber_col]: robber_row + 1;
        TRUE: robber_row;
    esac;

tmp_robber_col :=
    case
        movement_robber = r & robber_col < {columns - 1} & !walls[robber_row][robber_col + 1]: robber_col + 1;
        movement_robber = l & robber_col > 0 & !walls[robber_row][robber_col - 1]: robber_col - 1;
        TRUE: robber_col;
    esac;
    '''

def generate_nusmv_model_1_cop(rows ,columns, board, cop_holder,robber_holder):
    model_content = f'''
MODULE main
DEFINE rows:={rows}; columns:={columns};
-- new   XSB    definition
-- C      C       Cop
-- R      R       Robber
-- _      _       Floor
-- #      #       Wall

VAR
    cop_row : 0..{rows-1};
    cop_col : 0..{columns-1};
    robber_row : 0..{rows-1};
    robber_col : 0..{columns-1};
    movement_cop : {{u, d, l, r, 0}};
    movement_robber : {{u, d, l, r, 0}};
    robber_turn : boolean;
    tmp_robber_row : 0..{rows-1};
    tmp_robber_col : 0..{columns-1};
    tmp_cop_row : 0..{rows-1};
    tmp_cop_col : 0..{columns-1};

ASSIGN

    init(robber_turn) := FALSE;
    init(movement_cop) := 0;
    init(movement_robber) := 0;
    init(cop_row) := {cop_holder[0]};
    init(cop_col) := {cop_holder[1]};
    init(robber_row) := {robber_holder[0]};
    init(robber_col) := {robber_holder[1]};

    '''
    model_content+= cop_location_change(rows,columns)
    model_content+= robber_location_change(rows,columns)
    model_content+= f'''

-- Update the actual position of the robber and the cop
next(robber_row) := tmp_robber_row;
next(robber_col) := tmp_robber_col;
next(cop_row) := tmp_cop_row;
next(cop_col) := tmp_cop_col;
next(robber_turn) := !robber_turn;

-- Movement logic for cop and robber
next(movement_cop):= 
    case
        (cop_row >= robber_row) & (manhattan_distance > next_manhattan_distance_if_up) & !walls[cop_row - 1][cop_col] & robber_turn : u;
        (cop_row <= robber_row) & (manhattan_distance > next_manhattan_distance_if_down) & !walls[cop_row + 1][cop_col] & robber_turn: d;
        (cop_col >= robber_col) & (manhattan_distance > next_manhattan_distance_if_left) & !walls[cop_row][cop_col - 1] & robber_turn: l;
        (cop_col <= robber_col) & (manhattan_distance > next_manhattan_distance_if_right) & !walls[cop_row][cop_col + 1] & robber_turn: r;        
        -- If the cop is blocked in the optimal direction, try other directions
        (cop_row >= robber_row) & (cop_row - 1 >= 0) & walls[cop_row - 1][cop_col] & (cop_col + 1 < columns) & !walls[cop_row][cop_col + 1] & robber_turn: r;  -- move right if blocked up
        (cop_row >= robber_row) & (cop_row - 1 >= 0) & walls[cop_row - 1][cop_col] & (cop_col - 1 >= 0) & !walls[cop_row][cop_col - 1] & robber_turn: l;  -- move left if blocked up
        (cop_row <= robber_row) & (cop_row + 1 < rows) & walls[cop_row + 1][cop_col] & (cop_col + 1 < columns) & !walls[cop_row][cop_col + 1] & robber_turn: r;  -- move right if blocked down
        (cop_row <= robber_row) & (cop_row + 1 < rows) & walls[cop_row + 1][cop_col] & (cop_col - 1 >= 0) & !walls[cop_row][cop_col - 1] & robber_turn: l;  -- move left if blocked down
        (cop_col >= robber_col) & (cop_col - 1 >= 0) & walls[cop_row][cop_col - 1] & (cop_row - 1 >= 0) & !walls[cop_row - 1][cop_col] & robber_turn: u;  -- move up if blocked left
        (cop_col >= robber_col) & (cop_col - 1 >= 0) & walls[cop_row][cop_col - 1] & (cop_row + 1 < rows) & !walls[cop_row + 1][cop_col] & robber_turn: d;  -- move down if blocked left
        (cop_col <= robber_col) & (cop_col + 1 < columns) & walls[cop_row][cop_col + 1] & (cop_row - 1 >= 0) & !walls[cop_row - 1][cop_col] & robber_turn: u;  -- move up if blocked right
        (cop_col <= robber_col) & (cop_col + 1 < columns) & walls[cop_row][cop_col + 1] & (cop_row + 1 < rows) & !walls[cop_row + 1][cop_col] & robber_turn: d;  -- move down if blocked right
        !robber_turn : 0;
        TRUE: movement_cop;
    esac;


next(movement_robber):= 
    case
        robber_turn : 0;  -- No movement if it's not the robber's turn
    
        -- Exclusive single direction movements
        !robber_turn & 
        (robber_row > 0) & !walls[robber_row - 1][robber_col] & 
        !(robber_row < {rows - 1} & !walls[robber_row + 1][robber_col]) & 
        !(robber_col > 0 & !walls[robber_row][robber_col - 1]) & 
        !(robber_col < {columns - 1} & !walls[robber_row][robber_col + 1]) : u;
    
        !robber_turn & 
        (robber_row < {rows - 1}) & !walls[robber_row + 1][robber_col] & 
        !(robber_row > 0 & !walls[robber_row - 1][robber_col]) & 
        !(robber_col > 0 & !walls[robber_row][robber_col - 1]) & 
        !(robber_col < {columns - 1} & !walls[robber_row][robber_col + 1]) : d;
    
        !robber_turn & 
        (robber_col > 0) & !walls[robber_row][robber_col - 1] & 
        !(robber_row > 0 & !walls[robber_row - 1][robber_col]) & 
        !(robber_row < {rows - 1} & !walls[robber_row + 1][robber_col]) & 
        !(robber_col < {columns - 1} & !walls[robber_row][robber_col + 1]) : l;
    
        !robber_turn & 
        (robber_col < {columns - 1}) & !walls[robber_row][robber_col + 1] & 
        !(robber_row > 0 & !walls[robber_row - 1][robber_col]) & 
        !(robber_row < {rows - 1} & !walls[robber_row + 1][robber_col]) & 
        !(robber_col > 0 & !walls[robber_row][robber_col - 1]) : r;
    
        -- Double direction movements
        !robber_turn & 
        (robber_row > 0) & !walls[robber_row - 1][robber_col] & 
        (robber_row < {rows - 1}) & !walls[robber_row + 1][robber_col] & 
        !(robber_col > 0 & !walls[robber_row][robber_col - 1]) & 
        !(robber_col < {columns - 1} & !walls[robber_row][robber_col + 1]) : {{u, d}};
    
        !robber_turn & 
        (robber_col > 0) & !walls[robber_row][robber_col - 1] & 
        (robber_col < {columns - 1}) & !walls[robber_row][robber_col + 1] & 
        !(robber_row > 0 & !walls[robber_row - 1][robber_col]) & 
        !(robber_row < {rows - 1} & !walls[robber_row + 1][robber_col]) : {{l, r}};
    
        !robber_turn & 
        (robber_row > 0) & !walls[robber_row - 1][robber_col] & 
        (robber_col > 0) & !walls[robber_row][robber_col - 1] &
        !(robber_row < {{rows - 1}} & !walls[robber_row + 1][robber_col]) &
        !(robber_col < {{columns - 1}} & !walls[robber_row][robber_col + 1]) : {{u, l}};
    
        !robber_turn & 
        (robber_row < {{rows - 1}}) & !walls[robber_row + 1][robber_col] & 
        (robber_col < {{columns - 1}}) & !walls[robber_row][robber_col + 1] &
        !(robber_row > 0 & !walls[robber_row - 1][robber_col]) &
        !(robber_col > 0 & !walls[robber_row][robber_col - 1]) : {{d, r}};
    
        !robber_turn & 
        (robber_row > 0) & !walls[robber_row - 1][robber_col] & 
        (robber_col < {{columns - 1}}) & !walls[robber_row][robber_col + 1] &
        !(robber_row < {{rows - 1}} & !walls[robber_row + 1][robber_col]) &
        !(robber_col > 0 & !walls[robber_row][robber_col - 1]) : {{u, r}};
    
        !robber_turn & 
        (robber_row < {{rows - 1}}) & !walls[robber_row + 1][robber_col] & 
        (robber_col > 0) & !walls[robber_row][robber_col - 1] &
        !(robber_row > 0 & !walls[robber_row - 1][robber_col]) &
        !(robber_col < {{columns - 1}} & !walls[robber_row][robber_col + 1]) : {{d, l}};
    
        -- Three direction movements
        !robber_turn & 
        (robber_row > 0) & !walls[robber_row - 1][robber_col] & 
        (robber_row < {{rows - 1}}) & !walls[robber_row + 1][robber_col] & 
        (robber_col > 0) & !walls[robber_row][robber_col - 1] &
        !(robber_col < {{columns - 1}} & !walls[robber_row][robber_col + 1]) : {{u, d, l}};
    
        !robber_turn & 
        (robber_row > 0) & !walls[robber_row - 1][robber_col] & 
        (robber_row < {{rows - 1}}) & !walls[robber_row + 1][robber_col] & 
        (robber_col < {{columns - 1}}) & !walls[robber_row][robber_col + 1] &
        !(robber_col > 0 & !walls[robber_row][robber_col - 1]) : {{u, d, r}};
    
        !robber_turn & 
        (robber_row > 0) & !walls[robber_row - 1][robber_col] & 
        (robber_col > 0) & !walls[robber_row][robber_col - 1] & 
        (robber_col < {{columns - 1}}) & !walls[robber_row][robber_col + 1] &
        !(robber_row < {{rows - 1}} & !walls[robber_row + 1][robber_col]) : {{u, l, r}};
    
        !robber_turn & 
        (robber_row < {{rows - 1}}) & !walls[robber_row + 1][robber_col] & 
        (robber_col > 0) & !walls[robber_row][robber_col - 1] & 
        (robber_col < {{columns - 1}}) & !walls[robber_row][robber_col + 1] &
        !(robber_row > 0 & !walls[robber_row - 1][robber_col]) : {{d, l, r}};
    
    
        -- All directions possible
        !robber_turn & 
        (robber_row > 0) & !walls[robber_row - 1][robber_col] & 
        (robber_row < {rows - 1}) & !walls[robber_row + 1][robber_col] & 
        (robber_col > 0) & !walls[robber_row][robber_col - 1] & 
        (robber_col < {columns - 1}) & !walls[robber_row][robber_col + 1] : {{u, d, l, r}};
    
        TRUE : 0;  -- Default to no movement if no valid conditions are met
    esac;

DEFINE

    manhattan_distance := abs(cop_row - tmp_robber_row) + abs(cop_col - tmp_robber_col);
    next_manhattan_distance_if_up := abs((cop_row - 1) - tmp_robber_row) + abs(cop_col - tmp_robber_col);
    next_manhattan_distance_if_down := abs((cop_row + 1) - tmp_robber_row) + abs(cop_col - tmp_robber_col);
    next_manhattan_distance_if_left := abs(cop_row - tmp_robber_row) + abs((cop_col - 1) - tmp_robber_col);
    next_manhattan_distance_if_right := abs(cop_row - tmp_robber_row) + abs((cop_col + 1) - tmp_robber_col);
'''

    model_content += f'''
walls :='''
    # creating the walls constant
    model_content += " [\n"
    for i in range(rows):
        model_content += "["
        for j in range(columns):
            if board[i][j] == '#':
                model_content += " TRUE"
            else:
                model_content += "FALSE"
            if j < columns - 1:
                model_content += ", "
        model_content += "]"
        if i < rows - 1:
            model_content += ",\n"

    model_content += "];"

    model_content += f'''
DEFINE

LTLSPEC F (tmp_cop_row = robber_row & tmp_cop_col = robber_col) --if always the cop cathes the tobber shows true, else false
    '''

    return model_content
    







    





    



