'''
Created on Jan. 26, 2019

@author: Dylan
'''

class Board:

    def __init__(self, parent, board_state, action, score, path_cost):
        self.parent_node = parent
        self.board_state = board_state
        self.action = action
        self.score = score
        self.path_cost = path_cost

        if self.board_state:
            self.map = ''.join(str(e) for e in self.board_state)

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map
