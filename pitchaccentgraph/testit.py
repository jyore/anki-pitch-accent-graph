# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aqt.qt import *
from aqt import mw
from aqt.utils import tooltip, showInfo

from .capture import CaptureWorker
from .gui.base import Dialog

received = []
def onDataReady(ref,exp,fn):
  received.append("%s(%s)" % (ref, fn))


class MyTest(Dialog):

  def __init__(self, mw):
    super(MyTest, self).__init__("Testing", mw)

    self.config_action = QAction("TEST STUFF", mw)
    mw.connect(self.config_action, SIGNAL("triggered()"), self.setup)
    mw.form.menuTools.addAction(self.config_action)

    self.thread = QThread()
    self.obj = CaptureWorker()
    self.obj.dataReady.connect(onDataReady)
    self.obj.moveToThread(self.thread)
    self.obj.finished.connect(self.thread.quit)
    self.obj.finished.connect(lambda: mw.progress.finish())
    self.thread.connect(self.thread, SIGNAL("finished()"), self.thread.terminate)


  def ui(self):
    layout = super(MyTest, self).ui()
    layout.addWidget(self.ui_buttons())

    return layout


  def setup(self):
    global received

    self.setLayout(self.ui())
    self.thread.start()    

    if self.exec_():
        pass


  def accept(self):
    mw.progress.start(immediate=True)
    QMetaObject.invokeMethod(self.obj, 'process', Qt.QueuedConnection,
          Q_ARG(list, build_notes())
    )
    super(MyTest, self).accept()


def build_notes():
  results = []

  nids = mw.col.db.all('select n.id from notes n')
  for nid, in nids:
    note = mw.col.getNote(nid)

    fields = mw.col.models.fieldNames(note.model())
    if 'Expression' in fields:
      ref = nid
      exp = mw.col.media.strip(note['Expression'])
      
      results.append((str(ref),exp))

  return results
