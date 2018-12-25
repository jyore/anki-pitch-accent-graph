# -*- coding: utf-8 -*-

from aqt.qt import *
from .base import Dialog
from ..capture import capture
from ..worker import Worker
from ..util import create_image_html

class SingleAdd(Dialog):

    def __init__(self, mw):
        super(SingleAdd, self).__init__("Add Pitch Accent Graph to Note", mw)
        self.mw = mw
        self.pool = QThreadPool()


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
        self.update_methods.addItems(["Append", "Prepend", "Replace"])

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

        super(SingleAdd, self).show()


    def accept(self):
        self.mw.progress.start(immediate=True, label="Generating Pitch Accent Graph...")
        self.pool.start(self.build_worker(self.destination_fields.currentIndex(), self.expression_field.text()))
        super(SingleAdd, self).accept()


    def build_worker(self, reference, expression):
        worker = Worker(capture, reference, expression)
        worker.signals.result.connect(self.process_results)
        worker.signals.error.connect(self.process_errors)
        return worker


    def process_results(self, result):
        ref = result['ref']
        fn = result['fn']

        action = self.update_methods.currentText()
        

        if action == "Append":
            self.editor.note.fields[ref] = "%s%s" % (self.editor.note.fields[ref], create_image_html(fn))
        elif action == "Prepend":
            self.editor.note.fields[ref] = "%s%s" % (create_image_html(fn), self.editor.note.fields[ref])
        else:
            self.editor.note.fields[ref] = create_image_html(fn)

        self.editor.note.flush()
        self.mw.reset()
        self.mw.progress.finish()
        

    def process_errors(self, err):
        self.mw.progress.finish()
        raise err[0](err[2])
        
