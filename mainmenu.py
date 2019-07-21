import tkinter as tk

class MainMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Create labelframe
        main_frame = tk.LabelFrame(self, text="Main menu")
        main_frame.pack(fill="both", expand=1, )
        label = tk.Label(main_frame, text="Dummy label 1 and some white space")
        label.pack()