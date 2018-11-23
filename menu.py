
import nuke

from nuke_align_motion import controller


menubar = nuke.menu('Nuke')
toolbar = nuke.menu('Nodes')
for menu in menubar, toolbar:
    if menu == menubar:
        fhofmann = menu.addMenu("fhofmann")
    else:
        fhofmann = menu.addMenu("fhofmann")

    fhofmann.addCommand("motion align", 'align_motion()', "f3")


def align_motion():
    reload(controller)
    controller.start()
