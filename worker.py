# -*- coding: utf-8 -*-
from aqt.qt import *


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error    = pyqtSignal(tuple)
    result   = pyqtSignal(object)


class Worker(QRunnable):

    def __init__(self, func, *args, **kwargs):
        super(Worker, self).__init__()
        self.func    = func
        self.args    = args
        self.kwargs  = kwargs
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
        except:
            exec_type, value = sys.exc_info()[:2]
            self.signals.error.emit((exec_type, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
