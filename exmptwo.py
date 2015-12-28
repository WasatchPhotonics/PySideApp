#!/usr/bin/env python
# Copyright (C) 2010 Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
"""
An example script showing how to use logging with multiprocessing.

The basic strategy is to set up a listener process which can have any logging
configuration you want - in this example, writing to rotated log files. Because
only the listener process writes to the log files, you don't have file
corruption caused by multiple processes trying to write to the file.

The listener process is initialised with a queue, and waits for logging events
(LogRecords) to appear in the queue. When they do, they are processed according
to whatever logging configuration is in effect for the listener process.

Other processes can delegate all logging to the listener process. They can have
a much simpler logging configuration: just one handler, a QueueHandler, needs
to be added to the root logger. Other loggers in the configuration can be set
up with levels and filters to achieve the logging verbosity you need.

A QueueHandler processes events by sending them to the multiprocessing queue
that it's initialised with.

In this demo, there are some worker processes which just log some test messages
and then exit.

This script was tested on Ubuntu Jaunty and Windows 7.

Copyright (C) 2010 Vinay Sajip. All Rights Reserved.
"""
# You'll need these imports in your own code
import logging
import logging.handlers
import multiprocessing
import platform

# Next two import lines for this demo only
from random import choice, random
import time

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
#
# Because you'll want to define the logging configurations for listener and workers, the
# listener and worker process functions take a configurer parameter which is a callable
# for configuring logging for that process. These functions are also passed the queue,
# which they use for communication.
#
# In practice, you can configure the listener however you want, but note that in this
# simple example, the listener does not apply level or filter logic to received records.
# In practice, you would probably want to do ths logic in the worker processes, to avoid
# sending events which would be filtered out between processes.
#
# The size of the rotated files is made small so you can see the results easily.
def listener_configurer():
    root = logging.getLogger()
    #h = logging.handlers.RotatingFileHandler('/tmp/mptest.log', 'a', 300, 10)
    h = logging.handlers.RotatingFileHandler('mptest.log', 'w')
    f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    root.addHandler(h)

    import sys
    strm = logging.StreamHandler(sys.stdout)
    frmt = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    strm.setFormatter(frmt)
    root.addHandler(strm)

# This is the listener process top-level loop: wait for logging events
# (LogRecords)on the queue and handle them, quit when you get a None for a
# LogRecord.
#def listener_process(queue, configurer, update_function):
def listener_process(queue, configurer):
    configurer()
    print "Post configurerer listenere"
    while True:
        try:
            record = queue.get()
            if record is None: # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record) # No level or filter logic applied - just do it!
            #print "Actual log process for %s" % record.msg

            # Can't do this - not picklable
            #update_function(record.msg)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            import sys, traceback
            print >> sys.stderr, 'Whoops! Problem:'
            traceback.print_exc(file=sys.stderr)

# Arrays used for random selections in this demo

LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING,
          logging.ERROR, logging.CRITICAL]

LOGGERS = ['a.b.c', 'd.e.f']

MESSAGES = [
    'Random message #1',
    'Random message #2',
    'Random message #3',
]

# The worker configuration is done at the start of the worker process run.
# Note that on Windows you can't rely on fork semantics, so each process
# will run the logging configuration code when it starts.
def worker_configurer(queue):
    h = QueueHandler(queue) # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG) # send all messages, for demo; no other level or filter logic applied.

# This is the worker process top-level loop, which just logs ten events with
# random intervening delays before terminating.
# The print messages are just so you know it's doing something!
def worker_process(queue, configurer):
    configurer(queue)
    name = multiprocessing.current_process().name
    print('Worker started: %s' % name)
    for i in range(3):
        time.sleep(0.1)
        logger = logging.getLogger(choice(LOGGERS))
        level = choice(LEVELS)
        message = choice(MESSAGES)
        logger.log(level, message)
    print('Worker process: Worker finished: %s' % name)

# Here's where the demo gets orchestrated. Create the queue, create and start
# the listener, create ten workers and start them, wait for them to finish,
# then send a None to the queue to tell the listener to finish.
def main():
    queue = multiprocessing.Queue(-1)

    # Remember you have to add a local log configurator for each
    # process, including this the parent process, but only on windows, as linux
    # seems to do this automatically. If you enable this on linux you will get
    # double messages at best, or forever looping log messages
    if "Linux" not in platform.platform():
        top_handler = QueueHandler(queue)
        root = logging.getLogger()
        root.addHandler(top_handler)
        root.setLevel(logging.DEBUG)
        root.debug("Post top level configurer")

    import sys
    from PySide import QtGui, QtCore
    from pysideapp import views
    app = QtGui.QApplication([])
    my_form = views.BasicWindow()

    # Now before starting the listener process, create the qt window,
    # and pass in the control to be updated. Which you can't do, because
    # it can't be pickled.
    #listener = multiprocessing.Process(target=listener_process,
                                       #args=(queue, listener_configurer,
                                             #upd_func))

    # So try and go the other way - down in the created form, add a
    # handling routine to the existing listener that will include a
    # update to the text control box. The best you could do there is
    # continuously read off the queue, add to the text control, then put
    # it back on the queue, but you will lose entries that make it to
    # the main process first.

    # You have to have the qt interface and the listener process in the
    # same process. So instead of creating a separate process, use the
    # qt timer interface to process the queue at every timeout. Or move
    # the qt app creation into the listener process function.

    # But you have to keep the qapplication exec and the listener stuff
    # in the same process, so try and push it all down into the qt app

    # Original
    listener = multiprocessing.Process(target=listener_process,
                                       args=(queue, listener_configurer))
    listener.start()

    # Qt driven loop listener
    #my_form.qt_log_setup(queue)
    # What this creates is a qt app with a zero timeout loop that looks
    # for a non empty queue, and updates the text control with the
    # current event, after it writes to disk and stdout. The separate
    # processes below write their logging events to the same queue,
    # which handles the thread safedness.



    workers = []
    for i in range(3):
        worker = multiprocessing.Process(target=worker_process,
                                       args=(queue, worker_configurer))
        workers.append(worker)
        worker.start()

    # Stop all the queues
    #for w in workers:
    #    w.join()
    #queue.put_nowait(None)
    #listener.join()


    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
