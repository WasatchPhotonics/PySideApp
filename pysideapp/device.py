""" Classes for device control testing around pm100 and multiprocessing
"""

import time
import Queue
import platform
import multiprocessing

from pysideapp import custom_logging

import logging
log = logging.getLogger(__name__)

class ExampleObject(object):
    def __init__(self):
        log.debug("Init of %s", self.__class__.__name__)
        super(ExampleObject, self).__init__()

    def perform_check(self):
        log.debug("perform check")
        log.info("perform check")
        log.warning("perform check")
        log.critical("perform check")

class QueueMPDevice(object):
    """ Use the poison pill pattern to exit the worker process. Create
    the started variable for external testability of process
    states.
    """
    def __init__(self, in_pytest=False):
        log.debug("Init of %s", self.__class__.__name__)
        super(QueueMPDevice, self).__init__()

        self.queue = multiprocessing.Queue()
        args = (self.queue, in_pytest)

        mpp = multiprocessing.Process
        self.process = mpp(target=self.worker, args=args)
        self.process.daemon = True

        self.started = False

    def create_new_log_on_windows_with_pytest(self, in_pytest):
        """ If operating on MS windows in a multiprocessing context
        while using pytest, the log prints to stdout will not appear.
        Create a new logger with a formatter to stdout if operating on
        windows only, and only if called within pytest. If you only
        check if within pytest and create the logger on linux, you will
        have two identical loggers.
        """
        if in_pytest == False:
            return log

        if "Windows" in platform.platform():
            self.my_log = custom_logging.to_stdout()
            self.my_log.debug("Custom pytest windows log setup")
            return self.my_log

        return log

    def worker(self, queue, in_pytest):
        """ Run forever until an poison pill is received. First setup a
        log so the pytest output looks the same as the executed python
        application.

        Don't use if queue.empty() for flow control on python 2.7 on
        windows, as it will hange. Use the catch of the queue empty
        exception as shown below instead.
        """
        log = self.create_new_log_on_windows_with_pytest(in_pytest)

        while(True):
            # Don't use if queue.empty() -- see above
            try:
                result = queue.get_nowait()
                if result == "DISCONNECT":
                    log.debug("Disonnect received, exiting loop")
                    break
            except Queue.Empty:
                #log.debug("Queue is empty")
                pass

            current = multiprocessing.current_process()
            log.debug("Worker process: %s", current.pid)
            time.sleep(0.01)

    def create(self):
        """ Start the running of the multiprocessing object. In an
        actual application you might also place commands on the queue to
        perform work inside the worker.
        """
        log.debug("Start the multiprocessing object")
        self.process.start()
        self.started = True

    def close(self):
        """ Issue the poison pill onto the queue consumed by the worker.
        Join the process and set the status variable.
        """
        log.debug("Close the multiprocessing object")
        self.queue.put("DISCONNECT")
        self.process.join()
        self.started = False
