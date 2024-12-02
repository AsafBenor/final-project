# Project Name

## Description
This project represents the final project for the Computer Engineering degree by Asaf Benor and Yontan Kupfer. The focus is on applying formal verification methods to analyze winning strategies in a cops and robbers chasing game.

The project demonstrates how formal verification techniques can be utilized to:
- Verify different strategies in the cops and robbers game
- Determine winning conditions for the cops
- Analyze game scenarios through formal methods

For a comprehensive understanding of the theoretical background, methodology, and detailed project analysis, please refer to the complete project book.

*Note: This work was completed as part of a Bachelor's degree in Computer Engineering.*

## Project Structure
### Files Overview
### Files Overview
- `nuxmv_run.py`: Main orchestration file that handles running NuXMV model checker. Manages game board initialization, model file creation, executing NuXMV, and parsing results for both one-cop and two-cops scenarios. Also includes visualization functionality.

- `modelGeneration2.py`: Generates the NuXMV model code for the single cop scenario. Defines the formal verification model including state variables, transitions, movement logic, and winning conditions for a single cop chasing the robber.

- `modelGeneration_2_cops.py`: Generates the NuXMV model code for the two cops scenario. Similar to modelGeneration2.py but includes more complex movement strategies and coordination logic for two cops chasing the robber, including special circle-based movement patterns.

- `simulator.py`: A standalone interactive simulation of the cops and robber game with Pygame. Allows manual control of the robber while cops move automatically, featuring special circle-based movement patterns and standard chase strategies.

- `output_simulator.py`: Visualization component that animates the game moves received from the NuXMV model checker's output. Creates a visual replay of the verification results using Pygame.

- `nuXmv-2.0.0-win64/`: Directory containing the NuXMV model checker binary and supporting files:
- `bin/`: Contains the NuXMV executable and generated SMV model files (`cop_robber_1_cop.smv` and `cop_robber_2_cops.smv`) that define the formal verification models.

- `node.py`: Defines the Node class that represents a game state in the graph-based approach. Each node contains positions of the robber and policeman, plus whose turn it is, with support for equality comparisons and hashing.

- `graph.py`: Implements the graph structure and game state analysis. Creates a graph of all possible game states and includes algorithms to find winning states using a backward-search approach from capture positions.

- `checker.py`: Main script for the graph-based analysis approach. Handles graph generation, saving/loading states, and provides an interactive interface to check specific game states and simulate gameplay from them.
  
  

## Setup and Configuration

### Part 1: NuXMV Model Checking
The main executable file for this part is `nuxmv_run.py`. Two key configurations are required before running:

#### 1. NuXMV Engine Selection
Three different engines are available in the SMV file:

1. BDD (Binary Decision Diagrams) - Lines 56-72
2. SAT (Boolean Satisfiability) - Lines 74-91
3. Default (BDD-based) - Lines 92-102

BDD and SAT are different approaches to model checking - BDD represents the state space as a compact decision diagram and is generally better for systems with many variables, while SAT converts the problem to a boolean satisfaction problem and can be more efficient for certain types of verification tasks.

To select an engine:
- Uncomment the section for your chosen engine
- Comment out the other two sections
- For SAT engine: Specify a bound limitation value in the configuration

Example: To use SAT engine, uncomment lines 74-91 and comment lines 56-72 and 92-102.

#### 2. Board Configuration
Two different board variables can be configured:
- For single cop scenario: Modify `board` variable on line 292
- For two cops scenario: Modify `board_2_cops` variable on line 317
- #### Board Configuration Rules
For all cases, board symbols:
- Empty cell: `_`
- Wall: `#`

#### 1. NuXMV Model Checking (nuxmv_run.py)
Single Cop Board (line 292):
- Cop: `C`
- Robber: `R`

Two Cops Board (line 317):
- First Cop: `C1`
- Second Cop: `C2`
- Robber: `R`
- Special Circle Wall: `X`

### Part 2: Interactive Simulator (simulator.py)
Configure board variable on line 26:
- Uses same symbols as NuXMV boards
- Control robber with WASD keys
- Cops follow verified strategies

### Part 3: Graph Algorithm (checker.py)
Configure board variable on line 182:
- Only wall positions needed
- Use `#` for walls

### Example of valid board configurations:

# Single cop board example (nuxmv_run.py)
board = [
   ['#', '#', '#', '#', '#'],
   ['#', 'R', '_', '_', '#'],
   ['#', '_', 'C', '_', '#'],
   ['#', '_', '_', '_', '#'],
   ['#', '#', '#', '#', '#']
]

### Two cops board example (nuxmv_run.py)
board_2_cops = [
   ['#', '#', '#', '#', '#'],
   ['#', 'C1', 'C2', '_', '#'],
   ['#', '_', 'X', 'X', '#'],
   ['#', '_', 'X', 'X', '#'],
   ['#', '_', '_', 'R', '#'],
   ['#', '#', '#', '#', '#']
]

# Checker board example (checker.py)
board = [
   '#####',
   '#___#',
   '#___#',
   '#####'
] 

## Running and Results

### Part 1: NuXMV Model Checking
After completing the necessary configurations, we can proceed to run the model checking component. The cops in this model follow a strategy of reducing their Manhattan distance from the robber. However, when both cops and the robber are near a circle wall (circle case), the cops employ a special strategy - one cop moves clockwise while the other moves counterclockwise around the circle. This strategy increases their chances of catching the robber and prevents an endless chase scenario where the robber could continuously circle around in the same direction.

To run this part, execute the `nuxmv_run.py` file. You'll be prompted to choose between the 1-cop or 2-cops version. Make sure you've defined the correct board configuration beforehand. The script will generate an SMV file in the `nuXmv-2.0.0-win64\bin` directory.

There are three possible outcomes from the model checking:
1. If the cops can catch the robber at some point, the specification returns as true and the process ends.
2. When using the SAT engine, if no counter-example is found within your chosen bound limit, it will indicate this result.
3. If the robber has a winning strategy (creating an endless chase), the system displays a GUI simulation of the chase while simultaneously showing the SMV output in the terminal, including the directional movements of each actor.

### Part 2: Interactive Simulator
The Interactive Simulator allows you to manually play as the robber and test the cops' behavior under the established rules. Run `simulator.py` to start the game. You control the robber using the keyboard:
- 'a' key: move left
- 's' key: move down
- 'd' key: move right
- 'w' key: move up

This simulator provides a hands-on way to understand and verify the cops' behavior under the rules set in the model checking component. You can also examine the circle case by defining circle walls as specified in the configuration section.

### Part 3: Graph Algorithm
The Graph Algorithm component offers a different analytical approach. After configuring the board, the system generates or updates a `graph_data.pkl` file - a pickle file containing all possible state positions for both cop and robber on your defined board. The system reports the total number of winning states (positions where the cop catches the robber).

When you run the program, it asks if you want to play an interactive game. If you choose to play, you'll need to input the initial positions for both the robber and the cop. The game board appears, and you can control the robber using A, S, D, W keys. In this version, the cop employs a different strategy from the NuXMV model checking - it attempts to reach the nearest winning state using the shortest path available in the graph. When the cop successfully captures the robber, the game ends with a "robber caught" message.
