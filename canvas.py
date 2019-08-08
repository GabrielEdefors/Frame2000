import tkinter as tk
import numpy as np
from element import Element


class Canvas(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Create the canvas object
        self.scrollregion_dimension = 10000
        self.canvas = tk.Canvas(self, bg='#FFFFFF',
                                scrollregion=(-self.scrollregion_dimension, -self.scrollregion_dimension / 2, self.scrollregion_dimension, self.scrollregion_dimension / 2))

        # Create scrollbars for canvas
        self.scrollbars()
        self.canvas.pack(side="left", expand=True, fill="both")

        # Bind a zoom method
        self.scale = 1
        self.canvas.bind("<MouseWheel>", self.zoomer)

        # Create grid
        self.gridsize_w = 50
        self.gridsize_h = 50
        self.create_grid()

        # Monitor mouse click for node positions
        self.coord_nodes = np.empty((0, 2), float)

        # Set iteration flag and call monitor_mouseclick
        self.monitor_mouseclick_flag = 0
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

        a = self.canvas.bbox("all")
        for i in range(-self.scrollregion_dimension, self.scrollregion_dimension, self.gridsize_w):
            self.canvas.create_line([(i, -int(-self.scrollregion_dimension / 2)),
                                     (i, int(-self.scrollregion_dimension / 2))])

        for i in range(int(-self.scrollregion_dimension / 2), int(self.scrollregion_dimension / 2), self.gridsize_h):
            self.canvas.create_line([(-self.scrollregion_dimension, i), (self.scrollregion_dimension, i)])

    def monitor_mouseclick(self, event):

        # Get the position relative the canvas
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)

        # Get the absolute position
        x = event.x
        y = event.y

        # Round to grid
        x = self.gridsize_w * self.scale * round(x_canvas / (self.gridsize_w * self.scale))
        y = self.gridsize_h * self.scale * round(y_canvas / (self.gridsize_h * self.scale))

        # Draw a node when a click occurs
        rad = self.scrollregion_dimension / 1000 * self.scale
        self.canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill="red")

        # Save the coordinates
        self.coord_nodes = np.append(self.coord_nodes, [[x, y]], axis=0)

        # When second node is drawn call the element class to create an element
        if self.monitor_mouseclick_flag == 1:

            # Append instance to the list
            self.parent.element_list.append(Element(self.coord_nodes))

        # Draw a line between each other node
        # x1 = self.coord_nodes[self.monitor_mouseclick_flag-1, 0]
        # y1 = self.coord_nodes[self.monitor_mouseclick_flag-1, 1]
        # x2 = self.coord_nodes[self.monitor_mouseclick_flag, 0]
        # y2 = self.coord_nodes[self.monitor_mouseclick_flag, 1]
        # self.canvas.create_line(x1, y1, x2, y2, width=2.5, activefill="red")

        # Save

        # Update flag
        self.monitor_mouseclick_flag += 1

        # Two clicks yields a new element, reset flag and coordinates
        if self.monitor_mouseclick_flag > 1:
            self.monitor_mouseclick_flag = 0
            self.coord_nodes = np.empty((0, 2), float)

    def zoomer(self,event):

        if event.delta > 0:
            zoomin_coefficient = 1.1
            self.canvas.scale("all", 0, 0, zoomin_coefficient, zoomin_coefficient)

            # Track scaling
            self.scale *= 1.1

            # Scale the last coordinate for correct line drawing
            self.coord_nodes[-1, :] *= zoomin_coefficient

        elif event.delta < 0:
            zoomout_coefficient = 0.9
            self.canvas.scale("all", 0, 0, zoomout_coefficient, zoomout_coefficient)

            # Track scaling
            self.scale *= 0.9

            # Scale the last coordinate for correct line drawing
            self.coord_nodes[-1, :] *= zoomout_coefficient
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))






