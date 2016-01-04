"""This is based heavily on:
http://ralsina.me/weblog/posts/BB955.html

Run:
    cd PySideApp
    python scripts/py2exe_PySideApp.py py2exe
"""

from distutils.core import setup
import py2exe

setup(windows=["scripts/PySideApp.py"],
      options={"py2exe": {

                            "dll_excludes": [ "MSVCP90.dll", "MSWSOCK.dll",
                                              "mswsock.dll", "powrprof.dll",
                                              "w9xpopen.exe",
                                            ],
                            "includes": [],
                            "excludes": [],

                            "bundle_files": 1,

                            "dist_dir": "built-dist-PySideApp",
                          },


              },

       data_files = [],
       zipfile=None
     )

