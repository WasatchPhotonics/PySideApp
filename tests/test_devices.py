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

