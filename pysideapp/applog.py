""" Demonstration program custom logging setup and helper functions. This is
based heavily on
http://plumberjack.blogspot.com/2010/09/using-logging-with-multiprocessing.html

The general approach is that the control portion of the application instantiates
a MainLogger object below. This will create a separate process that looks for
log events on a queue. Each process of the application then registers a queue
handler, and writes its log events. The MainLogger loop will collect and write
these log events to file and any other defined logging location.

"""
import os
import sys
import logging
import platform
import multiprocessing

def get_location():
    """ Determine the location to store the log file. Current directory
    on Linux, or %PROGRAMDATA% on windows - usually c:\ProgramData\
    """
    # For convenience, replace the dot with an underscore to help windows know
    # it is a text file.
    module_name = __name__.replace(".", "_")
    suffix = "%s.txt" % module_name

    if "Linux" in platform.platform():
        return suffix

    log_dir = ""
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

    windows_file = "%s/%s" % (log_dir, suffix)
    return(windows_file)

def process_log_configure(log_queue):
    """ Called at the beginning of every process, including the main process.
    Adds a queue handler object to the root logger to be processed in the main
    listener.

    Only on Windows though. Apparently Linux will pass the root logger amongst
    processes as expected, so if you add another queue handler you will get
    double log prints.
    """
    root_log = logging.getLogger()
    if "Windows" in platform.platform():
        queue_handler = QueueHandler(log_queue)
        root_log.addHandler(queue_handler)
        root_log.setLevel(logging.DEBUG)

    root_log.debug("Sub process setup configuration")

def get_text_from_log():
    """ Mimic the capturelog style of just slurping the entire log
    file contents.
    """

    log_text = ""

    with open(get_location()) as log_file:
        for line_read in log_file:
            log_text += line_read

    return log_text


def log_file_created():
    """ Helper function that returns True if file exists, false otherwise.
    """
    filename = get_location()
    if os.path.exists(filename):
        return True

    return False

def delete_log_file_if_exists():
    """ Remove the specified log file and return True if succesful.
    """
    filename = get_location()

    if os.path.exists(filename):
        os.remove(filename)

    if os.path.exists(filename):
        print "Problem deleting: %s", filename
        return False
    return True

def explicit_log_close():
    """ Apparently, tests run in py.test will not remove the existing
    handlers as expected. This mainfests as hanging tests during py.test
    runs, or after non-termination hang of py.test after all tests report
    succesfully. Only on linux though, windows appears to Do What I Want.
    Use this function to close all of the log file handlers, including the
    QueueHandler custom objects.
    """
    root_log = logging.getLogger()
    handlers = root_log.handlers[:]
    for handler in handlers:
        handler.close()
        root_log.removeHandler(handler)



class QueueHandler(logging.Handler):
    """
    Copied verbatim from PlumberJack (see above)
    This is a logging handler which sends events to a multiprocessing queue.

    The plan is to add it to Python 3.2, but this can be copy pasted into
    user code for use with earlier Python versions.
    """

    def __init__(self, log_queue):
        """
        Initialise an instance, using the passed queue.
        """
        logging.Handler.__init__(self)
        self.log_queue = log_queue

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
            self.log_queue.put_nowait(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class MainLogger(object):
    def __init__(self):
        self.log_queue = multiprocessing.Queue(-1)
        self.listener = multiprocessing.Process(target=self.listener_process,
                                        args=(self.log_queue, self.listener_configurer))
        self.listener.start()

        # Remember you have to add a local log configurator for each
        # process, including this, the parent process
        top_handler = QueueHandler(self.log_queue)
        root_log = logging.getLogger()
        root_log.addHandler(top_handler)
        root_log.setLevel(logging.DEBUG)
        root_log.debug("Top level log configuration")

    def listener_configurer(self):
        """ Setup file handler and command window stream handlers. Every log
        message received on the queue handler will use these log configurers.
        """

        log_dir = get_location()

        root = logging.getLogger()
        h = logging.FileHandler(log_dir, 'w') # Overwrite previous run
        frmt = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        h.setFormatter(frmt)
        root.addHandler(h)

        # Specifing stderr as the log output location will cause the creation of
        # a _module_name_.exe.log file when run as a post-freeze windows
        # executable.
        strm = logging.StreamHandler(sys.stdout)
        strm.setFormatter(frmt)
        root.addHandler(strm)

    # This is the listener process top-level loop: wait for logging events
    # (LogRecords)on the queue and handle them, quit when you get a None for a
    # LogRecord.
    def listener_process(self, log_queue, configurer):
        configurer()
        while True:
            try:
                record = log_queue.get()
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
        """ Wrapper to add a None poison pill to the listener process queue to
        ensure it exits.
        """
        self.log_queue.put_nowait(None)
        self.listener.join()
