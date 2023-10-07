from tkinter import BOTH, DISABLED, E, NORMAL, W, Frame, IntVar, ttk, DoubleVar
from customtkinter import CTkSlider, CTkButton, BooleanVar, CTkSwitch, CTkCheckBox, CTkRadioButton, CTk

from canvas import CustomCanvas
from society import Society

class Window():
    # FIELDS:
    # root
    # canvas
    # start_stop_button

    # Define lead colors for window
    PRIMARY_COLOR = "#8B5742"
    BG_COLOR = "oldlace"
    DISABLED_COLOR = "grey"

    def __init__(self):
        self.root = CTk()
        self.root.geometry("900x700") # Window size
        self.root.title("Group Creativity")
        self.root.resizable(0, 0) # No full-screen
        self.root.protocol("WM_DELETE_WINDOW", self.on_close) # stop thread on close

        self.society = Society()

        # top frame
        top_frame = Frame(self.root, bg=self.BG_COLOR, height=200)
        top_frame.pack(fill=BOTH)
        top_frame.columnconfigure(0, weight=4)
        top_frame.columnconfigure(1, weight=1)

# PARAMS FRAME

        # params frame
        params_frame=Frame(top_frame, bg=self.BG_COLOR, highlightbackground=self.PRIMARY_COLOR, highlightthickness=2)
        params_frame.grid(column=0, row=0, sticky='WENS')

        # creativity slider
        self.creativity_mean_slider_label=ttk.Label(master=params_frame, text="Mean creativity", font=('Arial', 14)
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.creativity_mean_slider_label.grid(column=0, row=0, columnspan=2, pady=(10, 15))
        creativity_mean_var = DoubleVar(value=self.society.creativity_mean)

        def creativity_mean_slider_event(value):
            self.creativity_mean_slider_value_label.configure(text=f'{value:.2f}')
            if value != self.society.creativity_mean:
                self.society.creativity_mean = value
                self.society.new_society()
                self.reset_canvas()

        self.creativity_mean_slider = CTkSlider(master=params_frame, fg_color='grey', progress_color=self.PRIMARY_COLOR
                                   , hover=False, button_color=self.PRIMARY_COLOR
			                        , from_=0, to=1, variable=creativity_mean_var, command=creativity_mean_slider_event)
        self.creativity_mean_slider.grid(column=0, row=1, padx=(20,0))
        self.creativity_mean_slider_value_label = ttk.Label(master=params_frame, font=('Arial', 12), text=f"{creativity_mean_var.get():.2f}"
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.creativity_mean_slider_value_label.grid(column=1, row=1, pady=(10, 5))

        # oppennes mean slider
        self.openness_mean_slider_label=ttk.Label(master=params_frame, text="Openness mean", font=('Arial', 14)
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.openness_mean_slider_label.grid(column=0, row=2, columnspan=2, pady=(30, 15))
        openness_mean_var = DoubleVar(value=self.society.openness_mean)

        def openness_mean_slider_event(value):
            self.openness_mean_slider_value_label.configure(text=f'{value:.2f}')
            if value != self.society.openness_mean:
                self.society.openness_mean=value
                self.society.new_society()
                self.reset_canvas()

        self.openness_mean_slider = CTkSlider(master=params_frame, fg_color='grey', progress_color=self.PRIMARY_COLOR
                                   , hover=False, button_color=self.PRIMARY_COLOR
			                        , from_=0, to=1, variable=openness_mean_var, command=openness_mean_slider_event)
        self.openness_mean_slider.grid(column=0, row=3, padx=(20,0))
        self.openness_mean_slider_value_label = ttk.Label(master=params_frame, font=('Arial', 12), text=f"{openness_mean_var.get():.2f}"
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.openness_mean_slider_value_label.grid(column=1, row=3, pady=(10, 5))

        # creativity force slider
        self.creativity_force_slider_label=ttk.Label(master=params_frame, text="Creativity force", font=('Arial', 14)
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.creativity_force_slider_label.grid(column=2, row=0, columnspan=2, pady=(10, 15))
        creativity_force_density_var = DoubleVar(value=self.society.creativity_force)

        def creativity_force_slider_event(value):
            self.creativity_force_slider_value_label.configure(text=f'{value:.2f}')
            if value != self.society.creativity_force:
                self.society.creativity_force=value
                self.society.new_society()
                self.reset_canvas()

        self.creativity_force_slider = CTkSlider(master=params_frame, fg_color='grey', progress_color=self.PRIMARY_COLOR
                                   , hover=False, button_color=self.PRIMARY_COLOR
			                        , from_=0, to=0.5, number_of_steps=10, variable=creativity_force_density_var, command=creativity_force_slider_event )
        self.creativity_force_slider.grid(column=2, row=1, padx=(20,0))
        self.creativity_force_slider_value_label = ttk.Label(master=params_frame, font=('Arial', 12), text=int(creativity_force_density_var.get())
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.creativity_force_slider_value_label.grid(column=3, row=1, pady=(10, 5))

    #     # field force slider
    #     self.force_slider_label=ttk.Label(master=params_frame, text="Field force", font=('Arial', 14)
	#    , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
    #     self.force_slider_label.grid(column=2, row=2, columnspan=2, pady=(30, 15))
    #     force_density_var = IntVar(value=self.society.field_force)

    #     def force_slider_event(value):
    #         self.force_slider_value_label.configure(text=int(value))
    #         if value != self.society.field_force:
    #             self.society.field_force=value
    #             self.society.new_society()
    #             self.reset_canvas()

    #     self.force_slider = CTkSlider(master=params_frame, fg_color='grey', progress_color=self.PRIMARY_COLOR
    #                                , hover=False, button_color=self.PRIMARY_COLOR
	# 		                        , from_=1, to=4, variable=force_density_var, number_of_steps=3, command=force_slider_event)
    #     self.force_slider.grid(column=2, row=3, padx=(20,0))
    #     self.force_slider_value_label = ttk.Label(master=params_frame, font=('Arial', 12), text=int(force_density_var.get())
	#    , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
    #     self.force_slider_value_label.grid(column=3, row=3, pady=(10, 5))


# BUTTON FRAME

        # button frame
        button_frame=Frame(top_frame, bg=self.BG_COLOR, highlightbackground=self.PRIMARY_COLOR, highlightthickness=2)
        button_frame.grid(column=1, row=0, sticky='WENS')

        # start stop button
        self.start_stop_button = CTkButton(button_frame, width=80, height=50, corner_radius=10, font=("Arial", 14)
                    , text_color=self.BG_COLOR, fg_color=self.PRIMARY_COLOR, hover=False, text="Run", command=self.start_stop_thread)
        self.start_stop_button.grid(column=0, row=0, padx=(30,0), pady=(10, 5))

        # next step button
        self.next_step_button = CTkButton(button_frame, width=80, height=50, corner_radius=10, font=("Arial", 14)
                    , text_color=self.BG_COLOR, fg_color=self.PRIMARY_COLOR, hover=False, text="Next step", command=self.next_step_command)
        self.next_step_button.grid(column=0, row=1, padx=(30,0), pady=(5, 5))

        # reset button
        self.reset_button = CTkButton(
            button_frame, width=80, height=50, corner_radius=10, font=("Arial", 14)
                    , text_color=self.BG_COLOR, fg_color=self.PRIMARY_COLOR, hover=False, text="Reset", command=self.reset_canvas)
        self.reset_button.grid(column=0, row=2, padx=(30,0), pady=(5,10))
        
        # create center panel with widgets
        center_frame = Frame(self.root, height=500)
        center_frame.configure(bg=self.BG_COLOR)
        center_frame.pack(fill=BOTH, expand=True)
        
        # create canvas in center widget
        self.root.update() # needed to use winfo functions (2 lines below)
        center_frame.update()
        self.canvas = CustomCanvas(center_frame, self.society, self, self.PRIMARY_COLOR, self.BG_COLOR, center_frame.winfo_width(), center_frame.winfo_height())
        self.canvas.pack()

        self.root.mainloop() # display window

# ------------- END OF __INIT__ -------------------------

    def start_stop_thread(self):
        if self.canvas.thread_running_event.is_set():
            self.canvas.stop_update()
            self.start_stop_button.configure(text='Run')
            self.set_param_widgets_active(True)
            self.set_next_step_button_active(True)
            self.set_reset_button_active(True)
        else:
            self.canvas.start_update()
            self.start_stop_button.configure(text='Stop')
            self.set_param_widgets_active(False)
            self.set_next_step_button_active(False)
            self.set_reset_button_active(False)
            self.canvas.animate_society()

    def next_step_command(self):
        self.society.next_step()
        self.canvas.draw_society()

    def reset_canvas(self):
        self.set_param_widgets_active(True)
        self.set_run_button_active(True)
        self.set_next_step_button_active(True)
        self.set_reset_button_active(True)  
        self.canvas.init_new()      

    def on_close(self):
        self.canvas.stop_update()
        self.root.destroy()

# v ------------------- ACITIVE / DISACTIVE ------------- v #
    def set_run_button_active(self, is_active:bool):
        if is_active:
            self.start_stop_button.configure(state=NORMAL, fg_color=self.PRIMARY_COLOR)
        else:
            self.start_stop_button.configure(state=DISABLED, fg_color=self.DISABLED_COLOR)

    def set_next_step_button_active(self, is_active:bool):
        if is_active:
            self.next_step_button.configure(state=NORMAL, fg_color=self.PRIMARY_COLOR)
        else:  
            self.next_step_button.configure(state=DISABLED, fg_color=self.DISABLED_COLOR)
    
    def set_reset_button_active(self, is_active:bool):
        if is_active:
            self.reset_button.configure(state=NORMAL, fg_color=self.PRIMARY_COLOR)
        else:
            self.reset_button.configure(state=DISABLED, fg_color=self.DISABLED_COLOR)

    def set_param_widgets_active(self, is_active:bool):
        if is_active:
            self.creativity_mean_slider.configure(state=NORMAL, progress_color=self.PRIMARY_COLOR, button_color=self.PRIMARY_COLOR)
            self.creativity_mean_slider_label.configure(foreground=self.PRIMARY_COLOR)
            self.creativity_mean_slider_value_label.configure(foreground=self.PRIMARY_COLOR)

            self.openness_mean_slider.configure(state=NORMAL, progress_color=self.PRIMARY_COLOR, button_color=self.PRIMARY_COLOR)
            self.openness_mean_slider_label.configure(foreground=self.PRIMARY_COLOR)
            self.openness_mean_slider_value_label.configure(foreground=self.PRIMARY_COLOR)

            self.creativity_force_slider.configure(state=NORMAL, progress_color=self.PRIMARY_COLOR, button_color=self.PRIMARY_COLOR)
            self.creativity_force_slider_label.configure(foreground=self.PRIMARY_COLOR)
            self.creativity_force_slider_value_label.configure(foreground=self.PRIMARY_COLOR)

            # self.force_slider.configure(state=NORMAL, progress_color=self.PRIMARY_COLOR, button_color=self.PRIMARY_COLOR)
            # self.force_slider_label.configure(foreground=self.PRIMARY_COLOR)
            # self.force_slider_value_label.configure(foreground=self.PRIMARY_COLOR)
            
        else:
            self.creativity_mean_slider.configure(state=DISABLED, progress_color=self.DISABLED_COLOR, button_color=self.DISABLED_COLOR)
            self.creativity_mean_slider_label.configure(foreground=self.DISABLED_COLOR)
            self.creativity_mean_slider_value_label.configure(foreground=self.DISABLED_COLOR)

            self.openness_mean_slider.configure(state=DISABLED, progress_color=self.DISABLED_COLOR, button_color=self.DISABLED_COLOR)
            self.openness_mean_slider_label.configure(foreground=self.DISABLED_COLOR)
            self.openness_mean_slider_value_label.configure(foreground=self.DISABLED_COLOR)

            self.creativity_force_slider.configure(state=DISABLED, progress_color=self.DISABLED_COLOR, button_color=self.DISABLED_COLOR)
            self.creativity_force_slider_label.configure(foreground=self.DISABLED_COLOR)
            self.creativity_force_slider_value_label.configure(foreground=self.DISABLED_COLOR)

            # self.force_slider.configure(state=DISABLED, progress_color=self.DISABLED_COLOR, button_color=self.DISABLED_COLOR)
            # self.force_slider_label.configure(foreground=self.DISABLED_COLOR)
            # self.force_slider_value_label.configure(foreground=self.DISABLED_COLOR)

