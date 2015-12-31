""" Controller tests that show the linkage between the data model, view, and
logging components.

Mimic the contents of the scripts/PySideApp.py setup section. Create the logger
with the queue handler as part of the test case, as opposed to having the
controller create the top level logger
"""

import time
from pysideapp import control
from pysideapp import applog

class TestControl:
    def test_control_logs_visible_to_caplog(self, caplog, qtbot):
        main_logger = applog.MainLogger()

        app_control = control.Controller(main_logger.log_queue)
        self.visualization_wait(app_control.form, qtbot)

        app_control.close()
        main_logger.close()
        assert "Control startup" in caplog.text()

    def test_view_logs_visible_to_caplog(self, caplog, qtbot):
        main_logger = applog.MainLogger()

        app_control = control.Controller(main_logger.log_queue)
        self.visualization_wait(app_control.form, qtbot)

        app_control.close()
        main_logger.close()
        assert "Init of BasicWindow" in caplog.text()

    def test_device_logs_in_file_only(self, caplog, qtbot):
        """ Shows the expected behavior. Demonstrates that the capturelog
        fixture on py.test does not see sub process entries.
        """
        assert applog.delete_log_file_if_exists() == True

        main_logger = applog.MainLogger()

        app_control = control.Controller(main_logger.log_queue)
        self.visualization_wait(app_control.form, qtbot)

        app_control.close()
        main_logger.close()
        log_text = applog.get_text_from_log()
        assert "SimulateSpectra setup" in log_text
        assert "SimulateSpectra setup" not in caplog.text()

    def test_control_starts_main_event_loop(self, caplog, qtbot):
        assert applog.delete_log_file_if_exists() == True

        main_logger = applog.MainLogger()

        app_control = control.Controller(main_logger.log_queue)
        self.visualization_wait(app_control.form, qtbot)

        app_control.close()
        main_logger.close()
        log_text = applog.get_text_from_log()
        assert "Setup main event loop" in caplog.text()


    def test_device_data_collect_updates_view(self, qtbot):
        main_logger = applog.MainLogger()

        app_control = control.Controller(main_logger.log_queue)

        self.visualization_wait(app_control.form, qtbot)
        txt_box = app_control.form.txt_box
        assert "2 spectra read" in txt_box.toPlainText()

        app_control.close()
        main_logger.close()


    def visualization_wait(self, my_form, qtbot, timeout=1000):
        """ Helper function that waits for a signal created by default
        on all widgets. Use qtbot to timeout when this signal is not
        received. This is for showing the form when developing tests.
        """
        signal = my_form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=timeout):
            my_form.show()
