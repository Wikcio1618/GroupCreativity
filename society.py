from math import floor, sqrt, exp
import numpy as np
from numpy import array
from random import randint, choice

from agent import Agent, AgentType

class Society:
    # FIELDS:
    # agents - array of agents
    # day - time iterations
    # progress
	# num_of_tasks how much tasks can one agent do

	def __init__(self, creativity_mean=0.5, openness_mean=0.5, num_of_agents=100
			  , creativity_force=0, openness_force=0, temperature=0):
		self.num_of_agents=num_of_agents
		self.creativity_mean = creativity_mean
		self.openness_mean = openness_mean
		self.creativity_force = creativity_force
		self.openness_force = openness_force
		self.temperature = temperature
		self.new_society()

	def new_society(self):
		self.progress = 0
		self.day = 0
        # create creative and conservative agents according to CREATIVE_DENSITY; position them
		self.agents = array([Agent() for _ in range(self.num_of_agents)])

		for _ in range(floor(self.creativity_mean * self.num_of_agents * 100)):
			choice(self.agents).add_creativity(0.01)
		for _ in range(floor(self.openness_mean * self.num_of_agents * 100)):
			choice(self.agents).add_openness(0.01)
 
	def next_step(self):
		# find idea_giver and neighbour
		considered_agents = set([])
		idea_giver = choice(self.agents)
		considered_agents.add(idea_giver)
		while len(considered_agents) < 2:
			print('test')
			voter = choice(self.agents)
			considered_agents.add(voter)

		vote_accepted=(np.random.uniform() < self.sigmoid(voter.openness - idea_giver.creativity, self.temperature))
		if vote_accepted:
			# idea accepted
			self.progress += idea_giver.creativity
			voter.add_openness(-self.openness_force)
			idea_giver.add_creativity(+self.creativity_force)
		else:
			idea_giver.add_creativity(-self.creativity_force)
			voter.add_openness(+self.openness_force)

		self.day += 1
	
	# runs society and returns number of days
	def run_until_target(self, max_days = 10**3, target_progress=5) -> int:
		self.new_society()
		while self.progress < target_progress and self.day < max_days:
			self.next_step()
		return self.day

	def run_until_time(self, time=100) -> int:
		self.new_society()
		for _ in range(time):
			self.next_step()
		return self.progress

	@staticmethod
	def sigmoid(x, T):
		if T==0:
			return np.heaviside(x, 0.5)
		return 1/(1+exp(-x/T))