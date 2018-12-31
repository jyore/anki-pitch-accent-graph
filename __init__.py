# -*- coding: utf-8 -*-

# NOTE: Add the support directory to the sys path so 
# that dependency modules can be imported
import os,sys
import platform
import struct

system = platform.system()
if system == 'Darwin':
    PLATFORM = 'osx'
elif system == 'Linux':
    if struct.calcsize('P') * 8 == 64:
        PLATFORM = 'linux_x86_64'
    else:
        PLATFORM = 'linux_i686'
else:
    PLATFORM = 'windows'

ppath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "support", PLATFORM)
if not os.path.isdir(os.path.join(ppath, 'PIL')):
    import zipfile
    with zipfile.ZipFile(os.path.join(ppath, 'PIL.zip')) as z:
        z.extractall(ppath)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "support", "common"))
sys.path.insert(0, ppath)



import anki
import time, random

from aqt import mw
from aqt.qt import *
from aqt.browser import Browser
from aqt.utils import tooltip, showInfo

from .gui.base import ICON
from .gui.bulk import BulkAdd
from .gui.single import SingleAdd


mw.pitchaccentgraphs = {
    'bulkadd': BulkAdd(mw),
    'single':  SingleAdd(mw)
}


# NOTE: Need to make this global or else the reference becomes lost
bulk_action = None

def browser_menu(browser):
    global bulk_action

    menu = QMenu("Pitch Accent Graphs", browser.form.menubar)
    browser.form.menubar.addMenu(menu)

    bulk_action = QAction("Bulk-add Pitch Accent Graphs", menu)
    bulk_action.triggered.connect(lambda: mw.pitchaccentgraphs['bulkadd'].show(browser))
    menu.addAction(bulk_action)

    def update_title_wrapper(browser):
        bulk_action.setEnabled(bool(browser.form.tableView.selectionModel().selectedRows()))

    Browser.updateTitle = anki.hooks.wrap(Browser.updateTitle, update_title_wrapper, 'before')


def context_menu(view, menu):
    submenu = QMenu("Pitch Accent Graph", menu)
    submenu.addAction("Add to Note", lambda: mw.pitchaccentgraphs['single'].show(view))
    menu.addMenu(submenu)


def editor_menu(buttons, editor):
    button = editor.addButton(
        ICON,
        "pitchaccentgraph",
        mw.pitchaccentgraphs['single'].show,
        tip="Add Pitch Accent Graph to Note"
    )

    buttons.insert(0, button)
    return buttons

anki.hooks.addHook("browser.setupMenus", browser_menu)
anki.hooks.addHook("EditorWebView.contextMenuEvent", context_menu)
anki.hooks.addHook("setupEditorButtons", editor_menu)
