# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import anki
import aqt

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
