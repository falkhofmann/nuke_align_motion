import nuke

from nuke_align_motion import controller


menubar = nuke.menu('Nuke')
toolbar = nuke.menu('Nodes')
for menu in menubar, toolbar:
    menu.addMenu("fhofmann").addCommand("motion align", 'controller.start()', "f3")
