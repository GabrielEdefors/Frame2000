import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
import numpy as np

from element import Element


class Canvas(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Create the canvas object
        self.scrollregion_dimension = 10000
        self.canvas = tk.Canvas(self, bg='#FFFFFF',
                                scrollregion=(-self.scrollregion_dimension, -self.scrollregion_dimension / 2,
                                self.scrollregion_dimension, self.scrollregion_dimension / 2))

        # Create scrollbars for canvas
        self.scrollbars()
        self.canvas.pack(side="left", expand=True, fill="both")

        # Bind a zoom method
        self.scale = 1
        self.canvas.bind("<MouseWheel>", self.zoomer)

        # Number of pixels per grid line
        self.grid_scalefactor = 50
        self.gridsize_w = self.grid_scalefactor
        self.gridsize_h = self.grid_scalefactor

        # Number of meters per grid line
        self.nmeters_gridline = 0.5

        # Call the method create_grid to draw the grid
        self.create_grid()

        # Create scalebar
        self.scalebar_l1_init = 1
        self.scalebar_l2_init = 5

        # Before zooming we have the initial scale bar lengths
        self.scalebar_l1 = self.scalebar_l1_init * round(self.scale, 2)
        self.scalebar_l2 = self.scalebar_l2_init * round(self.scale, 2)

        # Call the method create_scalebar to create the scalebar
        self.create_scalebar()

        # Monitor mouse click for node positions
        self.coord_nodes_canvas = np.empty((0, 2), float)
        self.coord_nodes_absolute = np.empty((0, 2), float)

        # Set an iteration flag for keeping track of first or second node of elements
        self.monitor_mouseclick_flag = 0

        # And a flag for keeping track of element number
        self.element_flag = 0

        # Bind the monitor mouseclick method to the left mouse button
        self.canvas.bind("<ButtonPress-1>", self.monitor_mouseclick)

        # Create a list for storing line tags
        self.line_ids = []

        # Define the size of the nodes drawn
        self.node_rad_init = self.scrollregion_dimension / 1500

        # Before zooming same as the initial radius
        self.node_rad = self.node_rad_init

    def scrollbars(self):

        # Create a horizontal scrollbar and pack it in the bottom of the frame
        hbar = tk.Scrollbar(self, orient="horizontal")
        hbar.pack(side="bottom", fill="x")
        hbar.config(command=self.canvas.xview)

        # Create a horizontal scrollbar and pack it in the bottom of the frame
        vbar = tk.Scrollbar(self, orient="vertical")
        vbar.pack(side="right", fill="y")
        vbar.config(command=self.canvas.yview)

        # Assign the scrollbars to the canvas
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    def create_grid(self):

        # Loop through each x-coordinate in the scroll region and draw grid lines
        for i in range(-self.scrollregion_dimension, self.scrollregion_dimension, self.gridsize_w):
            self.canvas.create_line([(i, -int(-self.scrollregion_dimension / 2)),
                                     (i, int(-self.scrollregion_dimension / 2))])

        # Loop through each y-coordinate in the scroll region and draw grid lines
        for i in range(int(-self.scrollregion_dimension / 2), int(self.scrollregion_dimension / 2), self.gridsize_h):
            self.canvas.create_line([(-self.scrollregion_dimension, i), (self.scrollregion_dimension, i)])

    def monitor_mouseclick(self, event):

        # Get the position relative the canvas
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)

        # Round to grid
        x_canvas_round = self.gridsize_w * self.scale * round(x_canvas / (self.gridsize_w * self.scale))
        y_canvas_round = self.gridsize_h * self.scale * round(y_canvas / (self.gridsize_h * self.scale))

        # Round to grid and scale coordinates for future computations
        x_absolute_round = self.gridsize_w * round(event.x / (self.gridsize_w * self.scale))\
                           / self.grid_scalefactor * self.nmeters_gridline

        y_absolute_round = self.gridsize_h * round(event.y / (self.gridsize_h * self.scale))\
                           / self.grid_scalefactor * self.nmeters_gridline

        # Draw a node when a click occurs
        self.canvas.create_oval(x_canvas_round-self.node_rad, y_canvas_round-self.node_rad, x_canvas_round+self.node_rad,
                                y_canvas_round+self.node_rad, fill="red", tag="temp_node")

        # Save the coordinates
        self.coord_nodes_canvas = np.append(self.coord_nodes_canvas, [[x_canvas_round, y_canvas_round]], axis=0)
        self.coord_nodes_absolute = np.append(self.coord_nodes_absolute, [[x_absolute_round, y_absolute_round]], axis=0)

        # When second node is drawn call the element class to create an element
        if self.monitor_mouseclick_flag == 1:

            # Append instance to the list
            self.parent.element_list.append(Element(self.coord_nodes_canvas,
                                                    self.coord_nodes_absolute,
                                                    self.element_flag))

            # Delete the two previous nodes
            self.canvas.delete('temp_node')

            # Use the draw element method to draw a line and two nodes representing the current element
            self.parent.element_list[-1].draw_element(self)

            # Update the element flag
            self.element_flag += 1

        # Update mouse click flag
        self.monitor_mouseclick_flag += 1

        # Two clicks yields a new element, reset flag and coordinates
        if self.monitor_mouseclick_flag > 1:
            self.monitor_mouseclick_flag = 0
            self.coord_nodes_canvas = np.empty((0, 2), float)
            self.coord_nodes_absolute = np.empty((0, 2), float)

    def zoomer(self,event):

        # Zoom in if delta>0
        if event.delta > 0:

            # Calculate the zoom in coefficient such that the scale is a multiple of the initial scale
            zoomin_coefficient = 2

            # Restrict the maximum zooming to 2x
            if self.scale < 4:
                self.canvas.scale("all", 0, 0, zoomin_coefficient, zoomin_coefficient)

                # Track scaling
                self.scale *= zoomin_coefficient

                # Update node radius
                self.node_rad = self.node_rad_init * self.scale

                # Update the scalebar
                self.scalebar_l1 = self.scalebar_l1_init / round(self.scale, 2)
                self.scalebar_l2 = self.scalebar_l2_init / round(self.scale, 2)

                # Reload the scalebar
                self.create_scalebar()

        # Zoom out if delta>0
        elif event.delta < 0:
            zoomout_coefficient = 0.5

            # Restrict the minimum zooming to 0.5x
            if self.scale > 0.25:
                self.canvas.scale("all", 0, 0, zoomout_coefficient, zoomout_coefficient)

                # Track scaling
                self.scale *= zoomout_coefficient

                # Update node radius
                self.node_rad = self.node_rad_init * self.scale

                # Update the scalebar
                self.scalebar_l1 = self.scalebar_l1_init / round(self.scale, 2)
                self.scalebar_l2 = self.scalebar_l2_init / round(self.scale, 2)

                # Reload the scalebar
                self.create_scalebar()

        # Bind all widgets on the canvas to the zoom method
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def right_click(self, event):

        # Get the canvas coordinates coordinates
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        # Find the item closest to the click
        item = self.canvas.find_closest(x, y)[0]

        # And the element that belongs to
        element_id = int(self.canvas.gettags(item)[0])

        # Call the method element_popup when with the current element as argument
        self.element_popup(element_id, event)

    def element_popup(self, element_id, event):

        # create a menu
        popup = tk.Menu(self, tearoff=0)
        popup.add_command(label="Delete Element")
        popup.add_command(label="Add Element Load")
        popup.add_separator()
        popup.add_command(label="Back")

        # Add a command for the delete element button
        popup.entryconfig("Delete Element", command=lambda: self.delete_element(element_id))

        # Add a command for the add element load
        popup.entryconfig("Add Element Load", command=lambda: self.parent.element_list[element_id].add_load(self))

        # Display the popup
        try:
            popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            popup.grab_release()

    def delete_element(self, element_id):

        # Call the elements method erase_element to delete widgets
        self.parent.element_list[element_id].erase_element(self.canvas)

        # Remove the instance from the instance list
        del self.parent.element_list[element_id]

        # Move all element_ids down one step for element numbers above the one deleted
        for index, element in enumerate(self.parent.element_list):
            if index >= element_id:
                element.element_id -= 1

                # Change the tags associated with the element
                element.change_tags(self)

        # Subtract 1 from the element flag
        self.element_flag -= 1

    def create_scalebar(self):

        # Create two text strings with 2 decimal places
        str1 = str("{:.1f}".format(self.scalebar_l1)).format("%.2f") + "m"
        str2 = str("{:.1f}".format(self.scalebar_l2)).format("%.2f") + "m" + "\n"

        # Join text 1 and 2 with adequate space to fit the image
        scalebar_string = (" " * 20).join([" ", str1])
        scalebar_string = (" " * 123).join([scalebar_string, str2])

        # Load image
        scalebar_image = tkinter.PhotoImage(file='scalebar.png')

        # Create a label with the frame self as parent
        label_scalebar = tk.Label(self, image=scalebar_image, text=scalebar_string, compound=tkinter.CENTER,
                                  anchor='w', justify="left")

        # Place it in the lower left corner
        label_scalebar.place(relx=0.03, rely=0.965, anchor="sw")
        label_scalebar.image = scalebar_image







