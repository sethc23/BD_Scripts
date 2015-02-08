#!/usr/bin/env python

# Prints the sub-folder hierarchy of a given folder as a list of folder names
# indented according to depth.

from appscript import *


# printfoldertree(app('Finder').home.folders['Documents'])
def printfoldertree(folder, indent=''):
    """Print a tab-indented list of a folder tree."""
    print indent + folder.name.get().encode('utf8')
    for folder in folder.folders.get():
        printfoldertree(folder, indent + '\t')

def path_to_front_Finder_window():
    finder = app('Finder')
    w = finder.Finder_windows[1]

    if w.exists():  # is there a Finder window open?
        if w.target.class_.get() == k.computer_object:
            # 'Computer' windows don't have a target folder, for obvious reasons.
            raise RuntimeError, "Can't get path to 'Computer' window."
        folder = w.target  # get a reference to its target folder
    else:
        folder = finder.desktop  # get a reference to the desktop folder
    path = folder.get(resulttype=k.alias).path  # get folder's path
    print path

def stagger_windows():
    x, y = 0, 44
    offset = 22

    for window in app('Finder').windows.get()[::-1]:
        x1, y1, x2, y2 = window.bounds.get()
        window.bounds.set((x, y, x2 - x1 + x, y2 - y1 + y))
        x += offset
        y += offset

def select_all_HTML_files():
    finder = app('Finder')
    finder.activate()
    w = finder.Finder_windows[1].target.get()
    w.files[its.name_extension.isin(['htm', 'html'])].select()

def get_selection():
    app(u'Finder').activate()
    return app(u'Finder').selection.get(resulttype=k.unicode_text)


