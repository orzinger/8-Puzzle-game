

class World_State:
    """
        Class describes world state

        state = world state,
        operator = operator which led to this state
        parent = parent of the state
        depth = depth from root of the state
        f_value = sum of g(x)+h(x) for A* algorithm

        __eq__ = function to compare two states
        __lt__ = function to compare which state is larger then the other one
    """
    def __init__(self, _state, _operate, _parent, _depth, _f_value):
        self.state = _state
        self.operator = _operate
        self.parent =_parent
        self.depth = _depth
        self.f_value = _f_value
    
    def __eq__(self, other):

        return self.state == other.state
    
    def __lt__(self, other):
        return self.f_value < other.f_value

    