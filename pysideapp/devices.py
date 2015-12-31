""" Simulated device components for PySideApp. Simple blocking calls with
simulated delays for simulated spectrometer readings. Long-polling
multiprocessing wrappers.
"""

import logging
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
