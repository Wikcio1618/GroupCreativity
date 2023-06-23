from math import sqrt
from numpy import array
from random import randint

from agent import Agent, AgentType

class Society():
    # -- GAME PARAMS -- #
    # space size 
    SPACE_SIZE = 100 
    # agents to space ratio
    AGENTS_DENSITY = 0.3
    # number of agents
    NUM_OF_AGENTS = int(SPACE_SIZE * AGENTS_DENSITY)
    # range of interaction
    RANGE = 4
    # interaction power (how much is range increased)
    FIELD_FORCE = 1
    # initial steps of agents (conservative, creative)
    INIT_STEP = (1, 3)
    # density of creative agents
    CREATIVE_DENSITY = 0.5
    # starting postition of agents - random or beginning
    POSITIONING_TYPE = 'random'

    # FIELDS:
    # agents - array of agents
    # targets - positions to be taken (set of ints) 


    def __init__(self):
        # create creative and conservative agents according to CREATIVE_DENSITY; position them
        self.agents = array(
            [
            Agent(type=AgentType.CONSERVATIVE, init_step=self.INIT_STEP) 
            for _ in range(self.NUM_OF_AGENTS)
            ])
        for i in range(int(self.CREATIVE_DENSITY * self.NUM_OF_AGENTS)):
            self.agents[i].type = AgentType.CREATIVE
        
        if self.POSITIONING_TYPE == 'random':
            for i in range(self.NUM_OF_AGENTS):
                self.agents[i].set_position(randint(0, self.SPACE_SIZE))
        elif self.POSITIONING_TYPE == 'beginnig':
            for i in range(self.NUM_OF_AGENTS):
                self.agents[i].set_position(0)

        for i in range(int(self.CREATIVE_DENSITY * self.NUM_OF_AGENTS)):
            self.agents[i].type = AgentType.CREATIVE

        # choose target positions randomly
        self.targets = set([])
        while len(self.targets < self.NUM_OF_AGENTS):
            self.targets.add(randint(0, self.SPACE_SIZE))
        

    def calculate_feedback(self):
        feedback_squared = 0
        for agent in self.agents:
            _step = 0
            nearest_target = 0
            while True:
                if agent.position + _step in self.targets:
                    nearest_target = agent.position + _step
                    break
                elif agent.position - _step in self.targets:
                    nearest_target = agent.position - _step
                    break
                _step += 1
            feedback += (agent.position - nearest_target) ** 2
        return sqrt(feedback_squared)


