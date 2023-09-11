from enum import Enum


class AgentType(Enum):
    CREATIVE = 'creative'
    SUPPORTIVE = 'supportive'


class Agent():
    # FIELDS:
    # creativity - float
    # openness

    def __init__(self, creativity = 0, openness = 0):
        self.creativity = creativity
        self.openness = openness

    def add_creativity(self, crea):
        self.creativity += crea
        if self.creativity < 0:
            self.creativity = 0
        elif self.creativity > 1:
            self.creativity = 1

    def add_openness(self, open):
        self.openness += open
        if self.openness < 0:
            self.openness = 0
        elif self.openness > 1:
            self.openness = 1