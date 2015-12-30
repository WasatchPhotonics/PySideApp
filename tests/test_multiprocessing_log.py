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

class TestLogFile():
    def test_log_file_is_created(self):
        assert self.log_file_does_not_exist() == True

        from pysideapp import app_logging
        main_logger = app_logging.MainLogger()
        main_logger.close()

        time.sleep(0.5)

        assert self.log_file_created() == True

    def log_file_created(self):
        filename = "mptest_log.txt"
        if os.path.exists(filename):
            return True

        return False

    def log_file_does_not_exist(self):
        filename = "mptest_log.txt"

        if os.path.exists(filename):
            os.remove(filename)

        if os.path.exists(filename):
            print "Problem deleting: %s", filename
            return False
        return True

