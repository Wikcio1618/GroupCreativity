from threading import Event, Thread
import time
from tkinter import Canvas
from tkinter import ttk

import numpy as np

from agent import Agent, AgentType
from society import Society


class CustomCanvas(Canvas):
    def __init__(self, root, primary_col, bg_color, width, height):
        self.PRIMARY_COLOR = primary_col
        self.BG_COLOR = bg_color
        self.WIDTH = width
        self.HEIGHT = height
        self.OUTER_MARGIN = 30.0 # margin on the left and right to the boxes

        self.Y_BOX_CENTER = self.HEIGHT * 0.35

		# Define the color for different elements
        self.TARGET_COLOR = "gold"
        self.BOX_COLOR = "blue"
        self.AGENT_COLOR = "red"
		
        super().__init__(root, width=self.WIDTH, height=self.HEIGHT, bg=bg_color
                         , bd=1, highlightbackground=primary_col, scrollregion=(0, 0, np.inf, 0))

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
            self.draw_society()

    def draw_society(self):
        self.delete("agents")
        self.delete("progress")
        for pos in range(Society.space_size):
            pos_agents = [agent for agent in Society.agents if agent.position == pos]
            for i, agent in enumerate(pos_agents):
                self.draw_agent(agent, i)

        self.draw_progress_bar()
        self.day_label.configure(text=Society.day)

        self.update()

    # function to draw an agent at a given (x) position
    def draw_agent(self, agent:Agent, y_pos:int):
        if agent.type == AgentType.CONSERVATIVE:
            x1 = self.x_box_center(agent.position) - self.box_size/2 + self.inner_margin
            x2 = self.x_box_center(agent.position) + self.box_size/2 - self.inner_margin
            y1 = self.Y_BOX_CENTER - self.box_size/2 + self.inner_margin - y_pos*self.box_size
            y2 = self.Y_BOX_CENTER + self.box_size/2 - self.inner_margin - y_pos*self.box_size
            self.create_oval(x1, y1 , x2, y2, fill=self.AGENT_COLOR, tags="agents")
        elif agent.type == AgentType.CREATIVE:
            x1 = self.x_box_center(agent.position) - self.box_size/2 + self.inner_margin
            x2 = self.x_box_center(agent.position)
            x3 = self.x_box_center(agent.position) + self.box_size/2 - self.inner_margin
            y1 = self.Y_BOX_CENTER + self.box_size/2 - self.inner_margin - y_pos*self.box_size
            y2 = self.Y_BOX_CENTER - self.box_size/2 + self.inner_margin - y_pos*self.box_size
            y3 = y1
            self.create_polygon([x1, y1, x2, y2, x3, y3], fill=self.AGENT_COLOR, tags="agents")

    def draw_progress_bar(self):
        x1 = 0.2 * self.WIDTH
        x2 = 0.8 * self.WIDTH
        y1 = self.HEIGHT * 0.7
        y2 = y1 + 20
        self.create_rectangle(x1, y1, x2, y2, fill="", outline=self.PRIMARY_COLOR)
        num_taken_targets = len(Society.agents) - len(Society.targets - set([agent.position for agent in Society.agents])) # '-' operator works like vienn diagram
        x2_progress = x1 + (x2 - x1) * num_taken_targets / len(Society.agents)
        self.create_rectangle(x1, y1, x2_progress, y2, fill=self.PRIMARY_COLOR, outline="", tags="progress")

    def init_new(self):
        Society.new_society()
        self.delete("all")
        self.box_size = (self.WIDTH - self.OUTER_MARGIN*2) / Society.space_size
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
        
        # day text
        ttk.Label(master=self, text="DAY:", font=('Arial', 17)
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR).place(x=self.WIDTH/2 - 15, y=self.HEIGHT * 0.85)

        # day counter label
        self.day_label = ttk.Label(master=self, text=Society.day, font=('Arial', 15)
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.day_label.place(x=self.WIDTH/2, y=self.HEIGHT * 0.85 + 30)

        self.draw_society()
        