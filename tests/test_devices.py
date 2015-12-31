""" Provide a set of tests cases to demonstrate a basic device that meets
wasatch needs. This includes simple blocking and long polling separate process
devices.
"""

import pytest

from PySide import QtCore, QtTest

from pysideapp import devices

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

