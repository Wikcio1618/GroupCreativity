from math import floor, sqrt
from numpy import array
from random import randint

from agent import Agent, AgentType

class Society:
    # -- GAME PARAMS -- #
    # space size 
    space_size = 50
    # agents to space ratio
    agents_density = 0.3
    # range of interaction
    range = 4
    # interaction power (how much is range increased)
    field_force = 1
    # initial steps of agents (conservative, creative)
    init_step = (1,3)
    # density of creative agents
    creative_density = 0.5
    # starting postition of agents - random or beginning
    positioning_type = "random"

    # FIELDS:
    # agents - array of agents
    # targets - positions to be taken (set of ints) 

    @classmethod
    def new_society(self, space_size=50, agents_density=0.3, creative_density=0.5, field_range=4, field_force=1, init_step=(1,3), positioning_type='random'):
        self.space_size=space_size
        self.agents_density=agents_density
        self.creative_density=creative_density
        self.field_range=field_range
        self.field_force=field_force
        self.init_step=init_step
        self.positioning_type=positioning_type
        self.num_of_agents=int(self.space_size*self.agents_density)

        # create creative and conservative agents according to CREATIVE_DENSITY; position them
        self.agents = array(
            [
            Agent(type=AgentType.CONSERVATIVE, init_step=init_step) 
            for _ in range(self.num_of_agents)
            ])
        for i in range(floor(self.creative_density * self.num_of_agents)):
            self.agents[i].type = AgentType.CREATIVE
        
        if self.positioning_type == 'random':
            for i in range(self.num_of_agents):
                self.agents[i].set_position(randint(0, self.space_size-1))
        elif self.positioning_type == 'beginnig':
            for i in range(self.num_of_agents):
                self.agents[i].set_position(0)

        for i in range(floor(self.creative_density * self.num_of_agents)):
            self.agents[i].type = AgentType.CREATIVE

        # choose target positions randomly
        self.targets = set([])
        while len(self.targets) < self.num_of_agents:
            self.targets.add(randint(0, self.space_size-1))

    @classmethod 
    def next_step(self):
        pass

    @classmethod
    def calculate_feedback(self):
        feedback_squared = 0
        for agent in self.agents:
            distance = 0
            while True:
                if agent.position + distance in self.targets:
                    break
                elif agent.position - distance in self.targets:
                    break
                distance += 1
            feedback += distance ** 2
        return sqrt(feedback_squared)


