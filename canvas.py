from threading import Event, Thread
import time
from tkinter import Canvas

import numpy as np

from agent import Agent, AgentType
from society import Society


class CustomCanvas(Canvas):
    def __init__(self, root, primary_col, bg_color, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        print(width)
        self.OUTER_MARGIN = 30.0 # margin on the left and right to the boxes

        self.Y_BOX_CENTER = self.HEIGHT/2

		# Define the color for different elements
        self.TARGET_COLOR = "gold"
        self.BOX_COLOR = "blue"
        self.AGENT_COLOR = "red"
		
        super().__init__(root, width=self.WIDTH, height=self.HEIGHT, bg=bg_color
                         , bd=1, highlightbackground=primary_col, scrollregion=(0, 0, np.inf, 0))

        Society.new_society()
        self.init_new()

        self.thread_running_event = Event() 
        self.canvasThread = Thread(target=self.animate_society)
        self.canvasThread.start()
	
	# make the canvas being updated
    def start_update(self):
        self.thread_running_event.set()
	
	# stop the canvas from updating
    def stop_update(self):
        self.thread_running_event.clear()

    def animate_society(self):
        while self.thread_running_event.is_set():
            self.draw_next_step()

    def draw_next_step(self):
        self.delete("agents")
        Society.next_step()
        for agent in Society.agents:
            self.draw_agent(agent)
        self.update()

    # function to draw an agent at a given (x) position
    def draw_agent(self, agent:Agent):
        if agent.type == AgentType.CONSERVATIVE:
            x1 = self.x_box_center(agent.position) - self.box_size/2 + self.inner_margin
            x2 = self.x_box_center(agent.position) + self.box_size/2 - self.inner_margin
            y1 = self.Y_BOX_CENTER - self.box_size/2 + self.inner_margin
            y2 = self.Y_BOX_CENTER + self.box_size/2 - self.inner_margin
            self.create_oval(x1, y1, x2, y2, fill=self.AGENT_COLOR, tags="agents")
        elif agent.type == AgentType.CREATIVE:
            x1 = self.x_box_center(agent.position) - self.box_size/2 + self.inner_margin
            x2 = self.x_box_center(agent.position)
            x3 = self.x_box_center(agent.position) + self.box_size/2 - self.inner_margin
            y1 = self.Y_BOX_CENTER + self.box_size/2 - self.inner_margin
            y2 = self.Y_BOX_CENTER - self.box_size/2 + self.inner_margin
            y3 = y1
            self.create_polygon([x1, y1, x2, y2, x3, y3], fill=self.AGENT_COLOR, tags="agents")

    def init_new(self):
        self.delete("all")
        self.box_size = (self.WIDTH - self.OUTER_MARGIN*2) / Society.space_size
        print(self.box_size)
        self.x_box_center = lambda x: self.OUTER_MARGIN + self.box_size/2 + x * self.box_size
        self.inner_margin = self.box_size * 0.15 # margin around agents in the box
        # draw row of boxes
        y1 = self.Y_BOX_CENTER - self.box_size/2
        y2 = self.Y_BOX_CENTER + self.box_size/2
        for x in range(Society.space_size):
            x1 = self.x_box_center(x) - self.box_size/2
            x2 = self.x_box_center(x) + self.box_size/2
            if x in Society.targets:
                self.create_rectangle(x1, y1, x2, y2, fill=self.TARGET_COLOR)
            else:
                self.create_rectangle(x1, y1, x2, y2, fill=self.BOX_COLOR)