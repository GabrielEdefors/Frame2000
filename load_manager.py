import tkinter as tk

from load_drawer import transversal_load


class LoadWindow(tk.Tk):
    """A class for managing load input for elements

        Instance variables:
            edof: An noe x 7 array on the form array([[el_1, dof1, dof2...dof6],
            [el_noe, dof1, dof2...dof6]])
    """

    def __init__(self, element_parent, canvas_parent):
        tk.Tk.__init__(self)
        self.title("Load Manager")
        self.iconbitmap('icon_beam_2000.ico')
        self.resizable(False,False)

        # Set the dimensions
        self.width = 700
        self.height = 400
        self.geometry("x".join([str(self.width), str(self.height)]))

        # Create a frame for storing the label frames
        self.left_frame = tk.Frame(self, width=self.width / 3, height=self.height)
        self.left_frame.pack(side="left", fill="y", expand="true")

        # Create a frame for storing the canvas
        self.canvas_load = tk.Frame(self)
        self.canvas_load.pack()

        # Create a label frame for each load case
        self.labelframe_transverse()
        self.labelframe_axial()
        self.labelframe_nodal()

        # Define the canvas size which the element will be drawn onto
        self.width_canvas = self.width * 2 / 3
        self.height_canvas = self.height

        # Create a canvas to the right of the label frames
        self.canvas_illustration = tk.Canvas(self.canvas_load, width=self.width_canvas, height=self.height_canvas)
        self.canvas_illustration.pack(expand=True, fill="both")

        # Create an illustration of the loading scenario
        self.add_illustration(element_parent, canvas_parent)

    def labelframe_transverse(self):

        # Add a label frame
        frame_transverse = tk.LabelFrame(self.left_frame, text="Transverse Line Load")
        frame_transverse.place(x=0, y=0, anchor="nw", width=self.width / 3, height=self.height / 3)

        # Add a menu for choosing load direction
        menu_transverse_options = ['Positive', 'Negative']

        initial_value_transverse = tk.StringVar(frame_transverse)
        initial_value_transverse.set(menu_transverse_options[0])

        popupMenu = tk.OptionMenu(frame_transverse, initial_value_transverse, *menu_transverse_options)
        popupMenu.grid(row=0, column=1)

        # Add a Label for the load direction menu
        label_transverse = tk.Label(frame_transverse, text="Choose Load Direction")
        label_transverse.grid(row=0, column=0)

    def labelframe_axial(self):

        # Add a label frame
        frame_axial = tk.LabelFrame(self.left_frame, text="Axial Line Load", width=self.width / 3)
        frame_axial.place(x=0, y=self.height / 3, anchor="nw", width=self.width / 3, height=self.height / 3)

        # Add a menu for choosing load direction
        menu_axial_options = ['Positive', 'Negative']

        initial_value_axial = tk.StringVar(frame_axial)
        initial_value_axial.set(menu_axial_options[0])

        popupMenu = tk.OptionMenu(frame_axial, initial_value_axial, *menu_axial_options)
        popupMenu.grid(row=0, column=1)

        # Add a Label for the load direction menu
        label_axial = tk.Label(frame_axial, text="Choose Load Direction")
        label_axial.grid(row=0, column=0)

    def labelframe_nodal(self):
        # Add a label frame
        frame_nodal = tk.LabelFrame(self.left_frame, text="Nodal point load", width=self.width / 3)
        frame_nodal.place(x=0, y=self.height * 2 / 3, anchor="nw", width=self.width / 3, height=self.height / 3)

        # Add a menu for choosing load direction
        menu_nodal_options = ['Positive', 'Negative']

        initial_value_nodal = tk.StringVar(frame_nodal)
        initial_value_nodal.set(menu_nodal_options[0])

        popupMenu = tk.OptionMenu(frame_nodal, initial_value_nodal, *menu_nodal_options)
        popupMenu.grid(row=0, column=1)

        # Add a Label for the load direction menu
        label_nodal = tk.Label(frame_nodal, text="Choose Load Direction")
        label_nodal.grid(row=0, column=0)

    def add_illustration(self, element_parent, canvas_parent):

        x1 = element_parent.coords_canvas[0, 0]
        y1 = element_parent.coords_canvas[0, 1]
        x2 = element_parent.coords_canvas[1, 0]
        y2 = element_parent.coords_canvas[1, 1]

        # Real distances between the nodes
        delta_x = abs(x2 - x1)
        delta_y = abs(y2 - y1)

        # Determine the scale factor from either the width or height
        if delta_x > self.width_canvas and delta_y < self.height_canvas:
            scale_factor = self.width_canvas / delta_x

        elif delta_y > self.height_canvas and delta_x < self.width_canvas:
            scale_factor = self.height_canvas / delta_y

        elif delta_x > self.width_canvas and delta_y > self.height_canvas:
            scale_factor = min(self.width_canvas / delta_x, self.width_canvas / delta_x)

        else:
            scale_factor = 1

        # Also define a margin to the borders
        margin_factor = 0.8

        # Scale the element to fit the canvas size
        delta_x_scaled = (x2 - x1) * scale_factor * margin_factor
        delta_y_scaled = (y2 - y1) * scale_factor * margin_factor

        x1 = self.width_canvas / 2 - delta_x_scaled / 2
        y1 = self.height_canvas / 2 - delta_y_scaled / 2
        x2 = self.width_canvas / 2 + delta_x_scaled / 2
        y2 = self.height_canvas / 2 + delta_y_scaled / 2

        # Node radius
        node_rad = canvas_parent.node_rad

        line = self.canvas_illustration.create_line(x1, y1, x2, y2, width=2.5, activefill="red")
        node1 = self.canvas_illustration.create_oval(x1 - node_rad, y1 - node_rad, x1 + node_rad,
                                                y1 + node_rad, fill="red")
        node2 = self.canvas_illustration.create_oval(x2 - node_rad, y2 - node_rad, x2 + node_rad,
                                                y2 + node_rad, fill="red")

        # Call the methods in load drawer to draw the loads
        magnitude_transversal = -10
        direction = "positive"

        transversal_load(x1, y1, x2, y2, magnitude_transversal, direction, element_parent.length, self.canvas_illustration)




