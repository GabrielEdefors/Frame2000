
class Element:

    """A class representing a beam element

    Instance variables:
        coord: coordinates of the beam, on the format x1, y1, x2, y2
        element_id: The element number, starting at 0

    Attributes:
        Length: The length of the elment.
    """

    def __init__(self, coord, element_id):
        self.coords = coord
        self.element_id = element_id
        self.length = ((self.coords[1, 0] - self.coords[0, 0]) ** 2 + (self.coords[1, 1] - self.coords[1, 0]) ** 2) ** 0.5
        # print(self.length)

    def draw_element(self, canvas, node_rad):
        """ Method for drawing a line and two nodes representing the element"""

        x1 = self.coords[0, 0]
        y1 = self.coords[0, 1]
        x2 = self.coords[1, 0]
        y2 = self.coords[1, 1]
        self.line = canvas.create_line(x1, y1, x2, y2, width=2.5, activefill="red", tag=self.element_id)
        self.node1 = canvas.create_oval(x1 - node_rad, y1 - node_rad, x1 + node_rad,
                           y1 + node_rad, fill="red", tag=self.element_id)
        self.node2 = canvas.create_oval(x2 - node_rad, y2 - node_rad, x2 + node_rad,
                                   y2 + node_rad, fill="red", tag=self.element_id)

        # Return the handles of the widgets for current element
        return self.line, self.node1, self.node2


    def erase_element(self, canvas):
        canvas.delete(self.line)
        canvas.delete(self.node1)
        canvas.delete(self.node2)





