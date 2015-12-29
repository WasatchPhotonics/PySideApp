""" example queue handler logging routines based on:
http://plumberjack.blogspot.com/2010/09/using-logging-with-multiprocessing.html
"""
import sys
import time
import logging
import logging.handlers
import multiprocessing


#log = logging.getLogger(__name__)

class SimulateMain(object):
    def __init__(self):
        super(SimulateMain, self).__init__()
        #log.debug("Start simulate main")

    def create_proc(self):

        queue = multiprocessing.Queue(-1)

        listener = multiprocessing.Process(target=self.listener_process,
                                        args=(queue, self.listener_configurer))
        listener.start()

        #h = QueueHandler(queue)
        #root = logging.getLogger()
        #root.addHandler(h)
        #root.setLevel(logging.DEBUG)
        #root.debug("In create proc")

        workers = []
        for i in range(1):
            worker = multiprocessing.Process(target=self.worker_process,
                                        args=(queue, self.worker_configurer))
            workers.append(worker)
            worker.start()
        for w in workers:
            w.join()
        queue.put_nowait(None)
        listener.join()

    def worker_configurer(self, queue):
        queue_h = QueueHandler(queue) # Just the one handler needed
        root = logging.getLogger()
        root.addHandler(queue_h)
        root.setLevel(logging.DEBUG) # send all messages, for demo; no other level or filter logic applied.

    def worker_process(self, queue, configurer):
        configurer(queue)
        name = multiprocessing.current_process().name
        print('Worker started: %s' % name)

        #logger = logging.getLogger(__name__)
        #logger.log(logging.INFO, "inside worker process %s", name)
        for i in range(10):
            time.sleep(0.1)
            root = logging.getLogger()
            root.debug("Inside a worker process")
            #logger = logging.getLogger(choice(LOGGERS))
            #level = choice(LEVELS)
            #message = choice(MESSAGES)
            #logger.log(level, message)

        print('Worker finished: %s' % name)

    def listener_configurer(self):
        root = logging.getLogger()
        file_h = logging.FileHandler("mptest.log", mode="w")
        frmt = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        file_h.setFormatter(frmt)
        root.addHandler(file_h)

        strm_h = logging.StreamHandler(sys.stdout)
        strm_h.setFormatter(frmt)
        root.addHandler(strm_h)

    def listener_process(self, queue, configurer):
        configurer()

        # This will not appear in the stdout, as you have to add it to the queue
        # handler, which for this demo is only done int he worker process
        print("PRINT Setup listener process")

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
