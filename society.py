from math import floor, sqrt
from numpy import array
from random import randint, shuffle

from agent import Agent, AgentType

class Society:
    # -- GAME PARAMS -- #
    # space size 
    # space_size = 50
    # agents to space ratio
    # agents_density = 0.3
    # range of interaction
    # field_range = 4
    # interaction power (how much is range increased)
    # field_force = 1
    # initial steps of agents (conservative, creative)
    # init_step = tuple([1,3])
    # density of creative agents
    # creative_density = 0.5
    # starting postition of agents - random or beginning
    # positioning_type = "random"


    # FIELDS:
    # agents - array of agents
    # targets - positions to be taken (set of ints) 
    # targets_left
    # day - time iterations

    def __init__(self, space_size=30, agents_density=0.3, creative_density=0.3
                 , field_range=3, field_force=0.05, positioning_type="random"):
        self.space_size=space_size
        self.agents_density=agents_density
        self.creative_density=creative_density
        self.field_range=field_range
        self.field_force=field_force
        self.positioning_type=positioning_type

        self.new_society()

    def new_society(self):
        self.day = 0
        # create creative and conservative agents according to CREATIVE_DENSITY; position them
        self.num_of_agents=int(self.space_size * self.agents_density)
        self.agents = array(
            [
            Agent(type=AgentType.CONSERVATIVE, space_size=self.space_size) 
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
        self.targets_left = self.targets.copy()
        self.check_targets()
 
    def next_step(self):
        self.day += 1
        # interaction between agents
        feedback = self.calculate_feedback()
        for agent in self.agents:
            if agent.type == AgentType.CONSERVATIVE and feedback < self.space_size * 0.1 and agent.step !=0:
                in_range_neighbours = [nei for nei in self.agents if abs(agent.position - nei.position) <= self.field_range]
                for nei in in_range_neighbours:
                    if nei.step != 0: # has not found target
                        nei.cool_down(self.field_force)

            elif agent.type == AgentType.CREATIVE and feedback > self.space_size * 0.1 and agent.step !=0:
                in_range_neighbours = [nei for nei in self.agents if abs(agent.position - nei.position) <= self.field_range]
                for nei in in_range_neighbours:
                    if nei.step != 0:
                        nei.shift_right(self.field_force)

        # print(feedback)
        # move agents
        for agent in self.agents:
            agent.move_random()

        self.check_targets()

    def check_targets(self):
        _temp_agents = self.agents.copy()
        shuffle(_temp_agents)
        for agent in _temp_agents:
            if agent.position in self.targets_left:
                agent.step = 0
                self.targets_left.remove(agent.position)

    def calculate_feedback(self):
        feedback_squared = 0
        for agent in [agent for agent in self.agents if agent.step != 0]:
            distance = 0
            while True:
                if (agent.position + distance in self.targets_left or 
                agent.position + self.space_size - distance in self.targets_left or 
                agent.position - distance in self.targets_left or 
                agent.position - self.space_size + distance in self.targets_left):
                    break
                distance += 1
            feedback_squared += distance ** 2
        return sqrt(feedback_squared / len(self.agents))

    def get_all_progress(self):
        if len(self.agents) == 0:
            progress = 1
        else:
            progress = (1 - len(self.targets_left) / len(self.agents))
        return progress
    
    def get_crea_progress(self):
        if len([agent for agent in self.agents if agent.type == AgentType.CREATIVE]) == 0:
            progress = 1
        else :
            progress = (len([agent for agent in self.agents if (agent.type == AgentType.CREATIVE and agent.step == 0)]) 
        / len([agent for agent in self.agents if agent.type == AgentType.CREATIVE]))
        return progress
    
    def get_cons_progress(self):
        if len([agent for agent in self.agents if agent.type == AgentType.CONSERVATIVE]) == 0:
            progress = 1
        else :
            progress = (len([agent for agent in self.agents if (agent.type == AgentType.CONSERVATIVE and agent.step == 0)]) 
        / len([agent for agent in self.agents if agent.type == AgentType.CONSERVATIVE]))
        return progress
