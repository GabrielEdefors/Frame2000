import tkinter as tk
import numpy as np

from mainmenu import MainMenu
from canvas import Canvas
from menubar import Menubar


class CreateGUI(tk.Tk):
    """The main class for the program

        Instance variables:
            edof: An noe x 7 array on the form array([[el_1, dof1, dof2...dof6],
            [el_noe, dof1, dof2...dof6]])
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Frame 2000")
        self.state('zoomed')
        self.iconbitmap('icon_beam_2000.ico')
        self.resizable(False,False)

        # Create a list for storing instances of the element class
        self.element_list = []

        # Create a dictionary to store the topology information
        self.edof = np.empty((0, 7), float)

        # Create instances of window content
        self.menubar = Menubar(self)
        self.canvas = Canvas(self)
        self.main_menu = MainMenu(self)

        # Place the instances in the window
        self.canvas.pack(side="left", fill="both", expand=1, pady=20, padx=20)
        self.main_menu.pack(side="right", fill=tk.Y, padx=10)

if __name__ == "__main__":
    app= CreateGUI()
    app.mainloop()
