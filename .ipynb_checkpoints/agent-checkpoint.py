from enum import Enum
from random import uniform


class AgentType(Enum):
    CONSERVATIVE = 'conservative'
    CREATIVE = 'creative'

class Agent():
    # FIELDS:
    # type (enum)
    # prob (of moving right)
    # position (in 1D its int)

    def __init__(self, type: AgentType, space_size:int, step = 1, prob = 0.5, position=0):
        self.type = type
        self.space_size=space_size
        self.position = position
        self.step = step
        self.prob = prob

    def move_random(self):
        _chance = uniform(0,1)
        if _chance < (1 - self.prob):
            self.position -= self.step
            while self.position < 0:
                self.position += self.space_size
        else:
            self.position += self.step
            while self.position >= self.space_size:
                self.position -= self.space_size

    def shift_right(self, force:float):
        self.prob += force
        if self.prob > 1:
            self.prob = 1

    def cool_down(self, force:float):
        self.prob -= force
        if self.prob < 0.5:
            self.prob = 0.5

    def set_position(self, position:int):
        self.position=position