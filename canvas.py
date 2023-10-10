from threading import Event, Thread
import time
from tkinter import Canvas, ttk
from matplotlib.backend_bases import RendererBase
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
        self.society = society

        self.MARGIN = 0.15
        self.AGENT_SIZE = 25
        # graph size
        self.figsize=(10,2)
        self.dpi=100
		
        super().__init__(root, width=self.WIDTH, height=self.HEIGHT, bg=bg_color
                         , bd=1, highlightbackground=primary_col, scrollregion=(0, 0, np.inf, 0))
        
    #     # day text
    #     ttk.Label(master=self, text="DAY:", font=('Arial', 17)
	#    , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR).place(x=self.WIDTH/2 - 15, y=self.HEIGHT * 0.85)

    #     # day counter label
    #     self.day_label = ttk.Label(master=self, text="0", font=('Arial', 15)
	#    , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
    #     self.day_label.place(x=self.WIDTH/2, y=self.HEIGHT * 0.85 + 30)

        # graph
        self.init_charts()

        self.init_new()

        self.thread_running_event = Event() 
        self.canvasThread = Thread(target=self.animate_society)
        self.canvasThread.start()

    # ----------------------- init ---------------------

    # function that updates colors with current state of society. is called by next step button and by animate society
    def draw_society(self):
        self.update_charts()
        for i, agent in enumerate(self.society.agents):
            colors = self.get_agent_colors(agent)
            for j, rectangle in enumerate(self.agents_obj[i]):
                self.itemconfig(rectangle, fill=colors[j])
        self.update()

    # function to draw an agent at a given position; returns address of the drawn rectangle
    def draw_agent(self, agent:Agent, x_pos:int, y_pos:int):
        x0 = x_pos
        x1 = x_pos + self.AGENT_SIZE/3
        x2 = x_pos + 2 * self.AGENT_SIZE/3
        x3 = x_pos + 3 * self.AGENT_SIZE/3
        y0 = y_pos
        y1 = y_pos + self.AGENT_SIZE

        colors = self.get_agent_colors(agent)

        agent_obj=[]
        agent_obj.append(self.create_rectangle(x0, y0, x1, y1, fill=colors[0], tags="agents"))
        agent_obj.append(self.create_rectangle(x1, y0, x2, y1, fill=colors[1], tags="agents"))
        agent_obj.append(self.create_rectangle(x2, y0, x3, y1, fill=colors[2], tags="agents"))

        return agent_obj
    
    # draws new agents; called by init_new
    def draw_new_agents(self):
        self.agents_obj=[]
        for agent in self.society.agents:
            self.agents_obj.append(self.draw_agent(agent, x_pos=np.random.randint(self.MARGIN*self.WIDTH, (1-self.MARGIN)*self.WIDTH)
                            , y_pos=np.random.randint(self.MARGIN*self.HEIGHT, self.HEIGHT-self.figsize[1]*self.dpi-70)))

    # called once in __init__ to draw a nice figure and graph in it
    def init_charts(self):
        # plot
        self.graph_progress_data=[]
        self.graph_x_data=[]
        figure = Figure(figsize=self.figsize, dpi=self.dpi, facecolor=self.BG_COLOR)
        self.plot = figure.add_subplot(121, facecolor=self.BG_COLOR)
        self.plot_obj, = self.plot.plot(self.graph_x_data, self.graph_progress_data, color=self.PRIMARY_COLOR, label="Progress")
        self.plot.set_ylim(bottom=0)
        self.plot.set_xlim(left=0)
        self.plot.set_xlabel("Day")
        self.plot.set_ylabel("Progress")
        self.plot.grid(True)
        self.plot.tick_params(colors=self.PRIMARY_COLOR)
        self.plot.yaxis.label.set_color(self.PRIMARY_COLOR)
        self.plot.yaxis.label.set_fontsize(16)
        self.plot.xaxis.label.set_color(self.PRIMARY_COLOR)
        self.plot.xaxis.label.set_fontsize(16)
        self.plot.set_autoscalex_on(True)
        self.plot.set_autoscaley_on(True)
        self.plot.legend()

        # histograms
        self.creativity_distribution_data = [agent.creativity for agent in self.society.agents]
        self.openness_distribution_data = [agent.openness for agent in self.society.agents]
        self.histogram = figure.add_subplot(122, facecolor=self.BG_COLOR)
        self.num_of_bins=int(np.sqrt(self.society.num_of_agents))
        hist_crea_data, hist_crea_bins = np.histogram(self.creativity_distribution_data, bins=self.num_of_bins, range=(0,1))
        hist_open_data, hist_open_bins = np.histogram(self.openness_distribution_data, bins=self.num_of_bins, range=(0,1))
        self.hist_obj_crea = self.histogram.hist(hist_crea_data, bins=hist_crea_bins, color='red', alpha=0.5, label='creativity')
        self.hist_obj_open = self.histogram.hist(hist_open_data, bins=hist_open_bins, color='blue', alpha=0.5, label='openness')
        self.histogram.set_xlim([0,1])
        self.histogram.set_ylim([0,0.8*self.society.num_of_agents])
        self.histogram.set_xlabel("Creativity/Openness")
        self.histogram.set_ylabel("Frequency")
        self.histogram.yaxis.label.set_color(self.PRIMARY_COLOR)
        self.histogram.yaxis.label.set_fontsize(16)
        self.histogram.legend()    

        self.charts = FigureCanvasTkAgg(figure, master=self)
        self.charts.draw()
        plot_widget = self.charts.get_tk_widget()
        plot_widget.place(x=0.05*self.WIDTH, y=self.HEIGHT-self.dpi*self.figsize[1]-40)


    # called everytime we want to draw current state on graph 
    def update_charts(self):
        self.graph_x_data.append(self.society.day)
        self.graph_progress_data.append(self.society.progress)
        self.plot_obj.set_data(self.graph_x_data, self.graph_progress_data)
        # self.plot.set_xticks([x for i, x in enumerate(self.graph_x_data) if x%4==0])
        # self.plot.set_yticks([x for i, x in enumerate(self.graph_x_data) if x%4==0])
        self.plot.set_xbound(0, self.society.day)
        self.plot.set_ybound(0, self.society.progress)


        self.creativity_distribution_data = [agent.creativity for agent in self.society.agents]
        self.openness_distribution_data = [agent.openness for agent in self.society.agents]
        for i, rect in enumerate(self.hist_obj_crea[2]):
            rect.set_height(np.histogram(self.creativity_distribution_data, bins=self.num_of_bins, range=(0,1))[0][i])
        for i, rect in enumerate(self.hist_obj_open[2]):
            rect.set_height(np.histogram(self.openness_distribution_data, bins=self.num_of_bins, range=(0,1))[0][i])

        self.charts.draw()

    # clear all lines on graph
    def reset_charts(self):
        del self.graph_x_data[:]
        del self.graph_progress_data[:]
        self.plot.set_xbound(0,1)
        self.plot.set_ybound(0,1)
        self.charts.draw()

    # it is called to prepare canvas to display society of new parameters
    def init_new(self):
        self.society.new_society()
        self.delete("all")

        self.draw_new_agents()
        self.reset_charts()
        self.draw_society()

    # make the canvas being updated
    def start_update(self):
        self.thread_running_event.set()
	
	# stop the canvas from updating
    def stop_update(self):
        self.thread_running_event.clear()

    # for continous evolution of society
    def animate_society(self):
        while self.thread_running_event.is_set():
            self.society.next_step()          
            self.draw_society()
            time.sleep(0.05)

    def get_agent_colors(self, agent:Agent) -> tuple:
        red_color = '#' + format(int((1-agent.creativity)*255), '02x') + "0000"
        blue_color = '#' '0000' + format(int((1-agent.openness)*255), '02x')
        yellow_color = '#00' + format(int((1-agent.resource)*255), '02x') + "00"
        return (red_color,blue_color, yellow_color)
        