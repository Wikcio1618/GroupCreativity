import math
import numpy as np
from random import randint, choice
from numba import jit

from agent import Agent

class Society:
    # FIELDS:
    # agents - array of agents
    # day - time iterations

	def __init__(self, crea_mean=10, crea_stddev=0.2, num_of_agents=100, thresh=None, temperature=0):
		self.num_of_agents = num_of_agents
		self.crea_dist  = np.random.normal(crea_mean, crea_stddev, self.num_of_agents)
		if thresh is None:
			thresh = crea_mean * crea_mean
		self.thresh = thresh
		self.temperature = temperature
		self.new_society(self.crea_dist)

	def new_society(self, crea_dist):
		self.day = 0
		# create agents and assign creativity according to distributions
		self.agents = np.array([Agent(creativity=crea_dist[i]) for i in range(self.num_of_agents)])

	def next_step(self):
		# find idea_giver and neighbour
		considered_agents = set([])
		agent_i = choice(self.agents)
		considered_agents.add(agent_i)
		while len(considered_agents) < 2:
			agent_j = choice(self.agents)
			considered_agents.add(agent_j)

		vote_accepted=(np.random.uniform() < self.sigmoid(math.pow(agent_j.creativity, 3) + math.pow(agent_i.creativity, 3) - self.thresh, self.temperature))
		if vote_accepted:
			agent_i.add_creativity(+1)
			agent_j.add_creativity(+1)
		else:
			agent_i.add_creativity(-1)
			agent_j.add_creativity(-1)

		self.day += 1
	
	def run_until_time(self, time):
		self.new_society(self.crea_dist)
		for _ in range(time):
			self.next_step()

	def get_crea_mean(self):
		return np.average([x.creativity for x in self.agents])

	def get_crea_stddev(self):
		return np.std([x.creativity for x in self.agents])

	@staticmethod
	def sigmoid(x, T):
		if T==0:
			return np.heaviside(x, 0)
		return 1/(1+np.exp(-x/T))