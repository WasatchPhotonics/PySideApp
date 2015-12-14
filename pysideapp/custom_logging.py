""" Helpers and log configuration for the PySideApp application.

This module is designed to provide a single interface for custom
application wide log configuration.

"""


import sys
import logging

def to_stdout():
    log = logging.getLogger()
    strm = logging.StreamHandler(sys.stdout)
    frmt = logging.Formatter("%(asctime)s %(name)s - %(levelname)s %(message)s")
    strm.setFormatter(frmt)
    log.addHandler(strm)
    log.setLevel(logging.DEBUG)
    return log



#class ExampleObject(object):
#    def __init__(self):
#        log.debug("Init of %s", self.__class__.__name__)
#        super(ExampleObject, self).__init__()
#
#    def perform_check(self):
#        log.
