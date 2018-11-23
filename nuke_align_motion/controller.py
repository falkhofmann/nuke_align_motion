import math

from nuke_align_motion import view
from nuke_align_motion.settings import THRESHOLD
from nuke_align_motion import model

reload(view)
reload(model)


class Controller:

    def __init__(self, view):
        self.view = view
        self.set_up_signals()

    def set_up_signals(self):
        self.view.trigger.connect(lambda x: self.align_nodes(x))

    def align_nodes(self, values):

        start_pos, end_pos = values

        h_direction, v_direction = model.get_direction(start_pos, end_pos)

        angle = self.analyze_angle(start_pos, end_pos)
        alignment = self.get_alignment(angle)
        model.align_nodes(alignment, angle, h_direction, v_direction)

    @staticmethod
    def get_alignment(angle):

        if abs(angle) < THRESHOLD:
            direction = 'horizontal'
        elif 90 - abs(angle) < THRESHOLD:
            direction = 'vertical'
        else:
            direction = 'diagonal'

        return direction

    @staticmethod
    def analyze_angle(start_pos, end_pos):

        hypotenuse = end_pos[0] - start_pos[0]
        if hypotenuse == 0:
            return 90
        else:
            opposite = end_pos[1] - start_pos[1]
            return math.degrees(math.atan(opposite/float(hypotenuse)))


def start():
    """Start up function."""

    if model.validate_selection():
        global VIEW  # pylint: disable=global-statement
        VIEW = view.Interface()
        VIEW.raise_()
        VIEW.show()

        Controller(VIEW)
