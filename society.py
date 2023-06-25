from math import floor, sqrt
from numpy import array, where
from random import randint, shuffle

from agent import Agent, AgentType

class Society:
    # -- GAME PARAMS -- #
    # space size 
    space_size = 50
    # agents to space ratio
    agents_density = 0.3
    # range of interaction
    field_range = 4
    # interaction power (how much is range increased)
    field_force = 1
    # initial steps of agents (conservative, creative)
    init_step = tuple([1,3])
    # density of creative agents
    creative_density = 0.5
    # starting postition of agents - random or beginning
    positioning_type = "random"


    # FIELDS:
    # agents - array of agents
    # targets - positions to be taken (set of ints) 
    # day - time iterations

    @classmethod
    def new_society(self):
        self.day = 0
        # create creative and conservative agents according to CREATIVE_DENSITY; position them
        self.num_of_agents=int(self.space_size * self.agents_density)
        self.agents = array(
            [
            Agent(type=AgentType.CONSERVATIVE, init_step=self.init_step, space_size=self.space_size) 
            for _ in range(self.num_of_agents)
            ])
        for i in range(floor(self.creative_density * self.num_of_agents)):
            self.agents[i].type = AgentType.CREATIVE
            self.agents[i].step = self.init_step[1]
        
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
        self.day += 1
        self.check_targets()
        for agent in self.agents:
            agent.move_random()

    @classmethod
    def check_targets(self):
        _temp_agents = self.agents.copy()
        shuffle(_temp_agents)
        for agent in _temp_agents:
            if agent.position in self.targets:
                agent.step = 0
                self.targets.remove(agent.position) # remove from targets temporarily

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


