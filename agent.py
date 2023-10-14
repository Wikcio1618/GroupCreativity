from enum import Enum


class AgentType(Enum):
    CREATIVE = 'creative'
    SUPPORTIVE = 'supportive'


class Agent():
    # FIELDS:
    # creativity - float
    # openness

	def __init__(self, creativity = 0, openness = 0, resource = 1):
		self.creativity = creativity
		self.openness = openness
		self.resource = resource

	def add_creativity(self, crea):
		self.creativity += crea
		# if self.creativity < 0:
		# 	self.creativity = 0
		# elif self.creativity > 1:
		# 	self.creativity = 1

	def add_openness(self, op):
		self.openness += op
		# if self.openness < 0:
		# 	self.openness = 0
		# elif self.openness > 1:
		# 	self.openness = 1
			
	def add_resource(self, res):
		self.resource += res
		if self.resource < 0:
			self.resource = 0
		elif self.resource > 1:
			self.resource = 1