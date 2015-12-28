""" GUI components for the PySideApp demonstration program. Provides a
bare bones interface with a single button that changes the text to the
current timestamp. Used to demonstrate pytest-qt qtbot button clicking.
"""
import datetime

from PySide import QtGui, QtCore

import Queue
import logging
# This does not write out the log.debug("XXXXX") entries to stdout or
# stderr
log = logging.getLogger(__name__)

# This does not write out the log.debug("XXXXX") entries to stdout or
# stderr
#import sys
#log = logging.getLogger()
#strm = logging.StreamHandler(sys.stderr)
#frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
#strm.setFormatter(frmt)
#log.addHandler(strm)
#log.setLevel(logging.INFO)



class BasicWindow(QtGui.QMainWindow):
    """ Provie a bare form layout with basic interactivity.
    """
    def __init__(self, parent=None, in_log_queue=None):
        log.debug("Init of %s" % self.__class__.__name__)
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

        self.deep_log = QtGui.QTextEdit("deep log")
        self.vbox.addWidget(self.deep_log)


        self.button.clicked.connect(self.change_text)

        #self.setup_signals()

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
        print "post log debug STDOUT: %s" % new_txt
        root = logging.getLogger()
        root.debug("After get logger: %s", new_txt)

    def on_log(self, input_text):
        """ Append the new text to the logging text edit control.
        """
        #print "In on log with [%s]" % input_text
        self.txt_log.append(input_text)

    def qt_log_setup(self, queue):
        self.log_queue = queue
        self.qt_listener_configurer()
        print "Post QT listener configurer"

        self.log_timer = QtCore.QTimer()
        self.log_timer.setSingleShot(True)
        self.log_timer.timeout.connect(self.qt_listener_process)
        self.log_timer.start(100)


    def qt_listener_configurer(self):
        root = logging.getLogger()
        #h = logging.handlers.RotatingFileHandler('/tmp/mptest.log', 'a', 300, 10)
        h = logging.handlers.RotatingFileHandler('mptest.log', 'w')
        f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        h.setFormatter(f)
        root.addHandler(h)


        import sys
        strm = logging.StreamHandler(sys.stdout)
        frmt = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        strm.setFormatter(frmt)
        root.addHandler(strm)

        print "About to call mid debug logger"
        root.debug("\n\nMid debug loggerl#######################")

    def qt_listener_process(self):
        #print "setup qt listener process"

        try:
            record = self.log_queue.get_nowait()
            if record is None: # We send this as a sentinel to tell the listener to quit.
                print "Terminating qt listener process"
                return
            logger = logging.getLogger(record.name)
            logger.handle(record) # No level or filter logic applied - just do it!
            print "QT Actual log process for %s" % record.msg

            # Update the current interface
            self.on_log(record.msg)
   
            # Can't do this - not picklable
            #update_function(record.msg)
        except Queue.Empty:
            # Older version of python on windows hang on if 
            # queue.empty()
            #print "Queue empty"
            pass

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            import sys, traceback
            print >> sys.stderr, 'Whoops! Problem:'
            traceback.print_exc(file=sys.stderr)

        #print "Every log timer start"
        self.log_timer.start(0)


class QTLogHandler(logging.Handler):
    """ Hook into the python native logging module to catch all lower
    level logging events and emit a signal to be processed by the qt
    interface.
    """
    def __init__(self):
        super(QTLogHandler, self).__init__()
        self.lts = LogToSignal()

    def emit(self, log_record):
        """ Why is the formatter not applied? Why can't you do
        log_record.asctime?
        """
        #rec_str = str(record.asctime) + " " + str(record.levelname) \
                  #+ " " + str(record.message)
        rec_str = "%s %s" % (log_record.name, log_record.msg)
        print "Set rec_str to: %s" % rec_str
        self.lts.log_update.emit(rec_str)

class LogToSignal(QtCore.QObject):
    """ Follows the example documentation to create a QObject based
    class used to re-emit the log string caught by the handler.
    """
    log_update = QtCore.Signal("QString")
