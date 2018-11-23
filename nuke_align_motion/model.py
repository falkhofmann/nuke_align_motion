import math

import nuke


def align_nodes(direction, angle, h_direction, v_direction):

    nodes = nuke.selectedNodes()

    edges = get_edge_nodes(nodes)

    if direction == 'horizontal':
        if h_direction == -1:
            reference = edges['west']
        else:
            reference = edges['east']
        align_horizontal(reference, nodes)

    elif direction == 'vertical':
        if v_direction == 1:
            reference = edges['north']
        else:
            reference = edges['south']
        align_vertical(reference, nodes)
    else:
        pass


def align_horizontal(reference, nodes):

    for node in nodes:
        node.knob('ypos').setValue(reference.ypos())


def align_vertical(reference, nodes):
    for node in nodes:
        node.knob('xpos').setValue(reference.xpos())


def align_diagonal(nodes, edges, h_direction, v_direction, angle):

    selection = nodes
    if h_direction == 1:
        x_start = edges['east']
    else:
        x_start = edges['west']

    for node in selection:
        if node is not x_start:
            ankathete = abs(node.xpos() - x_start.xpos())
            vertical_distance = ankathete * math.tan(angle)
            node['ypos'].setValue(node.ypos() + vertical_distance)


def get_direction(start_pos, end_pos):

    if start_pos[0] - end_pos[0] < 0:
        x_direction = 1
    else:
        x_direction = -1

    if start_pos[1] - end_pos[1] < 0:
        y_direction = -1
    else:
        y_direction = 1

    return x_direction, y_direction


def get_edge_nodes(nodes):

    east, west, north, south = nodes[0], nodes[0], nodes[0], nodes[0]

    for node in nodes:
        if node.xpos() < east.xpos():
            east = node
        if node.xpos() > west.xpos():
            west = node
        if node.ypos() < south.ypos():
            south = node
        if node.ypos() > north.ypos():
            north = node

    return {'east': east, 'west': west, 'north': north, 'south': south}


def validate_selection():
    return True if nuke.selectedNodes() else False
