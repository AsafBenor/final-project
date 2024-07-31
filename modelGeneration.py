#Update cops row and col according to movment
def cop_location_change(rows,columns):
    model_content = f'''
tmp_cop_row :=
    
case
    movment_cop = u  &  cop_row > 0 & !walls[cop_row - 1][cop_col]: cop_row - 1;
    movment_cop = d  &  cop_row < {rows - 1} & !walls[cop_row + 1][cop_col]: cop_row + 1;
    TRUE: cop_row;
esac;

tmp_cop_col :=
case
    movment_cop = r  &  cop_col < {columns - 1} & !walls[cop_row][cop_col + 1]: cop_col + 1;
    movment_cop = l & cop_col > 0 & !walls[cop_row][cop_col - 1]: cop_col - 1;
    TRUE: cop_col;
esac;

        '''
    return model_content

#Update robbers row and col according to movment
def robber_location_change(rows,columns):
    model_content = f'''
tmp_robber_row :=
case
    movment_robber = u & robber_row > 0 & !walls[robber_row - 1][robber_col]: robber_row - 1;
    movment_robber = d & robber_row < {rows - 1} & !walls[robber_row + 1][robber_col]: robber_row + 1;
    TRUE: robber_row;
esac;

tmp_robber_col :=
case
    movment_robber = r & robber_col < {columns - 1} & !walls[robber_row][robber_col + 1]: robber_col + 1;
    movment_robber = l & robber_col > 0 & !walls[robber_row][robber_col - 1]: robber_col - 1;
    TRUE: robber_col;
esac;
        '''
    return model_content

# main function to generate the .smv file
def generate_nusmv_model(rows ,columns, board, cop_holder,robber_holder):
    model_content = f'''
MODULE main
DEFINE rows:={rows}; columns:={columns};
-- new   XSB    defunition
-- C      C       Cop
-- R      R       Robber
-- _      _       Floor
-- #      #       Wall

VAR
    cop_row : 0..{rows-1}; --current cops row
    cop_col : 0..{columns-1}; --current cop col
    robber_row : 0..{rows-1}; --current robbers row
    robber_col : 0..{columns-1}; --current robber col
    movment_cop : {{u, d, l, r, 0}};
    movment_robber : {{u, d, l, r, 0}};
    robber_turn : boolean;
    tmp_robber_row : 0..{rows-1};
    tmp_robber_col : 0..{columns-1};
    tmp_cop_row : 0..4;
    tmp_cop_col : 0..4;

ASSIGN

init(robber_turn) := FALSE;
init(movment_cop) := 0;
init(movment_robber) := 0;
init(cop_row) := {cop_holder[0]}; init(cop_col) := {cop_holder[1]};
init(robber_row) := {robber_holder[0]}; init(robber_col) := {robber_holder[1]};

    '''
    model_content+= cop_location_change(rows,columns)
    model_content+= robber_location_change(rows,columns)
    model_content+= f'''

-- Update the actual position of the robber
next(robber_row) := tmp_robber_row;
next(robber_col) := tmp_robber_col;

-- Update the actual position of the cop
next(cop_row) := tmp_cop_row;
next(cop_col) := tmp_cop_col;

next(robber_turn) := !robber_turn;

next(movment_cop):= 
case
    (cop_row > robber_row) & (manhattan_distance > next_manhattan_distance_if_up) & robber_turn : u;
    (cop_row < robber_row) & (manhattan_distance > next_manhattan_distance_if_down) & robber_turn: d;
    (cop_col > robber_col) & (manhattan_distance > next_manhattan_distance_if_left) & robber_turn: l;
    (cop_col < robber_col) & (manhattan_distance > next_manhattan_distance_if_right) & robber_turn: r;
    !robber_turn : 0;
    TRUE: movment_cop;
esac;

next(movment_robber):= 
case
    !robber_turn : {{u,d,l,r}};
    robber_turn : 0;
    TRUE : movment_robber;
esac;
    '''


    model_content+= f'''
DEFINE
--manhattan_distance := abs(cop_row - robber_row) + abs(cop_col - robber_col);
--next_manhattan_distance_if_up := abs((cop_row - 1) - robber_row) + abs(cop_col - robber_col);
--next_manhattan_distance_if_down := abs((cop_row + 1) - robber_row) + abs(cop_col - robber_col);
--next_manhattan_distance_if_left := abs(cop_row - robber_row) + abs((cop_col - 1) - robber_col);
--next_manhattan_distance_if_right := abs(cop_row - robber_row) + abs((cop_col + 1) - robber_col);

manhattan_distance := abs(cop_row - tmp_robber_row) + abs(cop_col - tmp_robber_col);
next_manhattan_distance_if_up := abs((cop_row - 1) - tmp_robber_row) + abs(cop_col - tmp_robber_col);
next_manhattan_distance_if_down := abs((cop_row + 1) - tmp_robber_row) + abs(cop_col - tmp_robber_col);
next_manhattan_distance_if_left := abs(cop_row - tmp_robber_row) + abs((cop_col - 1) - tmp_robber_col);
next_manhattan_distance_if_right := abs(cop_row - tmp_robber_row) + abs((cop_col + 1) - tmp_robber_col);
'''
# cop_on_wall := walls[cop_row][cop_col];
# robber_on_wall := walls[robber_row][robber_col];
#      '''

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

#     model_content += f'''
# JUSTICE

# !(cop_on_wall | robber_on_wall);
#     '''
    model_content += f'''
DEFINE


--Oposite cases

SPEC EG (tmp_cop_row != robber_row | tmp_cop_col != robber_col) -- if there is at least one scenarion the the robber run from the cop shows true, else fales
LTLSPEC G F (tmp_cop_row = robber_row & tmp_cop_col = robber_col) --if always the cop cathes the tobber shows true, else false
    '''

    return model_content
    




    

    





    





    



