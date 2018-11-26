
# Import third party modules
from PySide2 import QtWidgets, QtGui, QtCore

from nuke_align_motion import settings

reload(settings)


class Interface(QtWidgets.QWidget):
    trigger = QtCore.Signal(object)

    def __init__(self):
        super(Interface, self).__init__()
        self.init_ui()
        self.installEventFilter(self)
        self.start = QtGui.QCursor().pos()
        self.end = QtGui.QCursor().pos()
        self.nodegraph = self.find_nodegraph()
        self.set_widget_position()

    def init_ui(self):
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, mouse_event):
        if mouse_event.button() == QtCore.Qt.RightButton:
            self.close()
        else:
            self.setMouseTracking(True)
            self.start = mouse_event.pos()

    def mouseReleaseEvent(self, mouse_event):
        self.end = mouse_event.pos()
        self.update()
        self.setMouseTracking(False)
        start = (self.start.x(), self.start.y())
        end = (self.end.x(), self.end.y())
        self.trigger.emit((start, end))
        self.close()

    def mouseMoveEvent(self, mouse_event):
        self.end = mouse_event.pos()
        self.update()

    def paintEvent(self, event):
        painter = self.get_painter()

        if self.nodegraph.hasFocus():
            color = QtGui.QColor(*settings.COLOR_ENABLE)
        else:
            color = QtGui.QColor(*settings.COLOR_DRAW)

        painter.fillRect(self.rect(), color)
        self.draw_line(painter)

    def draw_line(self, painter):
        begin = 4
        end = begin/2
        # points = (QtCore.QPoint(self.start.x() - begin, self.start.y() - begin),
        #           QtCore.QPoint(self.start.x() + begin, self.start.y() + begin),
        #
        #           QtCore.QPoint(self.end.x() + end, self.end.y() + end),
        #           QtCore.QPoint(self.end.x() - end, self.end.y() - end)
        #           )
        #
        # path = QtGui.QPainterPath()
        # path.addPolygon(points)
        # painter.fillPath(path, self._gradient())

        pen = QtGui.QPen(self._gradient(), 5)
        painter.setPen(pen)
        painter.drawLine(self.start, self.end)

        self._elipse(painter)

    def _elipse(self, painter):
        size = settings.ELIPSE_WIDTH
        painter.setBrush(QtGui.QColor(*settings.COLOR_START))
        painter.drawEllipse(self.start, size, size)
        painter.setBrush(QtGui.QColor(*settings.COLOR_END))
        painter.drawEllipse(self.end, size, size)

    def _gradient(self):
        gradient = QtGui.QRadialGradient(self.start, settings.GRADIENT_WIDTH)
        gradient.setColorAt(0, QtGui.QColor(*settings.COLOR_START))
        gradient.setColorAt(1, QtGui.QColor(*settings.COLOR_END))
        return gradient

    def get_painter(self):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.HighQualityAntialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        return painter

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate, QtCore.QEvent.FocusOut]:
            self.close()
            return True

    @staticmethod
    def find_nodegraph():
        stack = QtWidgets.QApplication.topLevelWidgets()
        while stack:
            widget = stack.pop()
            if widget.windowTitle() == 'Node Graph':
                return widget.children()[-1]
            stack.extend(c for c in widget.children() if c.isWidgetType())

    def set_widget_position(self):
        self.setGeometry(self.nodegraph.rect())
        self.move(self.nodegraph.mapToGlobal(self.nodegraph.pos()))
