class Agent():
    # FIELDS:
    # creativity - float

	def __init__(self, creativity = 0):
		self.creativity = creativity

	def add_creativity(self, crea):
		self.creativity += crea
		# if self.creativity < 0:
		# 	self.creativity = 0
		# elif self.creativity > 1:
		# 	self.creativity = 1