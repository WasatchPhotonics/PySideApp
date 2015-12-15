""" tests for multiprocessing simulation devices provided in PySideApp
"""

import time

from pysideapp import device
from pysideapp import custom_logging

log = custom_logging.to_file_and_stdout()

class TestMultiprocessingDevice:
    def test_poison_pill_technique(self):
        """ Invalid implementations of a multiprocessing architecture
        will cause this test to fail at different levels. See the device
        module itself for details on these potential failures and
        workarounds.
        """
        mp_device = device.QueueMPDevice(in_pytest=True)
        mp_device.create()

        assert mp_device.started == True

        sleep_dur = 0.3
        log.debug("Main process sleep: %s", sleep_dur)
        time.sleep(sleep_dur)

        mp_device.close()
        assert mp_device.started == False


    def test_only_worker_portion_pytest_coverage_workaround(self):
        import multiprocessing
        mp_device = device.QueueMPDevice(in_pytest=True)

        local_queue = multiprocessing.Queue()
        in_pytest = True

        local_queue.put("DISCONNECT")
        mp_device.worker(local_queue, in_pytest)

    #def test_sub_process_logs_are_received_in_pytest_mode(self):

    #def test_sub_process_logs_are_discarded_without_pytest_mode(self):

