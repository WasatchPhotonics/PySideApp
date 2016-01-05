"""This is based heavily on:
http://ralsina.me/weblog/posts/BB955.html

Run:
    cd PySideApp
    python scripts/py2exe_PySideApp.py py2exe
"""

from distutils.core import setup
import py2exe

setup(windows=[
                {   "script":"scripts/PySideApp.py",
                    "icon_resources": 
                    [
                        (0, "pysideapp/assets/images/PySideAppIcon.ico")
                    ],
                }
              ],
      options={"py2exe": {

                            "dll_excludes": [ "MSVCP90.dll", "MSWSOCK.dll",
                                              "mswsock.dll", "powrprof.dll",
                                              "w9xpopen.exe",
                                            ],
                            "includes": [],
                            "excludes": [],

                            "dist_dir": "scripts/built-dist-PySideApp",
                          },


              },

       # Create a subdirectory imageformats and put the qico4.dll file
       # inside of it.  This is required to read the application icon at
       # runtime.
       data_files = [],
       #data_files = [
                        #("imageformats",
                         #["C:\Python27\Lib\site-packages\PySide\plugins\imageformats\qico4.dll"]),
                    #],
       zipfile=None
     )

