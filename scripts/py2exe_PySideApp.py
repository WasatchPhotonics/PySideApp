"""This is based heavily on:
http://ralsina.me/weblog/posts/BB955.html

"""

from distutils.core import setup
import py2exe

setup(console=["exmp_four.py"],
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

