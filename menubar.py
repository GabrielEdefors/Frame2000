import tkinter as tk

class Menubar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.add_command(label="Dummy command")
        parent.config(menu=self)