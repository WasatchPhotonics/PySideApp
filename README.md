# PySideApp
Minimal application demonstrating core features for deployable applications

[![Build Status](https://travis-ci.org/WasatchPhotonics/PySideApp.svg?branch=master)](https://travis-ci.org/WasatchPhotonics/PySideApp.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/WasatchPhotonics/PySideApp/badge.svg?branch=master&service=github)](https://coveralls.io/github/WasatchPhotonics/PySideApp?branch=master)

PySideApp is designed to be the baseline project structure for the next
level of Wasatch Photonics customer facing software. The main design
goals are:

PySide Gui application development
    Develop on Windows and Linux with PySide 

MVC Architecture:
   Well defined interfaces for easier testability 

100% Test Coverage:
    Use pytest-qt and qtbot to click buttons and simulator an operator

Continuous Integration ready:
    Example travis configuration
    draft appveyor configuration

Multiprocessing:
    Provide framework for long-polling reads from hardware

Logging:
    Capture log output in test, verify logging configuration
    Log from multiple processes on multiple platforms

Executable building:
    Use py2exe to build a distributable binary on Windows

Installer creation:
    Example InnoSetup configuration file for installer distribution.


Running tests:

    First, install the python package in development mode:
        python setup.py develop

    All Tests, with coverage report showing missing lines:
        py.test tests/ --cov=pysideapp --cov-report term-missing

    Individually:
        py.test tests/test_views.py 

    Single test case:
        py.test tests/test_views.py -k test_form_has_text_and_button

    Showing log prints during the process:
        py.test tests/test_device.py --capture=no

        If pytest-capturelog is installed:
        py.test tests/test_device.py --capture=no 





