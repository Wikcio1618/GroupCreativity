from enum import Enum
from random import uniform

class AgentType(Enum):
    CONSERVATIVE = 'conservative'
    CREATIVE = 'creative'

class Agent():
    # FIELDS:
    # type (enum)
    # step (next step range)
    # position (in 1D its int)

    def __init__(self, type: AgentType, init_step:tuple, position=0):
        self.type = type
        if type == AgentType.CONSERVATIVE:
            self.range = init_step[0]
        elif type == AgentType.CREATIVE:
            self.range = init_step[1]
        self.position = position

    def move_random(self):
        _chance = uniform(0,1)
        if _chance < 0.5:
            self.position -= self.range
        else:
            self.position += self.range

    def give_zeal(self):
        pass

    def cool_down(self):
        pass

    def set_position(self, position:int):
        self.position=position