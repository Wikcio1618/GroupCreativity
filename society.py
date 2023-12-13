import math
import numpy as np
from random import choice
import itertools
from matplotlib import cm
from matplotlib.colors import Normalize

from agent import Agent

class Society:
    # FIELDS:
    # agents - array of agents
    # day - time iterations
	# temperature
	# thresh

	def __init__(self, crea_mean=10, crea_stddev=0.2, num_of_agents=100, thresh=0, temperature=0):
		self.num_of_agents = num_of_agents
		self.crea_dist  = np.round(np.random.normal(crea_mean, crea_stddev, self.num_of_agents))
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

		vote_accepted=(np.random.uniform() < self.pair_chance(agent_i.creativity, agent_j.creativity))

		if vote_accepted:
			agent_i.add_creativity(+1)
			agent_j.add_creativity(+1)
		else:
			agent_i.add_creativity(-1)
			agent_j.add_creativity(-1)

		self.day += 1
	
	def run_until_time(self, time):
		while self.day < time:
			self.next_step()

	def get_crea_mean(self):
		return np.average([x.creativity for x in self.agents])

	def get_crea_stddev(self):
		return np.std([x.creativity for x in self.agents])

	def society_success_chance(self):
		pairs_idxs = list(itertools.combinations(range(self.num_of_agents), 2))
		chance = 0
		for pair in pairs_idxs:
			chance += self.pair_chance(self.agents[pair[0]].creativity, self.agents[pair[1]].creativity)
		chance /= len(pairs_idxs)
		return chance

	# assumed that possibility of drawing himself is low
	def agent_success_chance(self, c_i):
		return np.average([self.pair_chance(c_i, agent.creativity) for agent in self.agents])

	def pair_chance(self, c_i, c_j):
		return Society.sigmoid(c_i**1 + c_j**1 - self.thresh, self.temperature)
	
	# how will num of agents in the bin change
	def society_density_slope(self):
		creas = np.array([agent.creativity for agent in self.agents])
		min, max = np.min(creas), np.max(creas)

		slopes = np.zeros(int(max-min+1))
		
		p_curr = (creas == min).sum() / len(creas)
		gamma_curr = self.agent_success_chance(min)
		p_next = (creas == min+1).sum() / len(creas)
		gamma_next = self.agent_success_chance(min+1)
		slopes[0] = -p_curr + p_next*(1 - gamma_next)
		for i in range(1, int(max  - min + 1)):
			p_prev = p_curr
			gamma_prev = gamma_curr
			p_curr = p_next
			gamma_curr = gamma_next
			slopes[i] = -p_curr + p_prev * gamma_prev

			gamma_next = self.agent_success_chance(min + i + 1)
			p_next = (creas == min + i + 1).sum() / len(creas)
			slopes[i] += p_next * (1 - gamma_next)

		return slopes 
	
	def get_entropy(self):
		_ , counts = np.unique([agent.creativity for agent in self.agents], return_counts=True)
		dens = np.divide(counts, self.num_of_agents)
		return -sum([d * math.log(d, self.num_of_agents) for d in dens])
	
	@staticmethod
	def sigmoid(x, T):
		if T==0:
			return np.heaviside(x, 0)
		return 1/(1+np.exp(-x/T))
	
	@staticmethod
	def get_coolwarm_color(parameter):
		# Ensure parameter is in the range [-1, 1]
		parameter = max(-1, min(1, parameter))
		# Create a ScalarMappable
		norm = Normalize(vmin=-1, vmax=1)
		scalar_map = cm.ScalarMappable(norm=norm, cmap=cm.coolwarm)
		# Map parameter to RGBA color
		color = scalar_map.to_rgba(parameter)
		return color