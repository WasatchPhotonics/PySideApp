# PySideApp
Minimal application demonstrating core features for deployable applications


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
    Log from multiple processes on multiple platforms

Executable building:
    Use py2exe to build a distributable binary on Windows

Installer creation:
    Example InnoSetup configuration file for installer distribution.


Running tests:

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





