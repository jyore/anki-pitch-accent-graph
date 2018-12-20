# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import anki
import aqt

from .gui.base import ICON
from .gui.bulk import BulkAdd
from .gui.single import SingleAdd


__all__ = ['menus']

aqt.mw.bulk_add = BulkAdd(aqt.mw)
aqt.mw.single_add = SingleAdd(aqt.mw)



def menus():

    def browser_menu(browser):
        menu = aqt.qt.QMenu("Pitch Accent Graphs", browser.form.menubar)
        browser.form.menubar.addMenu(menu)

        bulk_action = aqt.qt.QAction("Bulk-add Pitch Accent Graphs", menu)
        bulk_action.triggered.connect(lambda: aqt.mw.bulk_add.show(browser))
        menu.addAction(bulk_action)

        def update_title_wrapper(browser):
            bulk_action.setEnabled(bool(browser.form.tableView.selectionModel().selectedRows()))

        aqt.browser.Browser.updateTitle = anki.hooks.wrap(
            aqt.browser.Browser.updateTitle,
            update_title_wrapper,
            'before'
        )

    def context_menu(view, menu):
        submenu = aqt.qt.QMenu("Pitch Accent Graph", menu)
        submenu.addAction("Add to Note", lambda: aqt.mw.single_add.show(view))
        menu.addMenu(submenu)


    def editor_menu(editor):

        btn = aqt.qt.QPushButton(ICON,None)
        btn.setFixedWidth(20)
        btn.setFixedHeight(20)
        btn.setFocusPolicy(aqt.qt.Qt.NoFocus)
        btn.setToolTip("Add Pitch Accent Graph to Note")
        btn.connect(btn, aqt.qt.SIGNAL("clicked()"), lambda: aqt.mw.single_add.show(editor)) 

        editor.iconsBox.addWidget(btn)
        

    anki.hooks.addHook("browser.setupMenus", browser_menu)
    anki.hooks.addHook("EditorWebView.contextMenuEvent", context_menu)
    anki.hooks.addHook("setupEditorButtons", editor_menu)
