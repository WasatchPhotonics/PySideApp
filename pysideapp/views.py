""" GUI components for the PySideApp demonstration program. Provides a
bare bones interface with a single button that changes the text to the
current timestamp. Used to demonstrate pytest-qt qtbot button clicking.
"""

import datetime

from PySide import QtGui, QtCore

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

        self.txt_log = QtGui.QTextEdit("Log text area")
        self.vbox.addWidget(self.txt_log)

        self.button.clicked.connect(self.change_text)

        self.setup_signals()

        self.setGeometry(30, 30, 400, 400)
        self.show()

    def setup_signals(self):
        self.qtl_handler = QTLogHandler()
        log.addHandler(self.qtl_handler)
        self.qtl_handler.lts.log_update.connect(self.on_log)

    def change_text(self):
        new_txt = "Button clicked: %s" % datetime.datetime.now()
        self.lbl_info.setText(new_txt)
        log.debug(new_txt)


    def on_log(self, input_text):
        """ Append the new text to the logging text edit control.
        """
        print "In on log with [%s]" % input_text
        self.txt_log.append(input_text)

# Hook into the python native logging module to catch all lower level logging
# events and emit a signal to be processed by the qt interface
class QTLogHandler(logging.Handler):
    """ Hook into the python native logging module to catch all lower
    level logging events and emit a signal to be processed by the qt
    interface.
    """
    def __init__(self):
        logging.Handler.__init__(self)
        self.lts = LogToSignal()

    def emit(self, log_record):
        print "Entire record: %s" % log_record
        #rec_str = str(record.asctime) + " " + str(record.levelname) \
                  #+ " " + str(record.message)
        rec_str = log_record.msg
        self.lts.log_update.emit(rec_str)

# Follows the example documentation to create a QObject based class used to
# re-emit the log string caught by the handler
class LogToSignal(QtCore.QObject):
    log_update = QtCore.Signal("QString")
