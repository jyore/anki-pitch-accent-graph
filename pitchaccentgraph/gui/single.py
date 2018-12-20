# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo


from .base import Dialog

from ..capture import CaptureWorker
from ..util import create_image_html


__all__ = ["SingleAdd"]

class SingleAdd(Dialog):

    def __init__(self, mw):
        super(SingleAdd, self).__init__("Add Pitch Accent Graph to Note", mw)

        self.thread = QThread()
        self.obj = CaptureWorker()
        self.obj.moveToThread(self.thread)

        self.obj.finished.connect(self.thread.quit)
        self.obj.finished.connect(lambda: mw.progress.finish())
        self.obj.finished.connect(lambda: mw.reset())
        self.thread.connect(self.thread, SIGNAL("finished()"), self.thread.terminate)
        
        self.obj.dataReady.connect(self.data_ready)


    def ui(self):
        layout = super(SingleAdd, self).ui()
        layout.addLayout(self.panel())
        layout.addWidget(self.ui_buttons())

        return layout

    def panel(self):
        layout = QGridLayout()
        
        self.expression_field = QLineEdit()
        self.destination_fields = QComboBox()
        self.update_methods = QComboBox()
        self.update_methods.addItems(["Append", "Replace"])

        # row 0
        layout.addWidget(QLabel("Expression:"), 0, 0, 1, 6)
        layout.addWidget(self.expression_field, 0, 6, 1, 12)

        # row 1
        layout.addWidget(QLabel("Destination Field:"), 1, 0, 1, 6)
        layout.addWidget(self.destination_fields, 1, 6, 1, 12)

        # row 2
        layout.addWidget(QLabel("Destination Update Method:"), 2, 0, 1, 6)
        layout.addWidget(self.update_methods, 2, 6, 1, 12)

        return layout


    def show(self, o):
        if hasattr(o, 'editor'):
            self.editor = o.editor
        else:
            self.editor = o


        fields = [ x['name'] for x in self.editor.note.model()['flds'] ]

        self.expression_field.setText(self.editor.note.fields[self.editor.currentField])
        self.expression_field.setFocus()
        self.destination_fields.clear()
        self.destination_fields.addItems(fields)

        self.thread.start()
        super(SingleAdd, self).show()


    def accept(self):
        mw.progress.start(immediate=True)
        QMetaObject.invokeMethod(self.obj, 'process', Qt.QueuedConnection,
            Q_ARG(list, [(str(self.destination_fields.currentIndex()), self.expression_field.text())])
        )
        super(SingleAdd, self).accept() 


    def data_ready(self, ref, exp, fn):

        ref = int(ref)
        if self.update_methods.currentIndex() == 0:
            self.editor.note.fields[ref] = self.editor.note.fields[ref] = "%s<div>%s</div>" % (self.editor.note.fields[ref], create_image_html(fn))
        else:
            self.editor.note.fields[ref] = create_image_html(fn)

        self.editor.note.flush()


