""" Controller tests that show the linkage between the data model, view, and
logging components.
Mimic the contents of the scripts/PySideApp.py setup section. Create the logger
with the queue handler as part of the test case, as opposed to having the
controller create the top level logger
"""

import time

from PySide import QtTest

from pysideapp import control
from pysideapp import applog


class TestControl:
    def visualization_wait(self, my_form, qtbot, timeout=1000):
        """ Helper function that waits for a signal created by default
        on all widgets. Use qtbot to timeout when this signal is not
        received.
        """
        signal = my_form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=timeout):
            my_form.show()

    def test_control_logs_visible_to_caplog(self, caplog, qtbot):
        main_logger = applog.MainLogger()

        app_control = control.Controller(main_logger.log_queue)
        self.visualization_wait(app_control.form, qtbot)

        app_control.close()
        time.sleep(1)

        main_logger.close()
        time.sleep(1)
        assert "Control startup" in caplog.text()
        self.explicit_log_close()


    def test_view_logs_visible_to_caplog(self, caplog, qtbot):
        main_logger = applog.MainLogger()

        app_control = control.Controller(main_logger.log_queue)
        self.visualization_wait(app_control.form, qtbot)

        app_control.close()
        time.sleep(1)

        main_logger.close()
        time.sleep(1)
        assert "Init of BasicWindow" in caplog.text()
        self.explicit_log_close()

    def test_device_logs_in_file_only(self, caplog, qtbot):
        """ Shows the expected behavior. Demonstrates that the capturelog
        fixture on py.test does not see sub process entries.
        """
        assert applog.delete_log_file_if_exists() == True

        main_logger = applog.MainLogger()

        app_control = control.Controller(main_logger.log_queue)
        self.visualization_wait(app_control.form, qtbot)

        app_control.close()
        time.sleep(1)

        main_logger.close()
        time.sleep(1)

        log_text = applog.get_text_from_log()
        assert "SimulateSpectra setup" in log_text
        assert "SimulateSpectra setup" not in caplog.text()
        self.explicit_log_close()


    def test_close_view_emits_control_signal(self, caplog, qtbot):
        """ Control script emits an event on a close condition to be processsed
        by the parent qt application, in this case qtbot. In the scripts file,
        it's the Qapplication.
        """
        main_logger = applog.MainLogger()
        app_control = control.Controller(main_logger.log_queue)

        QtTest.QTest.qWaitForWindowShown(app_control.form)

        signal = app_control.control_exit_signal.exit
        with qtbot.wait_signal(signal, timeout=1):
            app_control.form.close()

        main_logger.close()
        time.sleep(1)
        assert "Control level close" in caplog.text()
        self.explicit_log_close()

    def explicit_log_close(self):
        """ Tests on windows will recreate a secondary log handler to
        stdout/file. Teardown does not see the expected log variable, so
        use this function to close all of the log file handlers.
        """
        import logging
        the_log = logging.getLogger()
        handlers = the_log.handlers[:]
        for handler in handlers:
            handler.close()
            the_log.removeHandler(handler)

