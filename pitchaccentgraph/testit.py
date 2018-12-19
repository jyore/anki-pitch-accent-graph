# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aqt.qt import *
from aqt import mw
from aqt.utils import tooltip, showInfo

from .capture import CaptureWorker

received = []
def onDataReady(ref,exp,fn):
  received.append("%s(%s)" % (ref, fn))


class MyTest():

  def __init__(self, mw):
    self.config_action = QAction("TEST STUFF", mw)
    mw.connect(self.config_action, SIGNAL("triggered()"), self.setup)
    mw.form.menuTools.addAction(self.config_action)

    self.swin = QDialog(mw)
    self.thread = QThread()
    self.obj = CaptureWorker()
    self.obj.dataReady.connect(onDataReady)
    self.obj.moveToThread(self.thread)
    self.obj.finished.connect(self.thread.quit)
    self.thread.connect(self.thread, SIGNAL("finished()"), self.swin, SLOT("accept()"))
    self.thread.connect(self.thread, SIGNAL("finished()"), self.thread.terminate)



  def setup(self):
    global received

    layout = QVBoxLayout()
    layout.addWidget(self.create_layout())
    self.swin.setLayout(layout)
    self.thread.start()    

    if self.swin.exec_():
      tooltip("Created files: %s" % ', '.join(received))
      received = []
      mw.progress.finish()



  def create_layout(self):
    hz_group_box = QGroupBox("Test Pitch Accent Capture")
    layout = QGridLayout()

    self.go = QPushButton("GO")
    self.go.clicked.connect(self.run)
    layout.addWidget(self.go, 0, 0, 3, 6)

    hz_group_box.setLayout(layout)
    return hz_group_box
    


  def run(self):
    mw.progress.start(immediate=True)
    QMetaObject.invokeMethod(self.obj, 'process', Qt.QueuedConnection,
          Q_ARG(list, build_notes())
    )


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
