from tkinter import BOTH, DISABLED, E, NORMAL, W, Frame, IntVar, ttk, DoubleVar
from customtkinter import CTkSlider, CTkButton, BooleanVar, CTkSwitch, CTkCheckBox, CTkRadioButton, CTk

from canvas import CustomCanvas

class Window():
    # FIELDS:
    # root
    # canvas
    # start_stop_button

    # Define lead colors for window
    PRIMARY_COLOR = "gold"
    BG_COLOR = "midnightblue"

    def __init__(self):
        self.root = CTk()
        self.root.geometry("900x700") # Window size
        self.root.title("Group Creativity")
        self.root.resizable(0, 0) # No full-screen
        self.root.protocol("WM_DELETE_WINDOW", self.on_close) # stop thread on close

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
        self.creativity_slider_label=ttk.Label(master=params_frame, text="Creative agents density", font=('Arial', 14)
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.creativity_slider_label.grid(column=0, row=0, columnspan=2, pady=(10, 15))
        creativity_density_var = DoubleVar(value=0.5)

        def creativity_slider_event(value):
            self.creativity_slider_value_label.configure(text=f'{value:.2f}')

        langton_slider = CTkSlider(master=params_frame, fg_color='grey', progress_color=self.PRIMARY_COLOR
                                   , hover=False, button_color=self.PRIMARY_COLOR
			                        , from_=0, to=1, variable=creativity_density_var, command=creativity_slider_event)
        langton_slider.grid(column=0, row=1, padx=(20,0))
        self.creativity_slider_value_label = ttk.Label(master=params_frame, font=('Arial', 12), text=f"{creativity_density_var.get():.2f}"
	   , foreground=self.PRIMARY_COLOR, background=self.BG_COLOR)
        self.creativity_slider_value_label.grid(column=1, row=1, pady=(10, 5))


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
        self.canvas = CustomCanvas(center_frame, self.PRIMARY_COLOR, self.BG_COLOR, center_frame.winfo_width(), center_frame.winfo_height())
        self.canvas.pack()

        self.root.mainloop() # display window

# ------------- END OF __INIT__ -------------------------

    def start_stop_thread(self):
        if self.canvas.thread_running_event.is_set():
            self.canvas.stop_update()
            self.start_stop_button.configure(text='Run')
        else:
            self.canvas.start_update()
            self.start_stop_button.configure(text='Stop')
            self.canvas.animate_society()

    def next_step_command(self):
        self.canvas.draw_next_step()

    def reset_canvas(self):
        self.canvas.init_new()

    def on_close(self):
        self.canvas.stop_update()
        self.root.destroy()