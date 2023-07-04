from threading import Event, Thread
import time
from tkinter import Canvas, ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

from agent import Agent, AgentType
from society import Society


class CustomCanvas(Canvas):
    def __init__(self, root, society, window, primary_col, bg_color, width, height):
        self.root = root
        self.window = window
        self.PRIMARY_COLOR = primary_col
        self.BG_COLOR = bg_color
        self.WIDTH = width
        self.HEIGHT = height
        self.OUTER_MARGIN = 30.0 # margin on the left and right to the boxes
        self.society = society

        self.Y_BOX_CENTER = self.HEIGHT * 0.35

		# Define the color for different elements
        self.TARGET_COLOR = "gold"
        self.BOX_COLOR = "blue"
        self.AGENT_COLOR = "red"
		
        super().__init__(root, width=self.WIDTH, height=self.HEIGHT, bg=bg_color
                         , bd=1, highlightbackground=primary_col, scrollregion=(0, 0, np.inf, 0))
        
        # day text
        ttk.Label(master=self, text="DAY:", font=('Arial', 17)
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR).place(x=self.WIDTH/2 - 15, y=self.HEIGHT * 0.85)

        # day counter label
        self.day_label = ttk.Label(master=self, text="0", font=('Arial', 15)
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.day_label.place(x=self.WIDTH/2, y=self.HEIGHT * 0.85 + 30)

        # graph
        self.init_graph()

        self.init_new()

        self.thread_running_event = Event() 
        self.canvasThread = Thread(target=self.animate_society)
        self.canvasThread.start()

    # ----------------------- init ---------------------

	
	# make the canvas being updated
    def start_update(self):
        self.thread_running_event.set()
	
	# stop the canvas from updating
    def stop_update(self):
        self.thread_running_event.clear()

    def animate_society(self):
        while self.thread_running_event.is_set():
            if self.society.get_all_progress() == 1:
                self.stop_update()
                self.window.start_stop_button.configure(text='Run')
                self.window.set_param_widgets_active(True)
                self.window.set_run_button_active(False)
                self.window.set_next_step_button_active(False)
                self.window.set_reset_button_active(True)
            else:
                self.society.next_step()          
                self.draw_society()
                time.sleep(0.5)

    # function that updates grid and graph with current state of society. is called by next step button and by animate society
    def draw_society(self):
        self.delete("agents")
        for pos in range(self.society.space_size):
            pos_agents = [agent for agent in self.society.agents if agent.position == pos]
            pos_agents_sorted = sorted(pos_agents, key=lambda agent: agent.step)
            for i, agent in enumerate(pos_agents_sorted):
                self.draw_agent(agent, i)
        self.update_graph()
        self.day_label.configure(text=self.society.day)
        if self.society.get_all_progress() == 1.0:
            self.window.set_param_widgets_active(True)
            self.window.set_run_button_active(False)
            self.window.set_next_step_button_active(False)
            self.window.set_reset_button_active(True)
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

    # called once in __init__ to draw a nice figure and graph in it
    def init_graph(self):
        self.graph_all_data=[]
        self.graph_crea_data=[]
        self.graph_cons_data = []
        self.graph_x_data=[]
        figure = Figure(figsize=(10,2), dpi=106, facecolor=self.BG_COLOR)
        self.plot = figure.add_subplot(111, facecolor="blue")
        self.line_cons, = self.plot.plot(self.graph_x_data, self.graph_cons_data, color="green", label="Conservative")
        self.line_crea, = self.plot.plot(self.graph_x_data, self.graph_crea_data, color=self.AGENT_COLOR, label="Creative")
        self.line_all, = self.plot.plot(self.graph_x_data, self.graph_all_data, color=self.PRIMARY_COLOR, label="All")
        self.plot.set_ylim(0,1)
        self.plot.set_xlim(left=0)
        self.plot.set_xlabel("Day")
        self.plot.set_ylabel("Progress")
        self.plot.grid(True)
        self.plot.tick_params(colors=self.PRIMARY_COLOR)
        self.plot.yaxis.label.set_color(self.PRIMARY_COLOR)
        self.plot.yaxis.label.set_fontsize(16)
        self.plot.legend()
        
        self.graph = FigureCanvasTkAgg(figure, master=self)
        self.graph.draw()
        plot_widget = self.graph.get_tk_widget()
        plot_widget.place(x=self.OUTER_MARGIN, y=self.HEIGHT * 0.5)


    def update_graph(self):
        self.graph_x_data.append(self.society.day)
        all_progress = self.society.get_all_progress()
        crea_progress = self.society.get_crea_progress()
        cons_progress = self.society.get_cons_progress()
        self.graph_all_data.append(all_progress)
        self.line_all.set_data(self.graph_x_data, self.graph_all_data)
        self.graph_crea_data.append(crea_progress)
        self.line_crea.set_data(self.graph_x_data, self.graph_crea_data)
        self.graph_cons_data.append(cons_progress)
        self.line_cons.set_data(self.graph_x_data, self.graph_cons_data)
        # for line in self.plot.get_lines(): # ax.lines:
        #     line.remove()
        # self.line_all, = self.plot.plot(self.graph_x_data, self.graph_all_data, color=self.PRIMARY_COLOR, label="All")
        # self.line_crea, = self.plot.plot(self.graph_x_data, self.graph_crea_data, color=self.AGENT_COLOR, label="Creative")
        # self.line_cons, = self.plot.plot(self.graph_x_data, self.graph_cons_data, color="green", label="Conservative")
        self.plot.set_xticks(self.graph_x_data)

        self.graph.draw()

    def reset_graph(self):
        self.graph_all_data = []
        self.graph_crea_data = []
        self.graph_cons_data = []
        self.graph_x_data = []
        # for line in self.plot.get_lines(): # ax.lines:
        #     line.remove()
        self.graph.draw()

    # it is called to prepare canvas to display society of new parameters
    def init_new(self):
        self.society.new_society()
        self.delete("all")
        self.reset_graph()

        self.box_size = (self.WIDTH - self.OUTER_MARGIN*2) / self.society.space_size
        self.x_box_center = lambda x: self.OUTER_MARGIN + self.box_size/2 + x * self.box_size
        self.inner_margin = self.box_size * 0.15 # margin around agents in the box
        # draw row of boxes
        y1 = self.Y_BOX_CENTER - self.box_size/2
        y2 = self.Y_BOX_CENTER + self.box_size/2
        for x in range(self.society.space_size):
            x1 = self.x_box_center(x) - self.box_size/2
            x2 = self.x_box_center(x) + self.box_size/2
            if x in self.society.targets:
                self.create_rectangle(x1, y1, x2, y2, fill=self.TARGET_COLOR)
            else:
                self.create_rectangle(x1, y1, x2, y2, fill=self.BOX_COLOR)

        self.draw_society()
        