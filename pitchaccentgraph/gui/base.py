# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aqt import mw
from aqt.qt import *

from ..version import VERSION


__all__ = ['ICON', 'Dialog']


ICON = QIcon(os.path.join(mw.pm.addonFolder(), "pitchaccentgraph", "gui", "icons", "icon.png").replace("\\","/"))


class Dialog(QDialog):

    FONT_HEADER = QFont()
    FONT_HEADER.setPointSize(12)
    FONT_HEADER.setBold(True)

    FONT_INFO = QFont()
    FONT_INFO.setItalic(True)

    FONT_LABEL = QFont()
    FONT_LABEL.setBold(True)

    FONT_TITLE = QFont()
    FONT_TITLE.setPointSize(16)
    FONT_TITLE.setBold(True)

    SPACING = 10


    def __init__(self, title, parent):
        super(Dialog, self).__init__(parent)

        self.title = title
        self.setModal(True)
        self.setLayout(self.ui())
        self.setWindowIcon(ICON)
        self.setWindowTitle(
            self.title if "Pitch Accent Graphs" in self.title else "Pitch Accent Graphs: %s" % self.title
        )
        self.setMinimumSize(400,100)


    def ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self.ui_banner())
        layout.addWidget(self.ui_divider(QFrame.HLine))
    
        return layout
    
    
    def ui_banner(self):
        title = QLabel(self.title)
        title.setFont(self.FONT_TITLE)
    
        version = QLabel("Pitch Accent Graphs\nv%s" % VERSION)
        version.setFont(self.FONT_INFO)
    
        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(self.SPACING)
        layout.addStretch()
        layout.addWidget(version)
    
        return layout
    
    
    def ui_divider(self, orientation_style=QFrame.VLine):
        frame = QFrame()
        frame.setFrameStyle(orientation_style | QFrame.Sunken)
    
        return frame


    def ui_buttons(self):
        buttons = QDialogButtonBox()
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        buttons.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        return buttons
