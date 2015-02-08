#!/usr/bin/env python

# Opens a file in TextEdit.

from appscript import *

def openFile():
    app('TextEdit').open(mactypes.Alias('Open_file_in_TextEdit.py'))

def saveFile(fname):
    app(u'TextEdit').activate()
    app(u'TextEdit').documents[1].save(in_=fname, as_=k.alias)

def recopy_as_plaintext():
    app(u'TextEdit').activate()
    app(u'TextEdit').make(new=k.document)
    app(u'System Events').processes[u'TextEdit'].key_code(17, using=[k.command_down, k.shift_down])
    app(u'System Events').processes[u'TextEdit'].key_code(9, using=k.command_down)
    app(u'System Events').processes[u'TextEdit'].key_code(17, using=[k.command_down, k.shift_down])
    app(u'System Events').processes[u'TextEdit'].windows[1].sheets[1].buttons[u'OK'].click()
    app(u'System Events').processes[u'TextEdit'].key_code(0, using=k.command_down)
    app(u'System Events').processes[u'TextEdit'].key_code(8, using=k.command_down)
