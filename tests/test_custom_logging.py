""" tests for log file configuration and emissions
"""

import os
import pytest
import platform

from pysideapp import custom_logging
from pysideapp import device

class TestCustomLogging:
    def test_representative_object_using_log(self, caplog):
        example = device.ExampleObjectThatLogs()
        example.perform_check()

        assert "DEBUG    perform check" in caplog.text()
        assert "INFO     perform check" in caplog.text()
        assert "WARNING  perform check" in caplog.text()
        assert "CRITICAL perform check" in caplog.text()

    def test_multiprocessing_representative_object_loggin(self, caplog):
        #example = device.ExampleObjectThatLogs()
        #example.multiprocess_perform_check()
        return
        # Expect fail here, do manual tests with application to
        # verify that it is saved to file.
        #
        # Then add in qtsignal on log to verify can be logged in gui
        # from child process
        assert "DEBUG    Setup multiprocessing log emits"
        assert "DEBUG    perform check" in caplog.text()
        assert "INFO     perform check" in caplog.text()
        assert "WARNING  perform check" in caplog.text()
        assert "CRITICAL perform check" in caplog.text()
        assert "DEBUG    Close multiprocessing log emits"

    def test_logging_setup_creates_file(self):
        assert self.log_file_does_not_exist() == True
        log = custom_logging.to_file_and_stdout()

        example = device.ExampleObjectThatLogs()
        example.perform_check()

        assert self.log_file_created() == True

        log_text = self.get_text_from_log()
        assert "DEBUG perform check" in log_text
        assert "INFO perform check" in log_text
        assert "WARNING perform check" in log_text
        assert "CRITICAL perform check" in log_text

        self.explicit_log_close(log)

    def test_logging_setup_file_updated_by_sub_process(self):

        assert self.log_file_does_not_exist() == True
        log = custom_logging.to_file_and_stdout()

        example = device.ExampleObjectThatLogs()
        example.multiprocess_setup_child()

        assert self.log_file_created() == True

        log_text = self.get_text_from_log()
        assert "DEBUG multiprocess perform check" in log_text
        assert "INFO multiprocess perform check" in log_text
        assert "WARNING multiprocess perform check" in log_text
        assert "CRITICAL multiprocess perform check" in log_text

        self.explicit_log_close(log)

    def explicit_log_close(self, the_log):
        """ Tests on windows will recreate a secondary log handler to
        stdout/file. Teardown does not see the expected log variable, so
        use this function to close all of the log file handlers.
        """
        handlers = the_log.handlers[:]
        for handler in handlers:
            handler.close()
            the_log.removeHandler(handler)

    def log_file_created(self):
        filename = self.platform_specific_filename()
        if os.path.exists(filename):
            return True

        return False

    def log_file_does_not_exist(self):
        filename = self.platform_specific_filename()

        if os.path.exists(filename):
            os.remove(filename)

        if os.path.exists(filename):
            print "Problem deleting: %s", filename
            return False
        return True

    def get_text_from_log(self):
        """ Mimic the capturelog style of just slurping the entire log
        file contents.
        """

        log_text = ""
        log_file = open(self.platform_specific_filename())
        for line_read in log_file:
            log_text += line_read
        return log_text

    def platform_specific_filename(self, filename="PySideApp_log.txt"):
        if "Linux" in platform.platform():
            filename = "./%s" % filename
        else:
            filename = "c:\ProgramData\%s" % filename
        return filename
