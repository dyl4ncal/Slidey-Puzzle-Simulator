'''
Created on Jan. 20, 2019

@author: Dylan Calado
'''
import sys
import collections
from eightpuzzle.puzzle_board import Board
from heapq import heapify, heappush, heappop
from collections import deque


#Final goal state of the 8-Puzzle board as defined by the assignment requirements.
goal_state = [1,2,3,4,5,6,7,8,0]
initial_state = list()

#Variable used to retrace the path through the tree from the goal state to the initial state.
goal_node = Board

move_sequence = list()
actual_path_length = 0
optimal_path_length = 0
successor_nodes_visited = 0   

#Prints the main menu.
def print_menu():
    print("""\n---------8_Puzzle Solver: Main Menu---------      
\n1. Set Initial 8-Puzzle State
2. Solve with Breadth First Search Algorithm
3. Solve with Best First Search Algorithm
4. Solve with A* Search Algorithm
5. Terminate Program\n""")

#Prints the menu for the user to select a heuristic function.
def select_heuristic_function():
    heuristic = input("""\n----Heuristic functions----\n
1. Tiles Out of Place
2. Manhattan Distance
3. My Custom Heuristic
\nSelect one of the above heuristic functions (1-3): """)
    
    if heuristic == "1":
        return "TilesOutOfPlace"
    elif heuristic == "2":
        return "ManhattanDistance"
    elif heuristic == "3":
        return "CustomHeuristic"
    else:
        print("Error: Invalid Input. You can only select option (1-3).")
        execute_program_loop()

#Main user interface logic.
def execute_program_loop():
    global initial_state    
        
    while True:
        print_menu()
        
        selected_option = input("Enter an option (1-5): ")

        if selected_option == "1":
            set_initial_state()
            
        elif selected_option == "2":
            if len(initial_state) == 0:
                set_initial_state()
            else:
                breadth_first_search(initial_state)
                output_results_to_console()
                
        elif selected_option == "3":
            if len(initial_state) == 0:
                set_initial_state()
            else:
                heuristic_function = select_heuristic_function()
                greedy_best_first_search(initial_state, heuristic_function)
                
        elif selected_option == "4":
            if len(initial_state) == 0:
                set_initial_state()
            else:
                heuristic_function = select_heuristic_function()
                a_star_search(initial_state, heuristic_function)           
            
        elif selected_option == "5":
            sys.exit(0)
        else:
            print("Error: Invalid Input. You can only select option (1-5).")

#Allows the user to set the puzzle's initial state and also checks if the state is valid.     
def set_initial_state():
    global initial_state, optimal_path_length
    sequence_string = input("\nEnter 8-Puzzle initial state (e.g. 235146078): ")
        
    #Assume initial state is valid and then check constraints.
    valid_initial_state = True
    optimal_path_length = 0
        
    #Checks input string for any repeated numbers.
    repeated_num_counter = collections.Counter(sequence_string)
    is_repeating_num = False
    for i in repeated_num_counter:
        if repeated_num_counter[i] > 1:
            is_repeating_num = True
        
    #Checks several conditions to make sure initial state is valid.
    is_in_range = True
    for i in range(len(sequence_string)):
        if sequence_string[i] == "9":
            is_in_range = False
            
    if is_repeating_num or not(is_in_range) or sequence_string.__len__() > 9 or len(sequence_string) < 9:
        valid_initial_state = False 
        
    if valid_initial_state:
        #Convert string input to list of integers.
        sequence_string = list(sequence_string)
        sequence_string = list(map(int, sequence_string))
        initial_state = sequence_string
        #Use BFS to determine if initial state entered is solvable. 
        is_solvable = breadth_first_search(initial_state)
        if is_solvable == 0:
            print("\nPuzzle is unsolvable.")
            set_initial_state()
            return 0
        else:
            print("\nSaving initial state entered as...", initial_state) 
    else:
        print("\nInput Error: You must enter each number in the range [0,8] exactly once.")
        set_initial_state()
      
#Performs Breadth First Search algorithm.  
def breadth_first_search(init_state):
    global goal_node, successor_nodes_visited, optimal_path_length
    
    successor_nodes_visited = 0
    open_list =  deque([Board(None, init_state, None, 0, 0)])
    closed_list = set()
    
    #Loop until open_list is empty.
    while open_list:
        
        current = open_list.popleft()

        closed_list.add(current.map)

        if current.board_state == goal_state:
            goal_node = current
            
            #BFS finds the optimal path length.
            optimal_path_length = len(generate_solution_path())
            actual_path_length = 0
            move_sequence.clear()            
            return open_list

        layer_n_nodes = get_children(current)

        for next_layer_n_node in layer_n_nodes:
            
            #If node hasn't been explored yet, add it to the open list.
            if next_layer_n_node.map not in closed_list:
                open_list.append(next_layer_n_node)
                closed_list.add(next_layer_n_node.map)
                
        if len(open_list) > successor_nodes_visited:
            successor_nodes_visited = len(open_list)  
    
    #If open_list becomes empty, no solution was found and puzzle is unsolvable.
    return 0
     
#Performs Greedy Best First Search algorithm.    
def greedy_best_first_search(init_state, heuristic):
    global goal_node, successor_nodes_visited
    
    successor_nodes_visited = 0
    open_list = list()
    closed_list = list()
    
    #Determine user's selected heuristic function then get heuristic value based on initial state.
    if heuristic == "TilesOutOfPlace":
        heuristic_val = tiles_out_of_place(init_state)
    elif heuristic == "ManhattanDistance":
        heuristic_val = manhattan_distance(init_state)
    elif heuristic == "CustomHeuristic":
        heuristic_val = my_custom_heuristic(init_state)
    
    heappush(open_list,(heuristic_val, Board(None, init_state, None, 0, 0)))
    
    #Loop until open_list is empty.
    while open_list:
        #Get board from (heuristic, board) tuple from priority queue.
        current_tuple = heappop(open_list)
        current_board = current_tuple[1]

        if current_board.board_state == goal_state:
            goal_node = current_board
            output_results_to_console()
            return open_list
        elif current_board.map not in closed_list:
            closed_list.append(current_board.map)
            successor_nodes = get_children(current_board)
            while successor_nodes:
                child = successor_nodes.pop(0)
                
                if heuristic == "TilesOutOfPlace":
                    heuristic_val = tiles_out_of_place(child.board_state)
                elif heuristic == "ManhattanDistance":
                    heuristic_val = manhattan_distance(child.board_state)
                elif heuristic == "CustomHeuristic":
                    heuristic_val = my_custom_heuristic(child.board_state)
   
                heappush(open_list, (heuristic_val, child))
                heapify(open_list)
                
        if len(open_list) > successor_nodes_visited:
            successor_nodes_visited = len(open_list)

#Performs A* Search algorithm.    
def a_star_search(init_state, heuristic):
    global goal_node, successor_nodes_visited
    
    successor_nodes_visited = 0
    open_list = list()
    closed_list = set()
    
    if heuristic == "TilesOutOfPlace":
        score = tiles_out_of_place(init_state)
    elif heuristic == "ManhattanDistance":
        score = manhattan_distance(init_state)
    elif heuristic == "CustomHeuristic":
        score = my_custom_heuristic(init_state)

    initial_board = Board(None, init_state, None, score, 0)

    #This is a tuple to go into item dictionary.
    #Score is the dictionary key and actions and boards are the values.
    current = (score, initial_board, 0)
    heappush(open_list, current)

    item = {}
    item[initial_board.map] = current

    while open_list:
        board = heappop(open_list)
        closed_list.add(board[1].map)

        if board[1].board_state == goal_state:
            goal_node = board[1]
            output_results_to_console()
            return open_list

        children = get_children(board[1])

        for child in children:
            if heuristic == "TilesOutOfPlace":
                h = tiles_out_of_place(child.board_state)
            elif heuristic == "ManhattanDistance":
                h = manhattan_distance(child.board_state)
            elif heuristic == "CustomHeuristic":
                h = my_custom_heuristic(child.board_state)
                
            #Calculates f(n) = h(n) + g(n).
            child.score = h + child.path_cost
            current = (child.score, child, child.action)

            #Logic to avoid redundant nodes that don't need to be searched.
            if child.map not in closed_list:
                heappush(open_list, current)
                closed_list.add(child.map)
                item[child.map] = current
            elif item[child.map][1].score > child.score and child.map in item:
                chosen_node = open_list.index((item[child.map][1].score, item[child.map][1], item[child.map][1].action))

                open_list[int(chosen_node)] = current
                item[child.map] = current
                heapify(open_list)
                
        if len(open_list) > successor_nodes_visited:
            successor_nodes_visited = len(open_list)
            
#Heuristic which counts the number of out of place tiles.
def tiles_out_of_place(current_state):
    heuristic_value = 0
    for i in range(9):
        if i+1 != current_state[i]:
            heuristic_value = heuristic_value + 1
    
    return heuristic_value

#Heuristic to calculate total Manhattan Distance of a particular state.
#Use division to get Manhattan Distance for horizontal movements.
#Use modulo to get Manhattan Distance for vertical movements.
#Use abs() to always get a positive heuristic value and then sum together all the distances.
def manhattan_distance(current_state):
    heuristic_value = sum(abs(index_current // 3 - index_goal // 3) + abs(index_current % 3 - index_goal % 3)
        for index_current, index_goal in ((current_state.index(i), goal_state.index(i)) for i in range(1, 9)))
    return heuristic_value

#My custom heuristic (which combines Manhattan Distance and Tiles Out of Place) 
def my_custom_heuristic(current_state):  
    
    #Heuristic number 1 is out of place tiles.  
    heuristic_value_1 = 0
    for i in range(9):
        if i+1 != current_state[i]:
            heuristic_value_1 = heuristic_value_1 + 1
     
    #Heuristic number 2 is Manhattan Distance. 
    heuristic_value_2 = 0        
    heuristic_value_2 = sum(abs(index_current // 3 - index_goal // 3) + abs(index_current % 3 - index_goal % 3)
        for index_current, index_goal in ((current_state.index(i), goal_state.index(i)) for i in range(1, 9)))
    
    heuristic_value_final = max(heuristic_value_1, heuristic_value_2)
    
    #Code to output which heuristic the function uses at each decision.
    #Can leave this commented out for normal program use.
    '''if heuristic_value_final == heuristic_value_1:
        print("Used heuristic 1")
    elif heuristic_value_final == heuristic_value_2:
        print("Used heuristic 2")'''   
    
    return heuristic_value_final
    
#Function to action the zero position around the board.
def move_zero_space(board_state, move_direction_code):
    state_update = board_state[:]
    position = state_update.index(0)
    
    #Zero position moves left (if it is a legal action).
    if move_direction_code == 'L':  
        if position not in range(0, 9, 3):
            new_position = state_update[position - 1]
            state_update[position - 1] = state_update[position]
            state_update[position] = new_position
            return state_update
        else:
            return None

    #Zero position moves right (if it is a legal action).
    if move_direction_code == 'R':
        if position not in range(2, 9, 3):
            new_position = state_update[position + 1]
            state_update[position + 1] = state_update[position]
            state_update[position] = new_position
            return state_update
        else:
            return None
        
    #Zero position moves up (if it is a legal action).
    if move_direction_code == 'U':
        if position not in range(0, 3):
            new_position = state_update[position - 3]
            state_update[position - 3] = state_update[position]
            state_update[position] = new_position
            return state_update
        else:
            return None

    #Zero position moves down (if it is a legal action).
    if move_direction_code == 'D':
        if position not in range(6, 9):
            new_position = state_update[position + 3]
            state_update[position + 3] = state_update[position]
            state_update[position] = new_position
            return state_update
        else:
            return None
    
#Function to return a list of the neighboring, or children, nodes.
def get_children(node):
    #global nodes_expanded
    #nodes_expanded += 1
    list_layer_n_nodes = list()

    #Creates the children nodes that could possibly be generated by moving the empty space left, right, up, or down (if the action is legal).
    #If one of the below moves is illegal, the None type is appended to the children list. 
    #Child created by moving zero position left.
    list_layer_n_nodes.append(Board(node, move_zero_space(node.board_state, 'L'), 'L', 0, node.path_cost+1))
    
    #Child created by moving zero position right.
    list_layer_n_nodes.append(Board(node, move_zero_space(node.board_state, 'R'), 'R', 0, node.path_cost+1))
    
    #Child created by moving zero position up.
    list_layer_n_nodes.append(Board(node, move_zero_space(node.board_state, 'U'), 'U', 0, node.path_cost+1))
    
    #Child created by moving zero position down.
    list_layer_n_nodes.append(Board(node, move_zero_space(node.board_state, 'D'), 'D', 0, node.path_cost+1))

    children_nodes = [layer_n_node for layer_n_node in list_layer_n_nodes if layer_n_node.board_state]

    return children_nodes

#Retraces the path taken from the starting node to the goal node (for output).
def generate_solution_path():
    global actual_path_length, goal_node, initial_state, move_sequence
    
    current = goal_node

    while current.board_state != initial_state:

        if current.action == 'L':
            movement = 'Left'
        elif current.action == 'R':
            movement = 'Right'
        elif current.action == 'U':
            movement = 'Up'
        elif current.action == 'D':
            movement = 'Down'
        
        current = current.parent_node
        move_sequence.insert(0, movement)
         
    actual_path_length = len(move_sequence)

    return move_sequence

#Prints some data about how efficiently the puzzle was solved.
def output_results_to_console():
    global move_sequence, actual_path_length, optimal_path_length, successor_nodes_visited
    
    move_sequence = generate_solution_path()
    print("\nPuzzle solved!\n")
    print("Empty space action sequence: ", move_sequence)
    print("Length of moves: ", actual_path_length)
    print("Optimal Path Length: ", optimal_path_length)
    print("Total successor nodes visited: ", successor_nodes_visited)
    
    #Reset outcome variables.
    move_sequence.clear()
    actual_path_length = 0
    successor_nodes_visited = 0
        
#Begin running the program by calling the execute_program_loop() function.
if __name__ == "__main__":
    execute_program_loop()
        
