""" Controller tests that show the linkage between the data model, view, and
logging components.

Mimic the contents of the scripts/PySideApp.py setup section. Create the logger
with the queue handler as part of the test case, as opposed to having the
controller create the top level logger
"""

from pysideapp import control

class TestControl:
    def test_control_logs_visible_to_caplog(self, caplog, qtbot):
        app_control = control.Controller()

        assert "Control startup" in caplog.text()

    def test_view_logs_visible_to_caplog(self, caplog, qtbot):
        app_control = control.Controller()

        assert "Init of BasicWindow" in caplog.text()


    #def test_device_logs_in_file_only(self, caplog):


    #def test_device_data_collect_updates_view(self, caplog):


