""" Provide a set of tests cases to demonstrate a basic device that meets
wasatch needs. This includes simple blocking and long polling separate process
devices.
"""

import time
import pytest

from PySide import QtCore, QtTest

from pysideapp import devices
from pysideapp import applog

class TestBasicDevice:

    def test_direct_logging_is_available(self, caplog):
        device = devices.SimulateSpectra()
        assert "SimulateSpectra setup" in caplog.text()

    def test_direct_device_is_available(self, caplog):
        device = devices.SimulateSpectra()
        result = device.read()
        while result is None:
            result = device.read()

        assert len(result) == 1024

    def test_subprocess_device_logging_is_unavailable(self, caplog):
        """ Shows the expected interactions between py.test, the caplog fixture,
        and logging from subprocesses. Specifically that pytest does not see the
        log statements printed from subprocess, you have to read them back from
        the file.
        """
        device = devices.LongPollingSimulateSpectra()
        device.close()
        assert "SimulateSpectra setup" not in caplog.text()

    def test_subprocess_device_logging_in_file(self, caplog):
        """ Define the application wide queue handler for the logging, assign it
        to the device process. This test is about demonstrating actual usage in
        order to process the results in py.test.

        One of the confusing aspects here may be that in a bare bones
        application example, the log prints to the console still appear, on
        windows and linux. pytest does not see them however. Slurp them back in
        from the log file, which seems to work in executable, bare bones
        application, and pytest mode.

        """

        assert applog.delete_log_file_if_exists() == True

        main_logger = applog.MainLogger()

        log_queue = main_logger.log_queue
        device = devices.LongPollingSimulateSpectra(log_queue)
        device.close()

        time.sleep(1.0) # make sure the process has enough time to emit

        main_logger.close()

        time.sleep(0.5) # required to let file creation happen

        log_text = applog.get_text_from_log()

        assert "SimulateSpectra setup" in log_text
