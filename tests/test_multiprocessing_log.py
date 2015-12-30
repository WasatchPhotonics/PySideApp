""" logging from multiple processes to a single handler is critical to wasatch
application goals. These tests ensure that the various components of the
application all log to same location on disk.

As of 2015-12-30 10:39, it is unknown how to work with py.test and the
capturelog fixture to read the log prints to stdout/stderr streams. The
workaround is to store all of the log events to disk, and re-read the file at
test completion.

"""

import os
import time

FILENAME = "mptest_log.txt"

class TestLogFile():
    def test_log_file_is_created(self):
        assert self.delete_log_file_if_exists() == True

        from pysideapp import app_logging
        main_logger = app_logging.MainLogger()
        main_logger.close()

        time.sleep(0.5) # required to let file creation happen

        assert self.log_file_created() == True


    def test_log_file_has_entries(self):
        assert self.delete_log_file_if_exists() == True

        from pysideapp import app_logging
        main_logger = app_logging.MainLogger()
        main_logger.close()

        time.sleep(0.5) # required to let file creation happen

        log_text = self.get_text_from_log()

        assert "Top level log configuration" in log_text

    def test_log_capture_fixture_can_read_top_level_log(self, caplog):
        from pysideapp import app_logging
        main_logger = app_logging.MainLogger()
        main_logger.close()

        assert "Top level log configuration" in caplog.text()



    def get_text_from_log(self):
        """ Mimic the capturelog style of just slurping the entire log
        file contents.
        """

        log_text = ""
        log_file = open(FILENAME)
        for line_read in log_file:
            log_text += line_read
        return log_text


    def log_file_created(self):
        """ Helper function that returns True if file exists, false otherwise.
        """
        filename = FILENAME
        if os.path.exists(filename):
            return True

        return False

    def delete_log_file_if_exists(self):
        """ Remove the specified log file and return True if succesful.
        """
        filename = FILENAME

        if os.path.exists(filename):
            os.remove(filename)

        if os.path.exists(filename):
            print "Problem deleting: %s", filename
            return False
        return True

