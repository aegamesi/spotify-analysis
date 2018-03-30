#!/usr/bin/python3

import secret
import wsgiref.handlers as wsg
import os
import sys
import traceback

try:
    from app import app as application
    if secret.DEBUG:
        from werkzeug.debug import DebuggedApplication
        application = DebuggedApplication(application, True)

    wsg.CGIHandler().run(application)
except:
    print('Content-Type: text/html')
    print()
    if secret.DEBUG:
        print("\n\n<pre>")
        sys.stderr = sys.stdout
        traceback.print_exc()
        print("</pre>")
    else:
        print('<h1>Error</h1>')

