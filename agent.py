class Agent():
    # FIELDS:
    # creativity - float

	def __init__(self, creativity = 0):
		self.creativity = creativity

	def add_creativity(self, crea):
		self.creativity += crea