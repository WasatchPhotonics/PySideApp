"""This is based heavily on:
http://ralsina.me/weblog/posts/BB955.html

Run:
    change the project_name and module_name variables below
    cd ProjectName
    python scripts/py2exe_application.py py2exe
"""

from distutils.core import setup
import py2exe

project_name = "PySideApp"
module_name = "pysideapp"

setup(windows=[
                {   "script":"scripts/%s.py" % project_name,
                    "icon_resources":
                    [
                        (0, "%s/assets/images/ApplicationIcon.ico" \
                            % module_name)
                    ],
                }
              ],
      options={"py2exe": {

                            "dll_excludes": [ "MSVCP90.dll", "MSWSOCK.dll",
                                              "mswsock.dll", "powrprof.dll",
                                              "w9xpopen.exe",
                                            ],
                            "includes": ["PySide"],
                            "excludes": [],

                            "dist_dir": "scripts/built-dist",
                          },


              },

       # Create a subdirectory imageformats and put the qico4.dll file
       # inside of it.  This is required to read the application icon at
       # runtime.
       #data_files = [],
       data_files = [
                        ("imageformats",
                         ["C:\Python27.10\Lib\site-packages\PySide\plugins\imageformats\qico4.dll"]
                        ),
                    ],
       zipfile=None
     )

