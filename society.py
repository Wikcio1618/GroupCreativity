from math import floor, sqrt
from numpy import array
from random import randint, choice

from agent import Agent, AgentType

class Society:
    # density of creative agents
    # creative_density = 0.5
    NUM_OF_NEIGHBOURS = 3
    TARGET_PROGRESS = 3

    # FIELDS:
    # agents - array of agents
    # day - time iterations
    # progress

    def __init__(self, creativity_mean, openness_mean, force=0.05, num_of_agents=25):
        self.num_of_agents=num_of_agents
        self.creativity_mean = creativity_mean
        self.openness_mean = openness_mean
        self.force = force
        self.new_society()

    def new_society(self):
        self.progress = 0
        self.day = 0
        # create creative and conservative agents according to CREATIVE_DENSITY; position them
        self.agents = array([Agent() for _ in range(self.num_of_agents)])

        for _ in range(floor(self.creativity_mean * self.num_of_agents * 100)):
            choice(self.agents).creativity += 0.01
        for _ in range(floor(self.openness_mean * self.num_of_agents * 100)):
            choice(self.agents).openness += 0.01
 
    def next_step(self):
        agent = choice(self.agents)
        neighbours = set([])
        # find neighbours
        while len(neighbours) < self.NUM_OF_NEIGHBOURS:
            neighbours.add(choice(self.agents))
        
        if sum([nei.openness for nei in neighbours])/len(neighbours) >= agent.creativity:
            # acceptance aquired
            self.progress += agent.creativity
            agent.add_creativity(self.force)
        else:
            agent.add_creativity(-self.force)

        self.day += 1
	
	# runs society and returns number of days
    def run_until_target(self, max_days = 10**5) -> int:
        self.new_society()
        while self.progress < self.TARGET_PROGRESS and self.day < max_days:
            self.next_step()
        return self.day

    def run_until_time(self, time=100) -> int:
        self.new_society()
        for _ in range(time):
            self.next_step()
        return self.progress