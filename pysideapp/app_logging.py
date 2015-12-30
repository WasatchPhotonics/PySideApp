import logging
import logging.handlers
import multiprocessing

import sys
import platform
from multiprocessing import Process, freeze_support

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

class QueueHandler(logging.Handler):
    """
    This is a logging handler which sends events to a multiprocessing queue.

    The plan is to add it to Python 3.2, but this can be copy pasted into
    user code for use with earlier Python versions.
    """

    def __init__(self, queue):
        """
        Initialise an instance, using the passed queue.
        """
        logging.Handler.__init__(self)
        self.queue = queue

    def emit(self, record):
        """
        Emit a record.

        Writes the LogRecord to the queue.
        """
        try:
            ei = record.exc_info
            if ei:
                dummy = self.format(record) # just to get traceback text into record.exc_text
                record.exc_info = None  # not needed any more
            self.queue.put_nowait(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class MainLogger(object):
    def __init__(self):
        self.queue = multiprocessing.Queue(-1)
        self.listener = multiprocessing.Process(target=self.listener_process,
                                        args=(self.queue, self.listener_configurer))
        self.listener.start()

        # Remember you have to add a local log configurator for each
        # process, including this the parent process
        top_handler = QueueHandler(self.queue)
        root = logging.getLogger()
        root.addHandler(top_handler)
        root.setLevel(logging.DEBUG)
        root.debug("Post top level configurer")

    def listener_configurer(self):
        log_dir = get_location()
        log_dir += "/%s_log.txt" % "mptest"
        root = logging.getLogger()
        h = logging.handlers.RotatingFileHandler(log_dir, 'w')
        f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        h.setFormatter(f)
        root.addHandler(h)

        strm = logging.StreamHandler(sys.stdout)
        frmt = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        strm.setFormatter(frmt)
        root.addHandler(strm)

    # This is the listener process top-level loop: wait for logging events
    # (LogRecords)on the queue and handle them, quit when you get a None for a
    # LogRecord.
    def listener_process(self, queue, configurer):
        configurer()
        while True:
            try:
                record = queue.get()
                if record is None: # We send this as a sentinel to tell the listener to quit.
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record) # No level or filter logic applied - just do it!
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                import sys, traceback
                print >> sys.stderr, 'Whoops! Problem:'
                traceback.print_exc(file=sys.stderr)

    def close(self):
        self.queue.put_nowait(None)
