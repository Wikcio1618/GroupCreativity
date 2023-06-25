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

    def __init__(self, type: AgentType, init_step:tuple, space_size:int, position=0):
        self.type = type
        self.space_size=space_size
        if type == AgentType.CONSERVATIVE:
            self.step = init_step[0]
        elif type == AgentType.CREATIVE:
            print(init_step[0])
            print(init_step[1])
            self.step = init_step[1]
        self.position = position

    def move_random(self):
        _chance = uniform(0,1)
        if _chance < 0.5:
            self.position -= self.step
            if self.position < 0:
                self.position += self.space_size
        else:
            self.position += self.step
            if self.position >= self.space_size:
                self.position -= self.space_size

    def give_zeal(self):
        pass

    def cool_down(self):
        pass

    def set_position(self, position:int):
        self.position=position