def cop_location_change(rows, columns, cop_number):
    return f'''
tmp_cop{cop_number}_row :=
    case
        movement_cop{cop_number} = u & cop{cop_number}_row > 0 & !walls[cop{cop_number}_row - 1][cop{cop_number}_col]: cop{cop_number}_row - 1;
        movement_cop{cop_number} = d & cop{cop_number}_row < {rows - 1} & !walls[cop{cop_number}_row + 1][cop{cop_number}_col]: cop{cop_number}_row + 1;
        TRUE: cop{cop_number}_row;
    esac;

tmp_cop{cop_number}_col :=
    case
        movement_cop{cop_number} = r & cop{cop_number}_col < {columns - 1} & !walls[cop{cop_number}_row][cop{cop_number}_col + 1]: cop{cop_number}_col + 1;
        movement_cop{cop_number} = l & cop{cop_number}_col > 0 & !walls[cop{cop_number}_row][cop{cop_number}_col - 1]: cop{cop_number}_col - 1;
        TRUE: cop{cop_number}_col;
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


def generate_nusmv_model_2_cop_circle(rows, columns, board, cop1_holder, cop2_holder, robber_holder):
    model_content = f'''
MODULE main
DEFINE rows:={rows}; columns:={columns};
-- new   XSB    definition
-- C      C       Cop
-- R      R       Robber
-- _      _       Floor
-- #      #       Wall

VAR
    cop1_row : 0..{rows - 1};
    cop1_col : 0..{columns - 1};
    cop2_row : 0..{rows - 1};
    cop2_col : 0..{columns - 1};
    robber_row : 0..{rows - 1};
    robber_col : 0..{columns - 1};
    movement_cop1 : {{u, d, l, r, 0}};
    movement_cop2 : {{u, d, l, r, 0}};
    movement_robber : {{u, d, l, r, 0}};
    robber_turn : boolean;
    tmp_robber_row : 0..{rows - 1};
    tmp_robber_col : 0..{columns - 1};
    tmp_cop1_row : 0..{rows - 1};
    tmp_cop1_col : 0..{columns - 1};
    tmp_cop2_row : 0..{rows - 1};
    tmp_cop2_col : 0..{columns - 1};

ASSIGN

    init(robber_turn) := FALSE;
    init(movement_cop1) := 0;
    init(movement_cop2) := 0;
    init(movement_robber) := 0;
    init(cop1_row) := {cop1_holder[0]};
    init(cop1_col) := {cop1_holder[1]};
    init(cop2_row) := {cop2_holder[0]};
    init(cop2_col) := {cop2_holder[1]};
    init(robber_row) := {robber_holder[0]};
    init(robber_col) := {robber_holder[1]};

    '''
    model_content += cop_location_change(rows, columns, 1)
    model_content += cop_location_change(rows, columns, 2)
    model_content += robber_location_change(rows, columns)
    model_content += f'''

-- Update the actual position of the robber and the cops
next(robber_row) := tmp_robber_row;
next(robber_col) := tmp_robber_col;
next(cop1_row) := tmp_cop1_row;
next(cop1_col) := tmp_cop1_col;
next(cop2_row) := tmp_cop2_row;
next(cop2_col) := tmp_cop2_col;
next(robber_turn) := !robber_turn;

-- Movement logic for cops and robber
next(movement_cop1):= 
    case
        --Circule cases (Clock direction)
        near_circle_wall & robber_touches_circle & (cop1_row - 1 >= 0) & circle_walls[cop1_row - 1][cop1_col] & (cop1_col - 1 >= 0) & !walls[cop1_row][cop1_col - 1] & robber_turn: l;  -- move left if blocked up
        near_circle_wall & robber_touches_circle & (cop1_col + 1 < columns) & circle_walls[cop1_row][cop1_col + 1] & (cop1_row - 1 >= 0) & !walls[cop1_row - 1][cop1_col] & robber_turn: u;  -- move up if blocked right
        near_circle_wall & robber_touches_circle & (cop1_row + 1 < rows) & circle_walls[cop1_row + 1][cop1_col] & (cop1_col + 1 < columns) & !walls[cop1_row][cop1_col + 1] & robber_turn: r;  -- move right if blocked down
        near_circle_wall & robber_touches_circle & (cop1_col - 1 >= 0) & circle_walls[cop1_row][cop1_col - 1] & (cop1_row + 1 < rows) & !walls[cop1_row + 1][cop1_col] & robber_turn: d;  -- move down if blocked left
        near_circle_wall & robber_touches_circle & circle_walls[cop1_row + 1][cop1_col + 1] & robber_turn & !walls[cop1_row][cop1_col + 1]: r; --move right if up left corrner
        near_circle_wall & robber_touches_circle & circle_walls[cop1_row + 1][cop1_col - 1] & robber_turn & !walls[cop1_row + 1][cop1_col]: d; --move down if up right corrner
        near_circle_wall & robber_touches_circle & circle_walls[cop1_row - 1][cop1_col - 1] & robber_turn & !walls[cop1_row][cop1_col - 1]: l; --move left if down right corrner
        near_circle_wall & robber_touches_circle & circle_walls[cop1_row - 1][cop1_col + 1] & robber_turn & !walls[cop1_row - 1][cop1_col]: u; --move up if down left corrner
        --Not circule cases
        (cop1_row > robber_row) & (manhattan_distance_cop1 > next_manhattan_distance_cop1_if_up) & !walls[cop1_row - 1][cop1_col] & robber_turn : u;
        (cop1_row < robber_row) & (manhattan_distance_cop1 > next_manhattan_distance_cop1_if_down) & !walls[cop1_row + 1][cop1_col] & robber_turn: d;
        (cop1_col > robber_col) & (manhattan_distance_cop1 > next_manhattan_distance_cop1_if_left) & !walls[cop1_row][cop1_col - 1] & robber_turn: l;
        (cop1_col < robber_col) & (manhattan_distance_cop1 > next_manhattan_distance_cop1_if_right) & !walls[cop1_row][cop1_col + 1] & robber_turn: r;        
        (cop1_row > robber_row) & (cop1_row - 1 >= 0) & walls[cop1_row - 1][cop1_col] & (cop1_col + 1 < columns) & !walls[cop1_row][cop1_col + 1] & robber_turn: r;  -- move right if blocked up
        (cop1_row > robber_row) & (cop1_row - 1 >= 0) & walls[cop1_row - 1][cop1_col] & (cop1_col - 1 >= 0) & !walls[cop1_row][cop1_col - 1] & robber_turn: l;  -- move left if blocked up
        (cop1_row < robber_row) & (cop1_row + 1 < rows) & walls[cop1_row + 1][cop1_col] & (cop1_col + 1 < columns) & !walls[cop1_row][cop1_col + 1] & robber_turn: r;  -- move right if blocked down
        (cop1_row < robber_row) & (cop1_row + 1 < rows) & walls[cop1_row + 1][cop1_col] & (cop1_col - 1 >= 0) & !walls[cop1_row][cop1_col - 1] & robber_turn: l;  -- move left if blocked down
        (cop1_col > robber_col) & (cop1_col - 1 >= 0) & walls[cop1_row][cop1_col - 1] & (cop1_row - 1 >= 0) & !walls[cop1_row - 1][cop1_col] & robber_turn: u;  -- move up if blocked left
        (cop1_col > robber_col) & (cop1_col - 1 >= 0) & walls[cop1_row][cop1_col - 1] & (cop1_row + 1 < rows) & !walls[cop1_row + 1][cop1_col] & robber_turn: d;  -- move down if blocked left
        (cop1_col < robber_col) & (cop1_col + 1 < columns) & walls[cop1_row][cop1_col + 1] & (cop1_row - 1 >= 0) & !walls[cop1_row - 1][cop1_col] & robber_turn: u;  -- move up if blocked right
        (cop1_col < robber_col) & (cop1_col + 1 < columns) & walls[cop1_row][cop1_col + 1] & (cop1_row + 1 < rows) & !walls[cop1_row + 1][cop1_col] & robber_turn: d;  -- move down if blocked right
        !robber_turn : 0;
        TRUE: movement_cop1;
    esac;

next(movement_cop2):= 
    case
        --Circule cases (Oposite of clock direction)
        near_circle_wall & robber_touches_circle & (cop2_row - 1 >= 0) & circle_walls[cop2_row - 1][cop2_col] & (cop2_col + 1 < columns) & !walls[cop2_row][cop2_col + 1] & robber_turn: r;  -- move right if blocked up
        near_circle_wall & robber_touches_circle & (cop2_col + 1 < columns) & circle_walls[cop2_row][cop2_col + 1] & (cop2_row + 1 < rows) & !walls[cop2_row + 1][cop2_col] & robber_turn: d;  -- move down if blocked right
        near_circle_wall & robber_touches_circle & (cop2_row + 1 < rows) & circle_walls[cop2_row + 1][cop2_col] & (cop2_col - 1 >= 0) & !walls[cop2_row][cop2_col - 1] & robber_turn: l;  -- move left if blocked down
        near_circle_wall & robber_touches_circle & (cop2_col - 1 >= 0) & circle_walls[cop2_row][cop2_col - 1] & (cop2_row - 1 >= 0) & !walls[cop2_row - 1][cop2_col] & robber_turn: u;  -- move up if blocked left
        near_circle_wall & robber_touches_circle & circle_walls[cop2_row + 1][cop2_col + 1] & robber_turn & !walls[cop2_row + 1][cop2_col]: d; --move down if up left corner
        near_circle_wall & robber_touches_circle & circle_walls[cop2_row + 1][cop2_col - 1] & robber_turn & !walls[cop2_row][cop2_col - 1]: l; --move left if up right corner
        near_circle_wall & robber_touches_circle & circle_walls[cop2_row - 1][cop2_col - 1] & robber_turn & !walls[cop2_row - 1][cop2_col]: u; --move up if down right corner
        near_circle_wall & robber_touches_circle & circle_walls[cop2_row - 1][cop2_col + 1] & robber_turn & !walls[cop2_row][cop2_col + 1]: r; --move right if down left corner
        --Not circule cases
        (cop2_row > robber_row) & (manhattan_distance_cop2 > next_manhattan_distance_cop2_if_up) & !walls[cop2_row - 1][cop2_col] & robber_turn : u;
        (cop2_row < robber_row) & (manhattan_distance_cop2 > next_manhattan_distance_cop2_if_down) & !walls[cop2_row + 1][cop2_col] & robber_turn: d;
        (cop2_col > robber_col) & (manhattan_distance_cop2 > next_manhattan_distance_cop2_if_left) & !walls[cop2_row][cop2_col - 1] & robber_turn: l;
        (cop2_col < robber_col) & (manhattan_distance_cop2 > next_manhattan_distance_cop2_if_right) & !walls[cop2_row][cop2_col + 1] & robber_turn: r;        
        (cop2_row > robber_row) & (cop2_row - 1 >= 0) & walls[cop2_row - 1][cop2_col] & (cop2_col + 1 < columns) & !walls[cop2_row][cop2_col + 1] & robber_turn: r;  -- move right if blocked up
        (cop2_row > robber_row) & (cop2_row - 1 >= 0) & walls[cop2_row - 1][cop2_col] & (cop2_col - 1 >= 0) & !walls[cop2_row][cop2_col - 1] & robber_turn: l;  -- move left if blocked up
        (cop2_row < robber_row) & (cop2_row + 1 < rows) & walls[cop2_row + 1][cop2_col] & (cop2_col + 1 < columns) & !walls[cop2_row][cop2_col + 1] & robber_turn: r;  -- move right if blocked down
        (cop2_row < robber_row) & (cop2_row + 1 < rows) & walls[cop2_row + 1][cop2_col] & (cop2_col - 1 >= 0) & !walls[cop2_row][cop2_col - 1] & robber_turn: l;  -- move left if blocked down
        (cop2_col > robber_col) & (cop2_col - 1 >= 0) & walls[cop2_row][cop2_col - 1] & (cop2_row - 1 >= 0) & !walls[cop2_row - 1][cop2_col] & robber_turn: u;  -- move up if blocked left
        (cop2_col > robber_col) & (cop2_col - 1 >= 0) & walls[cop2_row][cop2_col - 1] & (cop2_row + 1 < rows) & !walls[cop2_row + 1][cop2_col] & robber_turn: d;  -- move down if blocked left
        (cop2_col < robber_col) & (cop2_col + 1 < columns) & walls[cop2_row][cop2_col + 1] & (cop2_row - 1 >= 0) & !walls[cop2_row - 1][cop2_col] & robber_turn: u;  -- move up if blocked right
        (cop2_col < robber_col) & (cop2_col + 1 < columns) & walls[cop2_row][cop2_col + 1] & (cop2_row + 1 < rows) & !walls[cop2_row + 1][cop2_col] & robber_turn: d;  -- move down if blocked right

        !robber_turn : 0;
        TRUE: movement_cop2;
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

    manhattan_distance_cop1 := abs(cop1_row - tmp_robber_row) + abs(cop1_col - tmp_robber_col);
    next_manhattan_distance_cop1_if_up := abs((cop1_row - 1) - tmp_robber_row) + abs(cop1_col - tmp_robber_col);
    next_manhattan_distance_cop1_if_down := abs((cop1_row + 1) - tmp_robber_row) + abs(cop1_col - tmp_robber_col);
    next_manhattan_distance_cop1_if_left := abs(cop1_row - tmp_robber_row) + abs((cop1_col - 1) - tmp_robber_col);
    next_manhattan_distance_cop1_if_right := abs(cop1_row - tmp_robber_row) + abs((cop1_col + 1) - tmp_robber_col);

    manhattan_distance_cop2 := abs(cop2_row - tmp_robber_row) + abs(cop2_col - tmp_robber_col);
    next_manhattan_distance_cop2_if_up := abs((cop2_row - 1) - tmp_robber_row) + abs(cop2_col - tmp_robber_col);
    next_manhattan_distance_cop2_if_down := abs((cop2_row + 1) - tmp_robber_row) + abs(cop2_col - tmp_robber_col);
    next_manhattan_distance_cop2_if_left := abs(cop2_row - tmp_robber_row) + abs((cop2_col - 1) - tmp_robber_col);
    next_manhattan_distance_cop2_if_right := abs(cop2_row - tmp_robber_row) + abs((cop2_col + 1) - tmp_robber_col);

    near_circle_wall := 
        ((cop1_row < {rows - 1} & cop1_col < {columns - 1} & circle_walls[cop1_row + 1][cop1_col + 1]) | 
        (cop1_row < {rows - 1} & cop1_col > 0 & circle_walls[cop1_row + 1][cop1_col - 1]) |
        (cop1_row > 0 & cop1_col > 0 & circle_walls[cop1_row - 1][cop1_col - 1]) |
        (cop1_row > 0 & cop1_col < {columns - 1} & circle_walls[cop1_row - 1][cop1_col + 1]) |
        (cop1_row > 0 & circle_walls[cop1_row - 1][cop1_col]) | 
        (cop1_row < {rows - 1} & circle_walls[cop1_row + 1][cop1_col]) | 
        (cop1_col > 0 & circle_walls[cop1_row][cop1_col - 1]) | 
        (cop1_col < {columns - 1} & circle_walls[cop1_row][cop1_col + 1])) &
        ((cop2_row < {rows - 1} & cop2_col < {columns - 1} & circle_walls[cop2_row + 1][cop2_col + 1]) | 
        (cop2_row < {rows - 1} & cop2_col > 0 & circle_walls[cop2_row + 1][cop2_col - 1]) | 
        (cop2_row > 0 & cop2_col < {columns - 1} & circle_walls[cop2_row - 1][cop2_col + 1]) | 
        (cop2_row > 0 & cop2_col > 0 & circle_walls[cop2_row - 1][cop2_col - 1]) | 
        (cop2_row > 0 & circle_walls[cop2_row - 1][cop2_col]) | 
        (cop2_row < {rows - 1} & circle_walls[cop2_row + 1][cop2_col]) | 
        (cop2_col > 0 & circle_walls[cop2_row][cop2_col - 1]) | 
        (cop2_col < {columns - 1} & circle_walls[cop2_row][cop2_col + 1]));


    robber_touches_circle :=
        (robber_row > 0 & robber_col > 0 & circle_walls[robber_row - 1][robber_col - 1]) |  -- Top-left
        (robber_row > 0 & robber_col < {columns - 1} & circle_walls[robber_row - 1][robber_col + 1]) |  -- Top-right
        (robber_row < {rows - 1} & robber_col > 0 & circle_walls[robber_row + 1][robber_col - 1]) |  -- Bottom-left
        (robber_row < {rows - 1} & robber_col < {columns - 1} & circle_walls[robber_row + 1][robber_col + 1]) |  -- Bottom-right
        (robber_row > 0 & circle_walls[robber_row - 1][robber_col]) |  -- Top
        (robber_row < {rows - 1} & circle_walls[robber_row + 1][robber_col]) |  -- Bottom
        (robber_col > 0 & circle_walls[robber_row][robber_col - 1]) |  -- Left
        (robber_col < {columns - 1} & circle_walls[robber_row][robber_col + 1]);  -- Right
'''

    model_content += f'''
    walls :='''
    # creating the walls constant
    model_content += " [\n"
    for i in range(rows):
        model_content += "["
        for j in range(columns):
            if board[i][j] == '#' or board[i][j] == 'X':
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
    circle_walls :='''
    # creating the walls constant
    model_content += " [\n"
    for i in range(rows):
        model_content += "["
        for j in range(columns):
            if board[i][j] == 'X':
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

LTLSPEC F ((tmp_cop1_row = robber_row & tmp_cop1_col = robber_col) | (tmp_cop2_row = robber_row & tmp_cop2_col = robber_col) | (cop1_row = tmp_robber_row & cop1_col = tmp_robber_col) | (cop2_row = tmp_robber_row & cop2_col = tmp_robber_col)) --if always the cop catches the robber shows true, else false
    '''

    return model_content