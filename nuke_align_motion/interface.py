from PySide2 import QtWidgets, QtGui, QtCore


class Interface(QtWidgets.QWidget):
    trigger = QtCore.Signal(object)

    def __init__(self):
        super(Interface, self).__init__()
        self.init_ui()
        self.start = QtGui.QCursor().pos()
        self.end = QtGui.QCursor().pos()

    def init_ui(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Mouse Tracker')
        self.label = QtWidgets.QLabel(self)
        self.label.resize(500, 40)
        self.show()

    def mousePressEvent(self, QMouseEvent):
        self.setMouseTracking(True)
        self.start = QMouseEvent.pos()

    def mouseReleaseEvent(self, QMouseEvent):
        self.end = QMouseEvent.pos()
        self.update()
        self.setMouseTracking(False)
        start = (self.start.x(), self.start.y())
        end = (self.end.x(), self.end.y())
        self.trigger.emit((start, end))

    def mouseMoveEvent(self, QMouseEvent):
        self.end = QMouseEvent.pos()
        self.update()

    def paintEvent(self, event):
        if self.pos:
            painter = self.get_painter()
            painter.drawLine(self.start.x(), self.start.y(), self.end.x(), self.end.y())

    def get_painter(self):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.blue)
        return painter

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Catch user key events.

        Args:
            event: (QtGui.event)

        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


