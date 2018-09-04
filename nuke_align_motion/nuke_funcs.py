import nuke


def align_nodes(direction, angle):
    nodes = nuke.selectednodes()

    first = nodes[0]
    last = nodes[-1]

    if direction == 'horizontal':
        align_horizontal(first, nodes)
    elif direction == 'vertical':
        align_vertical(first, nodes)
    else:
        align_diagonal(nodes, first, last, angle)


def align_horizontal(reference, nodes):

    for node in nodes:
        node.setXPos(reference.xpos())


def align_vertical(reference, nodes):
    for node in nodes:
        node.setYPos(reference.ypos())


def align_diagonal(nodes, first, last, angle):

    previos_node = first

    for node in nodes:
        distance = node.xpos() - previos_node.xpos()
