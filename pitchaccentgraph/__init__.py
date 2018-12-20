# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import anki
import aqt


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


    anki.hooks.addHook("browser.setupMenus", browser_menu)
    anki.hooks.addHook("EditorWebView.contextMenuEvent", context_menu)
    


#from .actions import add_to_note, bulk_add, configure
#
#__all__ = ['menus']
#
#
#def menus():
#
#  def browser_menu(browser):
#    action = aqt.qt.QAction("Bulk-add Pitch Accent Graphs", browser)
#    action.triggered.connect(lambda: bulk_add(browser))
#    browser.form.menuEdit.addSeparator()
#    browser.form.menuEdit.addAction(action)      
#
#  def config_menu(mw):
#    action = aqt.qt.QAction("Pitch Accent Graphs...", mw)
#    mw.connect(action, aqt.qt.SIGNAL("triggered()"), lambda: configure(mw))
#    mw.form.menuTools.addAction(action)
#
#  def context_menu(view, menu):
#    submenu = aqt.qt.QMenu("Pitch Accent Graphs", menu)
#    submenu.addAction("Add to Note",lambda: add_to_note(menu))
#    menu.addMenu(submenu)
#
#
#  anki.hooks.addHook("browser.setupMenus", browser_menu)
#  anki.hooks.addHook("EditorWebView.contextMenuEvent", context_menu)
#  config_menu(aqt.mw)
