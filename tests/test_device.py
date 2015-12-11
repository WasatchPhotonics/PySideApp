""" tests for multiprocessing simulation devices provided in PySideApp
"""

import time

from pysideapp import device
from pysideapp import custom_logging

log = custom_logging.to_stdout()

#import multiprocessing
#multiprocessing.log_to_stderr(logging.DEBUG)

class TestMultiprocessingDevice:
    def test_poison_pill_technique(self):
        mp_device = device.QueueMPDevice(pytest=True)
        mp_device.create()

        assert mp_device.process_started == True

        sleep_dur = 0.3
        log.debug("Main process sleep: %s", sleep_dur)
        time.sleep(sleep_dur)

        mp_device.close()
        assert mp_device.process_started == False

class TestProcessLogs:
    def test_object_has_log_debug(self):
        from fastpm100 import devices
        mp_device = devices.QueueMPDevice()
        mp_device.create()

        sleep_dur = 1
        count = 0
        while(1):
            log.debug("Sleep: %s", sleep_dur)
            time.sleep(sleep_dur)
            count += 1
            if count > 3:
                break

        mp_device.close()


    #def test_object_called_linked_in_pyside_has_log_prints(self):

