'''
Created on Jan. 20, 2019

@author: Dylan Calado
'''

class Board:

    def __init__(self, parent, board_state, action, score, path_cost):
        self.parent_node = parent
        self.board_state = board_state
        self.action = action
        self.score = score
        self.path_cost = path_cost
        
        #Define "map" format for board objects.
        if self.board_state:
            self.map = ''.join(str(tile) for tile in self.board_state)
            
    #Override "greater than" method to define it in terms of 8-Puzzle boards.
    def __gt__(self, compare):
        return self.map > compare.map

    #Override "equals" method to define it in terms of 8-Puzzle boards.
    def __eq__(self, compare):
        return self.map == compare.map
