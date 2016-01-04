# PySideApp

Why is this build broken? Queue Handler removal in py.test                                                
                                                                                                              
I never want to see this error again, so these two builds are left in                                         
here with the debug statements and broken build statuses. Run py.test on                                      
Linux, and you should see a hang in the test suite. Possibly after all                                        
tests have been run, possibly in a specific test. Run py.test on Windows                                      
and all of the tests will report successful with no hang.                                                     
Run the tests/test_ files individually, and all is well.
This is apparently due to the addition of the QueueHandler to the custom
logging. Removing the queuehandler from the root logger at the end of
every test case appears to clear up this issue. 


Again, this is only if the entire test suite is run. And only at
specific iteractions of the custom logging setup and py.test.  This
particular branch will hang on the 5th test of test_devices.py when all
tests are run with py.test. But only on Linux and Travis, not on MS
windows.








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




