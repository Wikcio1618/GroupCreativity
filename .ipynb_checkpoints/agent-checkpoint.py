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