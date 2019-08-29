import math

def coordinates_parallel_line(x1, y1, x2, y2, length_element, delta, length_line):

    # Length factor
    length_factor = length_line / length_element

    # Coordinate distances
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Coordinate displacements
    displacement_x = delta_y * delta / length_element
    displacement_y = -delta_x * delta / length_element

    # New coordinates
    x1_offset = x1 + delta_x * (1-length_factor)/2 + displacement_x
    y1_offset = y1 + (1-length_factor)/2 * delta_y + displacement_y
    x2_offset = x2 - (1-length_factor)/2 * delta_x + displacement_x
    y2_offset = y2 - (1-length_factor)/2 * delta_y + displacement_y

    # Calculate the coordinates for the element text, place in the middle with twice the offset
    x_text_annotation = x1 + delta_x / 2 + displacement_x * 2
    y_text_annotation = y1 + delta_y / 2 + displacement_y * 2

    return x1_offset, y1_offset, x2_offset, y2_offset, x_text_annotation, y_text_annotation

