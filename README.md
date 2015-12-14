# PySideApp
Minimal application demonstrating core features for deployable applications

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

    All Tests:
        py.test tests/ --cov=pysideapp 

    With coverage report showing missing lines:
        coverage report -m 

    Individually:
        py.test tests/test_views.py 

    Single test case:
        py.test tests/test_views.py -k test_form_has_text_and_button

    Showing log prints during the process:
        py.test tests/test_device.py --capture=no





