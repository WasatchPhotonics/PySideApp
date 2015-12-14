""" tests for gui layout using pyside
"""

import pytest

from PySide import QtCore, QtTest

from pysideapp import views
from pysideapp import device
from pysideapp import custom_logging

log = custom_logging.to_stdout()

class TestBasicWindow:

    @pytest.fixture
    def my_form(self, qtbot):
        """ Create the new QMainWindow from the view at every test
        setup.
        """
        log.debug("Setup form fixture")
        new_form = views.BasicWindow()
        return new_form

    def visualization_wait(self, my_form, qtbot, timeout=1000):
        """ Helper function that waits for a signal created by default
        on all widgets. Use qtbot to timeout when this signal is not
        received.
        """
        signal = my_form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=timeout):
            my_form.show()

    def test_form_has_text_and_button_controls(self, my_form, qtbot):
        QtTest.QTest.qWaitForWindowShown(my_form)

        assert my_form.lbl_info.text() == "PySideApp Default"
        assert my_form.width() == 400
        assert my_form.height() == 400

    def test_form_button_click_changes_label(self, my_form, qtbot):
        QtTest.QTest.qWaitForWindowShown(my_form)

        assert my_form.button.text() == "Change Text"
        assert my_form.lbl_info.text() == "PySideApp Default"

        qtbot.mouseClick(my_form.button, QtCore.Qt.LeftButton)

        # For debugging the application events, use visualization wait
        self.visualization_wait(my_form, qtbot)

        assert "Button clicked" in my_form.lbl_info.text()

    def test_logging_control_is_available(self, my_form, qtbot):
        QtTest.QTest.qWaitForWindowShown(my_form)

        self.visualization_wait(my_form, qtbot)
        assert my_form.txt_log.toPlainText() == "Log text area"

    def test_button_click_adds_to_log_text(self, my_form, qtbot):
        qtbot.mouseClick(my_form.button, QtCore.Qt.LeftButton)

        self.visualization_wait(my_form, qtbot)

        expect_str = "Log text area\npysideapp.views Button clicked"
        actual_str = my_form.txt_log.toPlainText()
        assert expect_str in actual_str

    def test_subprocess_logging_adds_to_log_text(self, my_form, qtbot):
        qtbot.mouseClick(my_form.button, QtCore.Qt.LeftButton)

        self.visualization_wait(my_form, qtbot, timeout=3000)

        example = device.ExampleObjectThatLogs()
        example.multiprocess_setup_child()

        self.visualization_wait(my_form, qtbot, timeout=3000)
        expect_str = "INFO multiprocess perform che"
        actual_str = my_form.txt_log.toPlainText()
        assert expect_str in actual_str
        print "actual string is: %s" % actual_str
