# import built-in modules
import math

# Import third party modules
import nuke

from nuke_align_motion import settings


def align_nodes(direction, h_direction, v_direction):

    nodes = nuke.selectedNodes()

    edges = get_edge_nodes(nodes)

    if direction == 'horizontal':
        if h_direction == -1:
            reference = edges['west']
        else:
            reference = edges['east']
        if check_threshold(reference, nodes, 'xpos'):
            spread_along_axis(nodes, reference, h_direction, 'xpos')
        align_horizontal(reference, nodes)

    elif direction == 'vertical':
        if v_direction == 1:
            reference = edges['north']
        else:
            reference = edges['south']
        if check_threshold(reference, nodes, 'ypos'):
            spread_along_axis(nodes, reference, -v_direction, 'ypos')
        align_vertical(reference, nodes)

    else:
        align_diagonal(nodes, h_direction, v_direction)


def align_horizontal(reference, nodes):
    for node in nodes:
        node.knob('ypos').setValue(reference.ypos())


def align_vertical(reference, nodes):
    for node in nodes:
        node.knob('xpos').setValue(reference.xpos())


def align_diagonal(nodes, h_direction, v_direction):

    sorted_nodes = sorted(nodes, key=lambda node: node.xpos()*h_direction)
    x_start = sorted_nodes[0]

    for node in sorted_nodes:
        if node is not x_start:
            ankathete = abs(x_start.xpos() - node.xpos())
            gegenkathete = abs(math.sin(45) * abs(ankathete))
            node['ypos'].setValue(x_start.ypos() - (gegenkathete * v_direction))


def spread_along_axis(nodes, reference, direction, axis):
    for index, node in enumerate(nodes):
        offset = index * settings.DEFAULT_DISTANCE * direction
        node.knob(axis).setValue(reference[axis].value()+offset)


def check_threshold(reference, nodes, axis):

    include = [node for node in nodes if abs(reference[axis].value() - node[axis].value()) < abs(node[axis].value())/settings.THRESHOLD_DISTANCE]

    if include == nodes:
        return True
    else:
        return False


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
