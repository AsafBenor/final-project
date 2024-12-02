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
