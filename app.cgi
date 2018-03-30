#!/usr/bin/python3

import wsgiref.handlers as wsg
import os
import sys
import traceback

debug = os.environ.get('DEBUG') is not None

try:
    from app import app as application
    if debug:
        from werkzeug.debug import DebuggedApplication
        application = DebuggedApplication(application, True)

    wsg.CGIHandler().run(application)
except:
    if debug:
        print("\n\n<pre>")
        sys.stderr = sys.stdout
        traceback.print_exc()
        print("</pre>")
    else:
        print('<h1>Error</h1>')

