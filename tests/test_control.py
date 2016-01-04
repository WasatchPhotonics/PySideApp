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
        time.sleep(1)

        main_logger.close()
        time.sleep(1)
        assert "Control startup" in caplog.text()

    def visualization_wait(self, my_form, qtbot, timeout=1000):
        """ Helper function that waits for a signal created by default
        on all widgets. Use qtbot to timeout when this signal is not
        received.
        """
        signal = my_form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=timeout):
            my_form.show()
