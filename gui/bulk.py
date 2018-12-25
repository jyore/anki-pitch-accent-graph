# -*- coding: utf-8 -*-

from aqt.qt import *
from .base import Dialog
from ..capture import capture
from ..worker import Worker
from ..util import create_image_html


class BulkAdd(Dialog):

    SPACER = QLabel()


    def __init__(self, mw):
        super(BulkAdd, self).__init__("Bulk-add", mw)
        self.mw = mw
        self.pool = QThreadPool()


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
        self.update_methods.addItems(["Append", "Prepend", "Replace"])

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
        self.total = len(self.nids)
        self.passed = 0
        self.failed = 0

        ntypes = {}
        for nid in self.nids:
            note = self.mw.col.getNote(nid)
            name = note.model()['name']
            if name in ntypes:
                continue
            else:
                ntypes[name] = self.mw.col.models.fieldNames(note.model())

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

        self.modify_label.setText("Modifying %s Notes" % self.total)
        self.validate()
        super(BulkAdd, self).show()


    def accept(self):

        if not self.validate():
            return

        self.mw.progress.start(immediate=True, label=self.build_progress_label())

        for nid in self.nids:
            note = self.mw.col.getNote(nid)
            fields = self.mw.col.models.fieldNames(note.model())
            if self.src_field.currentText() in fields and self.dst_field.currentText() in fields:
                self.pool.start(self.build_worker(
                    nid,
                    note[self.src_field.currentText()]
                ))
            else:
                self.failed += 1

        super(BulkAdd, self).accept()



    def validate(self):
        passed = True
        msg = ""

        if self.dst_field.count() < 1:
            passed = False
            msg = "No common field available for Source/Destination from selected card types"


        self.warning.setText(msg)
        self.src_field.setEnabled(passed)
        self.dst_field.setEnabled(passed)
        self.update_methods.setEnabled(passed)
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(passed)

        if passed:
            self.warning.hide()
        else:
            self.warning.show()

        return passed


    def build_worker(self, reference, expression):
        worker = Worker(capture, reference, expression)
        worker.signals.result.connect(self.process_results)
        worker.signals.error.connect(self.process_errors)
        return worker

    
    def build_progress_label(self):
        return "Generating %s Graphs\nSuccess: %s    Failed: %s" % (self.total, self.passed, self.failed)


    def process_results(self, result):

        reference = result['ref']
        fn = result['fn']

        action = self.update_methods.currentText()
        destination = self.dst_field.currentText()
        note = self.mw.col.getNote(reference)        


        if action == "Append":
            note[destination] = "%s%s" % (note[destination], create_image_html(fn))
        elif action == "Prepend":
            note[destination] = "%s%s" % (create_image_html(fn), note[destination])
        else:
            note[destination] = create_image_html(fn)

        note.flush()
        self.mw.reset()

        self.passed += 1
        self.mw.progress.update(label=self.build_progress_label())
        self.exit_if_done()


    def process_errors(self, err):
        self.failed += 1
        self.mw.progress.update(label=self.build_progress_label())
        self.exit_if_done()
        raise err[0](err[1])


    def exit_if_done(self):
        if (self.passed + self.failed) >= self.total:
            self.mw.progress.finish()
