from PySide2 import QtWidgets, QtGui, QtCore
from operator import mul

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
        size = 5

        points = (QtCore.QPoint(self.start.x() - size, self.start.y() - size),
                  QtCore.QPoint(self.start.x() + size, self.start.y() + size),
                  QtCore.QPoint(self.end.x() + size, self.end.y() + size),
                  QtCore.QPoint(self.end.x() - size, self.end.y() - size)
                  )

        path = QtGui.QPainterPath()
        path.addPolygon(points)
        painter.fillPath(path, self._gradient())

        if self.nodegraph.hasFocus():
            color = QtGui.QColor(255, 120, 0, 70)
        else:
            color = QtGui.QColor(0, 120, 150, 70)
        painter.fillRect(self.rect(), color)

    def _gradient(self):

        length = [self.start.x() - self.end.x(), self.start.y() - self.end.y()]
        gradient = QtGui.QRadialGradient(self.start, 200)
        gradient.setColorAt(0, QtCore.Qt.red)
        gradient.setColorAt(1, QtCore.Qt.black)
        return gradient

    def get_painter(self):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.HighQualityAntialiasing)
        pen = QtGui.QPen(QtCore.Qt.DashDotDotLine | QtCore.Qt.RoundCap)
        pen.setWidthF(5.0)
        painter.setPen(pen)
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
