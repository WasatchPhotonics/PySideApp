# PySideApp
Minimal application demonstrating core features for deployable applications

[![Travis Build Status](https://travis-ci.org/WasatchPhotonics/PySideApp.svg?branch=master)](https://travis-ci.org/WasatchPhotonics/PySideApp?branch=master)
[![Appveyor Build Status](https://ci.appveyor.com/api/projects/status/uq88jhfykrh6k940?svg=true)](https://ci.appveyor.com/project/NathanHarrington/pysideapp)
[![Coverage Status](https://coveralls.io/repos/WasatchPhotonics/PySideApp/badge.svg?branch=master&service=github)](https://coveralls.io/github/WasatchPhotonics/PySideApp?branch=master)

PySideApp is designed to be the baseline project structure for the next
level of Wasatch Photonics customer facing software. The main design
goals are:

    PySide Gui application development
        Develop on Windows and Linux with PySide 

    MVC Architecture:
        Well defined interfaces for easier testability 

    100% Test Coverage:
        Use pytest-qt and qtbot to click buttons and simulate an operator

    Continuous Integration ready:
        Example travis configuration
        Example appveyor configuration

    Multiprocessing:
        Provide framework for long-polling reads from hardware

    Logging:
        Capture log output in test, verify logging configuration
        Log from multiple processes on multiple platforms

    Executable building:
        Use pyinstaller to build a distributable binary on Windows

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


Converting to a new project:
    Copy over this full directory tree, and replace every instance of
    PySideApp with the new project name. Pay attention to the case
    sensitivity where appropriate. For example, if the new project name
    is FastPM100, you would do:

    cd projects
    git clone https://github.com/WasatchPhotonics/PySideApp FastPM100

    cd FastPM100
    rm -rf .git
    mv pysideapp fastpm100
    mv scripts/PySideApp.py scripts/FastPM100.py

    In the following files, change the module name from pysideapp to
    fastpm100:
    setup.py
    tests/test_applog.py
    tests/test_control.py
    tests/test_devices.py
    tests/test_views.py

    Update README.md, replace PySideApp with FastPM100

    Update .travis.yml, replace pysideapp module name with fastpm100.

    Update appveyor.yml, in pyinstall section, change pysideapp in
    assets directory to fastpm100.  Change scripts/PySideApp.py to
    scripts/AutoFallOff.py.  Change PySideApp.zip file entries to
    FastPM100.zip

    Update scripts/Application_InnoSetup.iss, change MyAppName from
    PySideApp to FastPM100 and module_name pysideapp to fastpm100.
    Generate a new UID for this application with the InnoSetup
    interface.

    Update scripts/create_installer.sh, change pysideapp in icon assets
    directory to fastpm100. Change scripts/PySideApp.py to
    scripts/AutoFallOff.py

    Update scripts/FastPM100.py change the module name references from
    pysideapp to fastpm100. Change the Class name from PySideApplication
    to FastPM100Application.

    git init
    git add ./
    git commit -a -m "Initial pysideapp conversion"

    Create project on github
    git remote add origin https://github.com/WasatchPhotonics/FastPM100.git
    git push -u origin master

    Use travis, appveyor, coveralls web interfaces to enable CI builds.
    Update travis, appveyor and coveralls badges after CI setup.

    To build the installer on windows, run:
    Install InnoSetup 5.5.1
    Install git-bash 2.7.2
    Install python(xy) 2.7.10

    cd AutoFallOff
    pip install pyinstaller
    python setup.py develop
    ./scripts/create_installer.sh

    The appveyor configuration builds this as well, using conda and
    nuget for package installations.
