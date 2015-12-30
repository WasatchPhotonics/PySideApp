""" PySideApp custom logging setup and helper functions. This is based heavily on
http://plumberjack.blogspot.com/2010/09/using-logging-with-multiprocessing.html

The general approach is that the control portion of the application instantiates
a MainLogger object below. This will create a separate process that looks for
log events on a queue. Each process of the application then registers a queue
handler, and writes its log events. The MainLogger loop will collect and write
these log events to file and any any other defined logging location.

"""
import sys
import logging
import platform
import multiprocessing

def get_location():
    """ Determine the location to store the log file. Current directory
    on Linux, or %PROGRAMDATA% on windows - usually c:\ProgramData\
    """
    log_dir = "./"
    return(log_dir)

class QueueHandler(logging.Handler):
    """
    Copied verbatim from PlumberJack (see above)
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
        # process, including this, the parent process
        top_handler = QueueHandler(self.queue)
        root = logging.getLogger()
        root.addHandler(top_handler)
        root.setLevel(logging.DEBUG)
        root.debug("Top level log configuration")

    def listener_configurer(self):
        """ Setup file handler and command window stream handlers. Every log
        message received on the queue handler will use these log configurers.
        """

        log_dir = get_location()
        log_dir += "/%s_log.txt" % "mptest"

        root = logging.getLogger()
        h = logging.FileHandler(log_dir, 'w') # Overwrite previous run
        frmt = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        h.setFormatter(frmt)
        root.addHandler(h)

        strm = logging.StreamHandler(sys.stdout)
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
        """ Wrapper to add a None poison pill to the listener process queue to
        ensure it exits.
        """
        self.queue.put_nowait(None)
