# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo


from .base import Dialog

from ..capture import CaptureWorker
from ..util import create_image_html


__all__ = ["BulkAdd"]

class BulkAdd(Dialog):

    SPACER = QLabel("")

    def __init__(self, mw):
        super(BulkAdd, self).__init__("Bulk-add", mw)

        self.thread = QThread()
        self.obj = CaptureWorker()
        self.obj.moveToThread(self.thread)
        
        self.obj.finished.connect(self.thread.quit)
        self.obj.finished.connect(lambda: mw.progress.finish())
        self.obj.finished.connect(lambda: mw.reset())
        self.obj.finished.connect(self.process_complete)
        self.thread.connect(self.thread, SIGNAL("finished()"), self.thread.terminate)
        
        self.obj.dataReady.connect(self.data_ready)


    def ui(self):
        layout = super(BulkAdd, self).ui()
        
        layout.addLayout(self.panel())
        layout.addWidget(self.ui_buttons())

        return layout


    def panel(self):
        layout = QGridLayout()

        self.modify_label = QLabel("Modifying 0 Notes")
        self.warning = QLabel("")
        self.warning.setStyleSheet("color:red")

        self.src_field = QComboBox()
        self.dst_field = QComboBox()

        self.update_methods = QComboBox()
        self.update_methods.addItems(["Append", "Replace"])

        # row 0
        layout.addWidget(self.modify_label, 0, 0, 1, 6)
        layout.addWidget(self.warning, 0, 6, 1, 12)

        # row 1
        layout.addWidget(self.SPACER, 1, 0, 1, 12)

        # row 2
        layout.addWidget(QLabel("Source Field:"), 2, 0, 1, 6)
        layout.addWidget(self.src_field, 2, 6, 1, 12)

        # row 3
        layout.addWidget(QLabel("Destination Field:"), 3, 0, 1, 6)
        layout.addWidget(self.dst_field, 3, 6, 1, 12)

        # row 4
        layout.addWidget(QLabel("Destination Update Method:"), 4, 0, 1, 6)
        layout.addWidget(self.update_methods, 4, 6, 1, 12)

        return layout


    def show(self, browser):        
        self.nids = browser.selectedNotes()

        ntypes = {}
        for nid in self.nids:
            note = mw.col.getNote(nid)
            
            name = note.model()['name']
            if name in ntypes:
                continue
            else:
                ntypes[name] = mw.col.models.fieldNames(note.model())

        result = None
        for ntype in ntypes:
            if result is None:
                result = ntypes[ntype]
            else:
                result = list(set(result) & set(ntypes[ntype]))

        result = sorted(result)

        self.src_field.clear()
        self.dst_field.clear()
        self.src_field.addItems(result)
        self.dst_field.addItems(result)

        self.modify_label.setText("Modifying %s Notes" % len(self.nids))
        super(BulkAdd, self).show()

        if self.validate():
            self.thread.start()    



    def accept(self):

        if not self.validate():
            return

        notes = []
        self.total = len(self.nids)
        self.failed = []
        for nid in self.nids:
            note = mw.col.getNote(nid)
            fields = mw.col.models.fieldNames(note.model())
            if self.src_field.text() in fields and self.dst_field.text() in fields:
                ref = nid
                exp = mw.col.media.strip(note[self.src_field.text()])

                notes.append((str(ref), exp))
            else:
                self.failed.append((nid,"missing source or destination field"))


        mw.progress.start(immediate=True)
        QMetaObject.invokeMethod(self.obj, 'process', Qt.QueuedConnection,
            Q_ARG(list, notes)
        )
        super(BulkAdd, self).accept() 


    def data_ready(self, ref, exp, fn):
        note = mw.col.getNote(long(ref))
        
        if self.update_methods.currentIndex() == 0:
            note[self.dst_field.text()] = "%s<div>%s</div>" % (note[self.dst_field.text()], create_image_html(fn))
        else:
            note[self.dst_field.text()] = create_image_html(fn)

        note.flush()


    def process_complete(self):
        showInfo("Added Pitch-Accent Graphs to %s/%s notes" % (self.total-len(self.failed), self.total))


    def validate(self):
        passed = True
        msg = ""

        if self.dst_field.count() < 1:
            passed = False
            msg = "No common field available for Source/Destination from card types"


        self.warning.setText(msg)
        self.src_field.setEnabled(passed)
        self.dst_field.setEnabled(passed)
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(passed)
        if passed:
            self.warning.show()
        else:
            self.warning.hide()

        return passed
