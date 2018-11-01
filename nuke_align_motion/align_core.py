from PySide2 import QtWidgets, QtCore
import math

from nuke_align_motion import interface
from nuke_align_motion.settings import THRESHOLD
# from nuke_align_motion import nuke_funcs

reload(interface)
# reload(nuke_funcs)


class Controller:

    def __init__(self):
        global interface_
        interface_ = interface.Interface()
        interface_.show()
        self.set_up_signals()

    def set_up_signals(self):
        interface_.trigger.connect(self.align_nodes)

    @QtCore.Slot(object)
    def align_nodes(self, values):
        start_pos, end_pos = values
        angle = self.analyze_angle(start_pos, end_pos)
        direction = self.get_direction(angle)
        # nuke_funcs.align_nodes(direction, angle)
        print(angle)
        print(direction)

    @staticmethod
    def get_direction(angle):

        if abs(angle) < THRESHOLD:
            direction = 'horizontal'
        elif 90 - abs(angle) < THRESHOLD:
            direction = 'vertical'
        else:
            direction = 'diagonal'

        return direction

    @staticmethod
    def analyze_angle(start, end):

        hypotenuse = end[0] - start[0]
        if hypotenuse == 0:
            return 90
        else:
            opposite = end[1] - start[1]
            return math.degrees(math.atan(opposite/float(hypotenuse)))


def start():
    """Start up function."""
    controller = Controller()


def start_from_main():
    app = QtWidgets.QApplication()
    controller = Controller()
    app.exec_()


if __name__ == '__main__':
    start_from_main()
