""" Helpers and log configuration for the PySideApp application.

This module is designed to provide a single interface for custom
application wide log configuration.
"""

import sys
import logging
import platform

def to_stdout():
    log = logging.getLogger()
    strm = logging.StreamHandler(sys.stdout)
    frmt = logging.Formatter("%(asctime)s %(name)s - %(levelname)s %(message)s")
    strm.setFormatter(frmt)
    log.addHandler(strm)
    log.setLevel(logging.DEBUG)
    return log


def get_location():
    """ Determine the location to store the log file. Current directory
    on Linux, or %PROGRAMDATA% on windows - usually c:\ProgramData\
    """
    log_dir = "./"

    if "Linux" in platform.platform():
        return log_dir

    try:
        import ctypes
        from ctypes import wintypes, windll
        CSIDL_COMMON_APPDATA = 35
        _SHGetFolderPath = windll.shell32.SHGetFolderPathW
        _SHGetFolderPath.argtypes = [wintypes.HWND,
                                    ctypes.c_int,
                                    wintypes.HANDLE,
                                    wintypes.DWORD, wintypes.LPCWSTR]

        path_buf = wintypes.create_unicode_buffer(wintypes.MAX_PATH)
        result = _SHGetFolderPath(0, CSIDL_COMMON_APPDATA, 0, 0, path_buf)
        log_dir = path_buf.value
    except:
        log.exception("Problem assigning log directory")

    return(log_dir)



def dependent_create(log, in_pytest=False):
    """ If operating on MS windows in a multiprocessing context
    while using pytest, the log prints to stdout will not appear.
    Create a new logger with a formatter to stdout if operating on
    windows only, and only if called within pytest. If you only
    check if within pytest and create the logger on linux, you will
    have two identical loggers.
    """
    if in_pytest == False:
        log.info("Non pytest, return existing log")
        return log

    if "Windows" in platform.platform():
        self.my_log = custom_logging.to_stdout()
        self.my_log.debug("Custom pytest windows log setup")
        return self.my_log

    log.info("In pytest, return existing log")
    return log

def to_file_and_stdout(application_name="PySideApp"):
    log = to_stdout()

    log_dir = get_location()
    log_dir += "/%s_log.txt" % application_name

    frmt = logging.Formatter("%(asctime)s %(name)s - %(levelname)s %(message)s")
    file_handler = logging.FileHandler(log_dir)
    file_handler.setFormatter(frmt)

    log.addHandler(file_handler)
    log.debug("Log file is: %s", log_dir)
    return log
