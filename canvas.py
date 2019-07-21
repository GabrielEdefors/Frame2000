import tkinter as tk


class Canvas(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Create the canvas object
        self.scrollregion_dimension = 10000
        self.canvas = tk.Canvas(self, bg='#FFFFFF',
                                scrollregion=(0, 0, 2 * self.scrollregion_dimension, self.scrollregion_dimension))

        # Create scrollbars for canvas
        self.scrollbars()
        self.canvas.pack(side="left", expand=True, fill="both")

        # Create grid
        self.gridsize_w = 50
        self.gridsize_h = 50
        self.create_grid()

        # Bind a zoom method
        self.scale = 1
        self.canvas.bind("<MouseWheel>", self.zoomer)

        # Monitor mouse click for node positions
        self.canvas.bind("<ButtonPress-1>", self.monitor_mouseclick)

    def scrollbars(self):
        hbar = tk.Scrollbar(self, orient="horizontal")
        hbar.pack(side="bottom", fill="x")
        hbar.config(command=self.canvas.xview)
        vbar = tk.Scrollbar(self, orient="vertical")
        vbar.pack(side="right", fill="y")
        vbar.config(command=self.canvas.yview)

        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    def create_grid(self):

        for i in range(0, 2 * self.scrollregion_dimension, self.gridsize_w):
            self.canvas.create_line([(i, 0), (i, self.scrollregion_dimension)])

        for i in range(0, self.scrollregion_dimension, self.gridsize_h):
            self.canvas.create_line([(0, i), (2 * self.scrollregion_dimension, i)])

    def monitor_mouseclick(self, event):

        # Get the position relative the canvas
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)

        # Get the absolute position
        x = event.x
        y = event.y

        # Round to grid
        x = self.gridsize_w * self.scale * round(x_canvas / self.gridsize_w * self.scale)
        y = self.gridsize_h * self.scale * round(y_canvas / self.gridsize_h * self.scale)

        # Draw a node when clicked
        rad = self.scrollregion_dimension / 1000 * self.scale
        self.canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill="red")

    def zoomer(self,event):
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)

            # Track scaling
            self.scale *= 1.1
        elif event.delta < 0:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)

            # Track scaling
            self.scale *= 0.9
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))


