# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import anki
import aqt


__all__ = ['menus']


#XXX: TEMP
def dummy(obj):
  from .capture import generate
  generate("あそこに立ってる人、もしかして部長!?", result)


#XXX: TEMP
def result(image):
  import uuid

  fn = "%s.png" % uuid.uuid4()
  image.save(fn) 
  aqt.utils.showInfo(fn)


def menus():

  def browser_menu(browser):
    action = aqt.qt.QAction("Bulk-add Pitch Accent Graphs", browser)
    action.triggered.connect(lambda: dummy(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(action)      

  def config_menu(mw):
    action = aqt.qt.QAction("Pitch Accent Graphs...", mw)
    mw.connect(action, aqt.qt.SIGNAL("triggered()"), lambda: dummy(mw))
    mw.form.menuTools.addAction(action)

  def context_menu(view, menu):
    submenu = aqt.qt.QMenu("Pitch Accent Graphs", menu)
    submenu.addAction("Add to Note",lambda: dummy(menu))
    menu.addMenu(submenu)


  anki.hooks.addHook("browser.setupMenus", browser_menu)
  anki.hooks.addHook("EditorWebView.contextMenuEvent", context_menu)
  config_menu(aqt.mw)
