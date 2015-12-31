""" Application level controller for PySideApp. Handles data model and UI
updates with MVC style architecture.
"""

import logging

from PySide import QtCore

from pysideapp import views, devices

# Do you want this here - or do you want the queue handler listener started
# here?
log = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, log_queue):
        log.debug("Control startup")

        # Create a separate process for the qt gui event loop
        self.form = views.BasicWindow()

        self.device = devices.LongPollingSimulateSpectra(log_queue)
        self.total_spectra = 0

        self.setup_main_event_loop()

    def setup_main_event_loop(self):
        """ Create a timer for a continuous event loop, trigger the start.
        """
        log.debug("Setup main event loop")
        self.main_timer = QtCore.QTimer()
        self.main_timer.setSingleShot(True)
        self.main_timer.timeout.connect(self.event_loop)
        self.main_timer.start(0)

    def event_loop(self):
        """ Process queue events, interface events, then update views.
        """
        result = self.device.read()
        if result is not None:
            self.total_spectra += 1
            self.form.txt_box.append("%s spectra read" \
                                     % self.total_spectra)

        self.main_timer.start(0)

    def close(self):
        self.device.close()

