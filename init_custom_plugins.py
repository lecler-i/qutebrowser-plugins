import os
import sys
from qutebrowser import app

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import buku_integration

orig_qt_mainloop = app.qt_mainloop

def hook_qt_mainloop():
    buku_integration.init()
    return orig_qt_mainloop()

app.qt_mainloop = hook_qt_mainloop
