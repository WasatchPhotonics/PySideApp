""" Provide a set of tests cases to demonstrate a basic gui that meets
wasatch needs. This includes menu bar, buttons, and text controls. Verify that
logging from the views with default setup is available to the capturelog
fixture.
"""

import pytest

from PySide import QtCore, QtTest

from pysideapp import views

class TestBasicWindow:

    @pytest.fixture(scope="function")
    def my_form(self, qtbot, request):
        """ Create the new QMainWindow from the view at every test
        setup.
        """
        new_form = views.BasicWindow()

        # Close the form when the test ends
        def form_close():
            new_form.close()
        request.addfinalizer(form_close)

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

    def test_direct_logging_is_available(self, my_form, qtbot, caplog):
        QtTest.QTest.qWaitForWindowShown(my_form)
        qtbot.mouseClick(my_form.button, QtCore.Qt.LeftButton)

        self.visualization_wait(my_form, qtbot)
        assert "Button clicked" in caplog.text()
