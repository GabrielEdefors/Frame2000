import tkinter as tk
import tkinter.messagebox
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

        # Set an iteration flag for keeping track of first or second node of elements
        self.monitor_mouseclick_flag = 0

        # And a flag for keeping track of element number
        self.element_flag = 0

        # Bind the monitor mouseclick method to the left mouse button
        self.canvas.bind("<ButtonPress-1>", self.monitor_mouseclick)

        # Create a list for storing line tags
        self.line_ids = []

        # Define the size of the nodes drawn
        self.node_rad = self.scrollregion_dimension / 1000 * self.scale

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
        self.canvas.create_oval(x-self.node_rad, y-self.node_rad, x+self.node_rad,
                                          y+self.node_rad, fill="red", tag="temp_node")

        # Save the coordinates
        self.coord_nodes = np.append(self.coord_nodes, [[x, y]], axis=0)

        # When second node is drawn call the element class to create an element
        if self.monitor_mouseclick_flag == 1:

            # Append instance to the list
            self.parent.element_list.append(Element(self.coord_nodes, self.element_flag))

            # Delete the two previous nodes
            self.canvas.delete('temp_node')

            # Use the draw element method to draw a line and two nodes representing the current element
            line, node1, node2 = self.parent.element_list[-1].draw_element(self.canvas, self.node_rad)

            # bind the current element to the right click method
            self.canvas.tag_bind(line, '<ButtonPress-3>', self.right_click)
            self.canvas.tag_bind(node1, '<ButtonPress-3>', self.right_click)
            self.canvas.tag_bind(node2, '<ButtonPress-3>', self.right_click)


            # Update the element flag
            self.element_flag += 1

        # Update mouse click flag
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
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def right_click(self, event):

        # Get the absolute coordinates
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        # Find the item closest to the click
        item = self.canvas.find_closest(x, y)[0]

        # And the element that belongs to
        element_id = int(self.canvas.gettags(item)[0])

        # Call the method delete_element_prompt
        left_click_button = tk.Button(self.canvas, text='Exit Application', command=self.delete_element_prompt)
        self.delete_element_prompt(element_id)

        # Remove the instance from the instance list

    def delete_element_prompt(self, element_id):
        message_box = tk.messagebox.askquestion("Delete element", "Are You Sure?", icon='warning')

        if message_box == 'yes':
            # Call the elements method delete widgets
            self.parent.element_list[element_id].erase_element(self.canvas)
        else:
            tk.messagebox.showinfo('Return', 'Thought so')







