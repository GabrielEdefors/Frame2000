import math
import tkinter as tk

from geometry_calculations import coordinates_parallel_line
from load_manager import LoadWindow


class Element:

    """A class representing a beam element

    Instance variables:
        coord: coordinates of the beam, on the format x1, y1, x2, y2
        element_id: The element number, starting at 0

    Attributes:
        Length: The length of the element.
    """

    def __init__(self, coords_canvas, coords_absolute, element_id):
        self.coords_canvas = coords_canvas
        self.coords_absolute = coords_absolute
        self.element_id = element_id

        # Calculate element length
        self.length = math.sqrt(((self.coords_absolute[1, 0] - self.coords_absolute[0, 0]) ** 2) +
                                ((self.coords_absolute[1, 1] - self.coords_absolute[0, 1]) ** 2))

    def draw_element(self, parent):
        """ Method for drawing a line and two nodes representing the element"""

        x1 = self.coords_canvas[0, 0]
        y1 = self.coords_canvas[0, 1]
        x2 = self.coords_canvas[1, 0]
        y2 = self.coords_canvas[1, 1]

        # Draw the widgets
        self.line = parent.canvas.create_line(x1, y1, x2, y2, width=2.5, activefill="red", tag=self.element_id)
        self.node1 = parent.canvas.create_oval(x1 - parent.node_rad, y1 - parent.node_rad, x1 +parent. node_rad,
                           y1 + parent.node_rad, fill="red", tag=self.element_id)
        self.node2 = parent.canvas.create_oval(x2 - parent.node_rad, y2 - parent.node_rad, x2 + parent.node_rad,
                                   y2 + parent.node_rad, fill="red", tag=self.element_id)

        # To get the coordinates of a parallel to the element arrow call coordinates_parallel_line
        offset_annotation_line = 0.5
        length_annotation_line = 0.6
        x1_arrow, y1_arrow, x2_arrow, y2_arrow, x_text_annotation, y_text_annotation = \
            coordinates_parallel_line(x1, y1, x2, y2, self.length, offset_annotation_line, length_annotation_line)

        # Draw the arrow
        self.arrow = parent.canvas.create_line(x1_arrow, y1_arrow, x2_arrow, y2_arrow, width=4,
                                        tag=self.element_id, arrow=tk.LAST)

        # Also create a text annotation with the element number, place it in the middle
        self.text_annotation = parent.canvas.create_text(x_text_annotation, y_text_annotation, fill="black",
                                                  font="calibri 10", tag=self.element_id,
                                                  text=str(self.element_id))

        # bind the current elements widgets to the right click method
        parent.canvas.tag_bind(self.line, '<ButtonRelease-3>', parent.right_click)
        parent.canvas.tag_bind(self.node1, '<ButtonRelease-3>', parent.right_click)
        parent.canvas.tag_bind(self.node2, '<ButtonRelease-3>', parent.right_click)
        parent.canvas.tag_bind(self.arrow, '<ButtonRelease-3>', parent.right_click)
        parent.canvas.tag_bind(self.text_annotation, '<ButtonRelease-3>', parent.right_click)

    def erase_element(self, canvas):
        canvas.delete(self.line)
        canvas.delete(self.node1)
        canvas.delete(self.node2)
        canvas.delete(self.arrow)
        canvas.delete(self.text_annotation)

    def change_tags(self, parent):
        parent.canvas.itemconfig(self.line, tag=self.element_id)
        parent.canvas.itemconfig(self.node1, tag=self.element_id)
        parent.canvas.itemconfig(self.node2, tag=self.element_id)
        parent.canvas.itemconfig(self.arrow, tag=self.element_id)
        parent.canvas.itemconfig(self.text_annotation, tag=self.element_id)
        parent.canvas.itemconfig(self.text_annotation, text=str(self.element_id))

    def add_load(self, parent):

        # Open the load window by calling LoadWindow
        load_window = LoadWindow(self, parent)


        return None






