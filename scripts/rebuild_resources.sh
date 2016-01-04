#!/bin/bash
#
# Run supporting pyrcc files to generate resource files and future
# designer conversions into python code. Run this from the home project
# directory like:
# BlueGraph % ./scripts/rebuild_resources.sh

CMD_NAME="pyside-rcc"


if [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "Windows detected"
    CMD_NAME="C:\Python27\Lib\site-packages\PySide\pyside-rcc.exe"
fi

echo "Rebuilding resources file"
$CMD_NAME \
    pysideapp/assets/pysideapp_resources.qrc \
    -o pysideapp/assets/pysideapp_resources_rc.py
    #assets/bluegraph_resources.qrc \
    #-o assets/bluegraph_resources_rc.py
