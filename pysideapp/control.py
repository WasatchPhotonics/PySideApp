""" Application level controller for PySideApp. Handles data model and UI
updates with MVC style architecture.
"""

import logging

from pysideapp import views

# Do you want this here - or do you want the queue handler listener started
# here?
log = logging.getLogger(__name__)


class Controller(object):
    def __init__(self):
        log.debug("Control startup")
        self.form = views.BasicWindow()

