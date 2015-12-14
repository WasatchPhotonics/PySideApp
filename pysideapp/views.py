""" GUI components for the PySideApp demonstration program. Provides a
bare bones interface with a single button that changes the text to the
current timestamp. Used to demonstrate pytest-qt qtbot button clicking.
"""

import datetime

from PySide import QtGui

import logging
log = logging.getLogger(__name__)

class BasicWindow(QtGui.QMainWindow):
    """ Provie a bare form layout with basic interactivity.
    """
    def __init__(self, parent=None):
        log.debug("Init of %s", self.__class__.__name__)
        super(BasicWindow, self).__init__(parent)

        # The main widget. Certain implementations will still create a
        # form with the geometry specified below. Enforce the central
        # widget for better portability.
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.vbox = QtGui.QVBoxLayout()
        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.vbox)
        self.central_widget.addWidget(self.main_widget)

        self.lbl_info = QtGui.QLabel("PySideApp Default")
        self.vbox.addWidget(self.lbl_info)

        self.button = QtGui.QPushButton("Change Text")
        self.vbox.addWidget(self.button)

        self.button.clicked.connect(self.change_text)

        self.setGeometry(30, 30, 400, 400)
        self.show()

    def change_text(self):
        new_txt = "Button clicked: %s" % datetime.datetime.now()
        log.debug("New txt: %s", new_txt)
        self.lbl_info.setText(new_txt)