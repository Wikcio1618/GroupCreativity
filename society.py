from math import floor, sqrt, exp
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
			  , num_of_voters=1, num_of_tasks=3, creativity_force=0, openness_force=0, temperature=0):
		self.num_of_agents=num_of_agents
		self.creativity_mean = creativity_mean
		self.openness_mean = openness_mean
		self.num_of_voters = num_of_voters
		self.num_of_tasks = num_of_tasks
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
		idea_giver = choice(self.agents)
		voters = set([])
        # find neighbours
		while len(voters) < self.num_of_voters:
			voters.add(choice(self.agents))
        
		_vote_result=0
		for voter in voters:
			if voter.openness >= idea_giver.creativity and voter.resource > (1-idea_giver.creativity):
				_vote_result += 1
			else:
				_vote_result += -1
		if _vote_result > 0:
			# idea accepted
			self.progress += idea_giver.creativity
			for voter in voters:
				if self.num_of_tasks !=0:
					voter.add_resource(-1/self.num_of_tasks)
				voter.add_openness(-self.openness_force)
			idea_giver.add_creativity(+self.creativity_force)
		else:
			for voter in voters:
				voter.add_openness(+self.openness_force)
			idea_giver.add_creativity(-self.creativity_force)

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

	def sigmoid(x, T):
		1/(1+exp(-x/T))