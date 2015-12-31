""" Simulated device components for PySideApp. Simple blocking calls with
simulated delays for simulated spectrometer readings. Long-polling
multiprocessing wrappers.
"""

import time
import Queue
import logging
import multiprocessing

from pysideapp import applog

log = logging.getLogger(__name__)

class SimulateSpectra(object):
    """ Provide a bare bones interface for reading simulated spectra from a
    simulated device.
    """
    def __init__(self):
        super(SimulateSpectra, self).__init__()
        log.debug("%s setup", self.__class__.__name__)

    def read(self):
        """ Return a test pattern of 0-1023 values across an 1024 length list.
        """
        return range(0, 1024)


class LongPollingSimulateSpectra(object):
    """ Wrap simulate spectra in a non-blocking interface run in a separate
    process.
    """
    def __init__(self, log_queue=None):
        self.response_queue = multiprocessing.Queue()
        self.command_queue = multiprocessing.Queue()

        args = (log_queue, self.command_queue, self.response_queue)
        self.poller = multiprocessing.Process(target=self.continuous_poll,
                                              args=args)
        self.poller.start()

    def close(self):
        """ Add the poison pill to the command queue.
        """
        self.command_queue.put(None)

    def continuous_poll(self, log_queue, command_queue, response_queue):
        """ Auto-acquire new readings from the simulated device. First setup the
        log queue handler. While waiting forever for the None poison pill on the
        command queue, continuously add 'acquire' commands and post the results
        on the response queue.
        """

        applog.process_log_configure(log_queue)

        self.device = SimulateSpectra()

        # Read forever until the None poison pill is received
        while True:
            command_queue.put("Acquire")
            try:
                record = command_queue.get()
                if record is None:
                    log.debug("Exit command queue")
                    break

                time.sleep(0.2)
                data = self.device.read()
                self.response_queue.put(data)
                log.debug("Collected data in continuous poll")
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                import sys, traceback
                print >> sys.stderr, 'Whoops! Problem:'
                traceback.print_exc(file=sys.stderr)

    def read(self):
        """ Don't use if queue.empty() for flow control on python 2.7 on
        windows, as it will hang. Use the catch of the queue empty exception as
        shown below instead.
        """
        result = None

        try:
            result = self.response_queue.get_nowait()
        except Queue.Empty:
            pass

        return result
