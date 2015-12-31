""" Simulated device components for PySideApp. Simple blocking calls with
simulated delays for simulated spectrometer readings. Long-polling
multiprocessing wrappers.
"""

import time
import logging
import multiprocessing

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
        self.command_queue.put(None)

    def continuous_poll(self, log_queue, command_queue, response_queue):
        self.device = SimulateSpectra()
        applog.process_log_configure(log_queue)
        while True:
            try:
                record = command_queue.get()
                if record is None: # We send this as a sentinel to tell the listener to quit.
                    log.debug("Exit command queue")
                    break

                data = self.device.read()
                self.response_queue.put(data)
                log.debug("In continuous poll")
                time.sleep(0.1)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                import sys, traceback
                print >> sys.stderr, 'Whoops! Problem:'
                traceback.print_exc(file=sys.stderr)

    def read(self):
        return self.device.read()

