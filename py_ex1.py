from World_State import World_State
from collections import deque
import time
from random import randint
import sys
from heapq import heappush, heappop, heapify

configuration=list()

Errors_Messages = {
    "OF": "Open File",
    "BS": "Board Size"
}

_expande_states = 0


def State_By_Operate(_state, operate, _board):
    """
        Manage the operates of the board, correspond to 8puzzle game

        _state = current state,
         operate = the operator which led to current state,
        _board = game board 
    """
    successor = _state [:]
    index_of_zero = successor.index(0)
    size = _board.board_size
    fullSize = _board.board_full_size

    if operate == "Up":
        if index_of_zero not in range(fullSize - size, fullSize):
            val = successor[index_of_zero + size]
            successor[index_of_zero + size] = successor [index_of_zero]
            successor [index_of_zero] = val
            
            return successor
        else:
            return None
    if operate == "Down":
        if index_of_zero not in range(0, size):
            val = successor[index_of_zero - size]
            successor[index_of_zero - size] = successor [index_of_zero]
            successor [index_of_zero] = val

            return successor
        else:
            return None
    if operate == "Left":
        if index_of_zero not in range(size - 1, fullSize, size):
            val = successor[index_of_zero + 1]
            successor[index_of_zero + 1] = successor [index_of_zero]
            successor[index_of_zero] = val

            return successor
        else:
            return None
    if operate == "Right":
        if index_of_zero not in range(0, fullSize, size):
            val = successor[index_of_zero - 1]
            successor[index_of_zero - 1] = successor [index_of_zero]
            successor[index_of_zero] = val

            return successor
        else:
            return None

def ExtendStateToSuccessors(_state, _board):
    """
        Function to evolving the successors of current state

        _state = current state,
        _board = game board 
    """
    _successors = list()

    _successors.append(World_State(State_By_Operate(_state.state, "Up", _board), "Up", _state, _state.depth + 1, 0))
    _successors.append(World_State(State_By_Operate(_state.state, "Down", _board), "Down", _state, _state.depth + 1, 0))
    _successors.append(World_State(State_By_Operate(_state.state, "Left", _board), "Left", _state, _state.depth + 1, 0))
    _successors.append(World_State(State_By_Operate(_state.state, "Right", _board), "Right", _state, _state.depth + 1, 0))

    _successors_list = [s for s in _successors if s.state]

    return _successors_list

def Manhaten_Distance(_board):
    """
        Function simulates manhatem distance
        between same squares - one at the original
        side and ther other at the target side

        _board = game board
    """
    sum = 0

    for square in range(1, _board.board_full_size):
        src_pos = _board.board_state.state.index(square)
        dest_pos = _board.goal_state.state.index(square)

        sum += abs(src_pos % _board.board_size - dest_pos % _board.board_size) + abs(src_pos // _board.board_size - dest_pos // _board.board_size)
    
    return sum


def DLS(_state, _board, _depth):
    """
        Calculate DFS iterative

        _state = current state,
        _board = game board,
        _depth = max depth
    """
    global _expande_states
    current = _state

    if current == _board.goal_state:
        return current
    if _depth <= 0:
        return None
    
    successors = ExtendStateToSuccessors(current, _board)
    _expande_states += len(successors)

    for successor in successors:
         result = DLS(successor, _board, _depth - 1)
         if result is not None:
             return result

def IDS(_board):
    """
        Implement IDS algorithm

        _board = game board
    """
    _max_depth = 0
    while True:
        state = DLS(_board.board_state, _board, _max_depth)
        if state is not None:
            return _max_depth, state
        _max_depth += 1


def BFS(board):
    """
        Implement BFS algorithm

        board = game board
    """
    goal = board.goal_state
    global _expande_states

    try:
        open_list= deque([board.board_state])
    except Exception as inst:
        print(inst)

    while open_list:
        state = open_list.popleft()
        _expande_states += 1
        if state == goal:
            return 0, state
        
        successors = ExtendStateToSuccessors(state, board)

        for successor in successors:
            if successor not in open_list:
                open_list.append(successor)
        


def AStar(board):
    """
        Implement A* algorithm

        board = game board
    """
    global _expande_states

    open_list = list()

    heappush(open_list, board.board_state)                        

    while open_list:

        current = heappop(open_list)

        if current == board.goal_state:
            return current.depth, current

        successors = ExtendStateToSuccessors(current, board)
        _expande_states += len(successors)

        for successor in successors:
            board.board_state = successor
            successor.f_value = Manhaten_Distance(board) + successor.depth
            heappush(open_list, successor)
        
    return None    



def Routing_To_Goal_State(initial_State, final_state):
    """
        Recorvering the path from goal state to initial state

        initial_State = initial state,
        final_state = goal state
    """
    state = final_state

    operatores = list()

    while initial_State != state:

        move= final_state.operator

        if move == "Up":
            operatores.insert(0, "U")
        elif move == "Down":
            operatores.insert(0, "D")
        elif move == "Left":
            operatores.insert(0, "L")
        else:
            operatores.insert(0, "R")
        
        state = state.parent
    
    return operatores
        

#Presenting all algorithms which are available 
algorithms = {
    1: IDS,
    2: BFS,
    3: AStar
    }      

def ExtractFileConfiguration():
    """
        Extract information from file,
        like: algorithm, board size, initial state
    """  

    with open("input.txt",'r') as fhandle:
        configuration.append(fhandle.readline()[:-1])
        configuration.append(fhandle.readline()[:-1])
        configuration.append(fhandle.readline())

    for i in range(0,len(configuration)-1):
        configuration[i]=int(configuration[i])

    configuration[-1] = str(configuration[-1]).split('-')

    configuration[-1] = list(int(i) for i in  configuration[-1])

def ExportFile(export_file):
    """
    Exporting information to output file,
    like: path to target, num of vertices expended, cost of path

    export_file = information to export
    """

    with open("output.txt",'a') as fhandle:
        fhandle.write("%s " %str(export_file["Path"]))
        fhandle.write("%s " % str(export_file["Expended Vertexes"]))
        fhandle.write("%s" % str(export_file["Algo profit"]))

class Board:
    """
        Class describes board

        init_state = initial state,
        board_state = current state on board,
        board_size = board is N*N so it's - N,
        board_full_size = board size N*N,
        goal_state = target state    
    """
    def __init__(self, _init_state, _size):
        self.init_state = World_State(_init_state,None,None,0,0)
        self.board_state = self.init_state
        self.board_size = _size
        self.board_full_size = _size ** 2
        _goal_state=set()
        
        while True:
            if len(_goal_state) >= self.board_full_size - 1:
                break
            _goal_state.add(randint(1,self.board_full_size-1))
        
        _goal_state = list(_goal_state)

        _goal_state.append(0)

        self.goal_state =  World_State(_goal_state,None,None,0,0)

    def _checkBoardSize(self):
        if self.board_full_size != len(self.board_state.state):
            print("Error: {}".format(Errors_Messages["BS"]))
            return None

class Game:
    """
        Class describes game

         algo = algorithm to evaluate,
        _board = game board
    """
    def __init__(self,_algo,_board):
        self.algo=algorithms[_algo]
        self.board=_board    

    def RunAlgo(self):

        algo_profit, final_state = self.algo(self.board)
        operators = Routing_To_Goal_State(self.board.init_state, final_state)
        str_operators = ''.join(str(s) for s in operators)
        export_file = {"Path": str_operators, "Expended Vertexes": _expande_states, "Algo profit": algo_profit}
        ExportFile(export_file)

def RunGame():
     """
        Run the game
     """
     ExtractFileConfiguration()
     board=Board(configuration[2],configuration[1])
     game=Game(configuration[0],board)
     game.RunAlgo()



def main():
    RunGame()

if __name__ == "__main__":
    main()

