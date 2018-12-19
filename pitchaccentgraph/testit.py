# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aqt.qt import *
from aqt import mw
from aqt.utils import tooltip, showInfo

from .capture import CaptureWorker

received = []
def onDataReady(exp):
  received.append(exp)


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
      tooltip("Created files: %s" % received)
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
    QMetaObject.invokeMethod(self.obj, 'processB', Qt.QueuedConnection,
          Q_ARG(list, ["私は車が２台ある","あそこに立ってる人、もしかして部長!?"])
    )
