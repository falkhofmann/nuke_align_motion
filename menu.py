import nuke

from nuke_align_motion import controller


menubar = nuke.menu('Nuke')
toolbar = nuke.menu('Nodes')
for menu in menubar, toolbar:
    if menu == menubar:
        fhofmann = menu.addMenu("fhofmann")
    else:
        fhofmann = menu.addMenu("fhofmann")

    fhofmann.addCommand("motion align", 'controller.start()', "f3")

