""" tests using queue handler for multiprocessing logs.
"""
import sys
import time
import logging
from pysideapp import queue_logging

#log = logging.getLogger()
#strm = logging.StreamHandler(sys.stdout)
#frmt = logging.Formatter("%(asctime)s %(name)s - %(levelname)s %(message)s")
#strm.setFormatter(frmt)
#log.addHandler(strm)
#log.setLevel(logging.DEBUG)

class TestQueueHandler():

    def test_queue_handler_listener_process_exists(self, caplog):
        my_proc = queue_logging.SimulateMain()
        my_proc.create_proc()
        time.sleep(1.0)
        expect = "Setup listener process"
        actual = caplog.text()
        print "Full caplog: [%s]" % actual
        assert expect in actual

        # This test failure is to demonstrate that the caplog capability is not
        # present for multiprocessing

    def test_reread_log_from_listener_processes(self):
        # Do the same test as above, but slurp in the contents of the log file
        # from disk
        my_proc = queue_logging.SimulateMain()
        my_proc.create_proc()
        time.sleep(1.0)
        expect = "Setup listener process"
        actual = self.get_text_from_log()
        print "Full caplog: [%s]" % actual
        assert expect in actual


    def test_queue_handler_log_capture(self, caplog):
        my_proc = queue_logging.create_proc()

        assert "Worker started: Process-2" in caplog.text()

    def get_text_from_log(self, filename="mptest.log"):
        """ Mimic the capturelog style of just slurping the entire log
        file contents.
        """

        log_text = ""
        log_file = open(filename)
        for line_read in log_file:
            log_text += line_read
        return log_text
